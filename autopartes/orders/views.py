from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from productos.models import Product
from users.models import Address
from orders.models import ProductsOrder
from orders.models import Order
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
        order = Order(total_price=data['total'][0], status="pendiente", address=address)
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
    orders = Order.objects.all().order_by('-id')
    paginator = Paginator(orders, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '../templates/orders/ver_ordenes.html', {'orders': page_obj})


def ver_desgloce(request, id):
    order = ProductsOrder.objects.filter(order_id=id)
    address = Address.objects.get(pk=id)
    prod = []
    for o in order:
        aux = Product.objects.get(id=o.product_id)
        prod.append(aux)

    return render(request,
                  '../templates/orders/ver_desgloce.html',
                  {'order': order, 'products': prod, 'address': address})

