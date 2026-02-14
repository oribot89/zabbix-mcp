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
    Tool(
        name="create_user",
        description="Create a new Zabbix user with specified role",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Unique username"},
                "password": {"type": "string", "description": "User password"},
                "role": {"type": "string", "description": "Role name (default: Super admin role)"},
                "email": {"type": "string", "description": "Optional email address"},
                "name": {"type": "string", "description": "Optional first name"},
                "surname": {"type": "string", "description": "Optional last name"},
            },
            "required": ["username", "password"],
        },
    ),
    Tool(
        name="update_user",
        description="Update user properties (password, role, etc.)",
        inputSchema={
            "type": "object",
            "properties": {
                "userid": {"type": "string", "description": "User ID"},
                "password": {"type": "string", "description": "New password"},
                "current_password": {"type": "string", "description": "Current password (required if changing password)"},
                "roleid": {"type": "string", "description": "New role ID"},
            },
            "required": ["userid"],
        },
    ),
    Tool(
        name="get_roles",
        description="List all available Zabbix roles",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="check_host_interface_availability",
        description="Check if host interface (agent) is available",
        inputSchema={
            "type": "object",
            "properties": {
                "hostid": {"type": "string", "description": "Host ID"},
            },
            "required": ["hostid"],
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


def handle_create_user(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle create_user tool."""
    try:
        from .user_management import UserManagement
        
        um = UserManagement(client)
        result = um.create_user(
            username=args.get("username"),
            password=args.get("password"),
            role=args.get("role", "Super admin role"),
            email=args.get("email"),
            name=args.get("name"),
            surname=args.get("surname")
        )
        
        if result["success"]:
            return f"✅ User created successfully\nUser ID: {result['userid']}\nUsername: {args.get('username')}"
        else:
            errors = "\n".join(result.get("validation_errors", []))
            return f"❌ Failed to create user\n{result['message']}\n{errors}"
    except Exception as e:
        return f"Error: {e}"


def handle_update_user(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle update_user tool."""
    try:
        from .user_management import UserManagement
        
        um = UserManagement(client)
        result = um.update_user(
            userid=args.get("userid"),
            password=args.get("password"),
            roleid=args.get("roleid"),
            current_password=args.get("current_password"),
            email=args.get("email"),
            name=args.get("name"),
            surname=args.get("surname")
        )
        
        if result["success"]:
            changes = ", ".join(result.get("changes_made", []))
            return f"✅ User updated successfully\nChanges: {changes}"
        else:
            return f"❌ {result['message']}"
    except Exception as e:
        return f"Error: {e}"


def handle_get_roles(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle get_roles tool."""
    try:
        from .user_management import UserManagement
        
        um = UserManagement(client)
        result = um.get_roles()
        
        if result["roles"]:
            output = f"📋 Available Roles ({result['total']}):\n\n"
            for role in result["roles"]:
                role_type = role.get("type", "unknown")
                output += f"• {role['name']} (ID: {role['roleid']}) - Type: {role_type}\n"
            return output
        else:
            return "No roles found"
    except Exception as e:
        return f"Error: {e}"


def handle_check_host_interface_availability(client: ZabbixClient, args: Dict[str, Any]) -> str:
    """Handle check_host_interface_availability tool."""
    try:
        from .user_management import UserManagement
        
        um = UserManagement(client)
        result = um.check_host_interface_availability(args.get("hostid"))
        
        status_emoji = {
            "available": "✅",
            "checking": "🔄",
            "unavailable": "❌",
            "unknown": "❓"
        }
        
        emoji = status_emoji.get(result["status"], "❓")
        output = f"{emoji} Host Interface Status\n"
        output += f"Host: {result.get('host', 'Unknown')}\n"
        output += f"Status: {result['status'].upper()}\n"
        
        if result["interfaces"]:
            output += f"Interfaces:\n"
            for iface in result["interfaces"]:
                output += f"  • {iface.get('ip')}:{iface.get('port')}\n"
        
        if result.get("error"):
            output += f"Error: {result['error']}"
        
        return output
    except Exception as e:
        return f"Error: {e}"


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
    "create_user": handle_create_user,
    "update_user": handle_update_user,
    "get_roles": handle_get_roles,
    "check_host_interface_availability": handle_check_host_interface_availability,
}


def get_tool_handler(name: str) -> Optional[Callable[[ZabbixClient, Dict[str, Any]], str]]:
    """Get handler for a tool by name."""
    return TOOL_HANDLERS.get(name)
