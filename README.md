# Zabbix MCP Server

A Model Context Protocol (MCP) server for integrating Zabbix monitoring platform with Claude and other AI assistants.

## Features

- 🖥️ **Host Management**: List and get details about monitored hosts
- 🔔 **Trigger Monitoring**: Query trigger status and history
- ⚠️ **Problem Alerts**: Get active problems and alerts
- 📊 **Metrics**: Access monitored items and historical data
- 👥 **Groups**: View host groups and organization
- 📅 **Events**: Query recent events
- 🔐 **Secure**: Token-based Zabbix API authentication

## Quick Start

### Prerequisites

- Python 3.10+
- Zabbix 6.0+ with API access
- Valid Zabbix API credentials

### Installation

```bash
git clone https://github.com/oribot89/zabbix-mcp.git
cd zabbix-mcp

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -e .
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your Zabbix credentials
```

### Testing Connection

```bash
python test_connection.py
```

### Running the Server

```bash
python -m zabbix_mcp.server
```

## Available Tools

### Query Tools (Read-Only)

#### get_hosts
List all monitored hosts in Zabbix.

#### get_problems
Get active problems/alerts.

#### get_triggers
List triggers with their current status.

#### get_events
Get recent events from Zabbix.

#### get_host_details
Get detailed information about a specific host.

**Parameters:**
- `hostname` (required): Name of the host to look up

#### get_items
Get monitored items (metrics).

**Parameters:**
- `hostname` (optional): Filter by hostname

#### get_host_groups
List all host groups.

#### get_system_status
Get overall system status and statistics.

#### get_templates
List all available Zabbix templates.

#### check_host_interface_availability
Check if a host's agent interface is available and responding.

**Parameters:**
- `hostid` (required): Host ID to check

### Management Tools (Write Operations)

#### create_host ⭐ **RECOMMENDED**
Create a new Zabbix host for monitoring containers or servers.

**Recommended Parameters:**
- `hostname` (required): Internal identifier (e.g., `beta-servicedesk`)
- `display_name` (required): Display name in frontend (e.g., `Beta Service Desk (CTID 105)`)
- `ip_address` (required): Agent IP for polling (e.g., `10.0.0.7`)
- `port` (optional): Agent port (default: `10050`)
- `group_id` (optional): Host group ID (default: `2` = Linux servers)
- `template_id` (optional): Template ID (default: `10001` = Linux by Zabbix agent)

**Why use API instead of manual DB edits:**
- Zabbix internal state properly synchronized
- Sequence tables automatically managed
- Interface marked available=1 immediately
- Agent polling begins within 30-60 seconds
- Guaranteed data consistency

**Example:**
```
Create host: beta-servicedesk
Display: Beta Service Desk (CTID 105)
IP: 10.0.0.7
Port: 10050
```

#### add_host_interface
Add a network interface to an existing host for agent polling.

**Parameters:**
- `hostid` (required): Host ID
- `ip_address` (required): IP address
- `port` (optional): Agent port (default: `10050`)
- `interface_type` (optional): 1=Agent, 2=SNMP, 3=IPMI, 4=JMX (default: 1)

#### link_template
Link a template to a host to auto-generate monitoring items.

**Parameters:**
- `hostname` (required): Host name
- `template_name` (required): Template name

#### sync_zabbix_sequences
Fix sequence table desynchronization (call once after manual DB operations).

**Note:** Only needed if sequences became out of sync. API-based operations handle this automatically.

## Claude Desktop Integration

Add to your Claude Desktop config file (`~/.config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "zabbix": {
      "command": "python",
      "args": ["-m", "zabbix_mcp.server"],
      "env": {
        "ZABBIX_HOST": "zabbix.example.com",
        "ZABBIX_USERNAME": "Admin",
        "ZABBIX_PASSWORD": "your-password"
      }
    }
  }
}
```

## License

MIT

## Author

Ori_ (oribot@edinprint3d.co.uk)
