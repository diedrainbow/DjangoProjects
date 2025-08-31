from django.db import models
from datetime import date, datetime
from django.utils import timezone

STATYS_CHOICES = {
    "Prodaction":   "Prodaction",
    "Pause":        "Pause",
    "Closed":       "Closed",
    "Deleted":      "Deleted",
}

class Order(models.Model):
    order_number        = models.CharField("Order number title", max_length=9)
    statys              = models.CharField("Statys title", max_length=15, choices=STATYS_CHOICES, default="Pause")
    date_add            = models.DateTimeField("Date add title", default=timezone.now())
    date_start          = models.DateField("Date start title", default=timezone.now())
    date_end            = models.DateField("Date end title", default=timezone.now())
    comment             = models.TextField("Comment title", null=True, blank=True)

KATEGORY_CHOICES = {
    "Ventilator":       "Ventilator",
    "Zernoprovod":      "Zernoprovod",
    "Zernosushilka":    "Zernosushilka",
    "Over":             "Over",
}

class Prodact(models.Model):
    #order               = models.models.OneToOneField(Order, on_delete = models.CASCADE, primary_key = True)
    order_number        = models.CharField("Order number title", max_length=9)
    number_in_order     = models.PositiveIntegerField("Number in Order title", default=0)
    name                = models.CharField("Prodact name title", max_length=40)
    factory_number      = models.PositiveIntegerField("Factory number title", null=True, blank=True)
    specification       = models.CharField("Specification title", max_length=40, null=True, blank=True)
    amount              = models.PositiveIntegerField("Amount title", default=0)
    kategory            = models.CharField("Kategory title", max_length=20, choices=KATEGORY_CHOICES, default="Over")
    comment             = models.TextField("Comment title", null=True, blank=True)

SHIFT_CHOICES = {
    "1": "1",
    "2": "2",
    "3": "3",
}

class CutOperation(models.Model):
    #order               = models.models.OneToOneField(Order, on_delete = models.CASCADE, primary_key = True)
    order_number        = models.CharField(max_length=15)
    number              = models.PositiveIntegerField()
    prodact_or_group    = models.CharField(max_length=50)
    material            = models.CharField(max_length=40)
    operation_number    = models.PositiveSmallIntegerField()
    size                = models.CharField(max_length=15)
    slash_time          = models.PositiveIntegerField()
    slash_date          = models.DateField()
    cut_time            = models.PositiveIntegerField()
    cut_date            = models.DateField()
    cut_work_shift      = models.PositiveSmallIntegerField(choices=SHIFT_CHOICES)
    comment             = models.CharField(max_length=50)