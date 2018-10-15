import pytest

from src.utils import check_fields


@pytest.mark.comments
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/comments/1', 200),
        ('/comments/0', 404),
        ('/comments/500', 200),
        ('/comments/501', 404),
        ('/posts/1/comments', 200),
        ('/posts/101/comments', 404)
    ])
def test_get_comment(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.comments
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar', 'postId': '1'
        }, 201),
        ('/posts/1/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar'
        }, 201),
        ('/comments', {'name': 'foo', 'email': 'a@a', 'body': 'bar'}, 400),
        ('/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar', 'postId': '101'
        }, 400),
        ('/comments', {}, 400),
        ('/comments', {'id': 101}, 400),
        ('/comments', {'id': 1}, 400),
        ('/comments/1', {'id': 1}, 400)
    ])
def test_create_comment(client, endpoint, data, expected_code):
    code, body = client.post(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 201:
        assert body.get('id'), 'The resource does not have ID!'
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert check_fields(data, body),\
            'Received data {} should contain' \
            'all fields of sent data {}!'.format(body, data)


@pytest.mark.comments
@pytest.mark.parametrize(
    'endpoint, data, expected_code, post_id',
    [
        ('/posts/1/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar'
        }, 201, '1'),
        ('/posts/2/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar'
        }, 201, '2'),
        ('/posts/101/comments', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar'
        }, 404, None),
        ('/posts/1/comments', {'id': 101}, 400, None),
        ('/posts/1/comments', {'id': 1}, 400, None)
    ])
def test_create_post_comment(client, endpoint, data, expected_code, post_id):
    code, body = client.post(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 201:
        assert body.get('id'), 'The resource does not have ID!'
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert post_id == body.get('postId'), \
            'postId is not correct!'


@pytest.mark.comments
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/comments/1', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar', 'postId': '1'
        }, 200),
        ('/comments/1', {'name': 'foo', 'email': 'a@a', 'body': 'bar'}, 200),
        ('/comments/1', {}, 400),
        ('/comments/1', {'id': 101}, 400),
        ('/comments/1', {'id': 10}, 400),
        ('/comments/501', {
            'name': 'foo', 'email': 'a@a', 'body': 'bar', 'postId': '1'
        }, 404)
    ])
def test_update_comment(client, endpoint, data, expected_code):
    code, body = client.put(
        endpoint,
        data=data)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)
    if code == 200:
        assert body.get('id'), 'The resource does not have ID!'
        # NOTE: Assume we send data with correct fields and
        #  received data should contain all fields of sent data
        assert check_fields(data, body),\
            'Received data {} should contain' \
            'all fields of sent data {}!'.format(body, data)


@pytest.mark.comments
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/comments/1', 200),
        ('/comments/0', 404),
        ('/comments/500', 200),
        ('/comments/501', 404)
    ])
def test_delete_comment(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.comments
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/comments?id=1', ['/comments/1']),
        ('/comments?id=0', []),
        ('/comments?id=500', ['/comments/500']),
        ('/comments?id=501', []),
        ('/comments?id=501&id=1', ['/comments/1']),
        ('/comments?id=500&id=1', ['/comments/1', '/comments/500']),
        ('/comments?postId=1', ['/posts/1/comments']),
        ('/comments?postId=1&postId=2',
         ['/posts/1/comments', '/posts/2/comments'])
    ])
def test_filter_comments(client, filter_endpoint, check_endpoints):
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
