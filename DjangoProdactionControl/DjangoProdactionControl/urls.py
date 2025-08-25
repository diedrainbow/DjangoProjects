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

from django.contrib import admin
from django.urls import path, include, re_path

import OrdersList.views

urlpatterns = [
    # pages
    path('admin/', admin.site.urls),
    path('', OrdersList.views.ordersList, name='urlOrdersList'),
    
    # interactions
    path('post_new_order/', OrdersList.views.post_new_order),
    path('load_prodacts/<str:request_order_number>', OrdersList.views.load_prodacts),
    
    # cells interactions
    path('api/cell/<int:spreadsheet_id>/<int:row>/<int:col>/', 
         OrdersList.views.update_cell_view, name='update_cell'),
    path('api/cell/<int:spreadsheet_id>/<int:row>/<int:col>/value/', 
         OrdersList.views.cell_value_view, name='cell_value'),
    path('api/cell/<int:spreadsheet_id>/<int:row>/<int:col>/edit/', 
         OrdersList.views.cell_edit_view, name='cell_edit'),
]