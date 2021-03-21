"""
A module to hold the request execution logic for the zum library.
"""

import httpx

from zum.requests.models import Request


def execute(base_url: str, request: Request) -> httpx.Response:
    """Executes a request with the base URL."""
    url = f"{base_url.rstrip('/')}{request.route}"
    return httpx.request(
        request.method, url, headers=request.headers, json=request.body
    )
