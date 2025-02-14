import logging
import operator
from functools import reduce
from pprint import pprint

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from recipes.forms import UserForm, RecipeForm
from recipes.models import Category

from rest_framework.viewsets import ModelViewSet

from recipes.permissions import IsAdminOrAuthorOrReadOnly
from recipes.serializers import RecipeApiSerializer
from recipes.models import Recipe

logger = logging.getLogger(__name__)


class RecipesApiRetrieveView(ListCreateAPIView):
    """
    Все сущности модели рецептов.
    Показывает все аттрибуты модели рецептов через список.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeApiSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_fields = [
        'name', 'description', 'cooking_steps', 'cooking_time',
    ]
    filter_backends = [
        SearchFilter, DjangoFilterBackend, OrderingFilter
    ]
    search_fields = ['name', 'description']


class RecipesApiUpdateView(RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeApiSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)


class RecipesApiDestroyView(RetrieveDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeApiSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)


class RecipeGeneralView(ListView):
    model = Recipe
    queryset = Recipe.objects.select_related('author') \
                   .prefetch_related('categories') \
                   .all().order_by('?')[:4]
    context_object_name = 'recipes'
    template_name = 'recipes/recipe_index.html'


class RecipeListView(ListView):
    queryset = Recipe.objects.select_related('author') \
        .prefetch_related('categories') \
        .all()
    context_object_name = 'recipes'
    template_name = 'recipes/recipe_list.html'
    paginate_by = 6
    logger.debug('An entity "RecipeListView" has been executed DEBUG mode.')
    logger.info('An entity "RecipeListView" has been executed INFO mode.')

    def get_queryset(self):
        queries = self.request.GET.get('q')
        if queries:
            queries = self.request.GET.get('q').split()
            qset1 = reduce(operator.__or__,
                           [Q(name__iregex=rf"{query}") | Q(description__iregex=fr"{query}") | Q(
                               categories__name__iregex=fr"{query}") for query in queries])
            object_list = Recipe.objects.select_related('author') \
                .prefetch_related('categories') \
                .filter(qset1).distinct()
            if object_list:
                return object_list
            else:
                object_list = Recipe.objects.select_related('author') \
                    .prefetch_related('categories') \
                    .all()
        else:
            object_list = Recipe.objects.select_related('author') \
                .prefetch_related('categories') \
                .all()
        return object_list


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

    paginate_by = 6


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'recipes/category_detail.html'

    def get_context_data(self, **kwargs):
        key = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)

        context['recipes'] = Recipe.objects.filter(categories__pk=key).select_related('author').prefetch_related(
            'categories')
        return context


def user_form(request):
    context = {
        'form': UserForm(),
    }
    return render(request, template_name='recipes/user_form.html', context=context)
