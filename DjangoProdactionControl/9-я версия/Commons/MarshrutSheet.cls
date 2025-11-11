VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "MarshrutSheet"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Option Base 1

Private Const GETval As Boolean = True
Private Const SETval As Boolean = False

Private ans As Long
Private Wb As Workbook
Private Sh As Worksheet

Private StartRow As Long
Private LastRow As Long

Private mat_col As Long
Private kol_col As Long
Private number_col As Long
Private name_col As Long
Private grave_col As Long
Private size_col As Long
Private marsh_col As Long
Private poddon_col As Long
Private comment_col As Long
Private etap1_col As Long
Private descr1_col As Long

Property Get dStartRow()
    dStartRow = StartRow
End Property

Property Get dLastRow()
    dLastRow = LastRow
End Property

Public Function OpenSheet() As Boolean
    If Wb Is Nothing Then Set Wb = ActiveWorkbook
    Set Sh = Wb.Worksheets(1)
    
    ' Проверяем структуру таблицы
    If Sh.Cells(15, 1).Value = "материал" _
    And Sh.Cells(15, 2).Value = "кол-во деталей" _
    And Sh.Cells(15, 3).Value = "номер чертежа" _
    And Sh.Cells(15, 4).Value = "наименование детали" _
    And Sh.Cells(15, 5).Value = "гравировка" _
    And Sh.Cells(15, 6).Value = "размер детали" _
    Then 'Самый новый бланк
        StartRow = 17
        mat_col = 1
        kol_col = 2
        number_col = 3
        name_col = 4
        grave_col = 5
        size_col = 6
        marsh_col = 7
        poddon_col = 21
        comment_col = 23
        etap1_col = 8
        descr1_col = 9
    ElseIf Sh.Cells(12, 1).Value = "материал" _
    And Sh.Cells(12, 2).Value = "кол-во деталей" _
    And Sh.Cells(12, 3).Value = "номер чертежа" _
    And Sh.Cells(12, 4).Value = "наименование детали" _
    And Sh.Cells(12, 5).Value = "гравировка" _
    And Sh.Cells(12, 6).Value = "размер детали" _
    Then ' Новый бланк
        StartRow = 14
        mat_col = 1
        kol_col = 2
        number_col = 3
        name_col = 4
        grave_col = 5
        size_col = 6
        marsh_col = 7
        poddon_col = 21
        comment_col = 23
        etap1_col = 8
        descr1_col = 9
    Else
        Debug.Print "Ошибка структуры файла " & Wb.Path
        OpenSheet = False
        Exit Function
    End If
    
    ' Определяем последнюю строку
    LastRow = Sh.Cells(Sh.Rows.Count, marsh_col).End(xlUp).row
    If LastRow < StartRow Then LastRow = StartRow
    
    OpenSheet = True
End Function

Public Function OpenFile(FilePath As String, Optional isSubMarsh As Boolean = False) As Boolean

    If isSubMarsh Then
    ElseIf Not FilePath Like "*1 Маршрут *.xlsx" Then
        'Debug.Print "Ошибка имени файла " & FilePath
        OpenFile = False
        Exit Function
    End If
    
    ' Проверяем существование файла
    If Len(Dir(FilePath)) = 0 Then
        Debug.Print "Ошибка существования файла " & FilePath
        OpenFile = False
        Exit Function
    End If
    
    ' Проверяем атрибуты файла
    Dim attr As Integer
    attr = GetAttr(FilePath)
    If Not (attr = 0 Or attr = 1 Or attr = 32) Then
        Debug.Print "Ошибка аттрибута файла (" & attr & ") " & FilePath
        OpenFile = False
        Exit Function
    End If
    
    ' Открываем файл
    Set Wb = Workbooks.Open(FilePath, 0, True) ' readonly
    If Wb Is Nothing Then
        Debug.Print "Ошибка открытия файла " & FilePath
        OpenFile = False
        Exit Function
    End If
    
    OpenFile = OpenSheet()
End Function

Public Sub CloseFile()
    Wb.Close (False)
End Sub

Public Sub ExtendTableRows(kolRows As Long)
    Sh.Range(Sh.Cells(StartRow, 1), Sh.Cells(LastRow, 23)).ClearContents
    Sh.Range(Sh.Cells(StartRow, 1), Sh.Cells(LastRow, 23)).Interior.Color = xlNone
    
    Dim deltaRows As Long: deltaRows = kolRows - (LastRow - StartRow)
    If deltaRows = 0 Then ' Количество строк в бланке и в таблице одинаковое
    ElseIf deltaRows < 0 Then ' Количество строк в бланке больше, надо удалять
        Sh.Range(Sh.Rows(StartRow), Sh.Rows(StartRow + (-deltaRows) - 1)).Delete
    ElseIf deltaRows > 0 Then ' Количество строк меньше, надо добавлять
        Sh.Range(Sh.Rows(StartRow), Sh.Rows(StartRow + deltaRows - 1)).Insert CopyOrigin:=xlFormatFromRightOrBelow
    End If
    
    ' Определяем последнюю строку
    LastRow = Sh.Cells(Sh.Rows.Count, mat_col).End(xlUp).row - 26
    If LastRow < StartRow Then LastRow = StartRow
    Sh.Range(Sh.Cells(StartRow, 1), Sh.Cells(LastRow, 23)).Borders.LineStyle = xlContinuous
    
    ' Правим формулы автосуммы
    Sh.Cells(LastRow + 1, 2).FormulaLocal = "=СУММ(B$" & StartRow & ":B" & LastRow & ")-СУММЕСЛИ(A$" & StartRow & ":A" & LastRow & ";"""";B$" & StartRow & ":B" & LastRow & ")"
    Sh.Cells(LastRow + 2, 2).FormulaLocal = "=ПРОМЕЖУТОЧНЫЕ.ИТОГИ(109;B$" & StartRow & ":B" & LastRow & ")"
    
End Sub

Public Function GetRowColor(row As Long) As Long
    GetRowColor = Sh.Cells(row, number_col).Interior.Color
End Function

Public Sub SetRowColor(row As Long, Color As Long)
    Sh.Range(Sh.Cells(row, 1), Sh.Cells(row, poddon_col + 2)).Interior.Color = Color
End Sub

Public Function ShortMaterial(Sortament As String)
    If InStr(1, Sortament, "лист оц.") <> 0 Then
        If Sortament = "лист оц.1,0 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.1,0 Zn275"
        ElseIf Sortament = "лист оц.1,5 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.1,5 Zn275"
        ElseIf Sortament = "лист оц.2,0 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.2,0 Zn275"
        ElseIf Sortament = "лист оц.3,0 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.3,0 Zn275"
        ElseIf Sortament = "лист оц.1,0 рулон 1250 марка 350 Zn275" Then
                Sortament = "лист оц.1,0 Zn275"
        ElseIf Sortament = "лист оц.1,5 рулон 1250 марка 350 Zn275" Then
                Sortament = "лист оц.1,5 Zn275"
        ElseIf Sortament = "лист оц.2,0 рулон 1250 марка 350 Zn275" Then
                Sortament = "лист оц.2,0 Zn275"
        ElseIf Sortament = "лист оц.2,0 лист 4000х1250 марка 350 Zn275" Then
                Sortament = "лист оц.2,0 Zn275"
        ElseIf Sortament = "лист оц.3,0 рулон 1250 марка 350 Zn275" Then
                Sortament = "лист оц.3,0 Zn275"
        ElseIf Sortament = "лист оц.3,0 лист 4000х1250 марка 350 Zn275" Then
                Sortament = "лист оц.3,0 Zn275"
        ElseIf Sortament = "лист оц.1,0 рулон 1250мм" Then
                Sortament = "лист оц.1,0"
        ElseIf Sortament = "лист оц.1,5 рулон 1250мм" Then
                Sortament = "лист оц.1,5"
        ElseIf Sortament = "лист оц.2,0 рулон 1250мм" Then
                Sortament = "лист оц.2,0"
        ElseIf Sortament = "лист оц.3,0 рулон 1250мм" Then
                Sortament = "лист оц.3,0"
        ElseIf Sortament = "лист оц.0,55 2500х1250 RAL 2004" Then
                Sortament = "лист оц.0,55 RAL"
        ElseIf Sortament = "лист оц.0,55 рулон 1250мм" Then
                Sortament = "лист оц.0,55"
        ElseIf Sortament = "лист оц.0,8 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.0,8 Zn275"
        ElseIf Sortament = "лист оц.1,2 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.1,2 Zn275"
        ElseIf Sortament = "лист оц.2,5 рулон 1250мм марка 350 Zn275" Then
                Sortament = "лист оц.2,5 Zn275"
        End If
    Else
        Sortament = Replace(Sortament, "сталь ", "")
    End If
    
    If Sortament = "лист 10 СВМПЭ РЕ1000" Then
            Sortament = "лист 10 РЕ1000"
    ElseIf Sortament = "лист 5 СВМПЭ РЕ1000" Then
            Sortament = "лист 5 РЕ1000"
    End If
    
    ShortMaterial = Sortament
End Function

'======================= Доступ к ячейкам разных столбцов ==========================
'=============================================================================
Private Function ShCol(Col As Long, row As Long, isGET As Boolean, Optional val As Variant = Empty) As Variant
    If isGET Then
        ShCol = Sh.Cells(row, Col).Value
    Else
        Sh.Cells(row, Col).Value = val
        ShCol = Empty
    End If
End Function

Public Function MatCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    MatCol = ShCol(mat_col, row, isGET, val)
End Function

Public Function KolCol(row As Long, isGET As Boolean, Optional val As Integer = 0) As Integer
    KolCol = ShCol(kol_col, row, isGET, val)
End Function

Public Function NumCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    NumCol = ShCol(number_col, row, isGET, val)
End Function

Public Function NameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    NameCol = ShCol(name_col, row, isGET, val)
End Function

Public Function GraveCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    GraveCol = ShCol(grave_col, row, isGET, val)
End Function

Public Function SizeCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SizeCol = ShCol(size_col, row, isGET, val)
End Function

Public Function MarshCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    MarshCol = ShCol(marsh_col, row, isGET, val)
End Function

Public Function PoddCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    PoddCol = ShCol(poddon_col, row, isGET, val)
End Function

Public Function CommCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    CommCol = ShCol(comment_col, row, isGET, val)
End Function

Public Function EtapCol(row As Long, i As Long, isGET As Boolean, Optional val As String = "") As String
    EtapCol = ShCol(etap1_col + (i - 1) * 2, row, isGET, val)
End Function

Public Function DescrCol(row As Long, i As Long, isGET As Boolean, Optional val As String = "") As String
    DescrCol = ShCol(descr1_col + (i - 1) * 2, row, isGET, val)
End Function



