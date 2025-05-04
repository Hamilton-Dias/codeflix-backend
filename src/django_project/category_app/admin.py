from django.contrib import admin

from src.django_project.category_app.models import Category
from src.django_project.genre_app.models import Genre

class CategoryAdmin(admin.ModelAdmin):
  pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, CategoryAdmin)
