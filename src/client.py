import requests
from urllib.parse import urljoin


def parse_response(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        try:
            decoded_json = resp.json()
        except Exception:
            decoded_json = None
        return resp.status_code, decoded_json
    return wrapper


class RESTAPIClient(object):

    def __init__(self, url):
        self.url = url

    def _make_url(self, endpoint=None):
        if endpoint:
            return urljoin(self.url, endpoint)
        return self.url

    @parse_response
    def get(self, endpoint=None, **kwargs):
        return requests.get(self._make_url(endpoint), **kwargs)

    @parse_response
    def post(self, endpoint=None, **kwargs):
        return requests.post(self._make_url(endpoint), **kwargs)

    @parse_response
    def put(self, endpoint=None, **kwargs):
        return requests.put(self._make_url(endpoint), **kwargs)

    @parse_response
    def delete(self, endpoint=None, **kwargs):
        return requests.delete(self._make_url(endpoint), **kwargs)
