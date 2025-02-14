from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe


class RecipeApiSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = (
        "pk", "name", "description", "cooking_steps", "cooking_time", "image", "author", "categories")
