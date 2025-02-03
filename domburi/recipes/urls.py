from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("recipes/", views.get_recipes, name='recipes')
]
