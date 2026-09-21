import pytest
from django.urls import reverse


def test_home_view(client):
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert reverse("home") in response.content.decode("utf-8")
    assert reverse("about") in response.content.decode("utf-8")
    assert reverse("time") in response.content.decode("utf-8")
    assert reverse("workdir") in response.content.decode("utf-8")
    assert reverse("convert") in response.content.decode("utf-8")


def test_convert_view_success(client, valid_params):
    url = reverse("convert")
    response = client.get(url, data=valid_params)

    assert response.status_code == 200
    assert "Информация о курсе на 19 сентября 2026 года" in response.content.decode(
        "utf-8"
    )
    assert "10.00 USD = 841.98 RUB" in response.content.decode("utf-8")


def test_convert_view_no_params(client):
    url = reverse("convert")
    response = client.get(url)

    assert response.status_code == 200
    assert "Пожалуйста, укажите параметры: from, to, amount" in response.content.decode(
        "utf-8"
    )


@pytest.mark.parametrize(
    "currency_data, expected_string",
    [
        ({"from": "USD", "to": "RUB", "amount": "10"}, "10.00 USD = 841.98 RUB"),
        ({"from": "EUR", "to": "RUB", "amount": "5"}, "5.00 EUR = 483.34 RUB"),
        ({"from": "RUB", "to": "USD", "amount": "1000"}, "1000.00 RUB = 11.80 USD"),
        ({"from": "usd", "to": "eur", "amount": "10"}, "10.00 USD = 8.60 EUR"),
    ],
)
def test_convert_math_calculations(client, currency_data, expected_string):
    url = reverse("convert")
    response = client.get(url, data=currency_data)

    assert response.status_code == 200
    assert expected_string in response.content.decode("utf-8")


@pytest.mark.parametrize(
    "invalid_data, expected_error",
    [
        (
            {"from": "USD", "to": "RUB", "amount": ""},
            "Один или несколько параметров не заполнены",
        ),
        (
            {"from": "", "to": "RUB", "amount": "10"},
            "Один или несколько параметров не заполнены",
        ),
        (
            {"from": "GBP", "to": "JPY", "amount": "100"},
            "Курс для пары GBP → JPY не найден",
        ),
        (
            {"from": "USD", "to": "RUB", "amount": "not-a-number"},
            "amount not-a-number не является корректным числом",
        ),
    ],
)
def test_convert_view_validation_errors(client, invalid_data, expected_error):
    url = reverse("convert")
    response = client.get(url, data=invalid_data)

    assert response.status_code == 200
    assert expected_error in response.content.decode("utf-8")


def test_time_view(client):
    url = reverse("time")
    response = client.get(url)

    assert response.status_code == 200

    html_content = response.content.decode("utf-8")

    assert "Страница загрузилась в:" in html_content
    assert "Ваше время" in html_content
    assert 'id="local-time"' in html_content
    assert "setInterval(updateTime, 1000);" in html_content


def test_workdir_view(client):
    url = reverse("workdir")
    response = client.get(url)

    assert response.status_code == 200

    html_content = response.content.decode("utf-8")

    assert "manage.py" in html_content


def test_about_view(client):
    url = reverse("about")
    response = client.get(url)

    assert response.status_code == 200

    html_content = response.content.decode("utf-8")

    assert "О проекте:" in html_content
    assert "Это простое веб-приложение для конвертации валют" in html_content
    assert "Доступные валюты: USD, EUR, RUB" in html_content
    assert reverse("convert") in html_content


# команда для проверки покрытие кода
# pytest --cov=. --cov-report=term-missing
