from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date, datetime
from .models import Order, Prodact, CutOperation
from .forms import OrderForm, ProdactForm, CutOperationForm

#----------- Orders ----------------------------------------------------
def ordersList(request):
    orders = Order.objects.all()
    order_form = OrderForm()
    context = {'orders': orders, 'order_form': order_form}
    return render(request, 'ordersList.html', context)
    #return HttpResponse("Hello, Django!")
    
def post_new_order(request):
    order, created = Order.objects.get_or_create(order_number = request.POST.get("order_number", ""))
    order_form = OrderForm(request.POST, instance=order)
    order_form.save()
    return redirect('urlOrdersList')
    

#----------- Prodacts ----------------------------------------------------
def load_prodacts(request, request_order_number):
    prodacts = Prodact.objects.all()
    prodacts = prodacts.filter(order_number = request_order_number)
    context = {'prodacts': prodacts, 'order_number': request_order_number}
    return render(request, 'prodactsList.html', context)
    




def new_prodact_form(request, prodact):
    context = {'prodact': prodact}
    return render(request, 'new_prodact_form.html', context)
    
def post_new_prodact(request, request_order_number):
    print ("view -> post_new_prodact() " + request_order_number)
    
    if request_order_number == "":
        print ("no order number")
        return load_prodacts(request, request_order_number)
        
    # получаем из данных запроса POST отправленные через форму данные
    
    try:
        new_prodact = Prodact.objects.get(  order_number = request_order_number, 
                                            number = request.POST.get("prodact_number", ""))
    except Order.DoesNotExist:
        new_prodact = Prodact()
    
    new_prodact.order_number = request_order_number
    new_prodact.number = request.POST.get("prodact_number", "")
    new_prodact.name = request.POST.get("prodact_name", "")
    new_prodact.factory_number = request.POST.get("prodact_factory_number", "")
    new_prodact.specification = request.POST.get("prodact_specification", "")
    new_prodact.amount = request.POST.get("prodact_amount", "")
    new_prodact.kategory = request.POST.get("prodact_kategory", "")
    new_prodact.comment = request.POST.get("prodact_comment", "")
    
    new_prodact.save()

    return load_prodacts(request, request_order_number)

