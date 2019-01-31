from django.shortcuts import get_object_or_404, render
from django.views import generic

from shop.models import Product, Category


class ProductList(generic.ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get(self, request, slug=None, *args, **kwargs):
        if slug is None:
            self.queryset = Product.objects.all()
        else:
            category = get_object_or_404(Category, slug=slug)
            self.queryset = Product.objects.filter(category=category, available=True)
        return render(request, self.template_name, {'products': self.queryset})


class ProductDetail(generic.DetailView):
    model = Product
