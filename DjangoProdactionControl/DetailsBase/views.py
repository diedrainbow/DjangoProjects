from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Detail, SB, Material
from .excel import load_from_csv, load_SB_from_xlsx
    

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
    date = detail.actual_date.strftime('%d.%m.%Y')
    detail_row = f"""
        <tr  class="detail_row" id="d{detail.id}"  hx-get="/clicked_detail/{detail.id}" hx-trigger="click" hx-target="#dialog">
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
		
		<td title='{detail.frw_file_name}'> {detail.frw_file_name} </td>
		<td title='{detail.cdw_file_name}'> {detail.cdw_file_name} </td>
		<td> {detail.frw_file_parts} </td>
		
		<td> {detail.stages} </td>
		<td> {detail.times} </td>
		<td title='{detail.descriptions}'> {detail.descriptions} </td>
        </tr>
    """
    return HttpResponse(detail_row)

def load_sb_row(request, sb_id):
    sb = SB.objects.get(id = sb_id)
    date = sb.actual_date.strftime('%d.%m.%Y')
    sb_row = f"""
        <td> {sb.id} </td>
		<td> {sb.number} </td>
		<td> {sb.name} </td>
		<td title='{sb.composition}'> {sb.composition} </td>
		<td> {date} </td>
		<td> {sb.comment} </td>
    """
    
    if 0.0 < sb.cdw_valid < 1.0:
        sb_row = sb_row + f"<td BGCOLOR='yellow'> {sb.cdw_file_name} </td>"
    else:
        sb_row = sb_row + f"<td> {sb.cdw_file_name} </td>"
        
    return HttpResponse(sb_row)

def detail_dialog(request, detail_id):
    dialog_str = f"""
        <dialog
        open="open"
        id="modal"
        aria-labelledby="heading"
        >
            <h2 id="heading">Detail = {detail_id} </h2>
            <p>Результат этих кнопок одинаковый.</p>

            <button type="button" onclick="window.closeMe.close()">
                Закрыть с помощью JavaScript
            </button>

            <form method="dialog">
                <!-- Если у тега <button> не указан type, то по-умолчанию он будет type="submit" ! -->
                <button>
                    Закрыть с помощью формы
                </button>
            </form>
            ::backdrop
        </dialog>
    """
    return HttpResponse(dialog_str)


