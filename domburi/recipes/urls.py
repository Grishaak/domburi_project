from django.urls import path

from . import views
from .views import RecipeGeneralView, RecipeDetailView, RecipeCreateView, RecipeListView, RecipeUpdateView, \
    CategoryListView, CategoryDetailView

app_name = 'recipes'

urlpatterns = [
    path("", RecipeGeneralView.as_view(), name='index'),
    path("recipes/", RecipeListView.as_view(), name='recipes_list'),
    path("recipes/<int:pk>", RecipeDetailView.as_view(), name='recipe_detail'),
    path("user-form/", views.user_form, name='user_form'),
    path("create-recipe/", RecipeCreateView.as_view(), name='recipe_create'),
    path("recipes/<int:pk>/update", RecipeUpdateView.as_view(), name='recipe_update'),

    path("recipes/categories/", CategoryListView.as_view(), name='category_list'),
    path("recipes/categories/<int:pk>", CategoryDetailView.as_view(), name='category_detail'),

    path("upload-file/", views.upload_file, name='upload_file'),
]
