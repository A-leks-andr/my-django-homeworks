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

# Названия рецептов для отображения в шаблоне.
RECIPE_TITLES = {
    "omlet": "Омлет",
    "pasta": "Паста",
    "buter": "Бутерброд",
}


def _get_servings(request):
    try:
        servings = int(float(request.GET.get("servings", 1)))
    except (ValueError, TypeError):
        servings = 1
    return max(servings, 1)


def index_view(request):
    # View для навигации по рецептам из списка, при добавлении новых рецептов
    # они автоматически будут отображаться в навигации

    response = "<h2>Список рецептов:</h2>"
    for k, v in RECIPE_TITLES.items():
        response += f"<h3><a href=/{k}/>{v}</a></h3>"
    return HttpResponse(response)


def recipe_view(request, name):
    servings = _get_servings(request)
    recipe = DATA.get(name, {})
    context = {
        "name": RECIPE_TITLES.get(name, name),
        "recipe": {
            ingredient: quantity * servings for ingredient, quantity in recipe.items()
        },
    }
    return render(request, "calculator/index.html", context)
