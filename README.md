
# ComfyUI OpenRouter Nodes

A set of custom ComfyUI nodes for talking to the [OpenRouter](https://openrouter.ai/) API.  
Includes:

- **OpenRouterNode** — standard chat completions (text-only)  
- **OpenRouterVisionNode** — multimodal chat completions (text + image)

## ✅ Features

- Zero external dependencies beyond Python stdlib, Pillow & NumPy  
- Built-in retry logic (up to 3 attempts) on HTTP/network errors  
- Configurable `max_tokens` for output length  
- Structured multimodal payload (sends image as `image_url`)  
- Detailed console logging via Python `logging`  

## ⚙️ Installation

1. Copy the folder `comfyui_openrouter/` into your ComfyUI `custom_nodes/` directory.  
2. Make sure you have these Python packages installed in the same environment as ComfyUI:
   ```bash
   pip install pillow numpy


3. Restart ComfyUI.
4. In the node graph, find the **OpenRouter** category — your nodes (`OpenRouterNode` and `OpenRouterVisionNode`) will be there.

## 🔑 Getting an API Key

1. Sign up or log in at:
   [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)
2. Create or copy your **Bearer** API key.
3. Paste it into the `api_key` input of each node.

## 🛠️ Usage

### OpenRouterNode (Text-only)

* **Inputs**

  * `api_key` (STRING) — your OpenRouter API key
  * `model_name` (STRING) — e.g. `deepseek/deepseek-r1-0528:free`
  * `system_prompt` (STRING)
  * `user_prompt` (STRING)

* **Output**

  * `response` (STRING) — the generated text

### OpenRouterVisionNode (Text + Image)

* **Inputs**

  * `api_key` (STRING)
  * `model_name` (STRING)
  * `system_prompt` (STRING)
  * `user_prompt` (STRING)
  * `img` (IMAGE) — any Pillow-compatible image or tensor
  * `max_tokens` (INT, optional, default=1024) — max tokens for the reply

* **Output**

  * `response` (STRING)

## 🎁 Free Models List

| Model Name                          | Tag  |
| ----------------------------------- | ---- |
| `qwen/qwen2.5-vl-32b-instruct:free` | free |
| `qwen/qwen2.5-vl-72b-instruct:free` | free |
| `deepseek/deepseek-r1-0528:free`    | free |
| `deepseek/deepseek-v3-base:free`    | free |


::contentReference[oaicite:0]{index=0}
```
