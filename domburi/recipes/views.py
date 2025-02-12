from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest, request
from django.shortcuts import render, redirect
import os

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView

from recipes.forms import UserForm, RecipeForm
from recipes.models import Recipe, Category


class RecipeGeneralView(ListView):
    queryset = Recipe.objects.select_related('author') \
                   .prefetch_related('categories') \
                   .order_by('?')[:4]
    context_object_name = 'recipes'
    template_name = 'recipes/recipe_list.html'


class RecipeListView(ListView):
    queryset = Recipe.objects.select_related('author') \
        .prefetch_related('categories') \
        .all()
    context_object_name = 'recipes'
    template_name = 'recipes/recipe_list.html'


class RecipeDetailView(DetailView):
    permission_denied_message = "Sorry but you can't see this recipe."
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe_detail.html'


class RecipeCreateView(PermissionRequiredMixin, FormView):
    permission_required = ["recipes.add_recipe", "recipes.change_recipe", "recipes.view_recipe", ]
    permission_denied_message = "Sorry but you need don't have enough permissions to create your own recipe"
    form_class = RecipeForm
    template_name = 'recipes/recipe_create.html'
    request = HttpRequest()
    success_url = reverse_lazy('recipes:recipes_list')

    def user_validate(self):
        if self.request.user.pk is not None:
            return True
        return False

    # def get_success_url(self):
    #     return reverse(
    #         "recipes:recipe_detail"
    #     )

    def form_valid(self, form):
        data = form.cleaned_data
        cats = form.cleaned_data.pop('categories')
        data['author_id'] = self.request.user.pk
        instance = Recipe.objects.create(**data)
        instance.categories.set(cats)

        return super().form_valid(form)


class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = 'name', 'description', 'cooking_time', 'cooking_steps', 'categories', 'image'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            "recipes:recipe_detail",
            kwargs={'pk': self.object.pk}
        )

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     cats = form.cleaned_data.pop('categories')
    #     object_mod = self.object
    #     object_mod.categories.set(cats)
    #
    #     object_mod.save()
    #
    #     return super().form_valid(form)


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


class CategoryListView(ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'recipes/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'recipes/category_detail.html'


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
#     return render(request, template_name='recipes/recipe_create.html', context=context)
