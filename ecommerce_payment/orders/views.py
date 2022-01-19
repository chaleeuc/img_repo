from django.shortcuts import render
from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem

def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':   
        order_key = request.POST.get('order_key')   # sent by ajax, as an unique identifier for the order being placed by the user
        user_id = request.user.id   
        carttotal = cart.get_total_price()

        # check for order, make sure no same order appear in the database
        if Order.objects.filter(order_key=order_key).exists():
            pass

        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1', address2='add2', total_paid=carttotal, order_key=order_key)
            # get the session data, and loop through it to create ordered item list
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'something'})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

# check billing status of user order, check true
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders