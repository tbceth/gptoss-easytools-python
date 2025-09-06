
"""
ChatService
===========

Service for orchestrating chat with OpenAI-compatible models and tool calling.
"""

import os
import json
import logging
from typing import Any, Dict, List
from dotenv import load_dotenv
from openai import OpenAI
from services.tool_service import ToolService, ToolServiceError

# Load environment variables
load_dotenv()
BASE_URL = os.environ.get("GPT_OSS_BASE_URL", "http://localhost:8080/v1")
API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_OSS_API_KEY")
MODEL = os.environ.get("GPT_OSS_MODEL", "gpt-oss-20b")

class ChatService:
    """
    Orchestrates chat with OpenAI-compatible models and tool calling.

    Features:
    - Accepts Harmony-style message separation: system, developer, and user messages.
    - Pass a custom tools schema in the constructor, or set self.tools after instantiation.
    - If tools is None, disables tool calling.
    - Supports dynamic tool schema changes at runtime.
    """

    def __init__(self, base_url: str = None, api_key: str = None, model: str = None, tools: List[Dict[str, Any]] = None):
        """
        Initialize ChatService.
        Args:
            base_url: OpenAI-compatible API base URL.
            api_key: API key for authentication.
            model: Model name to use.
            tools: List of tool schemas (optional).
        """
        self.client = OpenAI(base_url=base_url or BASE_URL, api_key=api_key or API_KEY)
        self.model = model or MODEL
        self.tool_service = ToolService()
        self.tools = tools if tools is not None else None

    def chat_completion(
        self,
        system_messages: List[Dict[str, Any]] = None,
        developer_messages: List[Dict[str, Any]] = None,
        user_messages: List[Dict[str, Any]] = None,
        max_rounds: int = 3,
        use_tools: bool = True
    ) -> str:
        """
        Run a chat completion with optional tool calling.
        Args:
            system_messages: List of system messages.
            developer_messages: List of developer messages.
            user_messages: List of user messages.
            max_rounds: Maximum chat rounds.
            use_tools: Whether to enable tool calling.
        Returns:
            Final assistant message as a string.
        """
        system_messages = system_messages or []
        developer_messages = developer_messages or []
        user_messages = user_messages or []
        messages = system_messages + developer_messages + user_messages
        for round_num in range(max_rounds):
            logging.info(f"Chat round {round_num+1} with messages: {messages}")
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if use_tools else None,
                tool_choice="auto" if (self.tools and use_tools) else None,
                temperature=0.2,
                max_tokens=512,
            )
            msg = resp.choices[0].message
            if use_tools and getattr(msg, "tool_calls", None):
                messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
                    tc.model_dump() for tc in msg.tool_calls
                ]})
                for tc in msg.tool_calls:
                    if tc.type != "function":
                        continue
                    name = tc.function.name
                    args = json.loads(tc.function.arguments or "{}")
                    try:
                        result = self.tool_service.call_tool(name, args)
                    except ToolServiceError as e:
                        result = {"error": str(e)}
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": name,
                        "content": json.dumps(result)
                    })
                continue
            messages.append({"role": "assistant", "content": msg.content or ""})
            return msg.content
        logging.warning("Hit max_rounds without a final answer.")
        return "Hit max_rounds without a final answer."
