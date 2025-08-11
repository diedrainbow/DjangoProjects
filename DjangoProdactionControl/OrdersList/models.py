from django.db import models

class Order(models.Model):
    order_number = models.CharField(max_length=15)
    statys = models.CharField(max_length=15)
    date_add = models.DateTimeField()
    date_start = models.DateField()
    date_end = models.DateField()
    comment = models.CharField(max_length=150)

class Prodact(models.Model):
    order_number = models.CharField(max_length=15)
    number_in_order_list = models.IntegerField()
    name = models.CharField(max_length=40)
    factory_number = models.IntegerField()
    amount = models.IntegerField()
    kategory = models.CharField(max_length=20)
    comment = models.CharField(max_length=40)

class CutOperation(models.Model):
    order_number = models.CharField(max_length=15)
    prodact_or_group = models.CharField(max_length=50) # prodact_or_group - number_in_order_list,amount,...
    material = models.CharField(max_length=40)
    operation_number = models.IntegerField()
    size = models.CharField(max_length=15)
    slash_time = models.IntegerField()
    slash_prodaction_date = models.DateField()
    cut_time = models.IntegerField()
    cut_prodaction_date = models.DateField()
    cut_work_shift = models.IntegerField()
    comment = models.CharField(max_length=40)