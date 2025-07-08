import urllib.request
import json
import logging

# Настраиваем логгер для этой ноды
logger = logging.getLogger("OpenRouterNode")
logger.setLevel(logging.DEBUG)  # выводим все DEBUG и выше
# Если нужно, можно добавить хэндлер, но ComfyUI обычно собирает логи в консоль сам.

class OpenRouterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key":      ("STRING", {"multiline": False}),
                "model_name":   ("STRING", {"multiline": False}),
                "system_prompt":("STRING", {"multiline": True}),
                "user_prompt":  ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION     = "call_openrouter"
    CATEGORY     = "OpenRouter"

    def call_openrouter(self, api_key, model_name, system_prompt, user_prompt):
        logger.info("OpenRouterNode: call_openrouter() started")

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
            ]
        }

        data = json.dumps(payload).encode("utf-8")

        logger.debug(f"OpenRouterNode: Prepared payload (truncated): {json.dumps(payload)[:500]}")
        logger.info(f"OpenRouterNode: Sending POST to {url}")
        logger.debug(f"OpenRouterNode: Headers: {headers}")
        logger.debug(f"OpenRouterNode: Payload bytes length: {len(data)}")

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                status = getattr(resp, "status", resp.getcode())
                logger.info(f"OpenRouterNode: HTTP response status: {status}")

                raw_body = resp.read().decode("utf-8")
                logger.debug(f"OpenRouterNode: Raw response body: {raw_body}")

                resp_json = json.loads(raw_body)
                content = resp_json["choices"][0]["message"]["content"]
                logger.info(f"OpenRouterNode: Extracted content length: {len(content)}")
                return (content,)

        except urllib.error.HTTPError as e:
            err = f"Error: HTTP {e.code}: {e.reason}"
            logger.error(f"OpenRouterNode: {err}")
            return (err,)

        except Exception as e:
            err = f"Error: {e}"
            logger.error(f"OpenRouterNode: Unexpected error: {e}", exc_info=True)
            return (err,)


# регистрация ноды
NODE_CLASS_MAPPINGS = {
    "OpenRouterNode": OpenRouterNode
}
