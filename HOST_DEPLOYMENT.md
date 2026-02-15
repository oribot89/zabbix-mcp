# Zabbix Host Deployment Guide

**Last Updated:** 2026-02-15 23:45 UTC  
**Status:** ✅ Production-Ready (Tested with 4 containers)

## Overview

Use the `create_host` MCP tool to deploy new Zabbix monitoring for containers or servers. This guide covers the proven API-based approach that works reliably.

## Quick Start (1-Command Deployment)

```bash
# Via MCP (recommended)
zabbix-mcp create_host \
  --hostname beta-servicedesk \
  --display_name "Beta Service Desk (CTID 105)" \
  --ip_address 10.0.0.7
```

Or programmatically:

```python
client = ZabbixClient("http://zabbix.example.com", "Admin", "password")
client.authenticate()

result = client.create_host(
    hostname="beta-servicedesk",
    display_name="Beta Service Desk (CTID 105)",
    ip_address="10.0.0.7",
    port="10050",
    group_id="2",  # Linux servers
    template_id="10001"  # Linux by Zabbix agent
)
```

## Step-by-Step Deployment

### Prerequisites

1. **Zabbix Server Running**
   - Endpoint: `http://zabbix.example.com/api_jsonrpc.php`
   - User: `Admin` with API access
   - Password: Available (stored in Vault or env var)

2. **Agent Installed on Container**
   - Zabbix Agent2 v7.0+
   - Running: `systemctl start zabbix-agent2`
   - Hostname set in config: `Hostname=instanceone-web`

3. **Network Connectivity**
   - Zabbix server can reach agent IP on port 10050
   - Test: `curl -I http://agent-ip:10050` (will fail gracefully - expected)

### Step 1: Create Host

```bash
create_host \
  --hostname instanceone-web \
  --display_name "InstanceOne Web (CTID 103)" \
  --ip_address 10.0.0.5
```

**Expected Response:**
```
✅ Host Created Successfully!

🖥️ Hostname: instanceone-web
📝 Display: InstanceOne Web (CTID 103)
🌐 IP: 10.0.0.5:10050
🔗 Host ID: 10692
📋 Interface ID: 43
📊 Template: Linked (10001)

Next: Wait 30-60 seconds for agent to start reporting metrics.
```

### Step 2: Wait for Agent Connection

The Zabbix server will:
1. Load the host configuration
2. Begin polling the agent on 10.0.0.5:10050
3. Mark interface as `available=1` once connection succeeds
4. Auto-generate items from linked template

**Timeline:**
- T+0s: Host created
- T+5s: Interface added, template linked
- T+10s: Server reads new configuration
- T+15-30s: First poll requests reach agent
- T+30-60s: First metrics appear in database

### Step 3: Verify

Check metric flow:

```bash
# Via MCP
check_host_interface_availability --hostid 10692

# SQL (if you have DB access)
SELECT h.name, COUNT(hu.value) 
FROM hosts h 
LEFT JOIN items i ON h.hostid = i.hostid 
LEFT JOIN history_uint hu ON i.itemid = hu.itemid 
WHERE h.hostid = 10692 
GROUP BY h.name;
```

**Expected:** Interface `available=1`, metrics growing

## Configuration Reference

### Agent Config (Container)

Before deploying, ensure agent is configured:

```bash
# On the container (e.g., CTID 103)
cat /etc/zabbix/zabbix_agent2.conf

# Should contain:
Server=10.0.0.3              # Zabbix server internal IP
Hostname=instanceone-web     # Must match create_host --hostname
ListenIP=0.0.0.0             # Listen on all interfaces
ListenPort=10050             # Standard port
```

### Common Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `hostname` | Required | Internal ID, no spaces, lowercase recommended |
| `display_name` | Required | User-friendly name, shown in frontend |
| `ip_address` | Required | IP for Zabbix server to reach agent |
| `port` | 10050 | Standard Zabbix agent port |
| `group_id` | 2 | Linux servers group (always use 2 for Linux) |
| `template_id` | 10001 | Linux by Zabbix agent (auto-generates 43+ items) |

### Available Templates

| ID | Name | Items | Use For |
|---|---|---|---|
| 10001 | Linux by Zabbix agent | 43 | Linux servers/containers |
| 10562 | Zabbix agent active | 71 | Active mode agents |
| 10563 | Generic by SNMP | - | SNMP devices |
| 10564 | ICMP Ping | - | Network devices |

## Troubleshooting

### Interface Stuck at available=0

**Symptom:** Host created but metrics not flowing, interface shows available=0

**Cause:** Server can't reach agent, or agent hostname mismatch

**Solution:**
1. Check agent is running: `systemctl status zabbix-agent2`
2. Verify hostname matches: `grep Hostname= /etc/zabbix/zabbix_agent2.conf`
3. Test connectivity: `nc -zv 10.0.0.5 10050` (from server)
4. Restart agent: `systemctl restart zabbix-agent2`
5. Wait 60 seconds, check again

### No Items Generated

**Symptom:** Host created, interface available=1, but no items listed

**Cause:** Template not linked or already unlinked

**Solution:**
```bash
# Re-link template
link_template \
  --hostname instanceone-web \
  --template_name "Linux by Zabbix agent"
```

### Metrics Not Appearing

**Symptom:** Items exist, interface available, but no metric values

**Cause:** Agent not responding to polls, or collection interval too long

**Solution:**
1. Check agent logs: `tail /var/log/zabbix/zabbix_agent2.log`
2. Look for "processing update request" messages
3. If none: agent not receiving polls (interface available issue)
4. Restart server: `systemctl restart zabbix-server`

### Host Already Exists

**Symptom:** Error "Host with the same name already exists"

**Cause:** Hostname not unique in Zabbix database

**Solution:**
```bash
# Use different hostname
create_host --hostname instanceone-web-v2 ...

# Or delete old host first (via UI or API)
```

## Sequence Synchronization

**When to use:** Only after manual database edits

If you made direct SQL edits and sequences are out of sync:

```bash
sync_zabbix_sequences
```

This outputs SQL commands to fix:
- `hosts.hostid` sequence
- `interface.interfaceid` sequence
- `items.itemid` sequence

**Note:** API-based operations (like `create_host`) handle sequences automatically. Only needed if you edited database manually.

## Best Practices

✅ **DO:**
- Use `create_host` MCP tool (handles full workflow)
- Verify agent config BEFORE deploying
- Wait 60 seconds before checking metrics
- Use Vault for credentials (avoid hardcoding)
- Document hostnames and IPs in your infrastructure tracker

❌ **DON'T:**
- Manually edit database (use API only)
- Mix API operations with DB edits (causes sequence desync)
- Create hosts without agent installed
- Assume immediate metric flow (takes 30-60s)
- Hardcode Zabbix passwords in code

## Performance Metrics

Typical deployment timeline:
- Host creation: < 1 second
- Interface setup: < 1 second
- Template linking: < 1 second
- First agent poll: 15-30 seconds
- First metrics in database: 30-60 seconds

Template auto-generates ~43 items for Linux servers.

## Automation Example

Deploy 4 containers at once:

```python
containers = [
    {"hostname": "instanceone-web", "ip": "10.0.0.5"},
    {"hostname": "vault-server", "ip": "10.0.0.6"},
    {"hostname": "beta-servicedesk", "ip": "10.0.0.7"},
    {"hostname": "beta-website", "ip": "10.0.0.8"},
]

for c in containers:
    result = create_host(
        hostname=c["hostname"],
        display_name=f"{c['hostname'].title()} (CTID)",
        ip_address=c["ip"]
    )
    print(f"✅ {c['hostname']}: {result}")
    time.sleep(5)

print(f"\n✅ All hosts deployed. Wait 60 seconds for metrics.")
```

## References

- [Zabbix API Documentation](https://www.zabbix.com/documentation/7.0/en/manual/api)
- [Zabbix Agent Setup](../ZABBIX_AGENT_SETUP.md)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)

## Support

If issues persist, check:
1. Agent logs: `/var/log/zabbix/zabbix_agent2.log`
2. Server logs: `/var/log/zabbix/zabbix_server.log`
3. Network: `ping agent-ip`, `nc -zv agent-ip 10050`
4. Zabbix UI: http://zabbix.example.com/ → Monitoring → Hosts

---

**Last Tested:** 2026-02-15 23:45 UTC on 4 production containers
