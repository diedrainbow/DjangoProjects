from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date, datetime
from .models import Order, Prodact, CutOperation


def ordersList(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'ordersList.html', context)
    #return HttpResponse("Hello, Django!")
    
def load_prodacts(request, request_order_number):
    prodacts = Prodact.objects.all()
    prodacts = prodacts.filter(order_number = request_order_number)
    context = {'prodacts': prodacts, 'order_number': request_order_number}
    return render(request, 'prodactsList.html', context)
    
def new_prodact_form(request):
    context = {}
    return render(request, 'new_prodact_form.html', context)

def post_new_order(request):
    # получаем из данных запроса POST отправленные через форму данные
    order_number1 = request.POST.get("order_number", "")
    order_statys = request.POST.get("order_statys", "prodaction")
    order_add = request.POST.get("order_add", "")
    order_start = request.POST.get("order_start", "")
    order_end = request.POST.get("order_end", "")
    order_comment = request.POST.get("order_comment", "")

    if order_number1 == "":
        print ("no order number")
        return redirect('urlOrdersList')

    if order_add == "":
        order_add = datetime.now()
    if order_start == "":
        order_start = date.today()
    if order_end == "":
        order_end = date.today()

    try:
        new_order = Order.objects.get(order_number=order_number1)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.date_add = order_add
    
    new_order.order_number = order_number1
    new_order.statys = order_statys
    #new_order.date_add = order_add
    new_order.date_start = order_start
    new_order.date_end = order_end
    new_order.comment = order_comment
    new_order.save()

    return redirect('urlOrdersList')
    
    
def post_new_prodact(request, request_order_number):
    # получаем из данных запроса POST отправленные через форму данные
    order_number = request_order_number
    prodact_number = request.POST.get("prodact_number", "")
    prodact_name = request.POST.get("prodact_name", "")
    prodact_factory_number = request.POST.get("prodact_factory_number", "")
    prodact_specification = request.POST.get("prodact_specification", "")
    prodact_amount = request.POST.get("prodact_amount", "")
    prodact_kategory = request.POST.get("prodact_kategory", "")
    prodact_comment = request.POST.get("prodact_comment", "")

    if order_number == "":
        print ("no order number")
        return redirect('urlOrdersList')

    if order_add == "":
        order_add = datetime.now()
    if order_start == "":
        order_start = date.today()
    if order_end == "":
        order_end = date.today()

    try:
        new_order = Order.objects.get(order_number=order_number1)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.date_add = order_add
    
    new_order.order_number = order_number1
    new_order.statys = order_statys
    #new_order.date_add = order_add
    new_order.date_start = order_start
    new_order.date_end = order_end
    new_order.comment = order_comment
    new_order.save()

    return redirect('urlOrdersList')

