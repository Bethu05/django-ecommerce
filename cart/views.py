from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm

'''
    Adding Products to the cart and updating quantities for existing products
    Allows only POST requests
    View receives Product ID as parameter
'''
@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    # Validate the form
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quality=cd['quantity'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

# Need to display the cart
def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    return render(request,'cart/detail.html',{'cart':cart,'categories':categories})