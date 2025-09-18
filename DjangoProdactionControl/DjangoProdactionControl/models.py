from django.db import models

class ProcessInfo(models.Model):
    # 
    process_title = models.CharField(max_length=50, null=True, blank=True)
    info_string1 = models.CharField(max_length=50, null=True, blank=True)
    info_string2 = models.CharField(max_length=50, null=True, blank=True)
    terminate = models.CharField(max_length=100, null=True, blank=True)