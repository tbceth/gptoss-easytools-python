# tools/weather.py
from .__base__ import ToolBase, register_tool

@register_tool
class WeatherService(ToolBase):
    name = "get_weather"
    description = "Get current weather by city name."
    parameters = {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City, e.g., 'Calgary'"},
            "unit": {"type": "string", "enum": ["c", "f"], "default": "c"}
        },
        "required": ["city"]
    }

    def get_weather(self, city: str, unit: str = "c"):
        # Stubbed example; replace with real API call if needed
        return {"city": city, "temp": 18.5, "unit": unit, "condition": "Sunny"}
