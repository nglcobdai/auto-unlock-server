import re
from ipaddress import ip_address
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

_HOSTNAME_PATTERN = re.compile(
    r"^(?=.{1,253}\.?$)(?!-)(?:[A-Za-z0-9-]{1,63}\.)*[A-Za-z0-9-]{1,63}\.?$"
)


class HostValidationMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in {"http", "websocket"}:
            await self.app(scope, receive, send)
            return

        host = self._get_host(scope)
        if not host or not self._is_valid_host(host):
            response = PlainTextResponse("Invalid Host header", status_code=400)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    @staticmethod
    def _get_host(scope: Scope) -> str | None:
        host_headers = [
            value.decode("ascii", errors="ignore").strip()
            for key, value in scope.get("headers", [])
            if key.lower() == b"host"
        ]
        if len(host_headers) != 1:
            return None
        return host_headers[0]

    @classmethod
    def _is_valid_host(cls, host: str) -> bool:
        if not host or any(char.isspace() for char in host):
            return False

        if host.startswith("["):
            if "]" not in host:
                return False
            address, port = host[1:].split("]", 1)
            return cls._is_valid_ip_address(address) and cls._is_valid_port(port)

        hostname, port = cls._split_host_and_port(host)
        if not hostname or not cls._is_valid_port(port):
            return False

        if cls._is_valid_ip_address(hostname):
            return True

        return _HOSTNAME_PATTERN.fullmatch(hostname) is not None

    @staticmethod
    def _split_host_and_port(host: str) -> tuple[str, str]:
        if host.count(":") > 1:
            return "", ""
        if ":" not in host:
            return host, ""
        hostname, port = host.rsplit(":", 1)
        return hostname, f":{port}"

    @staticmethod
    def _is_valid_ip_address(host: str) -> bool:
        try:
            ip_address(host)
        except ValueError:
            return False
        return True

    @staticmethod
    def _is_valid_port(port: str) -> bool:
        if not port:
            return True
        if not port.startswith(":"):
            return False
        port_number = port[1:]
        return port_number.isdecimal() and 0 < int(port_number) <= 65535
