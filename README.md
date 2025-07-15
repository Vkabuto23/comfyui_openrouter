
# ComfyUI Custom Nodes: OpenRouter & Ollama  
Набор кастомных кастомных нод для ComfyUI, позволяющих работать с API OpenRouter и Ollama.

Включает четыре ноды:  
- **OpenRouterNode** — стандартные чат-комплишны (только текст)  
- **OpenRouterVisionNode** — мультимодальные чат-комплишны (текст + изображение)  
- **OllamaNode** — стандартные чат-комплишны через Ollama (только текст)  
- **OllamaVisionNode** — мультимодальные чат-комплишны через Ollama (текст + изображение)  

⚙️ **Установка**  
1. Скопируйте папку `comfyui_openrouter/` и файлы нод Ollama (`comfyui_ollama_node.py`, `comfyui_ollama_vision_node.py`) в ваш каталог `custom_nodes/` внутри ComfyUI.  
2. Убедитесь, что в среде ComfyUI установлены нужные пакеты:  
   ```bash
   pip install pillow numpy


3. (Опционально) В корне `custom_nodes/` можно сделать `git clone` вашего репозитория, чтобы удобно подтягивать обновления:

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/Vkabuto23/comfyui_openrouter.git
   ```
4. Перезапустите ComfyUI.
5. В графе нод появятся категории **OpenRouter** и **Ollama** с соответствующими нодами.

🔑 **API-ключ для OpenRouter**

1. Зарегистрируйтесь или войдите на:
   [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)
2. Создайте или скопируйте ваш Bearer API Key.
3. Вставьте его в поле `api_key` у нод **OpenRouterNode** и **OpenRouterVisionNode**.

📦 **Ollama Integration**

1. Скачайте и установите Ollama CLI для вашей ОС:
   [https://ollama.com/#download](https://ollama.com/#download)
2. Перейдите в терминал и подтяните модель `qwen2.5vl:7b`:

   ```bash
   ollama pull qwen2.5vl:7b
   ```
3. Запустите HTTP-сервер Ollama (по умолчанию на `localhost:11434`):

   ```bash
   ollama serve
   ```
4. В нодах **OllamaNode** и **OllamaVisionNode** введите:

   * `ip_port`: `localhost:11434`
   * `model_name`: `qwen2.5vl:7b`

🛠️ **Использование**

### OpenRouterNode (текст)

**Входы**

* `api_key` (STRING) — ваш OpenRouter API Key
* `model_name` (STRING) — например, `deepseek/deepseek-r1-0528:free`
* `system_prompt` (STRING)
* `user_prompt` (STRING)
* `temperature` (FLOAT, по умолчанию 0.7)

**Выход**

* `response` (STRING)

### OpenRouterVisionNode (текст + изображение)

**Входы**

* `api_key` (STRING)
* `model_name` (STRING)
* `system_prompt` (STRING)
* `user_prompt` (STRING)
* `img` (IMAGE) — любое изображение Pillow или тензор
* `max_tokens` (INT, по умолчанию 1024)
* `temperature` (FLOAT, по умолчанию 0.7)

**Выход**

* `response` (STRING)

### OllamaNode (текст)

**Входы**

* `ip_port` (STRING) — например, `localhost:11434`
* `model_name` (STRING) — `qwen2.5vl:7b`
* `system_prompt` (STRING)
* `user_prompt` (STRING)
* `temperature` (FLOAT, по умолчанию 0.7)

**Выход**

* `response` (STRING)

### OllamaVisionNode (текст + изображение)

**Входы**

* `ip_port` (STRING)
* `model_name` (STRING)
* `system_prompt` (STRING)
* `user_prompt` (STRING)
* `img` (IMAGE)
* `max_tokens` (INT, по умолчанию 1024)
* `temperature` (FLOAT, по умолчанию 0.7)

**Выход**

* `response` (STRING)

🎁 **Список бесплатных моделей OpenRouter**

| Модель                              | Тег  |
| ----------------------------------- | ---- |
| `qwen/qwen2.5-vl-32b-instruct:free` | free |
| `qwen/qwen2.5-vl-72b-instruct:free` | free |
| `deepseek/deepseek-r1-0528:free`    | free |
| `deepseek/deepseek-v3-base:free`    | free |

---
