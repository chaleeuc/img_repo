import json

from account.models import Address
from cart.cart import Cart
from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from .models import DeliveryOptions
from orders.models import Order, OrderItem
from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient

@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)

    context = {'deliveryoptions': deliveryoptions,}
    return render(request, 'checkout/delivery_choices.html', context)

@login_required
def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        delivery_option = int(request.POST.get('deliveryoption'))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        # get a new session for the user
        # i.e., user might leave before purchase, and come back later
        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': delivery_type.id,
            }
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        response = JsonResponse({'total': updated_total_price, 'delivery_price': delivery_type.delivery_price})
        return response

@login_required
def delivery_address(request):
    session = request.session
    # simple checks
    if 'purchase' not in session:
        messages.success(request, 'Select a delivery option to purchase')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    # get addresses associated with the user
    addresses = Address.objects.filter(customer=request.user).order_by('-default')  

    if 'address' not in request.session:
        session['address'] = {'address_id': str(addresses[0].id)}
    
    else:
        session['address']['address_id'] = str(addresses[0].id)
        session.modified = True

    context = {'addresses': addresses,}
    return render(request, 'checkout/delivery_address.html', context)

# PayPal Integration
# sandbox account:  sb-1a1hi12017074@personal.example.com
# sandbox password: 1U%bY22:
@login_required
def payment_selection(request):
    # simple check 
    ''' got rid of delivery options, no need to check for session data 
    session = request.session
    if 'address' not in session:
        messages.success(request, 'Select a delivery address to purchase')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    '''
    context = {}
    return render(request, 'checkout/payment_selection.html', context)

@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body['orderID']
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)   # paypal function, send data to paypal api
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value
    cart = Cart(request)
    order = Order.objects.create(
        user_id = user_id,
        full_name = response.result.purchase_units[0].shipping.name.full_name,
        email = response.result.payer.email_address,
        address1 = response.result.purchase_units[0].shipping.address.address_line_1,
#        address2 = response.result.purchase_units[0].shipping.address.address_line_2,
        postal_code = response.result.purchase_units[0].shipping.address.postal_code,
        country_code = response.result.purchase_units[0].shipping.address.country_code,
        total_paid = response.result.purchase_units[0].amount.value,
        order_key = response.result.id,
        payment_option = 'paypal',
        billing_status = True,
    )
    order_id = order.pk

    for item in cart:
        OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
    
    return JsonResponse('Payment completed!', safe=False)

@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()

    context = {}
    return render(request, 'checkout/payment_successful.html', {})
