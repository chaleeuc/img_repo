from shop.models import Product
from decimal import Decimal
from django.conf import settings
from checkout.models import DeliveryOptions
class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')  
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}

        self.cart = cart

    # add item to session data
    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id] = { 'price': str(product.regular_price), 'qty': qty} 

        self.save()

    # delete item from session data
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.save()

    # update item in session data
    def update(self, product, qty):
        product_id = str(product)
        qty = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        
        self.save()

    # iterate over data in the cart for cart summary
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def __len__(self):
        # cart data + count quantity of items
        return sum(item['qty'] for item in self.cart.values())

    # total price of products in cart
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    # get delivery cost
    def get_delivery_price(self):
        newprice = 0.00
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price

        return newprice

    # price including flat shipping
    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        # check for delivery information in session data
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    # clear session data, for ordering purpose
    def clear(self):
        del self.session['skey']
        del self.session['address']
        del self.session['purchase']
        self.save()

    # save session data, if there are any changes 
    def save(self):
        self.session.modified = True


    # for chekcout class
    def cart_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        total = subtotal + Decimal(deliveryprice)

        return total

"""
Code in this file has been inspried/reworked from other known works. Plese ensure that
the License below is included in any of your work that is directly copied from
this source file.


MIT License


Copyright (c) 2019 Packt


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""