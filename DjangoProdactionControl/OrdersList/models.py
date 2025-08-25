from django.db import models

class Order(models.Model):
    order_number        = models.CharField(max_length=15)
    statys              = models.CharField(max_length=15)
    date_add            = models.DateTimeField()
    date_start          = models.DateField()
    date_end            = models.DateField()
    comment             = models.CharField(max_length=150)

class Prodact(models.Model):
    order               = models.models.OneToOneField(Order, on_delete = models.CASCADE, primary_key = True)
    sheet_row           = models.PositiveIntegerField()
    name                = models.CharField(max_length=40)
    factory_number      = models.PositiveIntegerField()
    specification       = models.CharField(max_length=40)
    amount              = models.PositiveIntegerField()
    kategory            = models.CharField(max_length=20)
    comment             = models.CharField(max_length=50)

class CutOperation(models.Model):
    order               = models.models.OneToOneField(Order, on_delete = models.CASCADE, primary_key = True)
    sheet_row           = models.PositiveIntegerField()
    prodact_or_group    = models.CharField(max_length=50)
    material            = models.CharField(max_length=40)
    operation_number    = models.PositiveSmallIntegerField()
    size                = models.CharField(max_length=15)
    slash_time          = models.PositiveIntegerField()
    slash_date          = models.DateField()
    cut_time            = models.PositiveIntegerField()
    cut_date            = models.DateField()
    cut_work_shift      = models.PositiveSmallIntegerField()
    comment             = models.CharField(max_length=50)