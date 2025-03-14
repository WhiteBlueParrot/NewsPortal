from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post, Author, User
from django.forms import DateInput


class PostFilter(FilterSet):
    author_username = CharFilter(
        field_name="author__user__username", lookup_expr="icontains", label="Author's Username"
    )
    created_at = DateFilter(
        field_name="created_at",
        lookup_expr="gt",  # Фильтрация по дате позже указанной
        widget=DateInput(attrs={'type': 'date'}),  # Добавляем <input type="date">
        label="Дата (позже)"
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'created_at': ['gt'],
        }