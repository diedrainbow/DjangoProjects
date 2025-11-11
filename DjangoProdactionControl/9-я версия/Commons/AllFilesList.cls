VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "AllFilesList"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Option Base 1

Private msgResult As Long
Private FolderPath As String
Private FSO As FileSystemObject
Private CurrentFolder As folder
Private SubFolder As folder
Private CurrentFile As file
Private FoldersList As Collection
Private FilesList As Collection
Private currentFolderIndex As Long

Property Get CurrentFolderPath() As String
    CurrentFolderPath = CurrentFile.ParentFolder.Path
End Property

Property Get CurrentFileName() As String
    CurrentFileName = CurrentFile.Name
End Property

Property Get CurrentFileDate() As Date
    CurrentFileDate = CurrentFile.DateLastModified
End Property

Public Function Init(Path As String) As Boolean
    Set FSO = New FileSystemObject
    Set FoldersList = New Collection
    Set FilesList = New Collection
    FolderPath = Path
        
    ' Берем путь папки с файлами и проверяем его вылидность
    If Not FSO.FolderExists(FolderPath) Then
        msgResult = MsgBox("Неправильный путь!", vbOKOnly, "Error!")
        Init = False
        Exit Function
    End If
        
    FoldersList.Add (FolderPath)
    SetLastFolderAsCurrent
    Init = True
End Function

Public Sub Out()
    ' Удаляем объекты
    Set FSO = Nothing
    Set CurrentFolder = Nothing
    Set SubFolder = Nothing
    Set CurrentFile = Nothing
    Set FoldersList = Nothing
    Set FilesList = Nothing
End Sub

Public Function GetNextFilePath() As String
    GetNextFilePath = ""
    GetNextFolderPath
    
    If FilesList.Count > 0 Then
        Set CurrentFile = FSO.GetFile(FilesList(1))
        FilesList.Remove (1)
        GetNextFilePath = CurrentFile.Path
    End If
End Function

Private Sub GetNextFolderPath()
        ' Идем по папкам пока они не кончились и пока не появятся файлы
    Do While FoldersList.Count > 0 And FilesList.Count = 0
        ' Добавляем все файлы в список файлов, проверяя аттрибуты
        For Each CurrentFile In CurrentFolder.Files
            If IsValidFile(CurrentFile) Then FilesList.Add (CurrentFile.Path)
        Next
    
        ' Добавляем все подпапки в список адресов
        For Each SubFolder In CurrentFolder.SubFolders
            If IsValidFolder(SubFolder) Then FoldersList.Add (SubFolder.Path)
        Next
        
        ' Удаляем адрес, который уже обработали
        FoldersList.Remove (currentFolderIndex)
        ' Берем последний адрес в списке
        If FoldersList.Count > 0 Then SetLastFolderAsCurrent
    Loop
End Sub

Private Function IsValidFile(file As file) As Boolean
    IsValidFile = (file.Attributes = Normal) Or _
                 (file.Attributes And ReadOnly) Or _
                 (file.Attributes And Archive)
        If Not IsValidFile Then Debug.Print "Ошибка атрибутов файла: " & file.Attributes & ", " & file.Path
End Function

Private Function IsValidFolder(folder As folder) As Boolean
    IsValidFolder = (folder.Attributes = Normal) Or _
            (folder.Attributes And ReadOnly) Or _
            (folder.Attributes And Archive) Or _
            (folder.Attributes And Directory)
        If Not IsValidFolder Then Debug.Print "Ошибка атрибутов папки: " & folder.Attributes & ", " & folder.Path
End Function

Private Sub SetLastFolderAsCurrent()
    currentFolderIndex = FoldersList.Count
    FolderPath = FoldersList(currentFolderIndex)
    Set CurrentFolder = FSO.GetFolder(FolderPath)
End Sub


