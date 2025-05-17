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


# @register.filter()
# def hide_forbidden(value):
#     words = value.split()
#     result = []
#     for word in words:
#         if word in forbidden_words:
#             result.append(word[0] + ((len(word) - 2) * '*') + word[-1])
#         else:
#             result.append(word)
#     return ''.join(result)


