from .openrouter_node import OpenRouterNode
from .openrouter_vision_node import OpenRouterVisionNode
from .comfyui_ollama_node import OllamaNode
from .comfyui_ollama_vision_node import OllamaVisionNode

NODE_CLASS_MAPPINGS = {
    "OpenRouterNode":        OpenRouterNode,
    "OpenRouterVisionNode":  OpenRouterVisionNode,
    "OllamaNode":            OllamaNode,
    "OllamaVisionNode":      OllamaVisionNode,
}
