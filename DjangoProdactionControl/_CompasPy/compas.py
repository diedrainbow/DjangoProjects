import os
import re
#import subprocess
import pythoncom
from win32com.client import Dispatch, gencache

# Подключение к API7 программы Kompas 3D
def get_kompas_api7():
    module = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
    api = module.IKompasAPIObject(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(module.IKompasAPIObject.CLSID, pythoncom.IID_IDispatch))
    const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
    return module, api, const

# Печатаем название программы
def get_application_name():
    module7, api7, const7 = get_kompas_api7()   # Подключаемся к API7 
    app7 = api7.Application                     # Получаем основной интерфейс
    app7.Visible = True                         # Показываем окно пользователю (если скрыто)
    app7.HideMessage = const7.ksHideMessageNo   # Отвечаем НЕТ на любые вопросы программы
    print(app7.ApplicationName(FullName=True))  # Печатаем название программы
    
# Посчитаем количество листов каждого из формата
def amount_sheet(doc7):
    sheets = {"A0": 0, "A1": 0, "A2": 0, "A3": 0, "A4": 0, "A5": 0}
    for sheet in range(doc7.LayoutSheets.Count):
        format = doc7.LayoutSheets.Item(sheet).Format  # sheet - номер листа, отсчёт начинается от 0
        sheets["A" + str(format.Format)] += 1 * format.FormatMultiplicity
    return sheets
    
# Прочитаем масштаб из штампа, ячейка №6
def stamp_scale(doc7):
    stamp = doc7.LayoutSheets.Item(0).Stamp  # Item(0) указывает на штамп первого листа 
    return stamp.Text(6).Str 
    
# Прочитаем основную надпись чертежа
def stamp(doc7):
    for sheet in range(doc7.LayoutSheets.Count):
        style_filename = os.path.basename(doc7.LayoutSheets.Item(sheet).LayoutLibraryFileName)
        style_number = int(doc7.LayoutSheets.Item(sheet).LayoutStyleNumber)

        if style_filename in ['graphic.lyt', 'Graphic.lyt'] and style_number == 1:
            stamp = doc7.LayoutSheets.Item(sheet).Stamp
            match = re.search(r"\d+:\d+", stamp.Text(6).Str)
            sc = ""
            if match: sc = match.group()
            return {"Scale": sc,
                    "Designer": stamp.Text(110).Str}

    return {"Scale": 'Неопределенный стиль оформления',
            "Designer": 'Неопределенный стиль оформления'}

# Просмотр всех ячеек
def parse_stamp(doc7, number_sheet):
    stamp = doc7.LayoutSheets.Item(number_sheet).Stamp
    for i in range(10000):
        if stamp.Text(i).Str:
            print('Номер ячейки = %-5d Значение = %s' % (i, stamp.Text(i).Str))

# Подсчет технических требований, в том случае, если включена автоматическая нумерация
def count_TT(doc7, module7):
    doc2D_s = doc7._oleobj_.QueryInterface(module7.NamesToIIDMap['IDrawingDocument'],
                                           pythoncom.IID_IDispatch)
    doc2D = module7.IDrawingDocument(doc2D_s)
    text_TT = doc2D.TechnicalDemand.Text

    count_tt = 0                                 # Количество пунктов технических требований
    for i in range(text_TT.Count):               # Проходим по каждой строчке технических требований
        if text_TT.TextLines[i].Numbering == 1:  # и проверяем, есть ли у строки нумерация
            count_tt += 1                        

    # Если нет нумерации, но есть текст
    if not count_tt and text_TT.TextLines[0]:
        count_tt += 1

    return count_tt

# Подсчёт размеров на чертеже, для каждого вида по отдельности
def count_dimension(doc7, module7):
    IKompasDocument2D = doc7._oleobj_.QueryInterface(module7.NamesToIIDMap['IKompasDocument2D'],
                                                     pythoncom.IID_IDispatch)
    doc2D = module7.IKompasDocument2D(IKompasDocument2D)
    views = doc2D.ViewsAndLayersManager.Views

    count_dim = 0
    for i in range(views.Count):
        ISymbols2DContainer = views.View(i)._oleobj_.QueryInterface(module7.NamesToIIDMap['ISymbols2DContainer'],
                                                                    pythoncom.IID_IDispatch)
        dimensions = module7.ISymbols2DContainer(ISymbols2DContainer)

        # Складываем все необходимые размеры
        count_dim += dimensions.AngleDimensions.Count + \
                     dimensions.ArcDimensions.Count + \
                     dimensions.Bases.Count + \
                     dimensions.BreakLineDimensions.Count + \
                     dimensions.BreakRadialDimensions.Count + \
                     dimensions.DiametralDimensions.Count + \
                     dimensions.Leaders.Count + \
                     dimensions.LineDimensions.Count + \
                     dimensions.RadialDimensions.Count + \
                     dimensions.RemoteElements.Count + \
                     dimensions.Roughs.Count + \
                     dimensions.Tolerances.Count

    return count_dim
    
    
# Подсчёт максимальных размеров для отдельных видов
def get_max_dimensions(doc7, module7):
    IKompasDocument2D = doc7._oleobj_.QueryInterface(module7.NamesToIIDMap['IKompasDocument2D'],
                                                     pythoncom.IID_IDispatch)
    doc2D = module7.IKompasDocument2D(IKompasDocument2D)
    views = doc2D.ViewsAndLayersManager.Views
    
    view_dimensions = dict()
    
    count_dim = 0
    for i in range(views.Count):
        ISymbols2DContainer = views.View(i)._oleobj_.QueryInterface(module7.NamesToIIDMap['ISymbols2DContainer'],
                                                                    pythoncom.IID_IDispatch)
        dimensions = module7.ISymbols2DContainer(ISymbols2DContainer)
        
        # Складываем линейные, горизонтальные размеры
        max_horizontal_dim = 0
        for j in range(dimensions.LineDimensions.Count):
            max_horizontal_dim = max(max_horizontal_dim, dimensions.LineDimensions.LineDimension(j).X1)
        
        # Складываем все необходимые размеры
        count_dim += dimensions.AngleDimensions.Count + \
                     dimensions.ArcDimensions.Count + \
                     dimensions.Bases.Count + \
                     dimensions.BreakLineDimensions.Count + \
                     dimensions.BreakRadialDimensions.Count + \
                     dimensions.DiametralDimensions.Count + \
                     dimensions.Leaders.Count + \
                     dimensions.LineDimensions.Count + \
                     dimensions.RadialDimensions.Count + \
                     dimensions.RemoteElements.Count + \
                     dimensions.Roughs.Count + \
                     dimensions.Tolerances.Count
        
        i_view = views.View(i)
        view_name = i_view.Name
        
        view_dimensions[view_name] = max_horizontal_dim
        count_dim = 0

    return view_dimensions



# Функция проверяет, запущена ли программа Kompas 3D
# def is_running():
    # proc_list = subprocess.Popen('tasklist /NH /FI "IMAGENAME eq KOMPAS*"',
                                 # shell=False,
                                 # stdout=subprocess.PIPE).communicate()[0]
    # return True if proc_list else False

def parse_design_documents(paths):
    # is_run = is_running()                           # Установим флаг, который нам говорит, 
                                                    # запущена ли программа до запуска нашего скрипта

    module7, api7, const7 = get_kompas_api7()       # Подключаемся к программе
    app7 = api7.Application                         # Получаем основной интерфейс программы
    app7.Visible = True                             # Показываем окно пользователю (если скрыто)
    app7.HideMessage = const7.ksHideMessageNo       # Отвечаем НЕТ на любые вопросы программы

    table = []                                      # Создаём таблицу параметров
    for path in paths:
        doc7 = app7.Documents.Open(PathName=path,
                                   Visible=True,
                                   ReadOnly=True)       # Откроем файл в видимом режиме без права его изменять

        #row = amount_sheet(doc7)                        # Посчитаем кол-во листов каждого формат
        #row.update(stamp(doc7))                         # Читаем основную надпись
        # row = get_max_dimensions(doc7, module7)
        # row.update({
            # "Filename": doc7.Name,                      # Имя файла
            # "CountTD": count_TT(doc7, module7),     # Количество пунктов технических требований
            # "CountDim": count_dimension(doc7, module7), # Количество размеров на чертеже
        # })
        table.append(get_max_dimensions(doc7, module7))                               # Добавляем строку параметров в таблицу

        doc7.Close(const7.kdDoNotSaveChanges)           # Закроем файл без изменения

    # if not is_run: app7.Quit()                          # Выходим из программы
    return table











