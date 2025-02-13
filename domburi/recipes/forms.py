from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import TextField
from django.forms import forms, CharField, EmailField, IntegerField, Textarea, FileField, MultipleChoiceField, \
    CheckboxSelectMultiple, ImageField, ModelForm, TextInput
from .models import Recipe
import django.forms.widgets as wgs
from recipes.models import Category


class UserForm(forms.Form):
    name = CharField(max_length=50, min_length=3, label='Name')
    email = EmailField(label='Email')
    firstname = CharField(max_length=50, min_length=1, label='Firstname')
    surname = CharField(max_length=50, min_length=1, label='Surname')


def validate_file(file: InMemoryUploadedFile):
    print(file.file, file.content_type)
    validated_img_types = ('image/jpeg', 'image/png', 'image/gif', 'image/jpg', 'image/webp')
    if file.content_type not in validated_img_types:
        raise ValidationError('File is not in right type. Should be jpeg, png, gif.')
    elif file.size > 1000000:
        raise ValidationError('File should be less than 1mb size.')


# class RecipeForm(forms.Form):
#     name = CharField(max_length=40, label='Name')
#     description = CharField(widget=Textarea, label='Description')
#     cooking_steps = IntegerField(min_value=1, max_value=10, label='Cooking Steps')
#     cooking_time = IntegerField(min_value=5, max_value=1440, label='Cooking Time')
#     image = ImageField(required=False, validators=[validate_file, ])
#     categories = MultipleChoiceField(choices=((i.pk, i.name) for i in Category.objects.all()),
#                                      widget=CheckboxSelectMultiple)


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'cooking_time', 'image', 'categories']

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Введите свое имя',
                }
            ),
            'description': Textarea(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Введите сюда ваше описание',
                }
            ),
            'cooking_steps': wgs.NumberInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'cooking_time': wgs.NumberInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'image': wgs.FileInput(
                attrs={
                    'class': 'form-input'
                }
            ),
        }
