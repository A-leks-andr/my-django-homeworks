import os

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


def home_view(request):
    template_name = "app/home.html"
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        "Главная страница": reverse("home"),
        "Показать текущее время": reverse("time"),
        "Показать содержимое рабочей директории": reverse("workdir"),
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
