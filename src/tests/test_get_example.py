def test_get_example(client):
    code, body = client.get('todos/1')
    assert code == 200, 'Response code is not 200!'
    assert body, 'Response body is empty'
