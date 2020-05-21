from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from productos.models import Product
from orders.models import ProductsOrder
from orders.models import Order
import json
import logging

# Create your views here.
logger = logging.getLogger(__name__)


def crear_orden(request):
    if request.method == 'POST':
        received_order = json.loads(request.body)
        data = json.loads(received_order['data'][0])
        logger.error(data['total'])
        order = Order(total_price=data['total'][0], status="pendiente")
        order.save()
        for product in received_order['products']:
            prod_decoded = json.loads(product)
            aux_product = Product.objects.get(pk=prod_decoded['prod_id'])
            prod_ord = ProductsOrder(
                order_id=order,
                product_id=aux_product,
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
    order = ProductsOrder.objects.get(order_id=id)
    logger.error(order[0])
    prod = []
    for o in order:
        aux = Product.objects.get(id = o.product_id)
        prod.append(aux)

    return render(request, '../templates/orders/ver_desgloce.html', {'order': order, 'products':prod})
