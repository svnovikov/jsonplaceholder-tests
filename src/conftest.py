import pytest

from src.client import RESTAPIClient


@pytest.fixture(scope='session')
def client():
    return RESTAPIClient('https://jsonplaceholder.typicode.com/')
