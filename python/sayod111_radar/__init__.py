"""Official zero-dependency Python client for Sayod 111 Intelligence Radar API."""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterator

DEFAULT_BASE_URL = "https://sayod111-radar-api.sayodyalawi.workers.dev"


class RadarAPIError(RuntimeError):
    def __init__(self, status: int, body: Any):
        super().__init__(f"Sayod 111 API error HTTP {status}: {body}")
        self.status = status
        self.body = body


class RadarClient:
    def __init__(self, api_key: str | None = None, base_url: str = DEFAULT_BASE_URL, timeout: int = 30):
        self.api_key = api_key.strip() if api_key else None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None, body: Any = None, auth: bool = False) -> Any:
        url = self.base_url + path
        if params:
            clean_p = {k: v for k, v in params.items() if v is not None and v != ""}
            if clean_p:
                url += "?" + urllib.parse.urlencode(clean_p)
        headers = {"Accept": "application/json", "User-Agent": "sayod111-radar-py/1.0.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif auth:
            raise ValueError("This endpoint requires a paid api_key (dp_live_...).")
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if resp.headers.get("Content-Type", "").startswith("application/json") else raw
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            raise RadarAPIError(exc.code, parsed) from exc

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/v1/health")

    def live_audit(self, domain: str, mode: str = "shopify") -> dict[str, Any]:
        return self._request("POST", "/v1/public/live-audit", body={"domain": domain, "mode": mode})

    def ria_search(self, q: str = "", state: str = "", mismatch_only: bool = False, limit: int = 15) -> dict[str, Any]:
        return self._request("GET", "/v1/public/ria-search", params={"q": q, "state": state, "mismatch_only": 1 if mismatch_only else 0, "limit": limit})

    def biotech_search(self, q: str = "", state: str = "", agency: str = "", limit: int = 15) -> dict[str, Any]:
        return self._request("GET", "/v1/public/biotech-search", params={"q": q, "state": state, "agency": agency, "limit": limit})

    def sample(self, vertical: str, fmt: str = "json") -> Any:
        return self._request("GET", f"/v1/public/sample/{vertical}", params={"format": fmt})

    def me(self) -> dict[str, Any]:
        return self._request("GET", "/v1/me", auth=True)

    def radar_page(self, vertical: str, limit: int = 50, min_score: int = 0, delta_only: bool = False, cursor: str | int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "min_score": min_score, "delta_only": 1 if delta_only else 0}
        if cursor is not None:
            params["after_crd" if vertical == "ria_wealth" else "after_id"] = cursor
        return self._request("GET", f"/v1/radar/{vertical}", params=params, auth=True)

    def iter_radar(self, vertical: str, max_pages: int = 10, **kwargs: Any) -> Iterator[dict[str, Any]]:
        cursor = None
        for _ in range(max_pages):
            page = self.radar_page(vertical, cursor=cursor, **kwargs)
            rows = page.get("data") or []
            if not rows:
                break
            yield from rows
            cursor = page.get("next_after_crd" if vertical == "ria_wealth" else "next_after_id")
            if not cursor:
                break

    def create_alert(self, feed_type: str, target_endpoint: str, cadence: str = "weekly") -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/alerts",
            body={"feed_type": feed_type, "delivery_channel": "webhook", "target_endpoint": target_endpoint, "cadence": cadence},
            auth=True,
        )
