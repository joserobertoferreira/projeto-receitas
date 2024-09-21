import math

from django.core.paginator import Paginator


def set_pagination_range(page_range, view_pages, current_page):
    middle_range = math.ceil(view_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    offset_range = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += offset_range

    if stop_range >= total_pages:
        start_range -= abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'view_pages': view_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'has_previous': current_page > middle_range,
        'has_next': stop_range < total_pages,
    }


def pagination(request, queryset, per_page, view_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = set_pagination_range(
        paginator.page_range, view_pages, current_page
    )

    return page_obj, pagination_range
