import urllib.request
import json
import logging

# Настраиваем логгер для этой ноды
logger = logging.getLogger("OpenRouterNode")
logger.setLevel(logging.DEBUG)

class OpenRouterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key":       ("STRING", {"multiline": False}),
                "model_name":    ("STRING", {"multiline": False}),
                "system_prompt": ("STRING", {"multiline": True}),
                "user_prompt":   ("STRING", {"multiline": True}),
            }
            ,
            "optional": {
                "temperature": ("FLOAT", {"default": 0.7}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION     = "call_openrouter"
    CATEGORY     = "OpenRouter"

    def call_openrouter(self, api_key, model_name, system_prompt, user_prompt, temperature=0.7):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json",
        }
        payload = {
            "model":    model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            "temperature": temperature,
        }
        data = json.dumps(payload).encode("utf-8")

        # Попробовать до 3 раз
        for attempt in range(1, 4):
            logger.info(f"OpenRouterNode: Attempt {attempt}/3")
            logger.debug(f"OpenRouterNode: POST {url} (payload {len(data)} bytes)")

            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req) as resp:
                    status = getattr(resp, "status", resp.getcode())
                    logger.info(f"OpenRouterNode: HTTP {status}")

                    raw = resp.read().decode("utf-8")
                    logger.debug(f"OpenRouterNode: Raw response: {raw}")

                    resp_json = json.loads(raw)
                    content = resp_json["choices"][0]["message"]["content"]
                    logger.info(f"OpenRouterNode: Got content length={len(content)}")
                    return (content,)

            except urllib.error.HTTPError as e:
                err = f"HTTPError {e.code}: {e.reason}"
                logger.warning(f"OpenRouterNode: {err} on attempt {attempt}")
                if attempt == 3:
                    return (f"Error: {err}",)
                # иначе продолжаем цикл

            except Exception as e:
                logger.warning(f"OpenRouterNode: Exception on attempt {attempt}: {e}", exc_info=True)
                if attempt == 3:
                    return (f"Error: {e}",)
                # иначе продолжаем цикл

# Регистрация ноды
NODE_CLASS_MAPPINGS = {
    "OpenRouterNode": OpenRouterNode
}
