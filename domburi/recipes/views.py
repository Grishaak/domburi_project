from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest, request
from django.shortcuts import render, redirect
import os

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView

from recipes.forms import UserForm, RecipeForm
from recipes.models import Recipe


class RecipeGeneralView(ListView):
    queryset = Recipe.objects.select_related('author') \
                   .prefetch_related('categories') \
                   .order_by('?')[:5]
    context_object_name = 'recipes'
    template_name = 'recipes/recipes.html'


class RecipeListView(ListView):
    queryset = Recipe.objects.select_related('author') \
        .prefetch_related('categories') \
        .all()
    context_object_name = 'recipes'
    template_name = 'recipes/recipes.html'
    paginate_by = 6


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/detailed_recipe.html'


class RecipeCreateView(FormView):
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'
    request = HttpRequest()
    success_url = reverse_lazy('recipes:recipes_list')

    def user_validate(self):
        if self.request.user.pk is not None:
            return True
        return False

    def form_valid(self, form):
        data = form.cleaned_data
        cats = form.cleaned_data.pop('categories')
        data['author_id'] = self.request.user.pk
        instance = Recipe.objects.create(**data)
        instance.categories.set(cats)

        return super().form_valid(form)


def upload_file(request):
    if request.method == 'POST' and request.FILES.get():
        print('In post')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print(filename, "saved")
        context = {
            'data': 'File is uploaded just fine.'
        }
    else:
        print('No content and method is not POST')
        context = {}
    return render(request, template_name='recipes/upload_file.html', context=context)


def user_form(request):
    context = {
        'form': UserForm(),
    }
    return render(request, template_name='recipes/user_form.html', context=context)

# def user_validate(request: HttpRequest):
#     if request.user.pk is not None:
#         return True
#     return False


# def create_recipe(request: HttpRequest):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES)
#         if form.is_valid() and user_validate(request):
#             data = form.cleaned_data
#             cats = form.cleaned_data.pop('categories')
#             data['author_id'] = request.user.pk
#             instance = Recipe.objects.create(**data)
#             instance.categories.set(cats)
#             url_revers = reverse('recipes:recipes_list')
#             return redirect(url_revers)
#         # else:
#         #     url_revers = reverse('recipes:create_recipe')
#         #     return redirect(url_revers)
#     else:
#         form = RecipeForm()
#     context = {
#         'form': form
#     }
#     return render(request, template_name='recipes/create_recipe.html', context=context)
