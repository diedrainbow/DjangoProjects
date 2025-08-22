"""
DetailsProdactionOnDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include, re_path

import OrdersList.views

urlpatterns = [
    # Uncomment the next line to enable the admin:
    #path('admin/', admin.site.urls, name='admin13'),
    path('', OrdersList.views.ordersList, name='ordersList'),
    re_path(r'^postuser/+', OrdersList.views.postuser),
    re_path(r'^load_prodacts/+', OrdersList.views.load_prodacts),
]