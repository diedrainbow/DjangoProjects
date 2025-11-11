VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} EditRow 
   Caption         =   "Уточнить строку"
   ClientHeight    =   6390
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   14865
   OleObjectBlob   =   "EditRow2.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "EditRow"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False


Option Explicit
Option Base 1

'Public f_Sh As Worksheet
'Public d_Sh As Worksheet
'Public x_Sh As Worksheet
'Public listSH As Worksheet
'
Public ans As Long
'Const myRed = rgbLightCoral 'RGB(250, 150, 150)
'
'Const t_NumberCol As Integer = 1
'Const FRWname As Integer = 2
'Const FRWfolder As Integer = 3
'Const FRWdata As Integer = 4
'Const t_LinkCol1 As Integer = 5
'Const CDWname As Integer = 6
'Const CDWfolder As Integer = 7
'Const CDWdata As Integer = 8
'Const t_LinkCol2 As Integer = 9
'Const t_StartRow As Integer = 4
''Const t_BaseRow As Integer = 17
'Const t_PartsCol As Integer = 10

' Константы Базы деталей
'===============================================
Public listSH As Worksheet
Const f_StartRow As Integer = 4
Const f_InfoCell As String = "B2"
Const f_PathCell As String = "B1"
Const f_FilterCell As String = "A1"
Const f_ProcessCell As String = "A2"

Const Material As Integer = 1
Const Number As Integer = 2
Const Name As Integer = 3
Const Grave As Integer = 4
Const Size As Integer = 5
Const Marsh As Integer = 6
Const Poddon As Integer = 7
Const Comment As Integer = 8
Const Data As Integer = 9

Const FRWname As Integer = 10
Const FRWfolder As Integer = 11
Const FRWdata As Integer = 12
Const CDWname As Integer = 13
Const CDWfolder As Integer = 14
Const CDWdata As Integer = 15
Const Parts As Integer = 16

Const Etap1 As Integer = 17
Const Descr1 As Integer = 18
Const Etap2 As Integer = 19
Const Descr2 As Integer = 20
Const Etap3 As Integer = 21
Const Descr3 As Integer = 22
Const Etap4 As Integer = 23
Const Descr4 As Integer = 24

' Константы Формы
'===============================================
Public FRWfilePath As String
Public CDWfilePath As String
Public StartFRWfilePath As String
Public StartCDWfilePath As String
Public OldFRWfilePath As String

Private Sub ChooseFRW_Click()
    With Application.FileDialog(msoFileDialogFilePicker)
        .AllowMultiSelect = True
        .Title = "Выберите файл"
        .Filters.Clear
        .Filters.Add "*.frw" & " files", "*." & "*.frw", 1
        '.FilterIndex = 2
        .InitialFileName = StartFRWfilePath
        '.InitialView = msoFileDialogViewDetails
        If .Show = 0 Then Exit Sub
        '
        If .SelectedItems.Count > 0 Then
            FRWfilePath = .SelectedItems(1)
            Dim FSO As New FileSystemObject
            TextBoxFRW.Text = FSO.GetFile(FRWfilePath).Name
            If .SelectedItems.Count > 1 Then TextBoxParts.Text = FSO.GetFile(.SelectedItems(2)).Name
            Set FSO = Nothing
        Else
            Exit Sub
        End If
    End With
End Sub

Private Sub ChooseCDW_Click()
    With Application.FileDialog(msoFileDialogFilePicker)
        .AllowMultiSelect = False
        .Title = "Выберите файл"
        .Filters.Clear
        .Filters.Add "*.cdw" & " files", "*." & "*.cdw", 1
        .Filters.Add "*.m3d" & " files", "*." & "*.m3d", 2
        .FilterIndex = 1
        .InitialFileName = StartCDWfilePath
        '.InitialView = msoFileDialogViewDetails
        If .Show = 0 Then Exit Sub
        '
        If .SelectedItems.Count > 0 Then
            CDWfilePath = .SelectedItems(1)
            Dim FSO As New FileSystemObject
            TextBoxCDW.Text = FSO.GetFile(CDWfilePath).Name
            Set FSO = Nothing
        Else
            Exit Sub
        End If
    End With
End Sub

Private Sub SpinButton1_Change()
    Set listSH = ActiveSheet
    listSH.Cells(SpinButton1.Value, ActiveCell.Column).Activate
    
    UserForm_Activate
End Sub

Private Sub WriteRow_Click()
    Set listSH = ActiveSheet
    Dim Row As Long
    Row = ActiveCell.Row
    
    'If listSH.Cells(Row, FRWname).Value = "" Or Row < t_StartRow Then EditRow.Hide
    
    Dim FSO As New FileSystemObject
    Dim FragmentFile As File
    Dim DrowFile As File
    
    If CheckBoxData.Value Then listSH.Cells(Row, Data) = Date
    
    If FSO.FileExists(FRWfilePath) Then
        Set FragmentFile = FSO.GetFile(FRWfilePath)
        listSH.Cells(Row, FRWname).Value = FragmentFile.Name
        listSH.Cells(Row, FRWfolder).Value = FragmentFile.ParentFolder.Path
        listSH.Cells(Row, FRWdata).Value = FragmentFile.DateLastModified
    End If
    
    If FSO.FileExists(CDWfilePath) Then
        Set DrowFile = FSO.GetFile(CDWfilePath)
        listSH.Cells(Row, CDWname).Value = DrowFile.Name
        listSH.Cells(Row, CDWfolder).Value = DrowFile.ParentFolder.Path
        listSH.Cells(Row, CDWdata).Value = DrowFile.DateLastModified
    End If
    
    '  Проверяет даты и закрашивает ячейки
    Utils.FilesDateChek Row, FRWname, CDWname
    
    listSH.Cells(Row, Parts) = TextBoxParts.Text
    listSH.Cells(Row, Material) = TextBoxMaterial.Text
    listSH.Cells(Row, Grave) = TextBoxGrave.Text
    listSH.Cells(Row, Size) = TextBoxSize.Text
    listSH.Cells(Row, Marsh) = TextBoxMarsh.Text
    listSH.Cells(Row, Poddon) = TextBoxPoddon.Text
    
    listSH.Cells(Row, Etap1) = TextBoxEtap1.Text
    listSH.Cells(Row, Descr1) = TextBoxDescr1.Text
    listSH.Cells(Row, Etap2) = TextBoxEtap2.Text
    listSH.Cells(Row, Descr2) = TextBoxDescr2.Text
    listSH.Cells(Row, Etap3) = TextBoxEtap3.Text
    listSH.Cells(Row, Descr3) = TextBoxDescr3.Text
    listSH.Cells(Row, Etap4) = TextBoxEtap4.Text
    listSH.Cells(Row, Descr4) = TextBoxDescr4.Text
    
    ' Удаляем объекты
    Set FragmentFile = Nothing
    Set DrowFile = Nothing
    Set FSO = Nothing
    
    EditRow.Hide
End Sub

Private Sub Cansel_Click()
    EditRow.Hide
End Sub

Private Sub FRWLink_Click()
    If TextBoxFRW.Text = "" Then Exit Sub
    Dim FSO As New FileSystemObject
    
    If FSO.FileExists(FRWfilePath) Then
        'ThisWorkbook.FollowHyperlink (FRWfilePath)
        Dim ws As Object
        Set ws = CreateObject("WScript.Shell")
        ws.Run """" & FRWfilePath & """"
        Set ws = Nothing
    End If
    
    Set FSO = Nothing
End Sub

Private Sub CDWLink_Click()
    If TextBoxCDW.Text = "" Then Exit Sub
    Dim FSO As New FileSystemObject
    
    If FSO.FileExists(CDWfilePath) Then
        'ThisWorkbook.FollowHyperlink (CDWfilePath)
        Dim ws As Object
        Set ws = CreateObject("WScript.Shell")
        ws.Run """" & CDWfilePath & """"
        Set ws = Nothing
    End If
    
    Set FSO = Nothing
End Sub

Private Sub UserForm_Activate()
    Set listSH = ActiveSheet
    Dim Row As Long
    Row = ActiveCell.Row
    SpinButton1.Value = Row
    SpinButton1.Min = f_StartRow
    CheckBoxData.Value = False
    
    If listSH.Cells(Row, Number).Value = "" Or Row < f_StartRow Then EditRow.Hide
    
    Dim FSO As New FileSystemObject
    Dim FragmentFile As File
    Dim DrowFile As File

    ' Если ячейка пустая, берем путь из ячейки выше
    If listSH.Cells(Row, FRWname) = "" Then
        StartFRWfilePath = listSH.Cells(Row - 1, FRWfolder) & "\" & listSH.Cells(Row - 1, FRWname)
        FRWfilePath = ""
    Else
        StartFRWfilePath = listSH.Cells(Row, FRWfolder) & "\" & listSH.Cells(Row, FRWname)
        FRWfilePath = StartFRWfilePath
    End If
    If listSH.Cells(Row, CDWname) = "" Then
        StartCDWfilePath = listSH.Cells(Row - 1, CDWfolder) & "\" & listSH.Cells(Row - 1, CDWname)
        CDWfilePath = ""
    Else
        StartCDWfilePath = listSH.Cells(Row, CDWfolder) & "\" & listSH.Cells(Row, CDWname)
        CDWfilePath = StartCDWfilePath
    End If
    
    OldFRWfilePath = FRWfilePath
    
'    If FSO.FileExists(FRWfilePath) Then
'        Set FragmentFile = FSO.GetFile(FRWfilePath)
'        If FragmentFile.DateLastModified < CDate(45453) Then
'            TextBoxFRW.BackColor = RGB(255, 240, 240)
'        Else
'            TextBoxFRW.BackColor = vbWhite
'        End If
'
'        If FSO.FileExists(CDWfilePath) Then
'            Set DrowFile = FSO.GetFile(CDWfilePath)
'            ' Проверяем даты
'            If FragmentFile.DateLastModified < DrowFile.DateLastModified Then
'                TextBoxFRW.BackColor = RGB(250, 150, 150)
'            Else
'                TextBoxFRW.BackColor = vbWhite
'            End If
'        End If
'    End If
    
    TextBoxNumber.Text = listSH.Cells(Row, Number) & " " & listSH.Cells(Row, Name)
    TextBoxFRW.Text = listSH.Cells(Row, FRWname)
    TextBoxCDW.Text = listSH.Cells(Row, CDWname)
    TextBoxParts.Text = listSH.Cells(Row, Parts)
    TextBoxMaterial.Text = listSH.Cells(Row, Material)
    TextBoxGrave.Text = listSH.Cells(Row, Grave)
    TextBoxSize.Text = listSH.Cells(Row, Size)
    TextBoxMarsh.Text = listSH.Cells(Row, Marsh)
    TextBoxPoddon.Text = listSH.Cells(Row, Poddon)
    
    TextBoxEtap1.Text = listSH.Cells(Row, Etap1)
    TextBoxDescr1.Text = listSH.Cells(Row, Descr1)
    TextBoxEtap2.Text = listSH.Cells(Row, Etap2)
    TextBoxDescr2.Text = listSH.Cells(Row, Descr2)
    TextBoxEtap3.Text = listSH.Cells(Row, Etap3)
    TextBoxDescr3.Text = listSH.Cells(Row, Descr3)
    TextBoxEtap4.Text = listSH.Cells(Row, Etap4)
    TextBoxDescr4.Text = listSH.Cells(Row, Descr4)
    
    Set FSO = Nothing
    Set FragmentFile = Nothing
    Set DrowFile = Nothing
End Sub

