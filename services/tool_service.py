
"""
ToolService
===========

Registry, discovery, and dispatch for tool services in GPT OSS.
"""


import os
import importlib
import logging
from typing import Any, Dict, List
from tools.__base__ import _TOOL_REGISTRY


class ToolServiceError(Exception):
    """Base exception for tool service errors."""
    pass

class ToolNotFoundError(ToolServiceError):
    """Raised when a requested tool is not found in the registry."""
    pass

class ToolExecutionError(ToolServiceError):
    """Raised when a tool fails to execute properly."""
    pass

class ToolService:
    """
    Registry, discovery, and dispatcher for tool functions.

    Features:
    - Automatic discovery and import of tool modules in the tools directory
    - Access registered tools and their schemas
    - Call tools directly via call_tool(name, args)
    - Get the OpenAI/Harmony tool schema for chat orchestration
    """

    def __init__(self, tool_dirs=None):
        """
        Initialize ToolService and discover tool modules.
        Args:
            tool_dirs: List of directories to search for tool modules (optional).
        """
        if tool_dirs is None:
            tool_dirs = [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools')]
        self._discover_tools(tool_dirs)
        self.services: Dict[str, Any] = {name: cls() for name, cls in _TOOL_REGISTRY.items()}
        self.tool_map: Dict[str, Any] = {}
        for name, service in self.services.items():
            method = getattr(service, name, None)
            if callable(method):
                self.tool_map[name] = method

    @staticmethod
    def _discover_tools(tool_dirs):
        """
        Import all tool modules in the given directories to populate the registry.
        """
        for tools_dir in tool_dirs:
            if not os.path.isdir(tools_dir):
                continue
            for filename in os.listdir(tools_dir):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_name = f"tools.{filename[:-3]}"
                    importlib.import_module(module_name)

    def call_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """
        Call a registered tool by name with arguments.
        Args:
            name: Tool name.
            args: Arguments for the tool.
        Returns:
            Tool result.
        Raises:
            ToolNotFoundError, ToolExecutionError
        """
        logging.info(f"Calling tool: {name} with args: {args}")
        if name in self.tool_map:
            try:
                return self.tool_map[name](**args)
            except Exception as e:
                logging.error(f"Error executing tool '{name}': {e}")
                raise ToolExecutionError(f"Error executing tool '{name}': {e}")
        logging.error(f"Tool '{name}' not found.")
        raise ToolNotFoundError(f"Tool '{name}' not found.")

    def get_tool_schema(self) -> List[Dict[str, Any]]:
        """
        Get the OpenAI/Harmony tool schema for all registered tools.
        Returns:
            List of tool schemas.
        """
        return [service.get_metadata() for service in self.services.values()]
