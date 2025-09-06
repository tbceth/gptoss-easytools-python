# tools/add.py
from .__base__ import ToolBase, register_tool

@register_tool
class AddService(ToolBase):
    name = "add"
    description = "Add two numbers."
    parameters = {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }

    def add(self, a, b):
        return {"sum": a + b}
