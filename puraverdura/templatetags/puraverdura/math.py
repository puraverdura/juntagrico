import math
from django import template
register = template.Library()

@register.filter
def quartile(percentage):
    return min(100, int(25 * math.floor(float(percentage) / 25)))