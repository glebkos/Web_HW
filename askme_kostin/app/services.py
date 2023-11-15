from django.core.paginator import Paginator


def paginate(request, objects, per_page=10):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        if paginator.num_pages < int(page):
            page = paginator.num_pages
        elif 1 > int(page):
            page = 1
    except:
        page = 1
    return paginator.page(page)
