from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
from datetime import date, datetime
from django.utils import timezone
import csv

def detailsBase(request):
    details = Detail.objects.all()
    # details = details.order_by(number)
    context = {'details': details}
    return render(request, 'detailsBase.html', context)




    
def load_from_file(request):
    FILENAME = r"d:\DjangoProject\DjangoProdactionControl\DetailsBase\details.csv"
    # FILENAME = r"d:\django\DjangoProdactionControl\DetailsBase\details.csv"
    
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file, delimiter=';')
            #header = next(reader)
            #print(header)
            count = 0
            
            for row in reader:
                try:
                    detail = Detail.objects.get(number = row[1])
                except Detail.DoesNotExist:
                    detail = Detail()
                
                # Общие данные о детали
                detail.material_name    = GetMaterialNameFromString(row[0])
                detail.number           = row[1]
                detail.name             = row[2]
                detail.grave            = row[3]
                detail.size             = row[4]
                detail.marshrut         = row[5]
                detail.poddon           = row[6]
                detail.comment          = row[7]
                act_date = DateTimeFromString(row[8])
                if act_date == None: act_date = datetime(2000, 1, 1, 1, 1, 1)
                detail.actual_date      = act_date
                
                # Ссылки на файлы чертежа и фрагмента
                if row[9] == "":
                    detail.frw_file_name    = ""
                    detail.frw_file_folder  = ""
                    detail.frw_file_date    = None
                    detail.frw_file_parts   = ""
                    detail.frw_valid        = 0.0
                else:    
                    detail.frw_file_name    = row[9].replace("[,]", ";")
                    detail.frw_file_folder  = row[10].replace("[,]", ";")
                    detail.frw_file_date    = DateTimeFromString(row[11])
                    detail.frw_file_parts   = row[15].replace("[,]", ";")
                    detail.frw_valid        = 1.0
                
                if row[12] == "":
                    detail.cdw_file_name    = ""
                    detail.cdw_file_folder  = ""
                    detail.cdw_file_date    = None
                    detail.cdw_valid        = 0.0
                else:
                    detail.cdw_file_name    = row[12].replace("[,]", ";")
                    detail.cdw_file_folder  = row[13].replace("[,]", ";")
                    detail.cdw_file_date    = DateTimeFromString(row[14])
                    detail.cdw_valid        = 1.0
                    
                # Технологические операции
                detail.stages           = row[16]+";"+row[18]+";"+row[20]+";"+row[22]+";"+row[24]+";"+";"
                detail.times            = ";;;;;;"
                detail.descriptions     = row[17]+";"+row[19]+";"+row[21]+";"+row[23]+";"+row[25]+";"+";"
                
                detail.save()
                count += 1
                print(f"Прогресс: {count} строк", end='\r')
            
    except Exception as ex:
        print("============================== ERROR ===============================")
        print(count, " строка => ", ex)
        print("====================================================================")
        return redirect('urlDetailsBase')
    
    print("\n === Complit")
    return redirect('urlDetailsBase')

def DateTimeFromString(date_string):
    if date_string == "": return None
    # Преобразование строки в объект datetime
    try:
        date_object = datetime.strptime(date_string, "%d.%m.%Y")
    except ValueError as e:
        date_object = datetime(2000, 1, 1, 1, 1, 1)
    return timezone.make_aware(date_object)

def GetMaterialNameFromString(material_string):
    if material_string == "": return ""
    
    try:
        material = Material.objects.get(original = material_string)
        return material.name
    except:
        pass
    
    material = Material()
    material.SetMaterialFromString( material_string )    
        
    try:
        material = Material.objects.get(name = material.name)
    except Material.DoesNotExist:
        if "..." not in material.name:
            #print("new material "+material.name)
            material.save()
        else:
            material.name = material.name + " [" + material_string + "]"
            
    return material.name



    
def SBBase(request):
    sbs = SB.objects.all()
    context = {'sbs': sbs}
    return render(request, 'SBBase.html', context)
    
def materialsBase(request):
    mat = Material.objects.all()
    context = {'mat': mat}
    return render(request, 'materialsBase.html', context)
    
    
    
    
    
def load_detail_row(request, detail_id):
    detail = Detail.objects.get(id = detail_id)
    detail_row = f"""
        <td> {detail.id} </td>
		<td> {detail.material_name} </td>
		<td> {detail.number} </td>
		<td> {detail.name} </td>
		<td> {detail.grave} </td>
		<td> {detail.size} </td>
		<td> {detail.marshrut} </td>
		<td> {detail.poddon} </td>
		<td> {detail.comment} </td>
		<td> {detail.actual_date} </td>
		
		<td> {detail.frw_file_name} </td>
		<td> {detail.cdw_file_name} </td>
		<td> {detail.frw_file_parts} </td>
		
		<td> {detail.stages} </td>
		<td> {detail.times} </td>
		<td> {detail.descriptions} </td>
    """
    return HttpResponse(detail_row)






