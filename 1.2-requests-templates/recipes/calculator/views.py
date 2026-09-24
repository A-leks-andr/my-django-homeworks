from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    "omlet": {
        "яйца, шт": 2,
        "молоко, л": 0.1,
        "соль, ч.л.": 0.5,
    },
    "pasta": {
        "макароны, кг": 0.3,
        "сыр, г": 0.05,
    },
    "buter": {
        "хлеб, ломтик": 1,
        "колбаса, ломтик": 1,
        "сыр, ломтик": 1,
        "помидор, ломтик": 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def index_view(request):
    response = (
        "<h2>Список рецептов:</h2>"
        "<h3><a href=/omlet/>Омлет</a></h3>"
        "<h3><a href=/pasta/>Паста</a></h3>"
        "<h3><a href=/buter/>Бутерброд</a></h3>"
    )
    return HttpResponse(response)


def omlet_view(request):
    amount = int(request.GET.get("servings", 1))
    context = {"name": "Омлет", "recipe": {}}
    for k, v in DATA["omlet"].items():
        context["recipe"][k] = v * amount
    return render(request, "calculator/index.html", context)


def pasta_view(request):
    amount = int(request.GET.get("servings", 1))
    context = {"name": "Паста", "recipe": {}}
    for k, v in DATA["pasta"].items():
        context["recipe"][k] = v * amount
    return render(request, "calculator/index.html", context)


def buter_view(request):
    amount = int(request.GET.get("servings", 1))
    context = {"name": "Бутерброд", "recipe": {}}
    for k, v in DATA["buter"].items():
        context["recipe"][k] = v * amount
    return render(request, "calculator/index.html", context)
