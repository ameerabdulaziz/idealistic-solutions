from .models import CartItem
from .views import _get_cart


def cart_items_info(request):
    cart = _get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    item_count, total = 0, 0
    for cart_item in cart_items:
        item_count += cart_item.quantity
        total += cart_item.sub_total()
    context = {
        'cart_items': cart_items,
        'item_count': item_count,
        'total': total,
    }
    return context
