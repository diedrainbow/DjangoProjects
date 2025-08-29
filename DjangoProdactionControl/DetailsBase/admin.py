from django.contrib import admin

# Register your models here.

from .models import Detail, SB, Material

admin.site.register(Detail)
admin.site.register(SB)
admin.site.register(Material)