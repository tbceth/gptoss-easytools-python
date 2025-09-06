

"""
test_tools.py
Script-based tests for ToolService and ChatService in GPT OSS.
"""

import os
import logging
from dotenv import load_dotenv
from services.tool_service import ToolService
from services.chat_service import ChatService


def test_tool_registration():
    tool_service = ToolService()
    tools = tool_service.get_tool_schema()
    print("Registered tools:")
    for tool in tools:
        print(f"- {tool['function']['name']}")
    assert any(t['function']['name'] == 'get_weather' for t in tools)
    assert any(t['function']['name'] == 'add' for t in tools)

def test_tool_call():
    tool_service = ToolService()
    result = tool_service.call_tool('add', {'a': 2, 'b': 3})
    print("Add result:", result)
    assert result['sum'] == 5

def test_chat_service():
    load_dotenv()

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_OSS_API_KEY")
    base_url = os.environ.get("GPT_OSS_BASE_URL", "http://localhost:8080/v1")
    model = os.environ.get("GPT_OSS_MODEL", "gpt-oss-20b")

    tool_service = ToolService()
    tools = tool_service.get_tool_schema()
    chat_service = ChatService(api_key=api_key, base_url=base_url, model=model, tools=tools)

    system_messages = [{"role": "system", "content": "You are a concise assistant."}]
    developer_messages = []
    user_messages = [{"role": "user", "content": "Add 10 and 5."}]

    response = chat_service.chat_completion(
        system_messages=system_messages,
        developer_messages=developer_messages,
        user_messages=user_messages
    )

    print("Chat response:", response)
    assert "15" in response or "sum" in response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_tool_registration()
    test_tool_call()
    test_chat_service()
    print("All tests passed.")
