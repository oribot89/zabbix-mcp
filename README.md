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

### get_hosts
List all monitored hosts in Zabbix.

### get_problems
Get active problems/alerts.

### get_triggers
List triggers with their current status.

### get_events
Get recent events from Zabbix.

### get_host_details
Get detailed information about a specific host.

**Parameters:**
- `hostname` (required): Name of the host to look up

### get_items
Get monitored items (metrics).

**Parameters:**
- `hostname` (optional): Filter by hostname

### get_host_groups
List all host groups.

### get_system_status
Get overall system status and statistics.

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
