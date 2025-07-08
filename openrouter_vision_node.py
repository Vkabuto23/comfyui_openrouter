import urllib.request
import json
import io
import base64
import logging

from PIL import Image
import numpy as np

# --- Настройка логгера ---
logger = logging.getLogger("OpenRouterVisionNode")
logger.setLevel(logging.DEBUG)
# ComfyUI поймает этот логгер и выведет сообщения в свою консоль.

class OpenRouterVisionNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key":       ("STRING", {"multiline": False}),
                "model_name":    ("STRING", {"multiline": False}),
                "system_prompt": ("STRING", {"multiline": True}),
                "user_prompt":   ("STRING", {"multiline": True}),
                "img":           ("IMAGE",  {}),  # Pillow Image или тензор/ndarray
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION     = "call_openrouter"
    CATEGORY     = "OpenRouter"

    def _to_pil(self, img):
        """Конвертация Tensor/ndarray→PIL.Image"""
        # Уже PIL?
        if isinstance(img, Image.Image):
            logger.debug(f"[to_pil] Input is PIL, size={img.size}, mode={img.mode}")
            return img

        # Получаем numpy-массив
        if hasattr(img, "cpu"):
            arr = img.cpu().detach().numpy()
        else:
            arr = np.array(img)
        logger.debug(f"[to_pil] raw array shape={arr.shape}, dtype={arr.dtype}")

        # Убираем единичные размерности
        arr = np.squeeze(arr)
        logger.debug(f"[to_pil] after squeeze shape={arr.shape}")

        # Float → uint8
        if np.issubdtype(arr.dtype, np.floating):
            arr = (arr * 255).clip(0, 255).astype(np.uint8)
            logger.debug("[to_pil] converted float→uint8")

        # Определяем формат
        if arr.ndim == 3:
            # каналы-first?
            if arr.shape[0] in (1, 3, 4):
                arr = np.transpose(arr, (1, 2, 0))
                logger.debug(f"[to_pil] transposed to H×W×C, shape={arr.shape}")
            ch = arr.shape[2]
            mode = {1: "L", 3: "RGB", 4: "RGBA"}.get(ch)
            if mode is None:
                raise TypeError(f"[to_pil] Unsupported channel count: {ch}")
        elif arr.ndim == 2:
            mode = "L"
        else:
            raise TypeError(f"[to_pil] Cannot handle array shape: {arr.shape}")

        pil = Image.fromarray(arr, mode)
        logger.debug(f"[to_pil] Created PIL, size={pil.size}, mode={pil.mode}")
        return pil

    def call_openrouter(self, api_key, model_name, system_prompt, user_prompt, img):
        logger.info("OpenRouterVisionNode: start call_openrouter()")

        # 1) → PIL.Image
        try:
            pil = self._to_pil(img)
        except Exception as e:
            logger.exception("Conversion to PIL failed")
            return (f"Error converting image: {e}",)
        logger.info(f"PIL image size={pil.size}, mode={pil.mode}")

        # 2) Скейлим до max 512px
        pil.thumbnail((512, 512))
        logger.info(f"Resized to {pil.size}")

        # 3) Сохраняем в JPEG (quality=75)
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=75)
        data_url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        logger.debug(f"Data URL length={len(data_url)}")

        # 4) Формируем структурированные сообщения
        messages = [
            {"role": "system", "content": [
                {"type": "text", "text": system_prompt}
            ]},
            {"role": "user", "content": [
                {"type": "text",      "text": user_prompt},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]}
        ]
        payload = {"model": model_name, "messages": messages}
        body = json.dumps(payload).encode("utf-8")
        logger.info(f"Sending POST (payload {len(body)} bytes) to /api/v1/chat/completions")

        # 5) Делаем запрос
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json"
        }
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                answer = resp_json["choices"][0]["message"]["content"]
                logger.info(f"Received response, length={len(answer)}")
                return (answer,)
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8")
            except:
                pass
            logger.error(f"HTTPError {e.code}: {e.reason}, body: {err_body}")
            return (f"Error: HTTP {e.code} {e.reason}",)
        except Exception as e:
            logger.exception("Unexpected error during request")
            return (f"Error: {e}",)

# регистрация ноды
NODE_CLASS_MAPPINGS = {
    "OpenRouterVisionNode": OpenRouterVisionNode
}
