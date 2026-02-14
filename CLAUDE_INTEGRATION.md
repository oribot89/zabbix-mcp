# Claude Desktop Integration Guide

## Quick Setup

Your Zabbix MCP is ready to integrate with Claude Desktop. Follow these steps:

### 1. Locate Your Claude Desktop Config

Find your Claude config file:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 2. Add the Zabbix MCP Configuration

Copy the `mcpServers` section from this file's config template into your Claude config:

```json
{
  "mcpServers": {
    "zabbix-mcp": {
      "command": "python",
      "args": ["-m", "zabbix_mcp.server"],
      "env": {
        "PYTHONPATH": "/home/openclaw_user/.openclaw/workspace/zabbix-mcp/src",
        "ZABBIX_HOST": "zabbix.instanceone.co",
        "ZABBIX_USERNAME": "Admin",
        "ZABBIX_PASSWORD": "zabbix",
        "ZABBIX_PORT": "443",
        "ZABBIX_HTTPS": "true",
        "ZABBIX_VERIFY_SSL": "true"
      },
      "cwd": "/home/openclaw_user/.openclaw/workspace/zabbix-mcp"
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

### 4. Verify Connection

Once Claude loads, try asking:

```
"What hosts are monitored in Zabbix?"
"Show me active problems"
"List all triggers"
"What's the system status?"
```

## Available Tools

The Zabbix MCP provides 8 tools for Claude to use:

### Monitoring & Status
- **get_system_status** - Overall system stats (hosts, problems, triggers)
- **get_hosts** - List all monitored hosts
- **get_problems** - Active problems/alerts
- **get_triggers** - Current trigger status

### Details
- **get_host_details** - Detailed host information (hostname required)
- **get_items** - Monitored metrics (optionally filtered by hostname)
- **get_host_groups** - All host groups
- **get_events** - Recent events from Zabbix

## Example Queries for Claude

```
"Which hosts have problems right now?"
"Show me details about the Proxmox host"
"What are the top issues in my infrastructure?"
"List all metrics being monitored"
"What happened in the last 10 events?"
```

## Troubleshooting

### MCP Not Connecting
1. Verify Python path is correct (absolute path required)
2. Check ZABBIX_HOST is reachable: `ping zabbix.instanceone.co`
3. Run the test script locally:
   ```bash
   cd /home/openclaw_user/.openclaw/workspace/zabbix-mcp
   source venv/bin/activate
   python test_connection.py
   ```

### Authentication Fails
1. Verify credentials in the config (Admin/zabbix)
2. Check Zabbix user exists and is active: https://zabbix.instanceone.co/
3. Ensure API access is enabled for the Admin user

### No Tools Available
1. Restart Claude Desktop
2. Check the Claude dev tools (Cmd+Shift+I) for MCP errors
3. Look for error messages in Claude's logs

## Advanced: Custom Configuration

If you need to change credentials or host, edit the `env` section:

```json
"env": {
  "ZABBIX_HOST": "your-zabbix-domain.com",
  "ZABBIX_USERNAME": "your-username",
  "ZABBIX_PASSWORD": "your-password",
  "ZABBIX_PORT": "443",
  "ZABBIX_HTTPS": "true"
}
```

Then restart Claude Desktop.

## Security Notes

⚠️ **WARNING**: The config above stores credentials in plain text. For production:

1. Use `.env` file instead (place at repo root):
   ```bash
   ZABBIX_HOST=zabbix.instanceone.co
   ZABBIX_USERNAME=Admin
   ZABBIX_PASSWORD=zabbix
   ZABBIX_PORT=443
   ZABBIX_HTTPS=true
   ZABBIX_VERIFY_SSL=true
   ```

2. Modify config to not include `env` section:
   ```json
   {
     "command": "python",
     "args": ["-m", "zabbix_mcp.server"],
     "cwd": "/home/openclaw_user/.openclaw/workspace/zabbix-mcp"
   }
   ```

3. The MCP server will automatically load from `.env`

## Next Steps

- **Explore monitoring**: Ask Claude about your infrastructure
- **Create custom queries**: Claude can help interpret Zabbix data
- **Set up alerts**: Integrate with Zabbix webhooks for proactive monitoring
- **Expand tools**: Add more specialized tools (templates, users, maintenance windows)

## Support

For issues or feature requests, see the [main README.md](README.md).
