#!/usr/bin/env python3
"""Test script to validate Zabbix MCP connection."""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zabbix_mcp.config import load_config
from zabbix_mcp.client import ZabbixClient


def test_connection():
    """Test connection to Zabbix and basic API calls."""
    
    print("🔄 Zabbix MCP Connection Test\n")
    
    print("1️⃣  Loading configuration...")
    try:
        config = load_config()
        print(f"   ✅ Loaded: {config.host}:{config.port}")
    except ValueError as e:
        print(f"   ❌ Config error: {e}")
        return False
    
    print("\n2️⃣  Creating API client...")
    try:
        client = ZabbixClient(
            base_url=config.base_url,
            username=config.username,
            password=config.password,
            verify_ssl=config.verify_ssl,
        )
        print(f"   ✅ Client created")
    except Exception as e:
        print(f"   ❌ Client error: {e}")
        return False
    
    print("\n3️⃣  Authenticating with Zabbix...")
    try:
        client.authenticate()
        print(f"   ✅ Authenticated")
    except Exception as e:
        print(f"   ❌ Auth error: {e}")
        return False
    
    print("\n4️⃣  Fetching hosts...")
    try:
        hosts = client.get_hosts()
        print(f"   ✅ Found {len(hosts)} hosts")
        for host in hosts[:3]:
            print(f"      • {host.get('name')} ({host.get('host')})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "="*50)
    print("✅ Connection test successful!")
    print("="*50)
    return True


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
