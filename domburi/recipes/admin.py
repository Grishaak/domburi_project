from django.contrib import admin
from recipes.models import Recipe, Category


class RecipeInline(admin.TabularInline):
    model = Recipe.categories.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_author', 'description_short', 'cooking_steps', 'cooking_time_time')
    list_display_links = ('pk', 'name', 'get_author',)
    ordering = 'pk',
    search_fields = 'pk', 'name', 'cooking_steps', 'cooking_time'
    inlines = [RecipeInline, ]
    fieldsets = [
        ('General fields', {
            'fields': ('name', 'author', 'description')
        }),
        ('Optional fields', {
            'fields': ('cooking_steps', 'cooking_time', 'categories', 'image'),
            'classes': ('wide',),
            'description': 'An optional fields.'
        }),
    ]

    def cooking_time_time(self, obj):
        hour = obj.cooking_time // 60
        minutes = obj.cooking_time % 60
        if hour and minutes:
            return f"{hour} h, {minutes} min."
        elif hour:
            return f"{hour} h."
        return f"{minutes} min."

    def get_queryset(self, request):
        return Recipe.objects.select_related('author')

    def get_author(self, obj):
        return obj.author.username

    get_author.short_description = "Author"

    def description_short(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'image')
    ordering = 'pk',
    search_fields = 'pk', 'name', 'description_short'

    def description_short(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
