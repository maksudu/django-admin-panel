from django.apps import apps
from django.db.models import Q
from django.http import JsonResponse

def get_queryset(request, app, model):
    model = apps.get_model(app, model)
    limit = int(request.GET.get('length'))
    start = int(request.GET.get('start'))
    draw = int(request.GET.get('draw'))
    fields = request.GET.get('fields')
    search = str(request.GET.get('search[value]'))

    order_field_id = int(request.GET.get('order[0][column]'))
    order_dir = request.GET.get('order[0][dir]')
    fields = [str(i) for i in fields.strip('[]').split(',')]

    offset = start + limit

    qs = model.objects.all().order_by(fields[order_field_id])[start:offset]
    if order_dir == 'desc':
        qs = model.objects.all().order_by('-'+fields[order_field_id])[start:offset]

    object_count = model.objects.all().count()

    '''if search is active'''

    if search != '':
        q = Q()
        # all_fields = [str(f.name) for f in model._meta.fields]
        all_fields = [str(f) for f in fields]
        for field in all_fields:
            q |= Q(**{'{0}__istartswith'.format(field): search})
        qs = model.objects.filter(q)[start:offset]
        object_count = model.objects.filter(q).count()
        if order_dir == 'desc':
            qs = model.objects.filter(q).order_by('-'+fields[order_field_id])[start:offset]

    data = list()
    for item in qs:
        data.append([render_column(item, column) for column in fields])

    response = {
        "draw": draw,
        "recordsTotal": object_count,
        "recordsFiltered": object_count,
        'data': data
    }
    return JsonResponse(response,safe=False)


def render_column(row, column):
    """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
    """
    # try to find rightmost object
    obj = row
    parts = column.split('.')
    for part in parts[:-1]:
        if obj is None:
            break
        obj = getattr(obj, part)

    # try using get_OBJECT_display for choice fields
    if hasattr(obj, 'get_%s_display' % parts[-1]):
        value = getattr(obj, 'get_%s_display' % parts[-1])()
    else:
        value = getattr(obj, parts[-1], None)

    if value is None:
        value = None

    if value and hasattr(obj, 'get_absolute_url'):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
    return value

