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
        """Make full url for given resource endpoint.

        :param endpoint: str, resource endpoint
        :return: str, full url
        """
        if endpoint:
            return urljoin(self.url, endpoint)
        return self.url

    def get_allowed_methods(self, endpoint, **kwargs):
        """Get allowed methods for resource.

        :param endpoint: str, resource endpoint
        :param kwargs: additional params to OPTIONS method
        :return: list, list of allowed methods
        or empty if status code is not 204
        """
        resp = requests.options(self._make_url(endpoint), **kwargs)
        if resp.status_code != 204:
            return []
        return resp.headers['Access-Control-Allow-Methods'].split(',')

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
    def patch(self, endpoint=None, **kwargs):
        return requests.patch(self._make_url(endpoint), **kwargs)

    @parse_response
    def delete(self, endpoint=None, **kwargs):
        return requests.delete(self._make_url(endpoint), **kwargs)
