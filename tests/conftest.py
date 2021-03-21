"""
Module to hold all the fixtures and stuff that needs to get auto-imported
by PyTest.
"""

import httpx
import pytest


@pytest.fixture
def patch_request(monkeypatch):
    class Response:
        def __init__(self, method, url, *args, **kwargs):
            self.method = method
            self.url = url
            self.args = args
            self.kwargs = kwargs
            self._error = TypeError if method is None else None
            self._error_text = "No method specified"

        @property
        def text(self):
            return self._error_text

        def json(self):
            if self._error:
                raise self._error(self._error_text)
            return {
                "method": self.method,
                "url": self.url,
                **self.kwargs,
            }

    def mock_request(method, url, *args, **kwargs):
        return Response(method, url, *args, **kwargs)

    monkeypatch.setattr(httpx, "request", mock_request)
    monkeypatch.setattr(httpx, "Response", Response)
