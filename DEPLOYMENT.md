# Zabbix MCP Deployment Guide

## Overview

This is a production-ready MCP server for integrating Zabbix with Claude and other AI assistants. It provides 8 tools for querying and interacting with Zabbix monitoring data.

## Installation

### Local Development

```bash
git clone https://github.com/oribot89/zabbix-mcp.git
cd zabbix-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

### Configuration

Copy `.env.example` to `.env` and update with your Zabbix credentials:

```bash
cp .env.example .env
```

Example `.env`:
```
ZABBIX_HOST=zabbix.instanceone.co
ZABBIX_USERNAME=Admin
ZABBIX_PASSWORD=zabbix
ZABBIX_PORT=443
ZABBIX_HTTPS=true
ZABBIX_VERIFY_SSL=true
```

### Testing

Before deploying, test the connection:

```bash
python test_connection.py
```

Expected output:
```
🔄 Zabbix MCP Connection Test

1️⃣  Loading configuration...
   ✅ Loaded: zabbix.instanceone.co:443

2️⃣  Creating API client...
   ✅ Client created

3️⃣  Authenticating with Zabbix...
   ✅ Authenticated

4️⃣  Fetching hosts...
   ✅ Found 5 hosts
```

## Running the Server

### Direct Execution

```bash
python -m zabbix_mcp.server
```

### With Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zabbix": {
      "command": "python",
      "args": ["-m", "zabbix_mcp.server"],
      "env": {
        "ZABBIX_HOST": "zabbix.instanceone.co",
        "ZABBIX_USERNAME": "Admin",
        "ZABBIX_PASSWORD": "zabbix",
        "ZABBIX_HTTPS": "true",
        "ZABBIX_PORT": "443"
      }
    }
  }
}
```

Then restart Claude Desktop.

## Available Tools

### get_hosts
Lists all monitored hosts with status and interface information.

**Parameters**: None

**Example**: "List all hosts in Zabbix"

### get_problems
Get currently active problems/alerts.

**Parameters**: 
- `limit` (optional): Maximum number to return (default: 50)

**Example**: "Show me all active problems"

### get_triggers
List triggers with current status.

**Parameters**:
- `limit` (optional): Maximum number to return (default: 50)

**Example**: "What triggers are in problem state?"

### get_events
Get recent events from Zabbix.

**Parameters**:
- `limit` (optional): Number of events to retrieve (default: 20)

**Example**: "Show me the last 10 events"

### get_host_details
Get detailed information about a specific host.

**Parameters**:
- `hostname` (required): Name of the host

**Example**: "Give me details about the Zabbix Server host"

### get_items
Get monitored items/metrics.

**Parameters**:
- `hostname` (optional): Filter by hostname

**Example**: "List all monitored items for the Proxmox host"

### get_host_groups
List all host groups.

**Parameters**: None

**Example**: "Show me all host groups"

### get_system_status
Get overall system status and statistics.

**Parameters**: None

**Example**: "What's the overall system status?"

## Architecture

```
zabbix-mcp/
├── src/zabbix_mcp/
│   ├── server.py       # MCP server implementation
│   ├── config.py       # Configuration loading
│   ├── client.py       # Zabbix API client
│   └── tools.py        # Tool definitions & handlers
├── test_connection.py  # Connection test script
├── README.md           # User documentation
└── DEPLOYMENT.md       # This file
```

## Troubleshooting

### "Authentication failed"
- Check `ZABBIX_USERNAME` and `ZABBIX_PASSWORD` are correct
- Verify the user has API access in Zabbix

### "Connection error"
- Verify `ZABBIX_HOST` and `ZABBIX_PORT` are correct
- Check `ZABBIX_HTTPS` matches your setup
- If using self-signed certificates: `ZABBIX_VERIFY_SSL=false`

### "No hosts found"
- Verify your Zabbix user has permission to view hosts
- Check host status in Zabbix UI

## Roadmap

- [ ] Problem acknowledgment tool
- [ ] Host creation/update/delete
- [ ] Template management
- [ ] Maintenance window scheduling
- [ ] Custom metric queries
- [ ] User and permission management
- [ ] Dashboard manipulation

## Security Notes

- **⚠️ Never commit .env to git** - use `.env.example` as template
- Store credentials in environment variables in production
- Use HTTPS when possible (`ZABBIX_HTTPS=true`)
- Restrict API token permissions in Zabbix to minimum needed
- For self-signed certificates, consider using `ZABBIX_VERIFY_SSL=false` only in development

## Support

For issues or feature requests, open an issue on GitHub: https://github.com/oribot89/zabbix-mcp

## License

MIT
