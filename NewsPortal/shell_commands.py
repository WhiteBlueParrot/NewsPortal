from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создание пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

# Создание авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создание категорий
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Наука')

# Создание постов
post1 = Post.objects.create(author=author1, post_type='A', title='Первая статья', text='Текст первой статьи')
post2 = Post.objects.create(author=author2, post_type='A', title='Вторая статья', text='Текст второй статьи')
news1 = Post.objects.create(author=author1, post_type='N', title='Первая новость', text='Текст первой новости')

# Присвоение категорий
post1.categories.add(category1, category2)
post2.categories.add(category3)
news1.categories.add(category4)

# Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user2, text='Комментарий к первой статье')
comment2 = Comment.objects.create(post=post2, user=user1, text='Комментарий ко второй статье')
comment3 = Comment.objects.create(post=news1, user=user2, text='Комментарий к первой новости')
comment4 = Comment.objects.create(post=post1, user=user1, text='Ещё один комментарий к первой статье')

# Лайки и дизлайки
post1.like()
post1.like()
post2.like()
post2.dislike()
news1.like()
comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# Лучший автор
best_author = Author.objects.order_by('-rating').first()
best_author.user.username
best_author.rating

# Лучший пост
best_post = Post.objects.order_by('-rating').first()
best_post.created_at
best_post.author.user.username
best_post.rating
best_post.title
best_post.preview()

# Комментарии лучшего поста
comments = Comment.objects.filter(post=best_post)
comments.all().values('created_at', 'user', 'rating', 'text')
