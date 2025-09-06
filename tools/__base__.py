# tools/__base__.py
# Base class and registry for tool services

_TOOL_REGISTRY = {}

def register_tool(cls):
    """Decorator to register a tool service class."""
    if hasattr(cls, 'name') and cls.name:
        _TOOL_REGISTRY[cls.name] = cls
    return cls

class ToolBase:
    """Base class for all tools/services."""
    name = None
    description = None
    parameters = None

    def get_metadata(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
