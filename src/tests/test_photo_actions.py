import pytest

from src.utils import check_fields


@pytest.mark.photos
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/photos/1', 200),
        ('/photos/0', 404),
        ('/photos/5000', 200),
        ('/photos/5001', 404),
        ('/albums/1/photos', 200),
        ('/albums/101/photos', 404)
    ])
def test_get_photo(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.photos
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952',
            'albumId': '1'
        }, 201),
        ('/albums/1/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 201),
        ('/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 400),
        ('/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952',
            'albumId': '101'
        }, 400),
        ('/photos', {}, 400),
        ('/photos', {'id': 101}, 400),
        ('/photos', {'id': 1}, 400),
        ('/photos/1', {'id': 1}, 400)
    ])
def test_create_photo(client, endpoint, data, expected_code):
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


@pytest.mark.photos
@pytest.mark.parametrize(
    'endpoint, data, expected_code, album_id',
    [
        ('/albums/1/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 201, '1'),
        ('/albums/2/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 201, '2'),
        ('/albums/101/photos', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 404, None),
        ('/albums/1/photos', {'id': 101}, 400, None),
        ('/albums/1/photos', {'id': 1}, 400, None)
    ])
def test_create_album_photo(client, endpoint, data, expected_code, album_id):
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
        assert album_id == body.get('albumId'), \
            'albumId is not correct!'


@pytest.mark.photos
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/photos/1', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952',
            'albumId': '10'
        }, 200),
        ('/photos/1', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
        }, 200),
        ('/photos/1', {}, 400),
        ('/photos/1', {'id': 101}, 400),
        ('/photos/1', {'id': 10}, 400),
        ('/photos/5001', {
            'title': 'foo',
            'url': 'https://via.placeholder.com/600/92c952',
            'thumbnailUrl': 'https://via.placeholder.com/150/92c952',
            'albumId': '10'
        }, 404)
    ])
def test_update_photo(client, endpoint, data, expected_code):
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


@pytest.mark.photos
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/photos/1', 200),
        ('/photos/0', 404),
        ('/photos/5000', 200),
        ('/photos/5001', 404)
    ])
def test_delete_photo(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.photos
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/photos?id=1', ['/photos/1']),
        ('/photos?id=0', []),
        ('/photos?id=5000', ['/photos/5000']),
        ('/photos?id=5001', []),
        ('/photos?id=5001&id=1', ['/photos/1']),
        ('/photos?id=5000&id=1', ['/photos/1', '/photos/5000']),
        ('/photos?albumId=1', ['/albums/1/photos']),
        ('/photos?albumId=1&albumId=2',
         ['/albums/1/photos', '/albums/2/photos'])
    ])
def test_filter_photos(client, filter_endpoint, check_endpoints):
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
