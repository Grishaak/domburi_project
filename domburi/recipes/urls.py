from django.urls import path

from . import views
from .views import RecipeGeneralView, RecipeDetailView, RecipeCreateView, RecipeListView

app_name = 'recipes'
urlpatterns = [
    path("", RecipeGeneralView.as_view(), name='index'),
    path("recipes/", RecipeListView.as_view(), name='recipes_list'),
    path("recipes/<int:pk>", RecipeDetailView.as_view(), name='recipe_detail'),
    path("upload-file/", views.upload_file, name='upload_file'),
    path("user-form/", views.user_form, name='user_form'),
    path("create-recipe/", RecipeCreateView.as_view(), name='create_recipe'),
]
