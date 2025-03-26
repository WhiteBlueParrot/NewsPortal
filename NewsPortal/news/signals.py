from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.conf import settings

from .models import PostCategory

print("✅ Signals module loaded!")


def send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails += [subscriber.email for subscriber in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers_emails)

    print(f"New post: {instance.title}")
    print(f"Subscribers: {subscribers_emails}")

    if subscribers_emails:
        send_notification(instance.preview(), instance.pk, instance.title, subscribers_emails)
    else:
        print("No subscribers found. Email not sent.")
