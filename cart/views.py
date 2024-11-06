from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from shop . models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def cart_details(request, tot=0, count=0):
    c_items = []
    try:
        ct = cartlist.objects.get(cart_id=c_id(request))  # Retrieve cart based on session
        c_items = items.objects.filter(cart=ct, active=True)  # Get active items in cart
        for i in c_items:
            tot += (i.prodt.price * i.quantity)  # Calculate total price correctly
            count += i.quantity  # Count total items
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {'ci': c_items, 't': tot, 'cn': count})  # Render cart details

         
def c_id(request):
    ct_id = request.session.session_key  # Get the current session key from the request
    if not ct_id:  # Check if the session key does not exist
        ct_id = request.session.create()  # Create a new session if it doesn't exist
    return ct_id  # Return the session key
    

def add_cart(request, product_id):
    prod = products.objects.get(id=product_id)  # Retrieve the product based on the provided product ID from the database

    try:
        ct = cartlist.objects.get(cart_id=c_id(request))  # Attempt to retrieve the existing cart using the cart ID from the session
    except cartlist.DoesNotExist:
        ct = cartlist.objects.create(cart_id=c_id(request))  # If the cart does not exist, create a new cart with the session cart ID
        ct.save()  # Save the new cart instance to the database (optional, as create() saves it automatically)

    try:
        c_item = items.objects.get(prodt=prod, cart=ct)  # Attempt to retrieve an existing item in the cart that matches the product
        if c_item.quantity < c_item.prodt.stock:  # Check if the current quantity of the item in the cart is less than the available stock
            c_item.quantity += 1  # If there is stock available, increment the quantity by 1
        c_item.save()  # Save the updated item back to the database
    except items.DoesNotExist:
        c_item = items.objects.create(prodt=prod, quantity=1, cart=ct)  # If the item is not found in the cart, create a new item entry
        c_item.save()  # Save the new item to the database (optional, as create() saves it automatically)

    return redirect('cartdetails')  # Redirect the user to the cart details page after adding the item

def min_cart(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    c_items=items.objects.get(prodt=prod,cart=ct)
    if c_items.quantity>1:
        c_items.quantity-=1
        c_items.save()
    else:
        c_items.delete()
    return redirect("cartdetails")
    

def cart_delete(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    c_items=items.objects.get(prodt=prod,cart=ct)
    c_items.delete()
    return redirect("cartdetails")


@login_required
def checkout_view(request):
    form = CheckoutForm()
    cart_items = items.objects.filter(cart__cart_id=c_id(request), active=True)
    total = sum(item.prodt.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                total_amount=total,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.prodt,
                    quantity=item.quantity
                )
                item.delete()  # Remove items from the cart after they’re added to the order

            return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total': total})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


