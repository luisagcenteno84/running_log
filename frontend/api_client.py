from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class ApiError(Exception):
    """Raised when the backend API returns an error response."""


@dataclass
class RunningTrackerApiClient:
    """Small HTTP client used by the Streamlit app."""

    base_url: str
    timeout: float = 10.0

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.base_url.rstrip('/')}{path}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise ApiError(f'Could not reach API at {self.base_url}: {exc}') from exc

        if response.is_error:
            detail = 'Request failed'
            try:
                payload = response.json()
                detail = payload.get('detail', detail)
            except ValueError:
                if response.text:
                    detail = response.text
            raise ApiError(f"{response.status_code}: {detail}")

        if not response.content:
            return None
        return response.json()

    def get_health(self) -> dict[str, Any]:
        return self._request('GET', '/health')

    def create_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request('POST', '/api/v1/users', json=payload)

    def sign_in(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request('POST', '/api/v1/users/sign-in', json=payload)

    def reset_password(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request('POST', '/api/v1/users/reset-password', json=payload)

    def update_goals(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request('PUT', f'/api/v1/users/{user_id}/goals', json=payload)

    def list_runs(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return self._request('GET', '/api/v1/runs', params=params)

    def create_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request('POST', '/api/v1/runs', json=payload)

    def get_stats(self, user_id: str | None = None) -> dict[str, Any]:
        params = {'user_id': user_id} if user_id is not None else None
        return self._request('GET', '/api/v1/stats', params=params)
