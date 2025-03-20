from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(FilterView):
    model = Post
    template_name = 'posts_search.html'
    filterset_class = PostFilter  # Подключаем фильтр
    context_object_name = 'posts'
    paginate_by = 5
    ordering = '-created_at'


# Создание новости (автоматически проставляем post_type = 'NW')
class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS  # Устанавливаем "новость"
        return super().form_valid(form)


# Создание статьи (автоматически проставляем post_type = 'AR')
class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE  # Устанавливаем "статья"
        return super().form_valid(form)


# Редактирование поста (post_type уже задан, менять не надо)
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'


# Удаление поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')  # Перенаправление после удаления
