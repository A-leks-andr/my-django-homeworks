from django.urls import reverse
from django.utils.formats import date_format


def test_index_redirects_to_catalog(client):
    """Корневой URL '/' перенаправляет на каталог."""
    response = client.get("/")

    assert response.status_code == 302
    assert response.url == reverse("catalog")


def test_catalog_returns_200(client):
    """Страница каталога открывается."""
    response = client.get(reverse("catalog"))

    assert response.status_code == 200


def test_catalog_without_sort_returns_all_phones(client, phone_factory):
    """Без параметра sort отображаются все телефоны."""
    phone_factory(_quantity=5)

    response = client.get(reverse("catalog"))

    assert response.status_code == 200
    assert response.context["phones"].count() == 5


def test_catalog_shows_phones(client, phone_factory):
    """В HTML каталога есть название телефона и ссылка на его страницу."""
    phone = phone_factory(name="Iphone X")

    response = client.get(reverse("catalog"))
    html = response.content.decode("utf-8")

    assert response.status_code == 200
    assert phone.name in html
    assert reverse("phone", args=[phone.slug]) in html


def test_catalog_sort_by_name(client, phone_factory):
    """?sort=name сортирует телефоны по алфавиту."""
    phone_factory(name="Bravo")
    phone_factory(name="Alpha")
    phone_factory(name="Charlie")

    response = client.get(reverse("catalog"), {"sort": "name"})
    names = list(response.context["phones"].values_list("name", flat=True))

    assert names == ["Alpha", "Bravo", "Charlie"]


def test_catalog_sort_by_min_price(client, phone_factory):
    """?sort=min_price сортирует от дешёвых к дорогим."""
    phone_factory(name="Nokia 8", price="30000.00")
    phone_factory(name="Iphone X", price="10000.00")
    phone_factory(name="Samsung Galaxy", price="50000.00")

    response = client.get(reverse("catalog"), {"sort": "min_price"})
    prices = [p.price for p in response.context["phones"]]

    assert prices == sorted(prices)


def test_catalog_sort_by_max_price(client, phone_factory):
    """?sort=max_price сортирует от дорогих к дешёвым."""
    phone_factory(name="Nokia 8", price="30000.00")
    phone_factory(name="Iphone X", price="10000.00")
    phone_factory(name="Samsung Galaxy", price="50000.00")

    response = client.get(reverse("catalog"), {"sort": "max_price"})
    prices = [p.price for p in response.context["phones"]]

    assert prices == sorted(prices, reverse=True)


def test_product_page_returns_200(client, phone_factory):
    """Страница телефона содержит название, изображение, цену, дату и LTE."""
    phone = phone_factory(
        name="Nokia 8",
        image="https://example.com/nokia-8.jpg",
        price="19999.99",
        release_date="2013-01-20",
        lte_exists=True,
    )
    phone.refresh_from_db()

    response = client.get(reverse("phone", args=[phone.slug]))
    html = response.content.decode("utf-8")
    assert response.status_code == 200
    assert phone.name in html
    assert phone.image in html
    assert str(phone.price).replace(".", ",") in html
    assert date_format(phone.release_date) in html
    assert "есть" in html  # фильтр yesno:"есть,нет" при lte_exists=True


def test_product_not_found_404(client):
    """Несуществующий slug возвращает 404."""
    response = client.get(reverse("phone", args=["nonexistent-slug"]))

    assert response.status_code == 404
