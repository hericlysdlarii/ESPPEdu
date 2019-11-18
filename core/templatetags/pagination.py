# -*- coding: utf-8 -*-

from django.template import Library


register = Library()


@register.inclusion_tag('pagination.html')
def pagination(request, paginator, page_obj, page_numbers, show_first, show_last):
    context = {}
    context['paginator'] = paginator
    context['request'] = request
    context['page_obj'] = page_obj
    context['page_numbers'] = page_numbers
    context['show_first'] = show_first
    context['show_last'] = show_last

    """
        var getvars
        copio as variaveis do GET

    """
    getvars = request.GET.copy()

    if 'page' in getvars:
        del getvars['page']
    if len(getvars) > 0:
        context['getvars'] = '&{0}'.format(getvars.urlencode())
    else:
        context['getvars'] = ''

    return context
