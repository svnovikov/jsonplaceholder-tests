import pytest

from src.utils import check_fields


@pytest.mark.users
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/users/1', 200),
        ('/users/0', 404),
        ('/users/10', 200),
        ('/users/11', 404)
    ])
def test_get_user(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}'\
        .format(code, expected_code)


@pytest.mark.users
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/users', {
            'company':
                {'bs': 'harness real-time e-markets',
                 'name': 'Romaguera-Crona',
                 'catchPhrase': 'Multi-layered client-server neural-net'},
            'phone': '1-770-736-8031 x56442', 'name': 'Leanne Graham',
            'email': 'Sincere@april.biz', 'username': 'Bret',
            'website': 'hildegard.org', 'address':
                {'zipcode': '92998-3874', 'suite': 'Apt. 556', 'geo':
                    {'lat': '-37.3159', 'lng': '81.1496'},
                 'city': 'Gwenborough', 'street': 'Kulas Light'}}, 201),
        ('/users', {
            'email': 'Sincere@april.biz', 'phone':
                '1-770-736-8031 x56442', 'address': {},
            'name': 'Leanne Graham', 'company': {},
            'website': 'hildegard.org', 'username': 'Bret'}, 201),
        ('/users', {
            'name': 'Leanne Graham', 'phone': '1-770-736-8031 x56442',
            'username': 'Bret', 'email': 'Sincere@april.biz',
            'website': 'hildegard.org'}, 201),
        ('/users', {'name': 'foo'}, 201),
        ('/users', {}, 400),
        ('/users', {'id': 11}, 400),
        ('/users', {'id': 1}, 400),
        ('/users/1', {'id': 1}, 400)
    ])
def test_create_user(client, endpoint, data, expected_code):
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


@pytest.mark.users
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/users/1', {
            'company':
                {'bs': 'harness real-time e-markets',
                 'name': 'Romaguera-Crona',
                 'catchPhrase': 'Multi-layered client-server neural-net'},
            'phone': '1-770-736-8031 x56442', 'name': 'Leanne Graham',
            'email': 'Sincere@april.biz', 'username': 'Bret',
            'website': 'hildegard.org', 'address':
                {'zipcode': '92998-3874', 'suite': 'Apt. 556', 'geo':
                    {'lat': '-37.3159', 'lng': '81.1496'},
                 'city': 'Gwenborough', 'street': 'Kulas Light'}}, 200),
        ('/users/1', {
            'email': 'Sincere@april.biz', 'phone':
                '1-770-736-8031 x56442', 'address': {},
            'name': 'Leanne Graham', 'company': {},
            'website': 'hildegard.org', 'username': 'Bret'}, 200),
        ('/users/1', {
            'name': 'Leanne Graham', 'phone': '1-770-736-8031 x56442',
            'username': 'Bret', 'email': 'Sincere@april.biz',
            'website': 'hildegard.org'}, 200),
        ('/users/1', {'name': 'foo'}, 200),
        ('/users/1', {}, 400),
        ('/users/10', {'id': 1}, 400),
        ('/users/11', {}, 404)
    ])
def test_update_user(client, endpoint, data, expected_code):
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


@pytest.mark.users
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/users/1', 200),
        ('/users/0', 404),
        ('/users/10', 200),
        ('/users/11', 404)
    ])
def test_delete_user(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.users
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/users?id=1', ['/users/1']),
        ('/users?id=0', []),
        ('/users?id=10', ['/users/10']),
        ('/users?id=11', []),
        ('/users?id=11&id=1', ['/users/1']),
        ('/users?id=10&id=1', ['/users/1', '/users/10'])
    ])
def test_filter_users_by_id(client, filter_endpoint, check_endpoints):
    code, body = client.get(filter_endpoint)
    assert code == 200, \
        'Actual response code does not equal expected code: {} != 200' \
        .format(code)
    if not check_endpoints:
        return
    check_bodies = [client.get(check_endpoint)[1]
                    for check_endpoint in check_endpoints]
    assert body == check_bodies, 'Filter does not work!'
