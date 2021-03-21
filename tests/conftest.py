"""
Module to hold all the fixtures and stuff that needs to get auto-imported
by PyTest.
"""

import httpx
import pytest


@pytest.fixture
def patch_request(monkeypatch):
    def mock_request(method, url, *args, **kwargs):
        return {
            "method": method,
            "url": url,
            "headers": kwargs["headers"],
            "json": kwargs["json"],
        }

    monkeypatch.setattr(httpx, "request", mock_request)
