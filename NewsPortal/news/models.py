from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = sum(post.rating * 3 for post in self.posts.all())
        self.rating += sum(comment.rating for comment in self.user.comment_set.all())
        for post in self.posts.all():
            for comment in post.comment_set.all():
                self.rating += comment.rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'статья'),
        (NEWS, 'новость'),
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    categories = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.text}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
