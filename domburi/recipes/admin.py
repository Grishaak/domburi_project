from django.contrib import admin
from recipes.models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
