import os

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

EXCHANGE_RATES = {
    "USD_RUB": 84.1975,
    "EUR_RUB": 96.6671,
    "USD_EUR": 0.86,
    "EUR_USD": 1.15,
    "RUB_USD": 0.0118,
    "RUB_EUR": 0.0103,
}


def is_numeric(string_value: str) -> bool:
    try:
        float(string_value)
        return True
    except (ValueError, TypeError):
        return False


def home_view(request):
    template_name = "app/home.html"
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        "Главная страница": reverse("home"),
        "Показать текущее время": reverse("time"),
        "Показать содержимое рабочей директории": reverse("workdir"),
        "О проекте": reverse("about"),
        "Конвертация валют": reverse("convert"),
    }

    context = {"pages": pages}
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, возвращается просто текст
    home_url = reverse("home")
    local_time = timezone.localtime(timezone.now())
    formatted_time = local_time.strftime("%H:%M:%S")
    back = f'Вернуться на <a href="{home_url}">главная</a> страницу'
    msg = f"Страница загрузилась в: {formatted_time}"

    msg_2 = (
        'Ваше время: <span id="local-time">Загрузка...</span>'
        "<script>"
        "  function updateTime() {"
        "    const now = new Date();"
        '    const timeString = now.toTimeString().split(" ")[0];'  # формат HH:MM:SS
        '    document.getElementById("local-time").innerText = timeString;'
        "  }"
        "  updateTime();"  # Запускаем сразу при загрузке
        "  setInterval(updateTime, 1000);"  # Обновляем каждую секунду
        "</script>"
    )
    resp_html = f"{back}<br><br>{msg}<br><br>{msg_2}"
    return HttpResponse(resp_html)


def workdir_view(request):
    home_url = reverse("home")
    back = f'Вернуться на <a href="{home_url}">главная</a> страницу'
    work_dir = os.getcwd()
    files = os.listdir(work_dir)
    files_text = "<br>".join(f"- {file}" for file in files)
    resp_html = f"{back}<br><br>Файлы в рабоче директории:<br><br>{files_text}"
    return HttpResponse(resp_html)


def about_view(request):
    home_url = reverse("home")
    convert_url = reverse("convert")
    back = f'Вернуться на <a href="{home_url}">главная</a> страницу'
    msg = (
        "<h2>О проекте:</h2>"
        "<p>Это простое веб-приложение для конвертации валют.</p>"
        "<h4>Как пользоваться:</h4>"
        f"1. Перейдите на страницу <a href='{convert_url}'>"
        "<code>/convert/</code></a><br>"
        "2. Добавьте параметры в URL:<br>"
        "<code>?from=USD&to=RUB&amount=100</code><br>"
        "Доступные валюты: USD, EUR, RUB."
    )

    resp_html = f"{back}<br><br>{msg}"
    return HttpResponse(resp_html)


def convert_view(request):
    home_url = reverse("home")
    back = f'Вернуться на <a href="{home_url}">главную</a> страницу'
    info = "Информация о курсе на 19 сентября 2026 года"

    if request.GET:
        from_currency = request.GET.get("from")
        to_currency = request.GET.get("to")
        amount = request.GET.get("amount")

        if not from_currency or not to_currency or not amount:
            msg = "Один или несколько параметров не заполнены"

        else:
            curs = f"{from_currency.upper()}_{to_currency.upper()}"

            if curs not in EXCHANGE_RATES:
                msg = f"Курс для пары {from_currency} → {to_currency} не найден"

            elif not is_numeric(amount):
                msg = f"amount {amount} не является корректным числом"

            else:
                result = EXCHANGE_RATES[curs] * float(amount)
                msg = (
                    f"{float(amount):.2f} {from_currency.upper()} = "
                    f"{result:.2f} {to_currency.upper()}"
                )

    else:
        msg = (
            "Вы перешли на страницу конвертера без параметров.<br><br>"
            "Пожалуйста, укажите параметры: from, to, amount<br><br>"
            "Пример: <code>/convert/?from=USD&to=RUB&amount=10</code>"
        )
    resp_html = f"{back}<br><br>{info}<br><br>{msg}"
    return HttpResponse(resp_html)
