from django.db import models

class Detail(models.Model):
    # Общие данные о детали
    material_name       = models.CharField(max_length=50)
    number              = models.CharField(max_length=80)
    name                = models.CharField(max_length=80)
    grave               = models.CharField(max_length=10)
    size                = models.CharField(max_length=30)
    marshrut            = models.CharField(max_length=60)
    poddon              = models.CharField(max_length=15)
    comment             = models.TextField()
    actual_date         = models.DateTimeField()
    
    # Ссылки на файлы чертежа и фрагмента
    frw_file_name       = models.FileField()
    frw_file_folder     = models.TextField()
    frw_file_date       = models.DateTimeField()
    frw_file_parts      = models.TextField()
    frw_valid           = models.SmallIntegerField()
    cdw_file_name       = models.FileField()
    cdw_file_folder     = models.TextField()
    cdw_file_date       = models.DateTimeField()
    cdw_valid           = models.SmallIntegerField()
    
    # Технологические операции
    stage1              = models.CharField(max_length=30)
    time1               = models.FloatField()
    description1        = models.TextField()
    stage2              = models.CharField(max_length=30)
    time2               = models.FloatField()
    description2        = models.TextField()
    stage3              = models.CharField(max_length=30)
    time3               = models.FloatField()
    description3        = models.TextField()
    stage4              = models.CharField(max_length=30)
    time4               = models.FloatField()
    description4        = models.TextField()
    stage5              = models.CharField(max_length=30)
    time5               = models.FloatField()
    description5        = models.TextField()
    stage6              = models.CharField(max_length=30)
    time6               = models.FloatField()
    description6        = models.TextField()
    stage7              = models.CharField(max_length=30)
    time7               = models.FloatField()
    description7        = models.TextField()


class SB(models.Model):
    # Общие данные о сборочном
    number              = models.CharField(max_length=100)
    name                = models.CharField(max_length=100)
    composition         = models.TextField()
    size                = models.CharField(max_length=50)
    comment             = models.TextField()
    actual_date         = models.DateTimeField()
    
    # Ссылка на файл чертежа
    cdw_file_name       = models.FileField()
    cdw_file_folder     = models.TextField()
    cdw_file_date       = models.DateTimeField()
    cdw_valid           = models.SmallIntegerField()
    
    
class Material(models.Model):
    name                = models.CharField(max_length=50) # например: лист 1.0 Zn350
    type                = models.CharField(max_length=30) # например: лист, круг, труба, уголок, швеллер и т.д
    thickness           = models.CharField(max_length=30) # например: 0.55, 0.8, 1.0, 3.0, 12, 20 и т.д
    material            = models.CharField(max_length=30) # например: ст.3, ст.45, Zn140, Zn350, AISI321, AISI430 и т.д
    variant1            = models.CharField(max_length=70) # старые варианты названий
    variant2            = models.CharField(max_length=70)
    variant3            = models.CharField(max_length=70)
    variant4            = models.CharField(max_length=70)
    variant5            = models.CharField(max_length=70)

