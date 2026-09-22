import pytest


@pytest.fixture(autouse=True)
def enable_db_for_all_tests(db):
    pass


@pytest.fixture
def valid_params():
    return {"from": "USD", "to": "RUB", "amount": "10"}
