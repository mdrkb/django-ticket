from django import template
from bs4 import BeautifulSoup
import bleach
import logging

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name='reset_html_styles')
def reset_html_styles(value):
    try:
        soup = BeautifulSoup(value, 'html5lib')

        # soup.find('div', id='divRplyFwdMsg').decompose()

        for div in soup.find_all('div', {'class': 'gmail_quote'}):
            div.decompose()

        for x in soup.find_all('p', {'text': ''}):
            x.extract()

        return bleach.clean(text=str(soup),
                            tags=['div', 'br', 'p', 'a', 'b', 'strong', 'i', 'ul', 'li', 'ol', 'u', 'span', 'font',
                                  'meta', 'style', 'table', 'tbody', 'td', 'tr', 'th', 'img', 'center'])
    except Exception as ex:
        logger.error(ex)
        return value
