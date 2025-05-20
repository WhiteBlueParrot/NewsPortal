from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(Post)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('post_type', 'title', 'text')
