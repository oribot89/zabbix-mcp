"""Configuration management for Zabbix MCP."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class ZabbixConfig:
    """Zabbix connection configuration."""
    
    host: str
    username: str
    password: str
    port: int = 80
    https: bool = False
    verify_ssl: bool = True
    
    @property
    def base_url(self) -> str:
        """Build base URL for Zabbix API."""
        protocol = "https" if self.https else "http"
        return f"{protocol}://{self.host}:{self.port}"
    
    @property
    def api_url(self) -> str:
        """Get Zabbix API endpoint."""
        return f"{self.base_url}/api_jsonrpc.php"


def load_config() -> ZabbixConfig:
    """Load configuration from environment variables."""
    load_dotenv()
    
    host = os.getenv("ZABBIX_HOST")
    if not host:
        raise ValueError("ZABBIX_HOST environment variable is required")
    
    username = os.getenv("ZABBIX_USERNAME", "Admin")
    password = os.getenv("ZABBIX_PASSWORD")
    if not password:
        raise ValueError("ZABBIX_PASSWORD environment variable is required")
    
    port = int(os.getenv("ZABBIX_PORT", "80"))
    https = os.getenv("ZABBIX_HTTPS", "false").lower() == "true"
    verify_ssl = os.getenv("ZABBIX_VERIFY_SSL", "true").lower() == "true"
    
    return ZabbixConfig(
        host=host,
        username=username,
        password=password,
        port=port,
        https=https,
        verify_ssl=verify_ssl,
    )
