from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ForeignKey, CharField, TextField, ImageField, IntegerField, ManyToManyField


def destination_of_image(instance: "Recipe", filename: str) -> str:
    return "".join(f"recipes/recipe_{instance.pk}/image/{filename}")


class Recipe(models.Model):
    name = CharField(max_length=40, null=False)
    description = TextField(max_length=2000, null=False, blank=True)
    cooking_steps = IntegerField(default=1,
                                 validators=[
                                     MaxValueValidator(100),
                                     MinValueValidator(1)
                                 ]
                                 )
    cooking_time = IntegerField(default=5, validators=[
        MaxValueValidator(1440),
        MinValueValidator(5)
    ])
    image = ImageField(null=True, blank=True, upload_to=destination_of_image)
    author = ForeignKey(User, on_delete=models.CASCADE, related_name='recipe')
    categories = ManyToManyField("Category", related_name='recipes')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'Рецепт: {self.name}.'


def destination_of_preview(instance: "Category", filename: str) -> str:
    return "".join(f"recipes/category_{instance.pk}/image/{filename}")


class Category(models.Model):
    name = CharField(null=False, max_length=30)
    description = TextField(max_length=700, null=False, blank=True)
    image = ImageField(null=True, blank=True, upload_to=destination_of_preview)

    def __str__(self):
        return f'Категория: {self.name}.'
