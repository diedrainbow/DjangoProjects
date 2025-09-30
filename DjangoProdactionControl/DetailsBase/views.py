from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
from .forms import DetailForm #, SB, Material
from .excel import load_from_csv, load_SB_from_xlsx, load_details_from_xlsx
    

def load_details_from_file(request):
    #FILENAME_CSV = r"d:\DjangoProject\DjangoProdactionControl\DetailsBase\details2.csv"
    #FILENAME_CSV = r"d:\django\DjangoProdactionControl\DetailsBase\details.csv"
    #load_from_csv(FILENAME_CSV)
    
    FILENAME_XLSX = r"k:\Обменник\_База деталей\9-я версия\База деталей 9.xlsm"
    #FILENAME_XLSX = r"d:\Documents\_База деталей 25-07-25\9-я версия\База деталей 9.xlsm"
    load_details_from_xlsx(FILENAME_XLSX)
    return redirect('urlDetailsBase')
    
def load_SB_from_file(request):
    FILENAME_XLSX = r"k:\Обменник\_База деталей\9-я версия\База деталей 9.xlsm"
    #FILENAME_XLSX = r"d:\Documents\_База деталей 25-07-25\9-я версия\База деталей 9.xlsm"
    load_SB_from_xlsx(FILENAME_XLSX)
    return redirect('urlSBBase')

    
def SBBase(request):
    sbs = SB.objects.only("id")
    context = {'sbs': sbs}
    return render(request, 'SBBase.html', context)
    
def materialsBase(request):
    mat = Material.objects.all()
    context = {'mat': mat}
    return render(request, 'materialsBase.html', context)
    
    
    
def detailsBase(request):
    details = Detail.objects.only("id")
    context = {'details': details}
    return render(request, 'detailsBase.html', context)
    
def load_detail_row(request, detail_id):
    detail = Detail.objects.get(id = detail_id)
    
    if detail.material == None: 
        material_name = '' 
    else:
        material_name = detail.material.name
        
    grave = detail.grave
    if grave == None: grave = ''
    
    comment = detail.comment
    if comment == None: comment = ''
    
    date_str = detail.actual_date.strftime('%d.%m.%Y') # document.getElementById('myModal').showModal()
    act_color = 'white'
    if detail.actual_date != None and detail.cdw_file_date != None:
        if detail.actual_date < detail.cdw_file_date: 
            act_color = 'red'
        
    frw_color = 'white'
    if detail.frw_file_name != None and detail.frw_file_name != '':
        if detail.frw_file_date != None and detail.cdw_file_date != None:
            if detail.frw_file_date < detail.cdw_file_date: frw_color = 'red'
        if 0.0 < detail.frw_valid < 1.0: frw_color = 'yellow'
    
    cdw_color = 'white'
    if detail.cdw_file_name != None and detail.cdw_file_name != '':
        if 0.0 < detail.cdw_valid < 1.0: cdw_color = 'yellow'
    
    
    detail_row = f"""
        <tr  class="detail_row" id="d{detail.id}"  hx-get="/clicked_detail/{detail.id}" hx-trigger="click" hx-target="#dialog">
        <td> {detail.id} </td>
		<td> {material_name} </td>
		<td> {detail.number} </td>
		<td> {detail.name} </td>
		<td> {grave} </td>
		<td> {detail.size} </td>
		<td> {detail.marshrut} </td>
		<td> {detail.poddon} </td>
		<td> {comment} </td>
		<td BGCOLOR='{act_color}'> {date_str} </td>
        <td BGCOLOR='{frw_color}' title='{detail.frw_file_name}'> {detail.frw_file_name} </td>
        <td BGCOLOR='{cdw_color}' title='{detail.cdw_file_name}'> {detail.cdw_file_name} </td>
        <td> {detail.frw_file_parts} </td>
		<td> {detail.stages} </td>
		<td> {detail.times} </td>
		<td title='{detail.descriptions}'> {detail.descriptions} </td>
        </tr>
    """
    return HttpResponse(detail_row)

def load_sb_row(request, sb_id):
    sb = SB.objects.get(id = sb_id)
    date_str = sb.actual_date.strftime('%d.%m.%Y')
    
    act_color = 'white'
    if sb.actual_date != None and sb.cdw_file_date != None:
        if sb.actual_date < sb.cdw_file_date: 
            act_color = 'red'
            
    cdw_color = 'white'
    if sb.cdw_file_name != None and sb.cdw_file_name != '':
        if 0.0 < sb.cdw_valid < 1.0: cdw_color = 'yellow'
    
    sb_row = f"""
        <td> {sb.id} </td>
		<td> {sb.number} </td>
		<td> {sb.name} </td>
		<td title='{sb.composition}'> {sb.composition} </td>
		<td BGCOLOR='{act_color}'> {date_str} </td>
		<td> {sb.comment} </td>
        <td BGCOLOR='{cdw_color}' title='{sb.cdw_file_name}'> {sb.cdw_file_name} </td>
    """
    return HttpResponse(sb_row)


def detail_dialog(request, detail_id):
    detail = Detail.objects.get(id = detail_id)
    detail_form = DetailForm(instance=detail)
    context = {'detail_form': detail_form}
    return render(request, 'detail_dialog.html', context)







