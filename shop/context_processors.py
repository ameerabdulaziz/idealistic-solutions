from .models import Category


def shop_links(request):
    links = Category.objects.all()
    return dict(shop_links=links)
