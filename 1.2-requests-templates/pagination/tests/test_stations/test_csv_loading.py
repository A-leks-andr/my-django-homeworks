import csv

import stations.views
from django.conf import settings


def test_load_bus_stations_with_valid_csv(tmp_path, monkeypatch):
    csv_file = tmp_path / "stations.csv"
    csv_file.write_text(
        "Name,Street,District\n"
        "Остановка 1,Улица 1,Район 1\n"
        "Остановка 2,Улица 2,Район 2\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(settings, "BUS_STATION_CSV", str(csv_file))

    loaded_stations, error = stations.views.load_bus_stations()

    assert len(loaded_stations) == 2
    assert loaded_stations[0] == {
        "Name": "Остановка 1",
        "Street": "Улица 1",
        "District": "Район 1",
    }
    assert loaded_stations[1]["District"] == "Район 2"
    assert error is None


def test_load_bus_stations_with_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "BUS_STATION_CSV", str(tmp_path / "no_such_file.csv"))

    loaded_stations, error = stations.views.load_bus_stations()

    assert loaded_stations == []
    assert error is not None
    assert "не удалось прочитать файл" in error
    assert "no_such_file.csv" in error


def test_load_bus_stations_with_unset_setting(monkeypatch):
    monkeypatch.setattr(settings, "BUS_STATION_CSV", None)

    loaded_stations, error = stations.views.load_bus_stations()

    assert loaded_stations == []
    assert error is not None
    assert "BUS_STATION_CSV не задана" in error


def test_load_bus_stations_with_bad_encoding(tmp_path, monkeypatch):
    csv_file = tmp_path / "bad_encoding.csv"
    # Невалидная UTF-8 последовательность: чтение бросит UnicodeDecodeError.
    csv_file.write_bytes(b"\xff\xfe\xfa")
    monkeypatch.setattr(settings, "BUS_STATION_CSV", str(csv_file))

    loaded_stations, error = stations.views.load_bus_stations()

    assert loaded_stations == []
    assert error is not None


def test_load_bus_stations_with_csv_error(tmp_path, monkeypatch):
    csv_file = tmp_path / "broken.csv"
    csv_file.write_text("Name\nvalue\n", encoding="utf-8")
    monkeypatch.setattr(settings, "BUS_STATION_CSV", str(csv_file))

    def raise_csv_error(*args, **kwargs):
        raise csv.Error("field larger than field limit")

    monkeypatch.setattr(csv, "DictReader", raise_csv_error)

    loaded_stations, error = stations.views.load_bus_stations()

    assert loaded_stations == []
    assert error is not None
