from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, CharField, TextField, ImageField, IntegerField, ManyToManyField


class Recipe(models.Model):
    name = CharField(max_length=40, null=False)
    description = TextField(max_length=2000, null=False, blank=True)
    cooking_steps = IntegerField(default=1)
    cooking_time = IntegerField(default=5)
    image = ImageField(null=True, blank=True)
    author = ForeignKey(User, on_delete=models.CASCADE, related_name='recipe')
    categories = ManyToManyField("Category", related_name='recipes')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'Рецепт: {self.name}.'


class Category(models.Model):
    name = CharField(null=False, max_length=30)
    description = TextField(max_length=200, null=False, blank=True)

    def __str__(self):
        return f'Категория: {self.name}.'