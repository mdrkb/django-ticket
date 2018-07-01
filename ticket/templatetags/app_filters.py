from django import template
from bs4 import BeautifulSoup
import bleach

register = template.Library()


@register.filter(name='reset_html_styles')
def reset_html_styles(value):
    soup = BeautifulSoup(value, 'html5lib')
    for div in soup.find_all('div', {'class': 'gmail_quote'}):
        div.decompose()

    for x in soup.find_all('p', {'text': ''}):
        x.extract()

    return bleach.clean(text=str(soup), tags=['div', 'br', 'p', 'a'])
