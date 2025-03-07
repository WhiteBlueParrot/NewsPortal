from django import template
import re

register = template.Library()

PROFANITY = ['редиска', 'бяка', 'глупец']


@register.filter()
def censor(text):
    if not isinstance(text, str):
        return text

    def replace(match):
        word = match.group(0)
        return word[0] + '*' * (len(word) - 1)

    pattern = r'\b(' + '|'.join(re.escape(word) for word in PROFANITY) + r')\b'
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)
