import pytest

from src.utils import check_fields


@pytest.mark.todos
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/todos/1', 200),
        ('/todos/0', 404),
        ('/todos/200', 200),
        ('/todos/201', 404),
        ('/users/1/todos', 200),
        ('/users/11/todos', 404)
    ])
def test_get_todo(client, endpoint, expected_code):
    code, body = client.get(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.todos
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/todos', {'title': 'foo', 'completed': 'true', 'userId': '1'}, 201),
        ('/users/1/todos', {'title': 'foo', 'completed': 'true'}, 201),
        ('/todos', {'title': 'foo', 'completed': 'true'}, 400),
        ('/todos', {'title': 'foo', 'completed': 'true', 'userId': 11}, 400),
        ('/todos', {}, 400),
        ('/todos', {'id': 201}, 400),
        ('/todos', {'id': 1}, 400),
        ('/todos/1', {'id': 1}, 400)
    ])
def test_create_todo(client, endpoint, data, expected_code):
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


@pytest.mark.todos
@pytest.mark.parametrize(
    'endpoint, data, expected_code, user_id',
    [
        ('/users/1/todos', {'title': 'foo', 'completed': 'true'}, 201, '1'),
        ('/users/2/todos', {'title': 'foo', 'completed': 'true'}, 201, '2'),
        ('/users/11/todos', {'title': 'foo', 'completed': 'true'}, 404, None),
        ('/users/1/todos', {'id': 101}, 400, None),
        ('/users/1/todos', {'id': 1}, 400, None)
    ])
def test_create_user_todo(client, endpoint, data, expected_code, user_id):
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


@pytest.mark.todos
@pytest.mark.parametrize(
    'endpoint, data, expected_code',
    [
        ('/todos/1', {
            'title': 'foo', 'completed': 'false', 'userId': '1'
        }, 200),
        ('/todos/1', {'title': 'foo', 'completed': 'true'}, 200),
        ('/todos/1', {}, 400),
        ('/todos/1', {'id': 101}, 400),
        ('/todos/1', {'id': 10}, 400),
        ('/todos/201', {
            'title': 'foo', 'completed': 'true', 'userId': '1'
        }, 404)
    ])
def test_update_todo(client, endpoint, data, expected_code):
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


@pytest.mark.todos
@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/todos/1', 200),
        ('/todos/0', 404),
        ('/todos/200', 200),
        ('/todos/201', 404)
    ])
def test_delete_todo(client, endpoint, expected_code):
    code, body = client.delete(endpoint)
    assert code == expected_code, \
        'Actual response code does not equal expected code: {} != {}' \
        .format(code, expected_code)


@pytest.mark.todos
@pytest.mark.parametrize(
    'filter_endpoint, check_endpoints',
    [
        ('/todos?id=1', ['/todos/1']),
        ('/todos?id=0', []),
        ('/todos?completed=true', []),
        ('/todos?id=1&completed=false', []),
        ('/todos?id=200', ['/todos/200']),
        ('/todos?id=201', []),
        ('/todos?id=201&id=1', ['/todos/1']),
        ('/todos?id=100&id=1', ['/todos/1', '/todos/100']),
        ('/todos?userId=1', ['/users/1/todos']),
        ('/todos?userId=1&userId=2', ['/users/1/todos', '/users/2/todos'])
    ])
def test_filter_todos(client, filter_endpoint, check_endpoints):
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
