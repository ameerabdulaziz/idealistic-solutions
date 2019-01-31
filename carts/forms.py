from django import forms

from carts.models import Cart, CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = (Cart, CartItem)
        fields = '__all__'
