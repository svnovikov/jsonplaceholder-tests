import pytest

from src.utils import check_fields


@pytest.mark.posts
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/posts/1', 200),
        ('/posts/0', 404),
        ('/posts/100', 200),
        ('/posts/101', 404),
        ('/users/1/posts', 200),
        ('/users/11/posts', 404)
    ])
def test_get_post(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.posts
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/posts', {'title': 'foo', 'body': 'bar', 'userId': '1'}, 201),
        ('/users/1/posts', {'title': 'foo', 'body': 'bar'}, 201),
        ('/posts', {'title': 'foo', 'body': 'bar'}, 400),
        ('/posts', {'title': 'foo', 'body': 'bar', 'userId': 11}, 400),
        ('/posts', {}, 400),
        ('/posts', {'id': 101}, 400),
        ('/posts', {'id': 1}, 400),
        ('/posts/1', {'id': 1}, 400)
    ])
def test_create_post(client, endpoint, data, expected_code):
    code, body = client.post(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 201:
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert check_fields(data, body),\
            'Received data {} should contain' \
            'all fields of sent data {}!'.format(body, data)


@pytest.mark.posts
@pytest.mark.parametrize(
    'endpoint, data, expected_code, user_id',
    [
        ('/users/1/posts', {'title': 'foo', 'body': 'bar'}, 201, '1'),
        ('/users/2/posts', {'title': 'foo', 'body': 'bar'}, 201, '2'),
        ('/users/11/posts', {'title': 'foo', 'body': 'bar'}, 404, None),
        ('/users/1/posts', {'id': 101}, 400, None),
        ('/users/1/posts', {'id': 1}, 400, None)
    ])
def test_create_user_post(client, endpoint, data, expected_code, user_id):
    code, body = client.post(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 201:
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert user_id == body.get('userId'), \
            'UserId is not correct!'


@pytest.mark.posts
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/posts/1', {'title': 'foo', 'body': 'bar', 'userId': '1'}, 200),
        ('/posts/1', {'title': 'foo', 'body': 'bar'}, 200),
        ('/posts/1', {}, 400),
        ('/posts/1', {'id': 101}, 400),
        ('/posts/1', {'id': 10}, 400),
        ('/posts/101', {'title': 'foo', 'body': 'bar', 'userId': '1'}, 404)
    ])
def test_update_post(client, endpoint, data, expected_code):
    code, body = client.put(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 200:
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert check_fields(data, body),\
            'Received data {} should contain' \
            'all fields of sent data {}!'.format(body, data)


@pytest.mark.posts
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/posts/1', 200),
        ('/posts/0', 404),
        ('/posts/100', 200),
        ('/posts/101', 404)
    ])
def test_delete_post(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.posts
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/posts?id=1', ['/posts/1']),
        ('/posts?id=0', []),
        ('/posts?id=100', ['/posts/100']),
        ('/posts?id=101', []),
        ('/posts?id=101&id=1', ['/posts/1']),
        ('/posts?id=100&id=1', ['/posts/1', '/posts/100']),
        ('/posts?userId=1', ['/users/1/posts']),
        ('/posts?userId=1&userId=2', ['/users/1/posts', '/users/2/posts'])
    ])
def test_filter_posts(client, filter_endpoint, check_endpoints):
    code, body = client.get(filter_endpoint)
    assert code == 200, \
        'Actual response code does not equal expected code: {} != 200' \
        .format(code)
    if not check_endpoints:
        return

    check_bodies = []
    for check_endpoint in check_endpoints:
        _, check_body = client.get(check_endpoint)
        if isinstance(check_body, list):
            check_bodies.extend(check_body)
        else:
            check_bodies.append(check_body)
    assert body == check_bodies, 'Filter does not work!'
