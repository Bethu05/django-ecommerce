from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
        # initialize the cart
    def __init__(self,request):
        # Store current session
        self.session = request.session
        # Try get the current session 
        cart = self.session.get(settings.CART_SESSION_ID)
        # save an empty cart in the session if there is no cart
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    # Add an item to the cart or update its quantity
    def add(self,product,quantity=1,override_quality=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quality':0,'price':str(product.price)}
        if override_quality:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] +=quantity
        self.save()
        
    # mark the session as 'modified' to make sure it gets saved
    def save(self):
        self.session.modified = True
    
    # Remove a product from the cart
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    # You will need to iterate through the items in cart and 
    # access the related Product instances in the databases
    # Thus the need to define the __iter__() method in class 
    def __iter__(self):
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            
            
            
    # Also need a way to return the length of items in the Cart
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    # Returns the grand total price of items in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    # Also a mathod to clear trhe cart session & remove cart from session
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()