from django.shortcuts import render,get_object_or_404
from . models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# Create your views here.

def home(request, c_slug=None):
    c_page = None  # Initialize c_page
    prod = None  # Initialize prod

    if c_slug is not None:  # Check if c_slug is provided
        c_page = get_object_or_404(categ, slug=c_slug)  # Get category by slug
        print(c_page)
        prod = products.objects.filter(category=c_page, available=True).order_by('name')  # Filter products
        print(prod)
    else:
        prod = products.objects.filter(available=True).order_by('name')  # Filter all available products
    
    paginator = Paginator(prod, 4)  # Show 3 products per page
    page = request.GET.get('page', 1)  # Get page number from the URL

    try:
        products_paginated = paginator.page(page)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)
    except InvalidPage:
        products_paginated = paginator.page(1)

    cat = categ.objects.all()  # Get all categories
    return render(request, 'index.html', {'products': products_paginated, 'ct': cat})

    


def proddetail(request, c_slug, product_slug):
    try:
        prod=products.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'productdetails.html',{'pr':prod})


def searching(request):
    prod=None
    Query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))
    return render(request,'search.html',{'qr':query,'pr':prod})