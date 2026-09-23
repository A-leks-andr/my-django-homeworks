import pytest


@pytest.fixture(autouse=True)
def enable_db_for_all_tests(db):
    pass


MOCK_STATIONS = [
    {"Name": f"Остановка {i}", "Street": f"Улица {i}", "District": f"Район {i}"}
    for i in range(1, 26)
]


@pytest.fixture(autouse=True)
def mock_bus_stations(monkeypatch):
    import stations.views

    monkeypatch.setattr(stations.views, "BUS_STATIONS", MOCK_STATIONS)
