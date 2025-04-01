from django.urls import path
from .views import (
    PostsList, PostDetail, PostsSearch, NewsCreateView,
    ArticleCreateView, PostUpdateView, PostDeleteView,
    CategoryListView, subscribe

)
from django.views.decorators.cache import cache_page

app_name = 'news'

urlpatterns = [
    path('', PostsList.as_view(), name='news_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),  # Ensure this is named 'post_detail'
    path('search/', PostsSearch.as_view(), name='post_search'),

    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),

    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),

    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
