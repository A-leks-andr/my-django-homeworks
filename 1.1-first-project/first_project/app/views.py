import math
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

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
        number = float(string_value)

    except (ValueError, TypeError):
        return False

    return math.isfinite(number)


def home_view(request):
    template_name = "app/home.html"

    pages = {
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
    back = f'Вернуться на <a href="{home_url}">главную</a> страницу'
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
    back = f'Вернуться на <a href="{home_url}">главную</a> страницу'
    work_dir = os.getcwd()
    files = os.listdir(work_dir)
    files_text = "<br>".join(f"- {escape(file)}" for file in files)
    resp_html = f"{back}<h3>Файлы в рабочей директории:</h3>{files_text}"
    return HttpResponse(resp_html)


def about_view(request):
    home_url = reverse("home")
    convert_url = reverse("convert")
    back = f'Вернуться на <a href="{home_url}">главную</a> страницу'
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

        esc_from = escape(from_currency.upper()) if from_currency else ""
        esc_to = escape(to_currency.upper()) if to_currency else ""
        esc_amount = escape(amount) if amount else ""

        if not from_currency or not to_currency or not amount:
            msg = "Один или несколько параметров не заполнены"

        else:
            curs = f"{from_currency.upper()}_{to_currency.upper()}"

            if curs not in EXCHANGE_RATES:
                msg = f"Курс для пары {esc_from} → {esc_to} не найден"

            elif not is_numeric(amount):
                msg = f"amount {esc_amount} не является корректным числом"

            else:
                result = EXCHANGE_RATES[curs] * float(amount)
                msg = f"{float(amount):.2f} {esc_from} = {result:.2f} {esc_to}"

    else:
        msg = (
            "Вы перешли на страницу конвертера без параметров.<br><br>"
            "Пожалуйста, укажите параметры: from, to, amount<br><br>"
            "Пример: <code>/convert/?from=USD&to=RUB&amount=10</code>"
        )
    resp_html = f"{back}<br><br>{info}<br><br>{msg}"
    return HttpResponse(resp_html)
