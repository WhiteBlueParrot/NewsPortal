from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.core.cache import cache
from django.utils.translation import gettext as _


class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


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
        today_posts = Post.objects.filter(author=self.request.user.author, created_at__date=now().date()).count()

        if today_posts >= 3:
            messages.error(self.request, _("Вы не можете публиковать более 3-х новостей в сутки!"))
            # Возвращаем пользователя на предыдущую страницу
            return redirect(self.request.META.get('HTTP_REFERER'))

        form.instance.post_type = Post.NEWS
        form.instance.author = self.request.user.author
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


class CategoryListView(PostsList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _("Вы успешно подписались на категорию")
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


class Index(View):
    def get(self, request):
        string = _('Hello world!')
        # return HttpResponse(string)
        context = {
            'string': string,
        }
        return HttpResponse(render(request, 'index.html', context))
