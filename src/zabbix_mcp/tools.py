"""MCP Tool definitions and handlers."""

import json
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

from mcp.types import Tool

from .client import ZabbixClient

# Tool definitions
TOOLS: List[Tool] = [
    Tool(
        name="get_hosts",
        description="List all monitored hosts in Zabbix",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="get_problems",
        description="Get active problems/alerts",
        inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}},
    ),
    Tool(
        name="get_triggers",
        description="List triggers with their current status",
        inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}},
    ),
    Tool(
        name="get_events",
        description="Get recent events from Zabbix",
        inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}},
    ),
    Tool(
        name="get_host_details",
        description="Get detailed information about a specific host",
        inputSchema={
            "type": "object",
            "properties": {"hostname": {"type": "string"}},
            "required": ["hostname"],
        },
    ),
    Tool(
        name="get_items",
        description="Get monitored items (metrics)",
        inputSchema={"type": "object", "properties": {"hostname": {"type": "string"}}},
    ),
    Tool(
        name="get_host_groups",
        description="List all host groups",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="get_system_status",
        description="Get overall system status and statistics",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="get_templates",
        description="List all available templates",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="link_template",
        description="Link a template to a host by names (hostname and template name)",
        inputSchema={
            "type": "object",
            "properties": {
                "hostname": {"type": "string", "description": "Host name"},
                "template_name": {"type": "string", "description": "Template name"},
            },
            "required": ["hostname", "template_name"],
        },
    ),
]


def handle_get_hosts(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_hosts tool."""
    try:
        hosts = client.get_hosts()
        if not hosts:
            return "No hosts found"
        
        result = f"📋 Found {len(hosts)} hosts:\n\n"
        for host in hosts[:20]:
            result += f"🖥️ {host.get('name', 'Unknown')} ({host.get('host', 'N/A')})\n"
            result += f"   Status: {'Enabled' if host.get('status') == '0' else 'Disabled'}\n"
        
        if len(hosts) > 20:
            result += f"\n... and {len(hosts) - 20} more hosts"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_problems(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_problems tool."""
    try:
        limit = args.get("limit", 50)
        problems = client.get_problems(limit=limit)
        
        if not problems:
            return "✅ No active problems"
        
        result = f"⚠️ Active Problems: {len(problems)}\n\n"
        for problem in problems[:10]:
            hosts = problem.get("hosts", [])
            host_names = ", ".join([h.get("name", "Unknown") for h in hosts])
            result += f"• {problem.get('name', 'Unknown')} - {host_names}\n"
        
        if len(problems) > 10:
            result += f"\n... and {len(problems) - 10} more"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_triggers(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_triggers tool."""
    try:
        limit = args.get("limit", 50)
        triggers = client.get_triggers(limit=limit)
        
        if not triggers:
            return "No triggers found"
        
        result = f"🔔 Found {len(triggers)} triggers:\n\n"
        for trigger in triggers[:10]:
            status = "🔴 PROBLEM" if trigger.get("value") == "1" else "🟢 OK"
            result += f"{status} - {trigger.get('description', 'Unknown')}\n"
        
        if len(triggers) > 10:
            result += f"... and {len(triggers) - 10} more"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_events(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_events tool."""
    try:
        limit = args.get("limit", 20)
        events = client.get_events(limit=limit)
        
        if not events:
            return "No events found"
        
        result = f"📅 Recent Events ({len(events)}):\n\n"
        for event in events[:10]:
            timestamp = datetime.fromtimestamp(int(event.get("clock", 0))).strftime("%Y-%m-%d %H:%M:%S")
            hosts = event.get("hosts", [])
            host_names = ", ".join([h.get("name", "Unknown") for h in hosts])
            result += f"⏰ {timestamp} - {host_names}\n"
        
        if len(events) > 10:
            result += f"... and {len(events) - 10} more"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_host_details(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_host_details tool."""
    try:
        hostname = args.get("hostname")
        if not hostname:
            return "Error: hostname required"
        
        host = client.get_host_by_name(hostname)
        if not host:
            return f"Host '{hostname}' not found"
        
        result = f"🖥️ Host Details: {host.get('name')}\n\n"
        result += f"Host ID: {host.get('hostid')}\n"
        result += f"Status: {'Enabled' if host.get('status') == '0' else 'Disabled'}\n"
        
        interfaces = host.get("interfaces", [])
        if interfaces:
            result += f"\nInterfaces ({len(interfaces)}):\n"
            for iface in interfaces:
                result += f"  - {iface.get('ip', 'N/A')} ({iface.get('type', 'Unknown')})\n"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_items(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_items tool."""
    try:
        hostname = args.get("hostname")
        hostid = None
        
        if hostname:
            host = client.get_host_by_name(hostname)
            if not host:
                return f"Host '{hostname}' not found"
            hostid = host.get("hostid")
        
        items = client.get_items(hostid=hostid) if hostid else client.get_items()
        
        if not items:
            return "No items found"
        
        result = f"📊 Monitored Items: {len(items)}\n\n"
        for item in items[:15]:
            result += f"• {item.get('name', 'Unknown')} ({item.get('key_', 'N/A')})\n"
        
        if len(items) > 15:
            result += f"... and {len(items) - 15} more"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_host_groups(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_host_groups tool."""
    try:
        groups = client.get_groups()
        
        if not groups:
            return "No host groups found"
        
        result = f"👥 Host Groups: {len(groups)}\n\n"
        for group in groups:
            result += f"• {group.get('name')} (ID: {group.get('groupid')})\n"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_system_status(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_system_status tool."""
    try:
        hosts = client.get_hosts()
        problems = client.get_problems()
        triggers = client.get_triggers()
        
        result = "📊 Zabbix System Status\n\n"
        result += f"Total Hosts: {len(hosts)}\n"
        result += f"Active Problems: {len(problems)}\n"
        result += f"Total Triggers: {len(triggers)}\n"
        
        problem_triggers = [t for t in triggers if t.get("value") == "1"]
        result += f"Problem Triggers: {len(problem_triggers)}\n"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_get_templates(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_templates tool."""
    try:
        templates = client.get_templates()
        
        if not templates:
            return "No templates found"
        
        result = f"📋 Available Templates: {len(templates)}\n\n"
        for template in templates[:20]:
            result += f"• {template.get('name')} ({template.get('host')})\n"
        
        if len(templates) > 20:
            result += f"\n... and {len(templates) - 20} more templates"
        
        return result
    except Exception as e:
        return f"Error: {e}"


def handle_link_template(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle link_template tool."""
    try:
        hostname = args.get("hostname")
        template_name = args.get("template_name")
        
        if not hostname or not template_name:
            return "Error: hostname and template_name are required"
        
        success = client.link_template_by_names(hostname, template_name)
        
        if success:
            return f"✅ Successfully linked template '{template_name}' to host '{hostname}'"
        else:
            return f"❌ Failed to link template '{template_name}' to host '{hostname}'"
    except Exception as e:
        return f"❌ Error: {e}"


# Tool handler registry
TOOL_HANDLERS: Dict[str, Callable[[ZabbixClient, Dict[str, Any]], str]] = {
    "get_hosts": handle_get_hosts,
    "get_problems": handle_get_problems,
    "get_triggers": handle_get_triggers,
    "get_events": handle_get_events,
    "get_host_details": handle_get_host_details,
    "get_items": handle_get_items,
    "get_host_groups": handle_get_host_groups,
    "get_system_status": handle_get_system_status,
    "get_templates": handle_get_templates,
    "link_template": handle_link_template,
}


def get_tool_handler(name: str) -> Optional[Callable[[ZabbixClient, Dict[str, Any]], str]]:
    """Get handler for a tool by name."""
    return TOOL_HANDLERS.get(name)
