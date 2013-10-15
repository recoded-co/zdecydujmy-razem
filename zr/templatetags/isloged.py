__author__ = 'marcinra'

from django.template import Library

register = Library()


@register.filter(name='isloged')
def isloged(arg):
    print '--------'
    print arg
    if arg=='AnonymousUser':
        return True
    else:
        return False