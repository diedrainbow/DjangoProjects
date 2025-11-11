Attribute VB_Name = "Utils"
Option Explicit
Option Base 1
Public ans As Long
Public Const sZero As String = ""
Public Const myRed As Long = 9869050
Public Const myLightRed As Long = 15132415

' Индекс цвета заливки
Function ЦВЕТЗАЛИВКИ(Ячейка As Range)
        ЦВЕТЗАЛИВКИ = Ячейка.Interior.Color
End Function

' Ожидание 1 секунды каждые Period строк, чтобы Эксель не зависал
Sub Wait1Sec(Count As Long, Optional Period As Long = 1000)
    If Count Mod Period = 0 Then Application.Wait Time:=Now + TimeSerial(0, 0, 1)
End Sub

' Ускорение работы
Sub TimeOptimize(mode As String)
    If mode = "on" Then
        'отключаем обновление экрана
        Application.ScreenUpdating = False
        'Отключаем автопересчет формул
        'Application.Calculation = xlCalculationManual
        'Отключаем отслеживание событий
        Application.EnableEvents = False
        'Отключаем разбиение на печатные страницы
        ActiveWorkbook.ActiveSheet.DisplayPageBreaks = False
    Else
        'Возвращаем обновление экрана
        Application.ScreenUpdating = True
        'Возвращаем автопересчет формул
        'Application.Calculation = xlCalculationAutomatic
        'Включаем отслеживание событий
        Application.EnableEvents = True
    End If
End Sub

Sub FilesDateChek(row As Long, f_Col As Long, d_Col As Long, Optional isPartsChek As Boolean = False)
    Dim listSH As Worksheet
    Set listSH = ActiveSheet
    
    Dim FSO As New FileSystemObject
    Dim f_File As file
    Dim d_File As file
    
    Dim f_Date As Date
    Dim d_Date As Date
    Dim default_Date As Date
    
    Dim f_DateCol As Long: f_DateCol = f_Col + 2
    Dim d_DateCol As Long: d_DateCol = d_Col + 2
    
    ' Пути файлов Фрагмента и Чертежа
    Dim frwFilePath As String
    Dim CDWfilePath As String
    frwFilePath = listSH.Cells(row, f_Col + 1) & "\" & listSH.Cells(row, f_Col)
    CDWfilePath = listSH.Cells(row, d_Col + 1) & "\" & listSH.Cells(row, d_Col)
    
    ' Проверяем существование Чертежа и обновляем его дату
    If listSH.Cells(row, d_Col) <> "" Then
        If FSO.FileExists(CDWfilePath) Then
            Set d_File = FSO.GetFile(CDWfilePath)
            d_Date = d_File.DateLastModified
            listSH.Cells(row, d_DateCol) = d_Date
            listSH.Cells(row, d_DateCol).Interior.Color = xlNone
        Else
            listSH.Cells(row, d_DateCol) = "Нет файла"
            listSH.Cells(row, d_DateCol).Interior.Color = myLightRed
        End If
    Else
        listSH.Cells(row, d_DateCol) = ""
        listSH.Cells(row, d_DateCol).Interior.Color = xlNone
    End If
    
    ' В "Список сборочных" и "Поиск в Базе" в f_Col передается непосредственно дата
    If listSH.Name = "Список сборочных" Or listSH.Name = "Поиск в Базе" Then
        f_DateCol = f_Col
        f_Date = CDate(listSH.Cells(row, f_DateCol))
        ' Сбрасываем цвета
        listSH.Cells(row, f_DateCol).Font.Color = vbBlack
        listSH.Cells(row, f_DateCol).Interior.Color = xlNone
    ' Иначе проверяем существование Фрагмента и обновляем его дату
    Else
        ' Сбрасываем цвета
        listSH.Cells(row, f_DateCol).Font.Color = vbBlack
        listSH.Cells(row, f_DateCol).Interior.Color = xlNone
        
        If listSH.Cells(row, f_Col) <> "" Then
            If FSO.FileExists(frwFilePath) Then
                Set f_File = FSO.GetFile(frwFilePath)
                f_Date = f_File.DateLastModified
                listSH.Cells(row, f_DateCol) = f_Date
                listSH.Cells(row, f_DateCol).Interior.Color = xlNone
            Else
                listSH.Cells(row, f_DateCol) = "Нет файла"
                listSH.Cells(row, f_DateCol).Interior.Color = myLightRed
            End If
        Else
            listSH.Cells(row, f_DateCol) = ""
            listSH.Cells(row, f_DateCol).Interior.Color = xlNone
        End If
    End If
    
    ' Если обе даты актуальны, сравниваем их
    If f_Date <> default_Date And d_Date <> default_Date Then
        listSH.Cells(row, f_DateCol).Interior.Color = xlNone
        If f_Date < d_Date Then listSH.Cells(row, f_DateCol).Interior.Color = myRed
    End If
    
    ' Если Фрагмент старше 10.07.24 (ввод новых гравировок)
    If f_Date <> default_Date And f_Date < CDate(45453) Then
        listSH.Cells(row, f_DateCol).Font.Color = vbRed
    End If
    
    ' Проверяем дату описания детали (9й столбик)
    If listSH.Name = "Список деталей" Then
        If listSH.Cells(row, 9) <> "" And d_Date <> default_Date Then
            listSH.Cells(row, 9).Interior.Color = xlNone
            If CDate(listSH.Cells(row, 9)) < d_Date Then listSH.Cells(row, 9).Interior.Color = myRed
        End If
    End If
    
    '============================== Для Сводной таблицы проверяем обработанные детали =================================================
    If isPartsChek Then
        Dim t_Sh As Worksheet
        Set t_Sh = ActiveSheet
        Dim fFile As file
        Dim PartsFolder As String: PartsFolder = t_Sh.Range("J1").Value
        Dim FilePath As String
        Dim t_FormatCol As Integer: t_FormatCol = f_Col + 3
        Dim t_DateCol1 As Integer: t_DateCol1 = f_Col + 2
        Dim t_FolderCol1 As Integer: t_FolderCol1 = f_Col + 1
        Dim t_NameCol1 As Integer: t_NameCol1 = f_Col
    
        t_Sh.Cells(row, t_FormatCol).Value = "DXF  NCE  NCEX"
        t_Sh.Cells(row, t_FormatCol).Font.Color = rgbWhiteSmoke
        t_Sh.Cells(row, t_FormatCol).Font.Bold = True
        
        Dim BaseDate As Date
        If IsDate(t_Sh.Cells(row, t_DateCol1)) Then BaseDate = CDate(t_Sh.Cells(row, t_DateCol1))
        ' Проверяем наличие и актуальность детали DXF
        FilePath = t_Sh.Cells(row, t_FolderCol1).Value & "\" & Replace(t_Sh.Cells(row, t_NameCol1).Value, ".frw", ".dxf")
        If FSO.FileExists(FilePath) Then
            Set fFile = FSO.GetFile(FilePath)
            If BaseDate <= fFile.DateLastModified Then
                t_Sh.Cells(row, t_FormatCol).Characters(1, 3).Font.Color = rgbGreen: BaseDate = fFile.DateLastModified
            Else
                t_Sh.Cells(row, t_FormatCol).Characters(1, 3).Font.Color = rgbRed
            End If
        End If
        
        ' Проверяем наличие и актуальность детали NCE
        FilePath = PartsFolder & "\NCE\" & t_Sh.Cells(row, 1).Value & "\" & Replace(t_Sh.Cells(row, t_NameCol1).Value, ".frw", ".nce")
        If FSO.FileExists(FilePath) Then
            Set fFile = FSO.GetFile(FilePath)
            If BaseDate <= fFile.DateLastModified Then
                t_Sh.Cells(row, t_FormatCol).Characters(6, 3).Font.Color = rgbGreen
            Else
                t_Sh.Cells(row, t_FormatCol).Characters(6, 3).Font.Color = rgbRed
            End If
        End If
        
        ' Проверяем наличие и актуальность детали NCEX
        FilePath = PartsFolder & "\NCEX\" & t_Sh.Cells(row, 1).Value & "\" & Replace(t_Sh.Cells(row, t_NameCol1).Value, ".frw", ".ncex")
        If FSO.FileExists(FilePath) Then
            Set fFile = FSO.GetFile(FilePath)
            If BaseDate <= fFile.DateLastModified Then
                t_Sh.Cells(row, t_FormatCol).Characters(11, 4).Font.Color = rgbGreen
            Else
                t_Sh.Cells(row, t_FormatCol).Characters(11, 4).Font.Color = rgbRed
            End If
        End If
        
        Set fFile = Nothing
    End If
    '=================================================================

    ' Удаляем объекты
    Set FSO = Nothing
    Set f_File = Nothing
    Set d_File = Nothing
End Sub

Function OpenFile(FilePath As String) As Boolean
    Dim FSO As New FileSystemObject
    
    If FSO.FileExists(FilePath) Then
        Dim ws As Object
        Set ws = CreateObject("WScript.Shell")
        ws.Run """" & FilePath & """"
        Set ws = Nothing
        OpenFile = True
    Else
        OpenFile = False
    End If
    
    Set FSO = Nothing
End Function

Function IsBookOpen(wbName As String) As Boolean
    Dim wbBook As Workbook
    For Each wbBook In Workbooks
'        If wbBook.Name <> ThisWorkbook.Name Then
            If Windows(wbBook.Name).Visible Then
                If wbBook.Name = wbName Then IsBookOpen = True: Exit For
            End If
'        End If
    Next wbBook
End Function

' Парсинг ячейки с составом сборочного
'==========================================================
Function SostavParsing(SoursStr As String) As String()

    Dim linesArr() As String
    Dim tableArr() As String
    Dim line() As String
    Dim i As Long
    
    linesArr = Split(SoursStr, vbNewLine)
    ReDim tableArr(UBound(linesArr), 3)
    
    For i = LBound(tableArr) To UBound(tableArr)
        line = Split(linesArr(i - 1), " | ")
        If UBound(line) = 2 Then
            tableArr(i, 1) = line(0)
            tableArr(i, 2) = line(1)
            tableArr(i, 3) = line(2)
        End If
    Next i
    
    SostavParsing = tableArr

End Function
'============================================================


