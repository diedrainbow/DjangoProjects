from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
from .excel import load_from_csv, load_from_xlsx
    

def load_from_file(request):
    #FILENAME_CSV = r"d:\DjangoProject\DjangoProdactionControl\DetailsBase\details2.csv"
    #FILENAME_CSV = r"d:\django\DjangoProdactionControl\DetailsBase\details.csv"
    #load_from_csv(FILENAME_CSV)
    
    #FILENAME_XLSX = r"k:\Обменник\_База деталей\9-я версия\База деталей 9.xlsm"
    FILENAME_XLSX = r"d:\Documents\_База деталей 25-07-25\9-я версия\База деталей 9.xlsm"
    load_from_xlsx(FILENAME_XLSX)
    return redirect('urlDetailsBase')

    
def SBBase(request):
    sbs = SB.objects.all()
    context = {'sbs': sbs}
    return render(request, 'SBBase.html', context)
    
def materialsBase(request):
    mat = Material.objects.all()
    context = {'mat': mat}
    return render(request, 'materialsBase.html', context)
    
    
    
def detailsBase(request):
    details = Detail.objects.all()
    # details = details.order_by(number)
    context = {'details': details}
    return render(request, 'detailsBase.html', context)
    
def load_detail_row(request, detail_id):
    detail = Detail.objects.get(id = detail_id)
    date = detail.actual_date.strftime('%d.%m.%Y')
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
		<td> {date} </td>
		
		<td> {detail.frw_file_name} </td>
		<td> {detail.cdw_file_name} </td>
		<td> {detail.frw_file_parts} </td>
		
		<td> {detail.stages} </td>
		<td> {detail.times} </td>
		<td> {detail.descriptions} </td>
    """
    return HttpResponse(detail_row)






