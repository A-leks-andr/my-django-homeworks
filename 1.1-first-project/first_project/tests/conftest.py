import pytest


@pytest.fixture(autouse=True)
def enable_db_for_all_tests(db):
    pass


@pytest.fixture
def valid_params():
    return {"from": "USD", "to": "RUB", "amount": "10"}


@pytest.fixture
def workdir_with_malicious_file(monkeypatch):
    """Подменяет рабочую директорию и список файлов на время теста."""
    files = ["<script>alert(1)</script>.py", "normal.py", "manage.py"]
    monkeypatch.setattr("app.views.os.getcwd", lambda: "/tmp")
    monkeypatch.setattr("app.views.os.listdir", lambda path: files)
    return files
