# GPT OSS

Modular, extensible OpenAI-compatible tool calling service for local and remote LLMs.

## Features
- Automatic discovery and registration of tool services via decorators
- Service registry and dynamic schema generation
- Chat orchestration with tool execution
- Harmony-style message separation (system, developer, user)
- Flexible configuration via environment variables or .env
- Support for custom tool directories

## Installation
```bash
pip install gpt-oss
```

## Usage
```python
from services.chat_service import ChatService
from services.tool_service import ToolService

# Optionally discover tools in a custom directory
custom_tool_dirs = ["/path/to/your/tools"]
tool_service = ToolService(tool_dirs=custom_tool_dirs)
tools = tool_service.get_tool_schema()

chat_service = ChatService(api_key="your-key", base_url="http://localhost:8080/v1", model="gpt-oss-20b", tools=tools)

messages = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Add 10 and 5."}
]

response = chat_service.chat_completion(messages)
print(response)
```

## CLI Example
```bash
python main.py
```

## Custom Tools
- Create a Python file in your tools directory
- Use the `@register_tool` decorator from `tools.__base__`
- Example:
```python
from tools.__base__ import ToolBase, register_tool

@register_tool
class MyTool(ToolBase):
    name = "my_tool"
    description = "Does something useful."
    parameters = { ... }
    def my_tool(self, ...):
        ...
```

## License
MIT
