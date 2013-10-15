__author__ = 'marcinra'

from django.template import Library

register = Library()


@register.filter(name='isloge')
def isloged(arg):
    print '--------'
    print arg
    if arg=='AnonymousUser':
        return False
    else:
        return True