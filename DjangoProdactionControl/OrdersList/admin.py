from django.contrib import admin

# Register your models here.

from .models import Order, Prodact, CutOperation

admin.site.register(Order)
admin.site.register(Prodact)
admin.site.register(CutOperation)