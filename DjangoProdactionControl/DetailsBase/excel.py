from .models import Detail, SB, Material
from datetime import date, datetime
from django.utils import timezone

import os
import csv
from openpyxl import load_workbook


def load_SB_from_xlsx(FILENAME):
    # Загрузка рабочей книги
    wb = load_workbook(filename=FILENAME, read_only=True)
    # Получение активного листа
    sheet = wb['Список сборочных']
    
    # Получение номера последней строки
    last_row_number = sheet.max_row
    print(f"Номер последней строки с данными: {last_row_number}")
    
    for row_number in range(4, last_row_number):
        sb_number = sheet.cell(row=row_number, column=2).value
        if sb_number == "": continue
        
        try:
            sb = SB.objects.get(number = sb_number)
        except SB.DoesNotExist:
            sb = SB()
            
        sb.number       = sb_number
        sb.name         = sheet.cell(row=row_number, column=3).value
        
        composition = sheet.cell(row=row_number, column=4).value
        if composition == None:
            composition = ""
        else:
            sb.composition  = composition.replace("_x000D_", "; ")
        
        sb.actual_date  = DateFromOpenpyxl(sheet.cell(row=row_number, column=5).value)
        sb.comment      = ""
        
        cdw_file_name = sheet.cell(row=row_number, column=6).value
        if cdw_file_name == "" or cdw_file_name == None or sheet.cell(row=row_number, column=8).value == "Нет файла":
            sb.cdw_file_name = ""
            sb.cdw_file_folder = ""
            sb.cdw_file_date = None
            sb.cdw_valid = 0.0
        else:
            sb.cdw_file_name = cdw_file_name
            sb.cdw_file_folder = sheet.cell(row=row_number, column=7).value
            sb.cdw_file_date = DateFromOpenpyxl(sheet.cell(row=row_number, column=8).value)
            
            if sheet.cell(row=row_number, column=6).fill is None:
                color_index = "00000000"
            else:
                color_index = sheet.cell(row=row_number, column=6).fill.start_color.index
            
            if color_index == "00000000":
                sb.cdw_valid = 1.0
            else:
                sb.cdw_valid = 0.5
        
        sb.save()
        print(f"Прогресс: {row_number} строк", end='\r')

            

    # Чтение данных из ячеек (например, из первой ячейки)
    # cell_value = sheet['B7'].value
    # print(f"Значение ячейки B7: {cell_value}")



def load_from_csv(FILENAME):
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
        return 
    
    print("\n === Complit")
    


def DateFromOpenpyxl(date):
    if date == None:
        date = datetime(2000, 1, 1, 1, 1, 1)
    return timezone.make_aware(date)
    

def DateTimeFromString(date_string):
    if date_string == "": return None
    # Преобразование строки в объект datetime
    try:
        date_object = datetime.strptime(date_string, "%d.%m.%Y")
    except ValueError as e:
        try:
            date_object = datetime.strptime(date_string, "%d.%m.%Y %H:%M")
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
