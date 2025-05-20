from django.contrib import admin
from .models import Category, Post, Author
from modeltranslation.admin import TranslationAdmin  # импортируем модель админки


class PostAdmin(TranslationAdmin):
    model = Post


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
