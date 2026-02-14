"""Zabbix API client wrapper."""

import requests
import logging
from typing import Any, Dict, List, Optional
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class ZabbixAPIError(Exception):
    """Zabbix API error."""
    pass


class ZabbixClient:
    """Zabbix API client for direct API access."""
    
    def __init__(self, base_url: str, username: str, password: str, verify_ssl: bool = True):
        """
        Initialize Zabbix API client.
        
        Args:
            base_url: Zabbix base URL (e.g., http://zabbix.example.com)
            username: Zabbix API username
            password: Zabbix API password
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api_jsonrpc.php"
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self._request_id = 0
    
    def _get_request_id(self) -> int:
        """Get next request ID."""
        self._request_id += 1
        return self._request_id
    
    def authenticate(self) -> bool:
        """
        Authenticate with Zabbix API.
        
        Returns:
            True if authentication successful
            
        Raises:
            ZabbixAPIError: If authentication fails
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "username": self.username,
                    "password": self.password,
                },
                "id": self._get_request_id(),
            }
            
            response = self.session.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise ZabbixAPIError(f"Authentication failed: {data['error']}")
            
            if "result" not in data:
                raise ZabbixAPIError("No token in response")
            
            self.token = data["result"]
            logger.info("Successfully authenticated with Zabbix")
            return True
            
        except RequestException as e:
            raise ZabbixAPIError(f"Connection error: {e}")
    
    def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make authenticated API call to Zabbix.
        
        Args:
            method: API method name (e.g., 'host.get')
            params: Method parameters
            
        Returns:
            API response result
            
        Raises:
            ZabbixAPIError: If API call fails
        """
        if not self.token:
            raise ZabbixAPIError("Not authenticated. Call authenticate() first.")
        
        if params is None:
            params = {}
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": self.token,
            "id": self._get_request_id(),
        }
        
        try:
            response = self.session.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                error_msg = data["error"]
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("data", str(error_msg))
                raise ZabbixAPIError(f"API error: {error_msg}")
            
            return data.get("result", {})
            
        except RequestException as e:
            raise ZabbixAPIError(f"Connection error: {e}")
    
    def get_hosts(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Get all hosts.
        
        Returns:
            List of hosts
        """
        params = {
            "output": "extend",
            "selectInterfaces": "extend",
        }
        params.update(kwargs)
        return self.call("host.get", params)
    
    def get_host_by_name(self, hostname: str) -> Optional[Dict[str, Any]]:
        """Get host by name."""
        hosts = self.call("host.get", {
            "output": "extend",
            "filter": {"host": hostname},
            "selectInterfaces": "extend",
        })
        return hosts[0] if hosts else None
    
    def get_triggers(self, **kwargs) -> List[Dict[str, Any]]:
        """Get all triggers."""
        params = {
            "output": "extend",
            "selectHosts": "extend",
        }
        params.update(kwargs)
        return self.call("trigger.get", params)
    
    def get_events(self, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """Get recent events."""
        params = {
            "output": "extend",
            "limit": limit,
            "sortfield": "clock",
            "selectHosts": "extend",
        }
        params.update(kwargs)
        return self.call("event.get", params)
    
    def get_problems(self, **kwargs) -> List[Dict[str, Any]]:
        """Get active problems."""
        params = {
            "output": "extend",
            "recent": True,
        }
        params.update(kwargs)
        return self.call("problem.get", params)
    
    def get_items(self, hostid: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
        """Get items, optionally filtered by host."""
        params = {
            "output": "extend",
            "selectHosts": "extend",
            "selectValueMaps": "extend",
        }
        if hostid:
            params["hostids"] = hostid
        params.update(kwargs)
        return self.call("item.get", params)
    
    def get_history(self, itemid: str, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """Get item history."""
        params = {
            "output": "extend",
            "itemids": itemid,
            "limit": limit,
            "sortfield": "clock",
        }
        params.update(kwargs)
        return self.call("history.get", params)
    
    def acknowledge_event(self, eventids: List[str], message: str = "") -> bool:
        """Acknowledge problem events."""
        self.call("event.acknowledge", {
            "eventids": eventids,
            "action": 1,
            "message": message,
        })
        return True
    
    def get_dashboards(self, **kwargs) -> List[Dict[str, Any]]:
        """Get dashboards."""
        params = {
            "output": "extend",
        }
        params.update(kwargs)
        return self.call("dashboard.get", params)
    
    def get_groups(self, **kwargs) -> List[Dict[str, Any]]:
        """Get host groups."""
        params = {
            "output": "extend",
        }
        params.update(kwargs)
        return self.call("hostgroup.get", params)
