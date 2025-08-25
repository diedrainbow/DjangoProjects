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
    context = {'prodacts': prodacts}
    return render(request, 'prodactsList.html', context)

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

    return redirect('urlOrdersList')
    
    
    
    
# Interactive Cells
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
#from .models import Spreadsheet, Cell

#def spreadsheet_view(request, spreadsheet_id):
#    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
#    return render(request, 'spreadsheet.html', {
#        'spreadsheet': spreadsheet,
#        'rows': range(1, 51),  # 50 строк
#        'cols': range(1, 27),  # 26 колонок (A-Z)
#    })

def cell_value_view(request, spreadsheet_id, row, col):
    if spreadsheet_id == 'prodacts_sheet' then:
        cell, created = Prodact.objects.get_or_create(
            sheet_row=row,
            col=col,
            defaults={'value': ''}
        )
        
    return render(request, 'partials/cell_value.html', {'cell': cell})
    

@require_http_methods(["POST"])
def update_cell_view(request, spreadsheet_id, row, col):
    value = request.POST.get('value', '')
    
    cell, created = Cell.objects.get_or_create(
        spreadsheet_id=spreadsheet_id,
        row=row,
        col=col
    )
    cell.value = value
    cell.save()
    
    return render(request, 'partials/cell_value.html', {'cell': cell})

def cell_edit_view(request, spreadsheet_id, row, col):
    cell, created = Cell.objects.get_or_create(
        spreadsheet_id=spreadsheet_id,
        row=row,
        col=col,
        defaults={'value': ''}
    )
    return render(request, 'partials/cell_edit.html', {'cell': cell})
