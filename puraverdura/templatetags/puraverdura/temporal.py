from django import template
from juntagrico.util import temporal

register = template.Library()


@register.simple_tag
def start_of_business_year():
    return temporal.start_of_business_year()
