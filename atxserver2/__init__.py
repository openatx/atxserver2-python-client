# coding: utf-8
#

import requests
import json


class Error(Exception):
    """ basic error """


class Client():
    def __init__(self, server_url: str, token: str):
        self._server_url = server_url
        self._token = token

    def _request(self, uri: str, method='get', **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + self._token}
        url = self._server_url.rstrip("/") + "/" + uri.lstrip("/")
        r = requests.request(method, url, **kwargs)
        r.raise_for_status()
        try:
            return r.json()
        except json.decoder.JSONDecodeError:
            raise RuntimeError(r.text)

    def user_info(self) -> dict:
        """
        Returns:
        {
            "username": "..xxx..",
        }
        """
        return self._request("/api/v1/user")

    def list_device(self, platform=None, present:bool=True, usable:bool=None) -> list:
        """
        Returns:
            list
        """
        params = {}
        if usable:
            params["usable"] = str(usable).lower()
        if present:
            params["present"] = str(present).lower()

        data = self._request("/api/v1/devices", params=params)
        devices = []
        for info in data['devices']:
            udid = info['udid']
            d = Device(self, udid, info)
            devices.append(d)
        return devices


class Device():
    def __init__(self, client: Client, udid: str, info: dict):
        self._client = client
        self._udid = udid
        self._info = info

    def acquire(self, idle_timeout: float = 6000.0):
        """
        Args:
            idle_timeout: device maxium using seconds
        """
        try:
            ret = self._client._request("/api/v1/user/devices",
                                        method="post",
                                        json={"udid": self._udid, "idleTimeout": idle_timeout})
            assert ret['success']
            resp = self._client._request("/api/v1/user/devices/" + self._udid)
            self._info = resp['device']
            return self._info
        except requests.HTTPError as e:
            raise Error(e)

    def release(self):
        ret = self._client._request("/api/v1/user/devices/" + self._udid,
                                    method="delete")
        return ret

    @property
    def info(self):
        return self._info

    @property
    def atx_agent_address(self):
        return self._info['source']['atxAgentAddress']

    @property
    def remote_connect_address(self):
        return self._info['source']['remoteConnectAddress']
