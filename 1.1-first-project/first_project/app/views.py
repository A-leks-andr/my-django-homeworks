from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import datetime
import os


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime('%H:%M:%S')
    msg = f'Текущее время: {formatted_time}'
    return HttpResponse(msg)


def workdir_view(request):
    work_dir = os.getcwd()
    files = os.listdir(work_dir)
    files_text = '<br>'.join(f"- {file}" for file in files)
    return HttpResponse(f"Файлы в рабочей директории: <br><br>{files_text}")
