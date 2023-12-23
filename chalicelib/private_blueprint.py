from chalicelib.auth import cors
from chalice import Blueprint


class PrivateBlueprint(Blueprint):
    def __init__(self, name):
        super().__init__(name)

    def _route(self, path, method):
        return self.route(path, methods=[method], cors=cors)

    def get(self, path):
        return self._route(path, "GET")

    def post(self, path):
        return self._route(path, "POST")

    def put(self, path):
        return self._route(path, "PUT")

    def delete(self, path):
        return self._route(path, "DELETE")

    @property
    def body(self):
        return self.current_request.json_body
