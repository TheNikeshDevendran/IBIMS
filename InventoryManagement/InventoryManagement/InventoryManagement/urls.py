"""
URL configuration for InventoryManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include("googleauthentication.urls")),
    path('accounts/',include("allauth.urls")),
    path('', views.login),
    path('logout/', views.logout),
    path('dashboard/', views.dashbord),
    path('AddProduct/', views.AddProduct),
    path('Authenticate/', views.Authenticate),
    path('displayStock/', views.displayLowStock),
    path('edit_by_name/<str:name>/', views.edit_by_name),
    path('updateStock/<str:pname>/',views.updateStock),
    path('deactive/<str:pname>/',views.Deactive),
    path('GenerateInvoice/',views.GenerateInvoice),
    path('TakeAway/',views.TakeAway),
    path('getData/<str:barcode>/',views.getData),
    path('mail/',views.send_mail_client),
    path('EmailValidator/',views.EmialValidator),
    path('AddItem/',views.AddItem),
    path('vendor/',views.vendor),
    path('BillingInfo/',views.BillingInfo),
    path('export-sales/', views.export_product_sales_to_excel, name='export_sales'),
    path('export-sales_prev/', views.export_product_sales_to_excel_prevoius,name='export-sales_prev'),
    path('gemini/', views.gemini_chat),
    path('Staff/', views.Staff),
    path('FreeseStaff/<str:email>/', views.FreeseStaff),
]
