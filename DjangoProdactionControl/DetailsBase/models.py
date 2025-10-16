from django.db import models

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
    
    class Meta:
        ordering = ['name']

    def SetMaterialFromString(self, mat):
        self.original = mat
        mat = mat.lower()
        
        '''
        if 'оц.' in mat:
            mat = mat.replace(' рулон', '')
            mat = mat.replace(' 1250мм', '')
            mat = mat.replace(' 1250', '')
            mat = mat.replace(' марка 350', '')
            mat = mat.replace(' лист 4000х1250', '')
        else:
            mat = mat.replace(' сталь 45', 'ст.45')
            mat = mat.replace(' сталь', '')
            mat = mat.replace(' СВМПЭ', '')
            mat = mat.replace(' 2500х1250 RAL 2004', ' RAL')
            mat = mat.replace(' оцинкованная', ' оц.')
        
        mat = mat.replace(',', '.')
        self.name = mat
        '''
        
        # type
        self.type = "..."
        self.size = "..."
        types = { 
            "лист рифленый чечевица": "чечевица",
            "лист просечно-вытяжной": "просечка",
            "лист": "лист", 
            "круг": "круг", 
            "труба оцинкованная": "труба оц.",
            "труба": "труба", 
            "уголок": "уголок", 
            "швеллер": "швеллер",
            "двутавр": "двутавр",
            "полоса": "полоса",
            "шестигранник": "шестигранник",
            "шпилька оцинкованная": "шпилька оц.",
            "шпоночный материал": "шпонка",
            "болт": "болт",
            "шестерня": "шестерня",
            }
        for t_key in types:
            if t_key in mat: 
                self.type = types[t_key]
                # size
                pos1 = len(t_key)+1
                pos2 = mat.find(" ", pos1)
                if pos2 == -1: pos2 = len(mat)
                self.size = mat[pos1 : pos2]
                break
        
        # sort
        self.sort = "..."
        self.color = "#000000"
        sorts = { 
            "марка 350": "Zn350",
            "zn275": "Zn350",
            "ral": "RAL",
            "оц.": "Zn",
            "ст.3": "ст.3", 
            "09г2с": "09Г2С",
            "aisi.321": "AISI.321",
            "aisi.430": "AISI.430",
            "ре1000": "РЕ1000",
            "пнд": "ПНД",
            "сталь 45": "ст.45",
            "алюминий": "алюминий",
            }
        for s_key in sorts:
            if s_key in mat: 
                self.sort = sorts[s_key]
                break
        
        self.name = self.type + " " + self.size + " " + self.sort
        self.name = self.name.replace(',', '.')
        

class Detail(models.Model):
    # Общие данные о детали
    material            = models.ForeignKey(Material, on_delete = models.SET_NULL, null=True, blank=True)
    number              = models.CharField(max_length=80)
    name                = models.CharField(max_length=80, default="")
    grave               = models.CharField(max_length=10, default="")
    size                = models.CharField(max_length=30, default="")
    marshrut            = models.CharField(max_length=60, default="")
    poddon              = models.CharField(max_length=15, default="")
    comment             = models.TextField( default="")
    actual_date         = models.DateTimeField()
    # Ссылки на файлы чертежа и фрагмента
    frw_file_name       = models.FileField( default="" )
    frw_file_folder     = models.FilePathField( default="" )
    frw_file_date       = models.DateTimeField( default=None )
    frw_file_parts      = models.TextField( default="" )
    frw_valid           = models.FloatField(default=0.0)
    cdw_file_name       = models.FileField( default="" )
    cdw_file_folder     = models.FilePathField( default="" )
    cdw_file_date       = models.DateTimeField( default=None )
    cdw_valid           = models.FloatField(default=0.0)
    # Технологические операции
    stages              = models.TextField(default=";;;;;;")
    times               = models.TextField(default=";;;;;;")
    descriptions        = models.TextField(default=";;;;;;")
    
    class Meta:
        ordering = ['number']
        
    def all_propertys_overrade_and_save(self, det):
        log_str = ""
        save_flag = False
        
        if self.material != det.material:
            save_flag = True
            self.material = det.material
            log_str += ";\tmaterial: " + str(self.material)
            
        if self.number != det.number:
            save_flag = True
            self.number = det.number
            log_str += ";\tnumber: " + self.number
            
        if self.name != det.name:
            save_flag = True
            self.name = det.name
            log_str += ";\tname: " + self.name
            
        if self.grave != det.grave:
            save_flag = True
            self.grave = det.grave
            log_str += ";\tgrave: " + self.grave
        
        if self.size != det.size:
            save_flag = True
            self.size = det.size
            log_str += ";\tsize: " + str(self.size)
        
        if self.marshrut != det.marshrut:
            save_flag = True
            self.marshrut = det.marshrut
            log_str += ";\tmarshrut: " + self.marshrut
        
        if self.poddon != det.poddon:
            save_flag = True
            self.poddon = det.poddon
            log_str += ";\tpoddon: " + self.poddon
        
        if self.comment != det.comment:
            save_flag = True
            self.comment = det.comment
            log_str += ";\tcomment: " + str(self.comment)
            
        if self.actual_date != det.actual_date:
            save_flag = True
            self.actual_date = det.actual_date
            log_str += ";\tactual_date: " + str(self.actual_date)
            
        if self.frw_file_name != det.frw_file_name:
            save_flag = True
            self.frw_file_name = det.frw_file_name
            log_str += ";\tfrw_file_name: " + str(self.frw_file_name)
            
        if self.frw_file_folder != det.frw_file_folder:
            save_flag = True
            self.frw_file_folder = det.frw_file_folder
            log_str += ";\tfrw_file_folder: " + str(self.frw_file_folder)
            
        if self.frw_file_date != det.frw_file_date:
            save_flag = True
            self.frw_file_date = det.frw_file_date
            log_str += ";\tfrw_file_date: " + str(self.frw_file_date)
            
        if self.frw_file_parts != det.frw_file_parts:
            save_flag = True
            self.frw_file_parts = det.frw_file_parts
            log_str += ";\tfrw_file_parts: " + self.frw_file_parts
            
        if self.frw_valid != det.frw_valid:
            save_flag = True
            self.frw_valid = det.frw_valid
            log_str += ";\tfrw_valid: " + str(self.frw_valid)
            
        if self.cdw_file_name != det.cdw_file_name:
            save_flag = True
            self.cdw_file_name = det.cdw_file_name
            log_str += ";\tcdw_file_name: " + str(self.cdw_file_name)
            
        if self.cdw_file_folder != det.cdw_file_folder:
            save_flag = True
            self.cdw_file_folder = det.cdw_file_folder
            log_str += ";\tcdw_file_folder: " + str(self.cdw_file_folder)
            
        if self.cdw_file_date != det.cdw_file_date:
            save_flag = True
            self.cdw_file_date = det.cdw_file_date
            log_str += ";\tcdw_file_date: " + str(self.cdw_file_date)
            
        if self.cdw_valid != det.cdw_valid:
            save_flag = True
            self.cdw_valid = det.cdw_valid
            log_str += ";\tcdw_valid: " + str(self.cdw_valid)
            
        if self.stages != det.stages:
            save_flag = True
            self.stages = det.stages
            log_str += ";\tstages: " + self.stages
            
        if self.descriptions != det.descriptions:
            save_flag = True
            self.descriptions = det.descriptions
            log_str += ";\tdescriptions: " + self.descriptions
            
        if save_flag:
            self.save()
            
        return log_str


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
    
    class Meta:
        ordering = ['number']
    
    

        
        




