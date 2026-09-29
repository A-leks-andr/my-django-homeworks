import pytest
from django.urls import reverse


def test_index_view(client):
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 200

    html = response.content.decode("utf-8")
    assert "/omlet/" in html
    assert "/pasta/" in html
    assert "/buter/" in html


@pytest.mark.parametrize(
    "recipe_name, expected_title",
    [
        ("omlet", "Омлет"),
        ("pasta", "Паста"),
        ("buter", "Бутерброд"),
    ],
)
def test_name_recipe_view(client, recipe_name, expected_title):
    url = reverse("recipe", args=[recipe_name])
    response = client.get(url)

    assert response.status_code == 200

    assert response.context["name"] == expected_title


def test_unknown_recipe_view(client):
    url = reverse("recipe", args=["pizza"])
    response = client.get(url)

    assert response.status_code == 200

    html = response.content.decode("utf-8")
    assert "Такого рецепта не знаю :(" in html


@pytest.mark.parametrize(
    "get_params, expected_eggs",
    [
        ({}, 2),
        ({"servings": 3}, 6),
        ({"servings": 10}, 20),
        ({"servings": "2.5"}, 4),
        ({"servings": ""}, 2),
        ({"servings": "abc"}, 2),
        ({"servings": "-3"}, 2),
    ],
)
def test_recipe_servings(client, get_params, expected_eggs):
    url = reverse("recipe", args=["omlet"])
    response = client.get(url, get_params)

    assert response.status_code == 200
    assert response.context["recipe"]["яйца, шт"] == expected_eggs
