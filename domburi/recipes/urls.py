from django.urls import path

from . import views
from .views import RecipeGeneralView, RecipeDetailView

app_name = 'recipes'
urlpatterns = [
    path("", views.index, name='index'),
    path("recipes/", RecipeGeneralView.as_view(), name='recipes_list'),
    path("recipes/<int:pk>", RecipeDetailView.as_view(), name='recipe_detail'),
    path("upload-file/", views.upload_file, name='upload_file'),
    path("user-form/", views.user_form, name='user_form'),
    path("create-recipe/", views.create_recipe, name='create_recipe'),
]
