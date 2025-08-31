from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
from datetime import date, datetime
from django.utils import timezone
import csv

def detailsBase(request):
    details = Detail.objects.all()
    context = {'details': details}
    return render(request, 'detailsBase.html', context)




    
def load_from_file(request):
    #FILENAME = r"d:\DjangoProject\DjangoProdactionControl\DetailsBase\details2.csv"
    FILENAME = r"d:\django\DjangoProdactionControl\DetailsBase\details.csv"
    
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file, delimiter=';')
            #header = next(reader)
            #print(header)
            
            for row in reader:
                try:
                    detail = Detail.objects.get(number = row[1])
                except Detail.DoesNotExist:
                    detail = Detail()
                
                # Общие данные о детали
                detail.material_name    = GetMaterialNameFromString(row[0])
                detail.number           = row[1] #.replace("[,]", ";")
                detail.name             = row[2]
                detail.grave            = row[3]
                detail.size             = row[4]
                detail.marshrut         = row[5]
                detail.poddon           = row[6]
                detail.comment          = row[7]
                detail.actual_date      = DateTimeFromString(row[8]) #datetime(2000, 1, 1, 1, 1, 1)
                # Ссылки на файлы чертежа и фрагмента
                detail.frw_file_name    = row[9]
                detail.frw_file_folder  = row[10]
                detail.frw_file_date    = DateTimeFromString(row[11])
                detail.frw_file_parts   = row[15]
                detail.frw_valid        = 1.0
                detail.cdw_file_name    = row[12]
                detail.cdw_file_folder  = row[13]
                detail.cdw_file_date    = DateTimeFromString(row[14])
                detail.cdw_valid        = 1.0
                # Технологические операции
                detail.stages           = ";;;;;;"
                detail.times            = ";;;;;;"
                detail.descriptions     = ";;;;;;"
                
                detail.save()
                print("-", end="")
            
    except Exception as ex:
        print("============================== ERROR ===============================")
        print(ex)
        print("====================================================================")
        return redirect('urlDetailsBase')
    
    return redirect('urlDetailsBase')

def DateTimeFromString(date_string):
    # Преобразование строки в объект datetime
    try:
        date_object = datetime.strptime(date_string, "%d.%m.%Y")
        #print(f"Строка '{date_string}' успешно преобразована в объект datetime: {date_object}")
        return timezone.make_aware(date_object)
    except ValueError as e:
        # print("================= ERROR =====================")
        # print(f"Ошибка преобразования строки '{date_string}': {e}")
        # print("=============================================")
        return timezone.make_aware(datetime(2000, 1, 1, 1, 1, 1))

def GetMaterialNameFromString(material_string):
    if material_string == "": return ""
        
    try:
        material2 = Material()
        material2.SetMaterialFromString( material_string )
        #print("=== try "+material.name)
        material = Material.objects.get(name = material2.name)
    except Material.DoesNotExist:
        material = Material()
        material.SetMaterialFromString( material_string )
        #print("=== exp "+material.name)
        if "..." not in material.name:
            print("new material "+material.name)
            material.save()
        else:
            material.name = material.name + " _" + material_string
            
    return material.name



    
def SBBase(request):
    return HttpResponse("SBBase")