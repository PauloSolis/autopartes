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

# Create your views here.
logger = logging.getLogger(__name__)


def crear_orden(request):
    if request.method == 'POST':
        received_order = json.loads(request.body)
        logger.error(received_order)
        data = json.loads(received_order['data'][0])
        address= json.loads(received_order['data'][1])
        address = Address.objects.get(pk=address['address'][0])
        logger.error(address)
        user_buying = User.objects.get(pk=request.user.id)
        order = Order(total_price=data['total'][0], status="pendiente", address=address, user=user_buying)
        order.save()
        for product in received_order['products']:
            prod_decoded = json.loads(product)
            aux_product = Product.objects.get(pk=prod_decoded['prod_id'])
            prod_ord = ProductsOrder(
                order=order,
                product=aux_product,
                quantity=prod_decoded['prod_quantity'],
                price=prod_decoded['price_at_sale'])
            prod_ord.save()
    return render(request, '../templates/landing.html')


def ver_ordenes(request):
    if( request.user.is_administrator ):
        orders = Order.objects.all().order_by('-id')
        paginator = Paginator(orders, 20)
        customers = []
        for o in orders:
            customer = User.objects.get(pk = o.user_id)
            customers.append(customer)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, '../templates/orders/ver_ordenes.html', {'orders': page_obj, 'customers': customers})
    else:
        orders_user = User.objects.get(pk=request.user.id)
        orders = Order.objects.filter(user=orders_user).order_by('-id')
        paginator = Paginator(orders, 20)
        addresses = []

        for o in orders:
            address = Address.objects.get(pk=o.address.id)
            addresses.append(address)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, '../templates/orders/ver_ordenes.html', {'orders': page_obj, 'addresses': addresses})




def ver_desgloce(request, id):
    order = ProductsOrder.objects.filter(order_id=id)
    aux = Order.objects.get(pk=id)
    address = Address.objects.get(pk=aux.address.id)
    prod = []
    for o in order:
        aux = Product.objects.get(id=o.product_id)
        prod.append(aux)

    return render(request,
                  '../templates/orders/ver_desgloce.html',
                  {'order': order, 'products': prod, 'address': address})

