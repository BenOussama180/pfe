from typing import Pattern
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>/', views.details, name='details'),
    # change url to the new syntax
    path('edit/<int:id>/', views.edituser, name='edit'),
    path('register-user/', views.registeruser, name='register'),
    path('delete-user/<int:id>/', views.deleteuser, name='delete'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    # TODO update to path
    # TODO change the name import_ to import_db  and importdb to import_db
    path('import-db/',views.import_db,name='import'),
    path('export-excel/',views.export_excel,name='export_excel'),
    path('export-csv/',views.export_csv,name='export_csv'),
    path('export-xml',views.export_xml,name='export_excel'),  
    path('export-db/', views.export, name='export'),
    path('parse-excel/', views.Parse_xl, name='Parse_xl'),
    path('parse-txt/', views.Parse_txt, name='Parse_txt'),
    path('parse-xml/', views.Parse_xml, name='Parse_xml')
]
