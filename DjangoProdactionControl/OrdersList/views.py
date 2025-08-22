from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from datetime import datetime
from .models import Order
from .models import Prodact


def ordersList(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'ordersList.html', context)
    #return HttpResponse("Hello, Django!")
    
def load_prodacts(request):
    prodacts = Prodact.objects.all()
    context = {'prodacts': prodacts}
    return render(request, 'prodactsList.html', context)

def postuser(request):
    # получаем из данных запроса POST отправленные через форму данные
    order_number1 = request.POST.get("order_number", "")
    order_statys = request.POST.get("order_statys", "prodaction")
    order_add = request.POST.get("order_add", "")
    order_start = request.POST.get("order_start", "")
    order_end = request.POST.get("order_end", "")
    order_comment = request.POST.get("order_comment", "")

    if order_number1 == "":
        print ("no order number")
        return ordersList(request)

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

    return ordersList(request)
