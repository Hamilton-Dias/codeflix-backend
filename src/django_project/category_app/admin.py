from django.contrib import admin

from src.django_project.category_app.models import Category
from src.django_project.genre_app.models import Genre
from src.django_project.cast_member_app.models import CastMember

class CategoryAdmin(admin.ModelAdmin):
  pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, CategoryAdmin)
admin.site.register(CastMember, CategoryAdmin)
