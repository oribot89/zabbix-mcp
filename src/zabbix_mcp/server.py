"""Zabbix MCP Server - Main MCP implementation."""

import logging
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult

from .config import load_config, ZabbixConfig
from .client import ZabbixClient, ZabbixAPIError
from .tools import TOOLS, get_tool_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZabbixMCPServer:
    """Zabbix MCP Server implementation."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("zabbix-mcp")
        self.config: ZabbixConfig | None = None
        self.client: ZabbixClient | None = None
        
        self.server.list_tools(self.list_tools)
        self.server.call_tool(self.handle_tool_call)
    
    def initialize(self) -> None:
        """Initialize configuration and authentication."""
        try:
            self.config = load_config()
            logger.info(f"Loaded config: {self.config.host}:{self.config.port}")
            
            self.client = ZabbixClient(
                base_url=self.config.base_url,
                username=self.config.username,
                password=self.config.password,
                verify_ssl=self.config.verify_ssl,
            )
            
            self.client.authenticate()
            logger.info("Successfully authenticated with Zabbix")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def list_tools(self) -> list[Tool]:
        """List available tools."""
        return TOOLS
    
    async def handle_tool_call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Handle tool calls from MCP clients."""
        try:
            if not self.client:
                return ToolResult(
                    content=[TextContent(type="text", text="Error: Zabbix client not initialized")],
                    is_error=True,
                )
            
            handler = get_tool_handler(name)
            if not handler:
                return ToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    is_error=True,
                )
            
            result = handler(self.client, arguments)
            
            return ToolResult(
                content=[TextContent(type="text", text=result)],
                is_error=False,
            )
            
        except ZabbixAPIError as e:
            logger.error(f"Zabbix API error: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Zabbix API error: {e}")],
                is_error=True,
            )
        except Exception as e:
            logger.error(f"Tool error: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {e}")],
                is_error=True,
            )
    
    def run(self) -> None:
        """Run the MCP server."""
        self.initialize()
        self.server.run()


def main():
    """Entry point."""
    mcp_server = ZabbixMCPServer()
    mcp_server.run()


if __name__ == "__main__":
    main()
