'''
Use the Form class to add products into the cart
quantity - allows selection of upto 20 items and convert input into integer
override - indicates wheather to  add the quantity to the existing quantity 
in cart for this product

'''

from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)