from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import UpdateView, ListView
from paypal.standard.forms import PayPalPaymentsForm
import stripe

from accounts.forms import UserProfileForm, UserForm
from carts.models import Cart, CartItem
from idealisticsolutions.settings import EMAIL_HOST_USER
from orders.models import Order, OrderItem
from shop.models import Product
from ticketing_system.models import Ticket


def _cart_id(request):
    """This function assigns the session to cart if it exists and if not it will create a session"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def _get_cart(request):
    """
    This function checks the user authentication and gets the cart by look up to user and if he is not authenticated it
    will get the cart by look up to his session
    """
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
    except:
        cart = None
    return cart


class CartItemListView(ListView):
    model = CartItem

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = _get_cart(self.request)
        context['cart_items'] = CartItem.objects.filter(cart=cart, active=True)
        context['total'], context['counter'] = 0, 0
        for cart_item in context['cart_items']:
            context['total'] += cart_item.sub_total()
            context['counter'] += cart_item.quantity
        return context


class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem

    def get_object(self, queryset=None):
        return Product.objects.get(id=self.kwargs.get('product_id'))

    def post(self, request, product_id=None, *args, **kwargs):
        quantity = 1
        if request.POST.get('quantity'):
            quantity = request.POST.get('quantity')

        product = self.get_object()
        try:
            print('test')
            if request.user.is_authenticated:
                print('auth')
                cart = Cart.objects.get(user=request.user)
            else:
                print('not-auth')
                cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            print('test2')
            if request.user.is_authenticated:
                print('auth2')
                cart = Cart.objects.create(user=request.user)
            else:
                print('not-auth2')
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += int(quantity)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
            cart_item.save()
        return redirect('cart:cart-detail')


@login_required()
def add_to_cart(request, product_id):
    if request.method == 'GET':
        return redirect('shop:product-list')
    if request.method == 'POST':
        quantity = 1
        if request.POST.get('quantity'):
            quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += int(quantity)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
            cart_item.save()
        return redirect('cart:cart-detail')


def _get_cart_item(request, product_id, cart):
    """This function takes request, product_id, and cart and gets the cart_item"""
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    return cart_item


def _cart_items_total(cart):
    """This function takes cart and looks up by it and count items total and count then return them"""
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    total, count = 0, 0
    for cart_item in cart_items:
        total += cart_item.sub_total()
        count += 1
    return total, count


def cart_quantity_decrease_ajax(request):
    """This function decreases cart item quantity"""
    cart = _get_cart(request)
    cart_item = _get_cart_item(request, request.POST['id'], cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    total, count = _cart_items_total(cart)
    data = {
        'quantity': cart_item.quantity,
        'sub_total': cart_item.sub_total(),
        'total': total,
        'cart_items_count': count,
    }
    return JsonResponse(data)


def cart_quantity_increase_ajax(request):
    """This function increases cart item quantity"""
    cart = _get_cart(request)
    cart_item = _get_cart_item(request, request.POST['id'], cart)
    cart_item.quantity += 1
    cart_item.save()
    total, count = _cart_items_total(cart)
    data = {
        'quantity': cart_item.quantity,
        'sub_total': cart_item.sub_total(),
        'total': total,
        'cart_items_count': count,
    }
    return JsonResponse(data)


def cart_delete_ajax(request):
    """This function deletes cart item from cart"""
    cart = _get_cart(request)
    cart_item = _get_cart_item(request, request.POST['id'], cart)
    cart_item.delete()
    total, count = _cart_items_total(cart)
    data = {
        'total': total,
        'cart_items_count': count,
    }
    return JsonResponse(data)


@login_required
def checkout(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    user_profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=request.user.userprofile)
    return render(request, 'carts/checkout.html', {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    })


def payment(request):
    cart = _get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    total, count = _cart_items_total(cart)

    # Paypal settings
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': int(total),
        'item_name': 'Item_Name_xyz',
        'invoice': 'Test Payment Invoice',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('home')),
        'cancel_return': 'http://{}{}'.format(host, reverse('cart:cart-payment')),
    }
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    # Stripe settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Idealistic Solutions - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            customer = stripe.Customer.create(email=email, source=token)
            stripe.Charge.create(amount=stripe_total, currency="usd", description=description, customer=customer.id)

            '''Creating the order'''
            try:
                print('order')
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingcity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    user=request.user,
                )
                order_details.save()
                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    oi.save()
                    '''Reduce stock when order is placed or saved'''
                    order_item.delete()
                    '''The terminal will print this message when the order is saved'''
                    print('The order has been created')
                try:
                    '''Calling the sendEmail function'''
                    send_mail(
                        'Registration Message',
                        'Thanks for join our site',
                        EMAIL_HOST_USER,
                        [email, EMAIL_HOST_USER],
                        fail_silently=False,
                    )
                    # Create New ticket
                    ticket_subject = 'New Order# '+ str(order_details.id)
                    ticket_content = '<b><p><strong>Order #</strong> <a href=' + '/orders/' + str(order_details.id) + '/' ' target=\"_blank\">'+str(order_details.id)+'</a></p> <p><strong>Order Status: </strong> Complete.</p></b>'
                    Ticket.objects.create(subject=ticket_subject,priority='H',status='O',content=ticket_content,customer_id=str(order_details.user.id),department_id=1 )
                    print('Yesyesyesyes')

                    send_email(order_details.id)
                    print('The order email has been sent to the customer.')


                except IOError as e:
                    return e
                return redirect('orders:thanks', order_details.id)
            except ObjectDoesNotExist:
                pass
        except stripe.error.CardError as e:
            return False, e
    return render(request, 'carts/payment.html', {
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description,
        'paypal_form': paypal_form,
    })


# Send mail
def send_email(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
    try:
        '''Sending the order'''
        subject = "Idealistc Solutions - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.emailAddress)]
        from_email = "orders@perfectcushionstore.com"
        order_information = {
            'transaction': transaction,
            'order_items':	order_items
        }
        message = get_template('carts/email/email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
