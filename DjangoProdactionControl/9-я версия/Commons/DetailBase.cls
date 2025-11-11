VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "DetailBase"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False


Option Explicit
Option Base 1
Private msgResult As Long

Private Const S_ZERO As String = ""
Private Const MY_RED As Long = 9869050
Private Const MY_LIGHT_RED As Long = 15132415
Private Const GETval As Boolean = True
Private Const SETval As Boolean = False
Private Const DEFAULT_DATE As Date = "01-01-2000"

' Константы Базы деталей
Private Const BASE_NAME As String = "База деталей 9.xlsm"

Private Const CELL_INFO As String = "B2"
Private Const CELL_PATH As String = "B1"
Private Const CELL_FILTER As String = "A1"
Private Const CELL_PROCESS As String = "A2"

Private Const COL_MATERIAL As Integer = 1
Private Const COL_NUMBER As Integer = 2
Private Const COL_NAME As Integer = 3
Private Const COL_GRAVE As Integer = 4
Private Const COL_SIZE As Integer = 5
Private Const COL_MARSH As Integer = 6
Private Const COL_PODDON As Integer = 7
Private Const COL_COMMENT As Integer = 8
Private Const COL_DATE As Integer = 9

Private Const COL_FRW_NAME As Integer = 10
Private Const COL_FRW_FOLDER As Integer = 11
Private Const COL_FRW_DATE As Integer = 12
Private Const COL_CDW_NAME As Integer = 13
Private Const COL_CDW_FOLDER As Integer = 14
Private Const COL_CDW_DATE As Integer = 15
Private Const COL_PARTS As Integer = 16

Private Const COL_ETAP1 As Integer = 17
Private Const COL_DESCR1 As Integer = 18

Private Const COL_SB_NUMBER As Integer = 2
Private Const COL_SB_NAME As Integer = 3
Private Const COL_SB_SOSTAV As Integer = 4
Private Const COL_SB_DATE As Integer = 5
Private Const COL_SB_CDW_NAME As Integer = 6
Private Const COL_SB_CDW_FOLDER As Integer = 7
Private Const COL_SB_CDW_DATE As Integer = 8

Private Const ROW_START As Integer = 4

' Общие переменные
Private dbSh As Worksheet
Private sbSh As Worksheet
Private dbLastRow As Long
Private SBLastRow As Long
Private dbNumArr() As Variant
Private sbNumArr() As Variant

Property Get DetailsLastRow() As Long
    DetailsLastRow = dbLastRow
End Property

Property Get SBsLastRow() As Long
    SBsLastRow = SBLastRow
End Property

'=================================================================
Public Function Init() As Boolean

    ' Ищем базу деталей и сборочных
    If Not Utils.IsBookOpen(BASE_NAME) Then
        msgResult = MsgBox("Не открыта " & BASE_NAME, vbOKOnly, "Error!")
        Init = False
        Exit Function
    End If
    Set dbSh = Nothing
    Set sbSh = Nothing
    Set dbSh = Application.Workbooks(BASE_NAME).Worksheets("Список деталей")
    Set sbSh = Application.Workbooks(BASE_NAME).Worksheets("Список сборочных")
    
    If dbSh Is Nothing Then
        msgResult = MsgBox("Список деталей не найден!", vbOKOnly, "Error!")
        Init = False
        Exit Function
    End If
    If sbSh Is Nothing Then
        msgResult = MsgBox("Список сборочных не найден!", vbOKOnly, "Error!")
        Init = False
        Exit Function
    End If
    
        ' Определяем последнюю строку
    dbLastRow = dbSh.Cells(dbSh.Rows.Count, COL_NUMBER).End(xlUp).row
    If dbLastRow < ROW_START Then dbLastRow = ROW_START
    SBLastRow = sbSh.Cells(sbSh.Rows.Count, COL_NUMBER).End(xlUp).row
    If SBLastRow < ROW_START Then SBLastRow = ROW_START
    
    ' Массивы номеров
    ReDim dbNumArr(1)
    ReDim sbNumArr(1)
'    ' Загружаем в массив сразу все номера
'    dbNumArr = dbSh.Range(dbSh.Cells(1, COL_NUMBER), dbSh.Cells(UBound(dbNumArr), COL_NUMBER)).Value
'    sbNumArr = sbSh.Range(sbSh.Cells(1, COL_NUMBER), sbSh.Cells(UBound(sbNumArr), COL_NUMBER)).Value
'    msgResult = MsgBox("Массив " & Not Not dbNumArr, vbOKOnly, "Error!")
    
    Init = True

End Function

Public Sub Out()
    ' Удаляем массивы номеров
    Erase dbNumArr
    Erase sbNumArr
End Sub

Public Sub DBSetInfoCell(info As String)
    dbSh.Range(CELL_INFO) = info
End Sub

Public Sub DBSetProcessCell(proc As String)
    dbSh.Range(CELL_PROCESS) = proc
End Sub

Public Sub SBSetInfoCell(info As String)
    sbSh.Range(CELL_INFO) = info
End Sub

Public Sub SBSetProcessCell(proc As String)
    sbSh.Range(CELL_PROCESS) = proc
End Sub

'================================== Функции поиска ==============================================
'================================================================================================
Private Sub ChekDbNumArr(ByRef start_row As Long, ByRef stop_row As Long)
    ' Если массив еще не создан, создаем
    If UBound(dbNumArr) = 1 Then
        ReDim dbNumArr(dbLastRow)
        dbNumArr = dbSh.Range(dbSh.Cells(1, COL_NUMBER), dbSh.Cells(UBound(dbNumArr), COL_NUMBER)).Value
    End If
    
    ' Проверка начального и конечного индексов поиска
    If start_row < 1 Or start_row > UBound(dbNumArr) Then start_row = 1
    If stop_row < 1 Or stop_row > UBound(dbNumArr) Then stop_row = UBound(dbNumArr)
    If start_row > stop_row Then start_row = stop_row
End Sub

Private Sub ChekSBNumArr(ByRef start_row As Long, ByRef stop_row As Long)
    ' Если массив еще не создан, создаем
    If UBound(sbNumArr) = 1 Then
        ReDim sbNumArr(SBLastRow)
        sbNumArr = sbSh.Range(sbSh.Cells(1, COL_NUMBER), sbSh.Cells(UBound(sbNumArr), COL_NUMBER)).Value
    End If
    
    ' Проверка начального и конечного индексов поиска
    If start_row < 1 Or start_row > UBound(sbNumArr) Then start_row = 1
    If stop_row < 1 Or stop_row > UBound(sbNumArr) Then stop_row = UBound(sbNumArr)
    If start_row > stop_row Then start_row = stop_row
End Sub

Public Function FindDetail_ByNumber(detailNumber As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekDbNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        If detailNumber = dbNumArr(i, 1) Then FindDetail_ByNumber = i: Exit Function
    Next i
    
    FindDetail_ByNumber = 0
End Function

Public Function FindSB_ByNumber(sbNumber As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekSBNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        If sbNumber = sbNumArr(i, 1) Then FindSB_ByNumber = i: Exit Function
    Next i
    
    FindSB_ByNumber = 0
End Function

Public Function FindDetail_ByNumberAndName(numberAndName As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekDbNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        ' Если деталь numberAndName начинается с (dbNumArr(i, 1) & " ")
        If InStr(1, numberAndName, dbNumArr(i, 1) & " ") = 1 Then FindDetail_ByNumberAndName = i: Exit Function
    Next i
    
    FindDetail_ByNumberAndName = 0
End Function

Public Function FindSB_ByNumberAndName(numberAndName As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekSBNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        If InStr(1, numberAndName, sbNumArr(i, 1) & " ") = 1 Then FindSB_ByNumberAndName = i: Exit Function
    Next i
    
    FindSB_ByNumberAndName = 0
End Function

Public Function FindDetail_ByPart(partOfNumber As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekDbNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        ' Если деталь detailShortNumber начинается с (dbNumArr(i, 1) & " ")
        If InStr(1, LCase(dbNumArr(i, 1)), LCase(partOfNumber)) = 1 Then FindDetail_ByPart = i: Exit Function
    Next i
    
    FindDetail_ByPart = 0
End Function

Public Function FindSB_ByPart(partOfNumber As String, Optional start_row As Long = 0, Optional stop_row As Long = 0) As Long
    ChekSBNumArr start_row, stop_row
    
    ' Ищем детали в массиве номеров деталей
    Dim i As Long
    For i = start_row To stop_row
        If InStr(1, LCase(sbNumArr(i, 1)), LCase(partOfNumber)) = 1 Then FindSB_ByPart = i: Exit Function
    Next i
    
    FindSB_ByPart = 0
End Function

Public Sub FindAndActivate(number As String, Optional start_row As Long = 0, Optional stop_row As Long = 0)
    Dim i As Long
    i = FindDetail_ByNumber(number, start_row, stop_row)
    If i > 0 Then
        dbSh.Activate
        dbSh.Cells(i, 2).Activate
        Exit Sub
    End If
    
    i = FindSB_ByNumber(number, start_row, stop_row)
    If i > 0 Then
        sbSh.Activate
        sbSh.Cells(i, 2).Activate
    End If
End Sub


'======================== Доступ к колонкам Базы =========================================
'============================ ДЕТАЛИ ============================================
Private Function DBShCol(Col As Long, row As Long, isGET As Boolean, Optional val As Variant = "") As Variant
    If isGET Then
        DBShCol = dbSh.Cells(row, Col).Value
    Else
        dbSh.Cells(row, Col).Value = val
        DBShCol = Empty
    End If
End Function

Public Function MaterialCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    MaterialCol = DBShCol(COL_MATERIAL, row, isGET, val)
End Function

Public Function NumberCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    NumberCol = DBShCol(COL_NUMBER, row, isGET, val)
End Function

Public Function NameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    NameCol = DBShCol(COL_NAME, row, isGET, val)
End Function

Public Function GraveCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    GraveCol = DBShCol(COL_GRAVE, row, isGET, val)
End Function

Public Function SizeCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SizeCol = DBShCol(COL_SIZE, row, isGET, val)
End Function

Public Function MarshCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    MarshCol = DBShCol(COL_MARSH, row, isGET, val)
End Function

Public Function PoddonCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    PoddonCol = DBShCol(COL_PODDON, row, isGET, val)
End Function

Public Function CommentCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    CommentCol = DBShCol(COL_COMMENT, row, isGET, val)
End Function

Public Function DateCol(row As Long, isGET As Boolean, Optional val As Date = DEFAULT_DATE) As Variant
    DateCol = DBShCol(COL_DATE, row, isGET, val)
End Function

Public Function PartsCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    PartsCol = DBShCol(COL_PARTS, row, isGET, val)
End Function

Public Function ColorFRWname(row As Long, isGET As Boolean, Optional val As Variant = xlNone) As Variant
    If isGET Then
        ColorFRWname = dbSh.Cells(row, COL_FRW_NAME).Interior.Color
    Else
        dbSh.Cells(row, COL_FRW_NAME).Interior.Color = val
        ColorFRWname = xlNone
    End If
End Function

Public Function ColorCDWname(row As Long, isGET As Boolean, Optional val As Variant = xlNone) As Variant
    If isGET Then
        ColorCDWname = dbSh.Cells(row, COL_CDW_NAME).Interior.Color
    Else
        dbSh.Cells(row, COL_CDW_NAME).Interior.Color = val
        ColorCDWname = xlNone
    End If
End Function

Public Function FRWnameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    FRWnameCol = DBShCol(COL_FRW_NAME, row, isGET, val)
End Function

Public Function FRWfolderCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    FRWfolderCol = DBShCol(COL_FRW_FOLDER, row, isGET, val)
End Function

Public Function FRWdateCol(row As Long, isGET As Boolean, Optional val As Date = DEFAULT_DATE) As Variant
    FRWdateCol = DBShCol(COL_FRW_DATE, row, isGET, val)
End Function

Public Function CDWnameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    CDWnameCol = DBShCol(COL_CDW_NAME, row, isGET, val)
End Function

Public Function CDWfolderCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    CDWfolderCol = DBShCol(COL_CDW_FOLDER, row, isGET, val)
End Function

Public Function CDWdateCol(row As Long, isGET As Boolean, Optional val As Date = DEFAULT_DATE) As Variant
    CDWdateCol = DBShCol(COL_CDW_DATE, row, isGET, val)
End Function

Public Function EtapCol(row As Long, i As Long, isGET As Boolean, Optional val As String = "") As String
    EtapCol = DBShCol(COL_ETAP1 + (i - 1) * 2, row, isGET, val)
End Function

Public Function DescrCol(row As Long, i As Long, isGET As Boolean, Optional val As String = "") As String
    DescrCol = DBShCol(COL_DESCR1 + (i - 1) * 2, row, isGET, val)
End Function

'============================= СБОРОЧНЫЕ =========================================
Private Function SBShCol(Col As Long, row As Long, isGET As Boolean, Optional val As Variant = "") As Variant
    If isGET Then
        SBShCol = sbSh.Cells(row, Col).Value
    Else
        sbSh.Cells(row, Col).Value = val
        SBShCol = Empty
    End If
End Function

Public Function SBnumberCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SBnumberCol = SBShCol(COL_SB_NUMBER, row, isGET, val)
End Function

Public Function SBnameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SBnameCol = SBShCol(COL_SB_NAME, row, isGET, val)
End Function

Public Function SBsostavCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SBsostavCol = SBShCol(COL_SB_SOSTAV, row, isGET, val)
End Function

Public Function SBdateCol(row As Long, isGET As Boolean, Optional val As Date = DEFAULT_DATE) As Variant
    SBdateCol = SBShCol(COL_SB_DATE, row, isGET, val)
End Function

Public Function SBCDWnameCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SBCDWnameCol = SBShCol(COL_SB_CDW_NAME, row, isGET, val)
End Function

Public Function SBCDWfolderCol(row As Long, isGET As Boolean, Optional val As String = "") As String
    SBCDWfolderCol = SBShCol(COL_SB_CDW_FOLDER, row, isGET, val)
End Function

Public Function SBCDWdateCol(row As Long, isGET As Boolean, Optional val As Date = DEFAULT_DATE) As Variant
    SBCDWdateCol = SBShCol(COL_SB_CDW_DATE, row, isGET, val)
End Function

