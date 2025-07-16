# noinspection PyPep8Naming
import urllib.request
import urllib.error
import json
import io
import base64
import logging

from PIL import Image
import numpy as np

logger = logging.getLogger("OpenRouterVisionNodeExperimental")
logger.setLevel(logging.DEBUG)

class OpenRouterVisionNodeExperimental:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key":       ("STRING", {"multiline": False}),
                "model_name":    ("STRING", {"multiline": False}),
                "system_prompt": ("STRING", {"multiline": True}),
                "user_prompt":   ("STRING", {"multiline": True}),
                "img":           ("IMAGE",  {}),
            },
            "optional": {
                "max_tokens":  ("INT",   {"default": 1024}),
                "temperature": ("FLOAT", {"default": 0.7}),
                "top_p":       ("FLOAT", {"default": 0.9}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION     = "call_openrouter"
    CATEGORY     = "OpenRouter"

    @staticmethod
    def _to_pil(img):
        """Convert tensor/ndarray to PIL.Image."""
        if isinstance(img, Image.Image):
            return img

        if hasattr(img, "cpu"):
            arr = img.cpu().detach().numpy()
        else:
            arr = np.array(img)
        arr = np.squeeze(arr)

        if np.issubdtype(arr.dtype, np.floating):
            arr = (arr * 255).clip(0, 255).astype(np.uint8)

        if arr.ndim == 3 and arr.shape[0] in (1, 3, 4):
            arr = np.transpose(arr, (1, 2, 0))

        if arr.ndim == 3:
            ch = arr.shape[2]
            mode = {1: "L", 3: "RGB", 4: "RGBA"}.get(ch)
            if mode is None:
                raise TypeError(f"Unsupported channels: {ch}")
        elif arr.ndim == 2:
            mode = "L"
        else:
            raise TypeError(f"Cannot handle shape: {arr.shape}")

        return Image.fromarray(arr, mode)

    def call_openrouter(self, api_key, model_name, system_prompt, user_prompt,
                        img, max_tokens=1024, temperature=0.7, top_p=0.9):
        # 1) Convert to PIL
        try:
            pil = self._to_pil(img)
        except Exception as e:
            logger.error("Conversion to PIL failed", exc_info=True)
            return (f"Error converting image: {e}",)

        # 2) Resize & encode
        pil.thumbnail((512, 512))
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=75)
        data_url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        logger.debug(f"[VisionNode] data_url length={len(data_url)}")

        # 3) Build structured messages
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user",   "content": [
                {"type": "text",      "text": user_prompt},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]}
        ]
        payload = {
            "model":      model_name,
            "messages":   messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p":       top_p,
        }
        body = json.dumps(payload).encode("utf-8")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json"
        }

        # 4) Up to 3 attempts
        for attempt in range(1, 4):
            logger.info(
                f"[VisionNodeExperimental] Attempt {attempt}/3 "
                f"(max_tokens={max_tokens}, temperature={temperature}, top_p={top_p})"
            )
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")

            try:
                with urllib.request.urlopen(req) as resp:
                    j = json.loads(resp.read().decode("utf-8"))
                    text = j["choices"][0]["message"]["content"]
                    logger.info(f"[VisionNode] Got content length={len(text)}")
                    return (text,)

            except urllib.error.HTTPError as e:
                err = f"HTTPError {e.code}: {e.reason}"
                logger.warning(f"[VisionNode] {err} on attempt {attempt}")
                if attempt == 3:
                    return (f"Error: {err}",)

            except Exception as e:
                logger.warning(f"[VisionNode] Exception on attempt {attempt}: {e}", exc_info=True)
                if attempt == 3:
                    return (f"Error: {e}",)

        # fallback
        return ("Error: exhausted retries",)

# register node
NODE_CLASS_MAPPINGS = {
    "OpenRouterVisionNodeExperimental": OpenRouterVisionNodeExperimental
}
