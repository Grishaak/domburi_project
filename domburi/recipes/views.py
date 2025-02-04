from django.http import HttpResponse
from django.shortcuts import render

from recipes.models import Recipe


def index(request):
    return render(request, template_name='recipes/index.html')


def get_recipes(request):
    context = {
        'recipes':
            Recipe.objects.select_related('author').prefetch_related('categories').all()
    }
    return render(request, template_name='recipes/recipes.html', context=context)
