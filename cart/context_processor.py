from . models import *
from . views import *

def count(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            ct = cartlist.objects.get(cart_id=c_id(request))  # Use get() for a single cart
            cti = items.objects.filter(cart=ct)  # Correctly filter items by cart
            for c in cti:
                item_count += c.quantity
        except cartlist.DoesNotExist:
            item_count = 0  # If the cart doesn't exist, item_count remains 0

    return {'itc': item_count}  # Correctly return a dictionary