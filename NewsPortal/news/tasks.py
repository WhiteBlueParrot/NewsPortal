from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from django.utils.timezone import now, timedelta


@shared_task
def send_news_notification(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()
    subscribers_emails = set()

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails.update(subscriber.email for subscriber in subscribers)

    html_content = render_to_string(
        'post_created_email.html',
        {'post': post, 'link': f"{settings.SITE_URL}/news/{post.id}"}
    )

    msg = EmailMultiAlternatives(
        subject=post.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers_emails),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_weekly_newsletter():
    last_week = now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        posts = Post.objects.filter(categories=category, created_at__gte=last_week)
        if posts.exists():
            subscribers_emails = [subscriber.email for subscriber in subscribers]
            html_content = render_to_string(
                'weekly_newsletter.html',
                {'category': category, 'posts': posts}
            )

            msg = EmailMultiAlternatives(
                subject=f"Еженедельная рассылка: {category.name}",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscribers_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
