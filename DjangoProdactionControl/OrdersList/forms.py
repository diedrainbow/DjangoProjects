from django import forms
from django.forms import ModelForm
from .models import Order, Prodact, CutOperation

# Create the form class.
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["order_number", "statys", "date_add", "date_start", "date_end", "comment"]

#class OrderForm(forms.Form):
#    order_number        = forms.CharField(max_length=15)
#    statys              = ChoiceField(choices=((1, "English"), (2, "German"), (3, "French"))) #forms.CharField(max_length=15)
#    date_add            = forms.DateTimeField()
#    date_start          = forms.DateField()
#    date_end            = forms.DateField()
#    comment             = forms.CharField(max_length=150)

class ProdactForm(forms.Form):
    order_number        = forms.CharField(max_length=15)
    number              = forms.IntegerField()
    name                = forms.CharField(max_length=40)
    factory_number      = forms.IntegerField()
    specification       = forms.CharField(max_length=40)
    amount              = forms.IntegerField()
    kategory            = forms.CharField(max_length=20)
    comment             = forms.CharField(max_length=50)

class CutOperationForm(forms.Form):
    order_number        = forms.CharField(max_length=15)
    number              = forms.IntegerField()
    prodact_or_group    = forms.CharField(max_length=50)
    material            = forms.CharField(max_length=40)
    operation_number    = forms.IntegerField()
    size                = forms.CharField(max_length=15)
    slash_time          = forms.IntegerField()
    slash_date          = forms.DateField()
    cut_time            = forms.IntegerField()
    cut_date            = forms.DateField()
    cut_work_shift      = forms.IntegerField()
    comment             = forms.CharField(max_length=50)