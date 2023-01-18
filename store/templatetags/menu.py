from django import template

from store.models import Instituition

register = template.Library()

@register.inclusion_tag('core/menu.html')
def menu():
    instituitions = Instituition.objects.all()

    return {'instituitions': instituitions}