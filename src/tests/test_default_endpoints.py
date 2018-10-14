import pytest


@pytest.mark.parametrize('endpoint', [
    '/posts',
    '/comments',
    '/albums',
    '/photos',
    '/users',
    '/todos'
])
def test_get_example(client, endpoint):
    code, body = client.get(endpoint)
    assert code == 200, 'Response code {} != 200 !'.format(code)


@pytest.mark.parametrize('endpoint', [
    '/posts',
    '/comments',
    '/albums',
    '/photos',
    '/users',
    '/todos'
])
def test_allowed_methods(client, endpoint):
    allowed_methods = ['GET', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE']
    methods = client.get_allowed_methods(endpoint)
    assert allowed_methods == methods, \
        'The endpoint {!r} should support the following methods: {}, ' \
        'but actually - {} !'.format(endpoint, allowed_methods, methods)
