from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
''' for email validation only
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
'''

# dashboard function
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from orders.views import user_orders
from orders.models import Order

@login_required
def dashboard(request):
    orders = user_orders(request)
    context = {'section': 'profile', 'orders': orders}
    return render(request, 'account/dashboard/dashboard.html', context)

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    context = {'user_form': user_form}
    return render(request, 'account/dashboard/edit_details.html', context)

@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False  # user won't be able to login while this is set
    user.save()
    logout(request)
    return redirect('/')    # send them to home

def account_register(request):
    if request.user.is_authenticated:        
        return redirect('/')

    # check user provided input
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            # save user data
            user = registerForm.save(commit = False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()

            '''
            # email setup if want non validated email to be registered to our page

            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site_domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # send email notification
            user.email_user(subject=subject, message=message)
            '''          
#            return HttpResponse('registered successfully')
            return redirect('account:login')

    else:
        registerForm = RegistrationForm()
        context = {'form': registerForm}

    return render(request, 'account/registration/register.html', context)

# ADDRESS SECTION
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)   # get the user his corresponding address

    context = {"address": addresses,}
    return render(request, 'account/dashboard/address.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('account:address'))            
    else:
        address_form = UserAddressForm()

    context = { 'form': address_form, }
    return render(request, 'account/dashboard/edit_address.html', context)

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse('account:address'))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    context = { 'form': address_form, }
    return render(request, "account/dashboard/edit_address.html", context)

@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()   # get the user selected address
    return redirect('account:address')

@login_required
def user_orders(request):
    user_id = request.user.id 
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    context = {
        'orders': orders,
    }
    return render(request, 'account/dashboard/user_orders.html', context)

@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    if 'delivery_address' in request.META.get('HTTP_REFERER'):
        return redirect('checkout:delivery_address')

    return redirect('account:addresses')

''' for email verification only 
def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')

    else:
        return render(request, 'account/registration/account_activation_failed.html')
'''