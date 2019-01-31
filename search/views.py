from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from shop.models import Product


def search_result(request):
    print('ok')
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query))
        print(products)
    return render(request, 'search/search_result.html', {'query': query, 'products': products})


class SearchResultView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            query = request.GET.get('q')
            products = Product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query))
            return render(request, 'search/search_result.html', {'query': query, 'products': products})
