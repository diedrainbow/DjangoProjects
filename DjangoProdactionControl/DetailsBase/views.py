from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
import csv

def detailsBase(request):
    details = Detail.objects.all()
    context = {'details': details}
    return render(request, 'detailsBase.html', context)




    
def load_from_file(request):
    FILENAME = "d:\DjangoProject\DjangoProdactionControl\DetailsBase\details2.csv"
    
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file, delimiter=';')
            #header = next(reader)
            
            for row in reader:
                detail, created = Detail.objects.get_or_create(number = row[1])
                print(created)
                # Общие данные о детали
                detail.material_name    = row[0]
                detail.number           = row[1] #.replace("[,]", ";")
                detail.name             = row[2]
                detail.grave            = row[3]
                detail.size             = row[4]
                detail.marshrut         = row[5]
                detail.poddon           = row[6]
                detail.comment          = row[7]
                detail.actual_date      = row[8]
                # Ссылки на файлы чертежа и фрагмента
                detail.frw_file_name    = row[9]
                detail.frw_file_folder  = row[10]
                detail.frw_file_date    = row[11]
                detail.frw_file_parts   = row[15]
                detail.frw_valid        = 1.0
                detail.cdw_file_name    = row[12]
                detail.cdw_file_folder  = row[13]
                detail.cdw_file_date    = row[14]
                detail.cdw_valid        = 1.0
                # Технологические операции
                detail.stages           = ";;;;;;"
                detail.times            = ";;;;;;"
                detail.descriptions     = ";;;;;;"
                
                detail.save()
            
    except Exception as ex:
        print("=========================================")
        print(ex)
        print("=========================================")
        return redirect('urlDetailsBase')
    
    return redirect('urlDetailsBase')





    
def SBBase(request):
    return HttpResponse("SBBase")