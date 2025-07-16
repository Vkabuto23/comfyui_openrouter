# comfyui_ollama_node.py

import urllib.request
import json
import logging

# Настраиваем логгер для этой ноды
logger = logging.getLogger("OllamaNodeExperimental")
logger.setLevel(logging.DEBUG)

class OllamaNodeExperimental:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ip_port":       ("STRING", {"multiline": False}),  # e.g. "localhost:11434"
                "model_name":    ("STRING", {"multiline": False}),
                "system_prompt": ("STRING", {"multiline": True}),
                "user_prompt":   ("STRING", {"multiline": True}),
            },
            "optional": {
                "max_tokens":  ("INT",   {"default": 1024}),
                "temperature": ("FLOAT", {"default": 0.7}),
                "top_p":       ("FLOAT", {"default": 0.9}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION     = "call_ollama"
    CATEGORY     = "Ollama"

    def call_ollama(self, ip_port, model_name, system_prompt, user_prompt,
                    max_tokens=1024, temperature=0.7, top_p=0.9):
        url = f"http://{ip_port}/v1/chat/completions"
        headers = {
            "Content-Type":  "application/json",
        }
        payload = {
            "model":    model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p":       top_p,
            }
        }
        data = json.dumps(payload).encode("utf-8")

        for attempt in range(1, 4):
            logger.info(
                f"OllamaExperimental: Attempt {attempt}/3 "
                f"(max_tokens={max_tokens}, temperature={temperature}, top_p={top_p})"
            )
            logger.debug(f"OllamaNode: POST {url} (payload {len(data)} bytes)")

            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req) as resp:
                    status = getattr(resp, "status", resp.getcode())
                    logger.info(f"OllamaNode: HTTP {status}")

                    raw = resp.read().decode("utf-8")
                    logger.debug(f"OllamaNode: Raw response: {raw}")

                    resp_json = json.loads(raw)
                    content = resp_json["choices"][0]["message"]["content"]
                    logger.info(f"OllamaNode: Got content length={len(content)}")
                    return (content,)

            except urllib.error.HTTPError as e:
                err = f"HTTPError {e.code}: {e.reason}"
                logger.warning(f"OllamaNode: {err} on attempt {attempt}")
                if attempt == 3:
                    return (f"Error: {err}",)

            except Exception as e:
                logger.warning(f"OllamaNode: Exception on attempt {attempt}: {e}", exc_info=True)
                if attempt == 3:
                    return (f"Error: {e}",)

        return ("Error: exhausted retries",)

# Регистрация ноды
NODE_CLASS_MAPPINGS = {
    "OllamaNodeExperimental": OllamaNodeExperimental
}
