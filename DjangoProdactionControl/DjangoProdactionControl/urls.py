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
import DetailsBase.views

urlpatterns = [
    # pages
    path('admin/', admin.site.urls),
    path('', OrdersList.views.ordersList, name='urlOrdersList'),
    
    path('details_base', DetailsBase.views.detailsBase, name='urlDetailsBase'),
    path('sb_base', DetailsBase.views.SBBase, name='urlSBBase'),
    path('materialsBase', DetailsBase.views.materialsBase, name='urlMaterialsBase'),
    path('details_base/load_from_file', DetailsBase.views.load_from_file, name='urlLoadFromFile'),
    
    # interactions
    re_path(r'^post_new_order/+', OrdersList.views.post_new_order),
    path('load_prodacts/<str:request_order_number>', OrdersList.views.load_prodacts),
    re_path(r'^post_new_prodact/+', OrdersList.views.post_new_prodact),
    path('new_prodact_form/', OrdersList.views.new_prodact_form),
    
    path('load_detail_row/<int:detail_id>', DetailsBase.views.load_detail_row),
    path('load_sb_row/<int:sb_id>', DetailsBase.views.load_sb_row),
]