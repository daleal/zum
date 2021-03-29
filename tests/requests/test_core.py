from pathlib import Path

import pytest

from zum.requests.core import generate_request
from zum.requests.errors import InvalidRequestBodyFileError
from zum.requests.models import Request


class TestGenerateRequestWithMissingBodyFilePath:
    def setup_method(self):
        self.raw_endpoint = {"route": "/example/", "method": "post", "body": "json"}
        self.arguments = []
        self.expected_route = "/example/"

    def test_request_generation_missing_file(self):
        with pytest.raises(InvalidRequestBodyFileError):
            generate_request(self.raw_endpoint, self.arguments)


class TestGenerateRequestWithNonExistantBodyFile:
    def setup_method(self):
        self.json_file_path = Path(".").joinpath(
            "tests", "requests", "non_existant_body_file.json"
        )
        self.raw_endpoint = {"route": "/example/", "method": "post", "body": "json"}
        self.arguments = [self.json_file_path.absolute()]
        self.expected_route = "/example/"

    def test_request_generation_missing_file(self):
        with pytest.raises(InvalidRequestBodyFileError):
            generate_request(self.raw_endpoint, self.arguments)

    def test_request_generation_body_file_is_a_folder(self):
        self.json_file_path.mkdir()
        with pytest.raises(InvalidRequestBodyFileError):
            generate_request(self.raw_endpoint, self.arguments)
        self.json_file_path.rmdir()


class TestGenerateRequestWithExistingBodyFile:
    def setup_method(self):
        self.json_file_path = Path(".").joinpath("tests", "requests", "json_body.json")
        self.raw_endpoint = {
            "route": "/example/{id}?query={query}",
            "method": "post",
            "params": ["id", "query"],
            "headers": ["Authorization"],
            "body": "json",
        }
        self.params = {"id": 35, "query": "mystring"}
        self.headers = {"Authorization": "Bearer F"}
        self.body = {"name": "Dani", "city": "Barcelona"}
        self.arguments = [
            self.params["id"],
            self.params["query"],
            self.headers["Authorization"],
            self.json_file_path.absolute(),
        ]
        self.expected_route = (
            f"/example/{self.params['id']}?query={self.params['query']}"
        )

        from json import dumps

        with self.json_file_path.open("a") as request_body_file:
            request_body_file.write(dumps(self.body))

    def test_request_generation(self):
        request = generate_request(self.raw_endpoint, self.arguments)
        self.json_file_path.unlink()

        assert isinstance(request, Request)
        assert request.params == self.params
        assert request.headers == self.headers
        assert request.body == self.body
        assert request.route == self.expected_route


class TestGenerateRequestWithoutBodyFile:
    def setup_method(self):
        self.raw_endpoint = {
            "route": "/example/{id}?query={query}",
            "method": "post",
            "params": ["id", "query"],
            "headers": ["Authorization"],
            "body": ["name", "city"],
        }
        self.params = {"id": 35, "query": "mystring"}
        self.headers = {"Authorization": "Bearer F"}
        self.body = {"name": "Dani", "city": "Barcelona"}
        self.arguments = [
            self.params["id"],
            self.params["query"],
            self.headers["Authorization"],
            self.body["name"],
            self.body["city"],
        ]
        self.expected_route = (
            f"/example/{self.params['id']}?query={self.params['query']}"
        )

    def test_request_generation(self):
        request = generate_request(self.raw_endpoint, self.arguments)
        assert isinstance(request, Request)
        assert request.params == self.params
        assert request.headers == self.headers
        assert request.body == self.body
        assert request.route == self.expected_route
