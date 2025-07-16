from .openrouter_node import OpenRouterNode
from .openrouter_vision_node import OpenRouterVisionNode
from .comfyui_ollama_node import OllamaNode
from .comfyui_ollama_vision_node import OllamaVisionNode
from .openrouter_node_experimental import OpenRouterNodeExperimental
from .openrouter_vision_node_experimental import OpenRouterVisionNodeExperimental
from .comfyui_ollama_node_experimental import OllamaNodeExperimental
from .comfyui_ollama_vision_node_experimental import OllamaVisionNodeExperimental

NODE_CLASS_MAPPINGS = {
    "OpenRouterNode":        OpenRouterNode,
    "OpenRouterVisionNode":  OpenRouterVisionNode,
    "OllamaNode":            OllamaNode,
    "OllamaVisionNode":      OllamaVisionNode,
    "OpenRouterNodeExperimental":       OpenRouterNodeExperimental,
    "OpenRouterVisionNodeExperimental": OpenRouterVisionNodeExperimental,
    "OllamaNodeExperimental":           OllamaNodeExperimental,
    "OllamaVisionNodeExperimental":     OllamaVisionNodeExperimental,
}
