from django.db import models

class Detail(models.Model):
    # Общие данные о детали
    material_name       = models.CharField(max_length=50, null=True, blank=True)
    number              = models.CharField(max_length=80)
    name                = models.CharField(max_length=80, null=True, blank=True)
    grave               = models.CharField(max_length=10, null=True, blank=True)
    size                = models.CharField(max_length=30, null=True, blank=True)
    marshrut            = models.CharField(max_length=60, null=True, blank=True)
    poddon              = models.CharField(max_length=15, null=True, blank=True)
    comment             = models.TextField( null=True, blank=True)
    actual_date         = models.DateTimeField()
    # Ссылки на файлы чертежа и фрагмента
    frw_file_name       = models.FileField( null=True, blank=True)
    frw_file_folder     = models.FilePathField( null=True, blank=True)
    frw_file_date       = models.DateTimeField( null=True, blank=True)
    frw_file_parts      = models.TextField( null=True, blank=True)
    frw_valid           = models.FloatField(default=0)
    cdw_file_name       = models.FileField( null=True, blank=True)
    cdw_file_folder     = models.FilePathField( null=True, blank=True)
    cdw_file_date       = models.DateTimeField( null=True, blank=True)
    cdw_valid           = models.FloatField(default=0)
    # Технологические операции
    stages              = models.TextField(default=";;;;;;")
    times               = models.TextField(default=";;;;;;")
    descriptions        = models.TextField(default=";;;;;;")


class SB(models.Model):
    # Общие данные о сборочном
    number              = models.CharField(max_length=100)
    name                = models.CharField(max_length=100, null=True, blank=True)
    composition         = models.TextField(null=True, blank=True)
    size                = models.CharField(max_length=50, null=True, blank=True)
    comment             = models.TextField(null=True, blank=True)
    actual_date         = models.DateTimeField()
    # Ссылка на файл чертежа
    cdw_file_name       = models.FileField(null=True, blank=True)
    cdw_file_folder     = models.FilePathField(null=True, blank=True)
    cdw_file_date       = models.DateTimeField(null=True, blank=True)
    cdw_valid           = models.FloatField(default=0)
    
    
class Material(models.Model):
    # например: лист 1.0 Zn350
    name                = models.CharField(max_length=50) 
    # например: лист, круг, труба, уголок, швеллер и т.д
    type                = models.CharField(max_length=30, null=True, blank=True) 
    # например: 0.55, 0.8, 1.0, 3.0, 12, 20 и т.д
    size                = models.CharField(max_length=30, null=True, blank=True) 
    # например: ст.3, ст.45, Zn140, Zn350, AISI321, AISI430 и т.д
    sort                = models.CharField(max_length=30, null=True, blank=True) 
    # 
    original            = models.CharField(max_length=50, null=True, blank=True)
    # цвет материала
    color               = models.CharField(max_length=7, null=True, blank=True)
    # 
    slash_time          = models.FloatField(default=0)
    plate_width         = models.FloatField(default=0)
    plate_lenght        = models.FloatField(default=0)
    square_m_weidth     = models.FloatField(default=0)

    def SetMaterialFromString(self, mat):
        mat = mat.lower()
        
        # type
        self.type = "..."
        self.size = "..."
        types = { 
            "лист": "лист", 
            "круг": "круг", 
            "труба": "труба", 
            "уголок": "уголок", 
            "швеллер": "швеллер",
            "двутавр": "двутавр",
            "полоса": "полоса",
            "шестигранник": "шестигранник",
            "шпилька оцинкованная": "шпилька оц.",
            "чечевица": "чечевица",
            "просеч": "просечка"
            }
        for t_key in types:
            if t_key in mat: 
                self.type = types[t_key]
                # size
                self.size = mat[len(t_key)+1 : mat.find(" ", len(t_key)+2)]
                break
        
        # sort
        self.sort = "..."
        self.color = "#000000"
        sorts = { 
            "оц.": "",
            "марка 350": "Zn350",
            "zn275": "Zn350",
            "ст.3": "ст.3", 
            "09г2с": "09Г2С",
            "aisi.321": "AISI.321",
            "aisi.430": "AISI.430",
            "ral": "RAL",
            "ре1000": "РЕ1000",
            "пнд": "ПНД",
            "сталь 45": "ст.45",
            "алюминий": "алюминий"
            }
        for s_key in sorts:
            if s_key in mat: 
                self.sort = sorts[s_key]
                break
        
        self.original = mat
        self.name = self.type + " " + self.size + " " + self.sort





