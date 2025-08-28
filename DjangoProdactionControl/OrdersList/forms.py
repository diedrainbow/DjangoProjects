from django import forms
from django.forms import ModelForm, DateInput
from .models import Order, Prodact, CutOperation

# Create the form class.
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["order_number", "statys", "date_start", "date_end", "comment"]
        widgets = {
            "date_start": DateInput(attrs={'type': 'date'}), #Textarea(attrs={"cols": 80, "rows": 20}),
            "date_end": DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            "order_number": {
                "max_length": "This Order number is too long.",
            },
        }


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