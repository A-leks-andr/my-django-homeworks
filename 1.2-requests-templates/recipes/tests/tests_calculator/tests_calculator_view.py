import pytest
from calculator.views import DATA
from django.urls import reverse


def test_index_view(client):
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 200

    html = response.content.decode("utf-8")
    assert reverse("omlet") in html
    assert reverse("pasta") in html
    assert reverse("buter") in html


@pytest.mark.parametrize(
    "get_params, expected_eggs",
    [
        ({}, 10),
        ({"servings": 3}, 30),
        ({"servings": 5}, 50),
    ],
)
def test_omlet_view(client, get_params, expected_eggs):
    original_data = DATA.copy()
    DATA.clear()
    DATA.update({"omlet": {"тестовое_яйцо": 10}})
    try:
        url = reverse("omlet")
        response = client.get(url, get_params)
        assert response.status_code == 200
        assert response.context["name"] == "Омлет"
        assert response.context["recipe"]["тестовое_яйцо"] == expected_eggs

    finally:
        DATA.clear
        DATA.update(original_data)


@pytest.mark.parametrize(
    "get_params, expected_cheese",
    [
        ({}, 5),
        ({"servings": 3}, 15),
        ({"servings": 5}, 25),
    ],
)
def test_pasta_view(client, get_params, expected_cheese):
    original_data = DATA.copy()
    DATA.clear()
    DATA.update({"pasta": {"тестовый_сыр": 5}})
    try:
        url = reverse("pasta")
        response = client.get(url, get_params)
        assert response.status_code == 200
        assert response.context["name"] == "Паста"
        assert response.context["recipe"]["тестовый_сыр"] == expected_cheese

    finally:
        DATA.clear
        DATA.update(original_data)


@pytest.mark.parametrize(
    "get_params, expected_bread",
    [
        ({}, 1),
        ({"servings": 3}, 3),
        ({"servings": 5}, 5),
    ],
)
def test_buter_view(client, get_params, expected_bread):
    original_data = DATA.copy()
    DATA.clear()
    DATA.update({"buter": {"тестовый_хлеб": 1}})
    try:
        url = reverse("buter")
        response = client.get(url, get_params)
        assert response.status_code == 200
        assert response.context["name"] == "Бутерброд"
        assert response.context["recipe"]["тестовый_хлеб"] == expected_bread

    finally:
        DATA.clear
        DATA.update(original_data)
