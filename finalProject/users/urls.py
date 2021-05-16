from typing import Pattern
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>/', views.details, name='details'),
    # change url to the new syntax
    path('edit/<int:id>/', views.editUser, name='edit'),
    path('register-user/', views.registerUser, name='register'),
    path('delete-user/<int:id>/', views.deleteUser, name='delete'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    # TODO update to path
    # TODO change the name import_ to import_db  and importdb to import_db
    url(r'^importdb/$', views.import_, name='import_'),
    url(r'^export_excel/$', views.export_excel, name='export_excel'),
    url(r'^export_csv/$', views.export_csv, name='export_csv'),
    url(r'^export_xml/$', views.export_xml, name='export_xml'),
    path('export-db/', views.export, name='export'),
    path('parse-excel/', views.Parse_xl, name='Parse_xl'),
    path('parse-txt/', views.Parse_txt, name='Parse_txt'),
    path('parse-xml/', views.Parse_xml, name='Parse_xml')
]
