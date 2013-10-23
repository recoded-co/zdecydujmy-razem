__author__ = 'marcinra'

from django.template import Library

register = Library()


@register.filter(name='isloged')
def isloged(arg):
    if str(arg) == 'AnonymousUser':
        return False
    else:
        return True

@register.filter(name='dirparser')
def dirparser(arg):
    if str(arg) == 'L':
        return 'left'
    elif arg== 'R':
        return 'right'
    else:
        return 'left'