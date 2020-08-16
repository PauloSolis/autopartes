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
from users.decorators import admin_required, seller_required
from django.shortcuts import render, redirect
from .forms import Status
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from reportlab.lib.units import inch

# Create your views here.


logger = logging.getLogger(__name__)


@login_required
def crear_orden(request):
    if request.method == 'POST':
        received_order = json.loads(request.body)
        data = json.loads(received_order['data'][0])
        address = json.loads(received_order['data'][1])
        address = Address.objects.get(pk=address['address'][0])
        user_buying = User.objects.get(pk=request.user.id)
        order = Order(total_price=data['total'][0], status="pendiente", address=address, user=user_buying)
        order.save()
        for product in received_order['products']:
            prod_decoded = json.loads(product)
            aux_product = Product.objects.get(pk=prod_decoded['prod_id'])
            aux_product.in_stock -= int(prod_decoded['prod_quantity'])
            aux_product.save()
            quantity = int(prod_decoded['prod_quantity'])
            price_at_sale = float(prod_decoded['price_at_sale'])
            individual_price = price_at_sale / quantity
            prod_ord = ProductsOrder(
                order=order,
                product=aux_product,
                quantity=prod_decoded['prod_quantity'],
                price=individual_price)
            prod_ord.save()
    return render(request, '../templates/landing.html')


@login_required
def ver_ordenes(request, search=None):
    if request.user.is_administrator | request.user.is_seller:
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
    user = User.objects.get(id=order.user_id)
    for o in order_p:
        aux = Product.objects.get(id=o.product_id)
        prod.append(aux)

    return render(request,
                  '../templates/orders/ver_desgloce.html',
                  {'order_products': order_p, 'products': prod, 'address': address, 'order': order, 'client': user})


@login_required
@seller_required
def change_status(request, id):
    order = Order.objects.get(id=id)
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


def make_report(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="orden.pdf"'

    order_p = ProductsOrder.objects.filter(order_id=id)
    order = Order.objects.get(pk=id)
    address = Address.objects.get(pk=order.address.id)
    prod = []
    user = User.objects.get(id=order.user_id)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Order info
    # psition on x,position on y,  y2, pos y
    p.setStrokeColorRGB(0.2, 0.5, 0.3)
    p.rect(330, 800, 220, 20)
    p.rect(330, 780, 220, 20)
    p.rect(330, 760, 220, 20)
    p.rect(330, 740, 220, 20)

    p.drawString(335, 805, 'Número de Orden ')
    p.drawString(335, 785, str(order.id))
    p.drawString(335, 765, 'Fecha de la Orden ')
    p.drawString(335, 745, str(order.created_on))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawInlineImage("./dashboard/static/images/urbanLogo.jpeg", 200, 740, 120, 82)
    p.drawInlineImage("./dashboard/static/images/logo1.png", 5, 740, 202, 82)

    p.rect(25, 700, 200, 20)
    p.rect(25, 680, 200, 20)
    p.rect(230, 700, 325, 20)
    p.rect(230, 680, 325, 20)

    p.rect(25, 655, 200, 20)
    p.rect(25, 635, 200, 20)
    p.rect(230, 655, 325, 20)
    p.rect(230, 635, 325, 20)

    p.drawString(235, 705, 'Cliente')
    p.drawString(235, 685, str(user.first_name + ' ' + user.last_name))
    p.drawString(235, 660, 'Dirección de Entrega')
    p.drawString(235, 640, str(address.state + ', ' + address.city + ', ' + address.address))

    p.drawString(30, 705, 'RUC / CI  ')
    p.drawString(30, 685, str(user.ruc))
    p.drawString(30, 660, 'Teléfono')
    p.drawString(30, 640, str(user.phone))

    # p.drawString(50, 500, 'Total de la orden: ')
    # p.drawString(200, 500, str(order.total_price))

    p.rect(25, 600, 150, 20)
    p.rect(175, 600, 200, 20)
    p.rect(375, 600, 70, 20)
    p.rect(445, 600, 50, 20)
    p.rect(495, 600, 60, 20)

    p.drawString(30, 605, 'Código de producto')
    p.drawString(180, 605, 'Código de producto')
    p.drawString(380, 605, 'Cantidad')
    p.drawString(450, 605, 'P. Unit.')
    p.drawString(500, 605, 'Importe')

    a = 585

    for o in order_p:
        p.rect(25, a - 5, 150, 20)
        p.rect(175, a - 5, 200, 20)
        p.rect(375, a - 5, 70, 20)
        p.rect(445, a - 5, 50, 20)
        p.rect(495, a - 5, 60, 20)

        aux = Product.objects.get(id=o.product_id)
        p.drawString(30, a, aux.product_code)
        p.drawString(180, a, aux.name + ' ' + aux.description)
        p.drawString(380, a, '$ ' + str(o.quantity))
        p.drawString(450, a, '$ ' + str(o.price))
        p.drawString(500, a, '$ ' + str(o.total))
        a -= 20
        if (a <= 45):
            p.showPage()
            a = 800

    if (a <= 45):
        p.showPage()
        a = 800
    p.rect(375, a - 25, 120, 20)
    p.rect(495, a - 25, 60, 20)
    p.drawString(380, a - 20, 'TOTAL (Incluye IVA)')
    p.drawString(500, a - 20, '$ ' + str(order.total_price))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
