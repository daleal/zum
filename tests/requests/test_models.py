from zum.requests.models import Request


class TestRequestModel:
    def setup_method(self):
        self.simple = {"route": "/example", "method": "get", "params": {}, "body": {}}
        self.complex = {
            "route": "/example/{id}?query={query}",
            "method": "get",
            "params": {"query": "nais", "id": 69},
            "body": {},
        }
        self.simple_route = "/example"
        self.complex_route = f"/example/{self.complex['params']['id']}?query={self.complex['params']['query']}"

    def test_simple_request_route_interpolation(self):
        request = Request(**self.simple)
        assert request.route == self.simple_route

    def test_complex_request_route_interpolation(self):
        request = Request(**self.complex)
        assert request.route == self.complex_route
