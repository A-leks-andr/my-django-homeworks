from django.urls import reverse


def test_index_view(client):
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 302
    assert response["Location"] == reverse("bus_stations")


def test_bus_stations_first_page(client):
    url = reverse("bus_stations")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["bus_stations"]) == 10

    page = response.context["page"]
    assert page.number == 1
    assert page.has_next() is True
    assert page.has_previous() is False

    html = response.content.decode("utf-8")
    assert "Остановка 1" in html


def test_bus_stations_second_page(client):
    url = reverse("bus_stations")
    response = client.get(url, {"page": 2})

    assert response.status_code == 200
    assert len(response.context["bus_stations"]) == 10

    page = response.context["page"]
    assert page.number == 2
    assert page.has_next() is True
    assert page.has_previous() is True

    html = response.content.decode("utf-8")
    assert "Остановка 11" in html


def test_bus_stations_last_page(client):
    url = reverse("bus_stations")
    response = client.get(url, {"page": 3})

    assert response.status_code == 200
    assert len(response.context["bus_stations"]) == 5

    page = response.context["page"]
    assert page.number == 3
    assert page.has_next() is False
    assert page.has_previous() is True

    html = response.content.decode("utf-8")
    assert "Остановка 21" in html
