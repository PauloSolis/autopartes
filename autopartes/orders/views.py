from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from productos.models import Product
from users.models import Address
from orders.models import ProductsOrder
from orders.models import Order
from orders.models import User
import json
import logging
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
from django.shortcuts import render, redirect
from .forms import Status


# Create your views here.


logger = logging.getLogger(__name__)

@login_required
def crear_orden(request):
    if request.method == 'POST':
        received_order = json.loads(request.body)
        logger.error(received_order)
        data = json.loads(received_order['data'][0])
        address = json.loads(received_order['data'][1])
        address = Address.objects.get(pk=address['address'][0])
        logger.error(address)
        user_buying = User.objects.get(pk=request.user.id)
        order = Order(total_price=data['total'][0], status="pendiente", address=address, user=user_buying)
        order.save()
        for product in received_order['products']:
            prod_decoded = json.loads(product)
            aux_product = Product.objects.get(pk=prod_decoded['prod_id'])
            print(aux_product.name)
            print(aux_product.in_stock)
            aux_product.in_stock -= int(prod_decoded['prod_quantity'])
            print(aux_product.in_stock)
            aux_product.save()
            prod_ord = ProductsOrder(
                order=order,
                product=aux_product,
                quantity=prod_decoded['prod_quantity'],
                price=prod_decoded['price_at_sale'])
            prod_ord.save()
    return render(request, '../templates/landing.html')


@login_required
@admin_required
def ver_ordenes(request, search=None):
    if request.user.is_administrator:
        if search:
            orders = search
        else:
            orders = Order.objects.all().order_by('-id')
        paginator = Paginator(orders, 20)
        customers = []
        for o in orders:
            customer = User.objects.get(pk=o.user_id)
            if customer not in customers:
                customers.append(customer)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if search:
            return page_obj, customers
        return render(request, '../templates/orders/ver_ordenes.html', {'orders': page_obj, 'customers': customers})

    else:
        orders_user = User.objects.get(pk=request.user.id)
        orders = Order.objects.filter(user=orders_user).order_by('-id')
        paginator = Paginator(orders, 20)

        addresses = []

        for o in orders:
            address = Address.objects.get(pk=o.address.id)
            if address not in addresses:
                addresses.append(address)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, '../templates/orders/ver_ordenes.html', {'orders': page_obj, 'addresses': addresses})


@login_required
def ver_desgloce(request, id):
    order_p = ProductsOrder.objects.filter(order_id=id)
    order = Order.objects.get(pk=id)
    address = Address.objects.get(pk=order.address.id)
    prod = []
    for o in order_p:
        aux = Product.objects.get(id=o.product_id)
        prod.append(aux)

    return render(request,
                  '../templates/orders/ver_desgloce.html',
                  {'order_products': order_p, 'products': prod, 'address': address, 'order': order})



@login_required
@admin_required
def change_status(request, id):
    order = Order.objects.get(id = id)
    form = Status(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('orders:ver_ordenes')
    context = {
        'form': form,
    }
    return render(request, '../templates/orders/change_status.html', context)

def search_order(request):
    query = request.GET.get('q', '')
    template = '../templates/orders/buscar_orden.html'
    if query:
        queryset = (Q(id__icontains=query)) | (Q(user__ruc__icontains=query))
        results = Order.objects.filter(queryset).distinct().order_by('id')
    else:
        results = []
    if results:
        page_obj, customers = ver_ordenes(request, results)
    else:
        page_obj = None
        customers = None
    context = {
        'orders': page_obj,
        'customers': customers,
        'query': query,
    }

    return render(request, template, context)

