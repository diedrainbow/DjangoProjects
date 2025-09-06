from django import forms
from django.forms import ModelForm, DateInput, TextInput
from .models import Detail, SB, Material

# Create the form class.
class DetailForm(ModelForm):
    class Meta:
        model = Detail
        fields = ["material_name", "number", "name", "grave", "size", "marshrut", "poddon", "comment", "frw_file_name", "cdw_file_name"]
        widgets = {
            "comment": TextInput(),
            #"date_start": DateInput(attrs={'type': 'date'}), #Textarea(attrs={"cols": 80, "rows": 20}),
            #"date_end": DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            "order_number": {
                "max_length": "This Order number is too long.",
            },
        }


