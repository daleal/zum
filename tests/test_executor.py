import pytest

from zum.executor import execute
from zum.requests.models import Request


class TestExecute:
    @pytest.fixture(autouse=True)
    def patch_request(self, patch_request):
        pass

    def setup_method(self):
        self.base_url = "http://localhost:8000"
        self.get = {
            "request": Request("/example", "get", {}, {}, {}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example",
                "headers": {},
                "json": {},
            },
        }
        self.post = {
            "request": Request("/example", "post", {}, {}, {}),
            "response": {
                "method": "post",
                "url": f"{self.base_url}/example",
                "headers": {},
                "json": {},
            },
        }
        self.only_params = {
            "request": Request("/example/{id}", "get", {"id": "2"}, {}, {}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example/2",
                "headers": {},
                "json": {},
            },
        }
        self.only_headers = {
            "request": Request("/example", "get", {}, {"token": "2"}, {}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example",
                "headers": {"token": "2"},
                "json": {},
            },
        }
        self.only_body = {
            "request": Request("/example", "get", {}, {}, {"name": "dani"}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example",
                "headers": {},
                "json": {"name": "dani"},
            },
        }
        self.params_and_headers = {
            "request": Request("/example/{id}", "get", {"id": "2"}, {"token": "2"}, {}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example/2",
                "headers": {"token": "2"},
                "json": {},
            },
        }
        self.params_and_body = {
            "request": Request(
                "/example/{id}", "get", {"id": "2"}, {}, {"name": "dani"}
            ),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example/2",
                "headers": {},
                "json": {"name": "dani"},
            },
        }
        self.headers_and_body = {
            "request": Request("/example", "get", {}, {"token": "2"}, {"name": "dani"}),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example",
                "headers": {"token": "2"},
                "json": {"name": "dani"},
            },
        }
        self.params_and_headers_and_body = {
            "request": Request(
                "/example/{id}", "get", {"id": "2"}, {"token": "2"}, {"name": "dani"}
            ),
            "response": {
                "method": "get",
                "url": f"{self.base_url}/example/2",
                "headers": {"token": "2"},
                "json": {"name": "dani"},
            },
        }

    def test_simple_requests(self):
        get_response = execute(self.base_url, self.get["request"])
        assert get_response == self.get["response"]

        post_response = execute(self.base_url, self.post["request"])
        assert post_response == self.post["response"]

    def test_only_params(self):
        response = execute(self.base_url, self.only_params["request"])
        assert response == self.only_params["response"]

    def test_only_headers(self):
        response = execute(self.base_url, self.only_headers["request"])
        assert response == self.only_headers["response"]

    def test_only_body(self):
        response = execute(self.base_url, self.only_body["request"])
        assert response == self.only_body["response"]

    def test_params_and_headers(self):
        response = execute(self.base_url, self.params_and_headers["request"])
        assert response == self.params_and_headers["response"]

    def test_params_and_body(self):
        response = execute(self.base_url, self.params_and_body["request"])
        assert response == self.params_and_body["response"]

    def test_headers_and_body(self):
        response = execute(self.base_url, self.headers_and_body["request"])
        assert response == self.headers_and_body["response"]

    def test_params_and_headers_and_body(self):
        response = execute(self.base_url, self.params_and_headers_and_body["request"])
        assert response == self.params_and_headers_and_body["response"]
