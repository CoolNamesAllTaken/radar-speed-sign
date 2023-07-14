"""
Module: 'urequests' on micropython-v1.19.1-rp2
"""
# MCU: {'ver': 'v1.19.1', 'build': '', 'sysname': 'rp2', 'platform': 'rp2', 'version': '1.19.1', 'release': '1.19.1', 'port': 'rp2', 'family': 'micropython', 'name': 'micropython', 'machine': 'Raspberry Pi Pico W with RP2040', 'nodename': 'rp2'}
from typing import Any

def get(url: str, **kwargs) -> Any:
    ...

def put(url: str, **kwargs) -> Any:
    ...


class Response():
    def __init__(self, f) -> None:
        ...

    def close(self) -> None:
        ...
    
    @property
    def status_code(self) -> int | None:
        """The status code of the response. Defaults to `None`"""
        ...

    @property
    def encoding(self) -> str | None:
        """The encoding of the response content. Defaults to `utf-8`"""
        ...

    @property
    def reason(self) -> bytes | None:
        """Like string representation of the status_code in bytes form. Defaults to `None`"""
        ...

    @property
    def headers(self) -> dict[str, str] | None:
        """The response headers. Defaults to `None`"""
        ...

    @property
    def text(self) -> str|None:
        ...
    
    def json(self) -> str|None:
        """requires `ujson` module"""
        ...

    @property
    def content(self) -> bytes | None:
        """The response content in bytes. Defaults to `None`"""
        ...

def request(
    method: str, 
    url: str, 
    data=None, 
    json=None, 
    headers={}, 
    stream=None,
    auth=None,
    timeout=None,
    parse_headers: bool=True,
    ) -> Response|None:
    """Could raise at least NotImplementedError, ValueError and OSErro"""
    ...

def head(url: str, **kwargs) -> Any:
    ...

def post(url: str, **kwargs) -> Any:
    ...

def patch(url: str, **kwargs) -> Any:
    ...

def delete(url: str, **kwargs) -> Any:
    ...

