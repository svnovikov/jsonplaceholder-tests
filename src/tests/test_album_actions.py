import pytest

from src.utils import check_fields


@pytest.mark.albums
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/albums/1', 200),
        ('/albums/0', 404),
        ('/albums/100', 200),
        ('/albums/101', 404),
        ('/users/1/albums', 200),
        ('/users/11/albums', 404)
    ])
def test_get_album(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.albums
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/albums', {'title': 'foo', 'userId': '1'}, 201),
        ('/users/1/albums', {'title': 'foo'}, 201),
        ('/albums', {'title': 'foo'}, 400),
        ('/albums', {'title': 'foo', 'userId': 11}, 400),
        ('/albums', {}, 400),
        ('/albums', {'id': 101}, 400),
        ('/albums', {'id': 1}, 400),
        ('/albums/1', {'id': 1}, 400)
    ])
def test_create_album(client, endpoint, data, expected_code):
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


@pytest.mark.albums
@pytest.mark.parametrize(
    'endpoint, data, expected_code, user_id',
    [
        ('/users/1/albums', {'title': 'foo'}, 201, '1'),
        ('/users/2/albums', {'title': 'foo'}, 201, '2'),
        ('/users/11/albums', {'title': 'foo'}, 404, None),
        ('/users/1/albums', {'id': 101}, 400, None),
        ('/users/1/albums', {'id': 1}, 400, None)
    ])
def test_create_user_album(client, endpoint, data, expected_code, user_id):
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
        assert user_id == body.get('userId'), \
            'UserId is not correct!'


@pytest.mark.albums
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/albums/1', {'title': 'foo', 'userId': '1'}, 200),
        ('/albums/1', {'title': 'foo'}, 200),
        ('/albums/1', {}, 400),
        ('/albums/1', {'id': 101}, 400),
        ('/albums/1', {'id': 10}, 400),
        ('/albums/101', {'title': 'foo', 'userId': '1'}, 404)
    ])
def test_update_album(client, endpoint, data, expected_code):
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


@pytest.mark.albums
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/albums/1', 200),
        ('/albums/0', 404),
        ('/albums/100', 200),
        ('/albums/101', 404)
    ])
def test_delete_album(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.albums
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/albums?id=1', ['/albums/1']),
        ('/albums?id=0', []),
        ('/albums?id=100', ['/albums/100']),
        ('/albums?id=101', []),
        ('/albums?id=101&id=1', ['/albums/1']),
        ('/albums?id=100&id=1', ['/albums/1', '/albums/100']),
        ('/albums?userId=1', ['/users/1/albums']),
        ('/albums?userId=1&userId=2', ['/users/1/albums', '/users/2/albums'])
    ])
def test_filter_albums(client, filter_endpoint, check_endpoints):
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
