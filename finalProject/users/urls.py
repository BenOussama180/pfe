from typing import Pattern
from unicodedata import name
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),

    path('edit/<int:id>/', views.edituser, name='edit'),
    ###########################################################""
    path('register-user/', views.registeruser, name='register'),
    ##########################################################""
    path('delete-user/<int:id>/', views.deleteuser, name='delete'),
    path('delete-rac/<int:id>/', views.deleteRac, name='deleteRac'),
    path('delete-sch/<int:id>/', views.deleteSch, name='deleteSch'),
    path('delete-ver/<int:id>/', views.deleteVer, name='deleteVer'),
    path('delete-nom/<int:id>/', views.deleteNom, name='deleteNom'),
    ##############################################################
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    # TODO update to path
    # TODO change the name import_ to import_db  and importdb to import_db
    path('import-db/', views.import_db, name='import'),
    path('export-db/', views.export, name='export'),
    #############################################
    path('export-excel-rac/', views.export_excel_rac, name='export_excel_rac'),
    path('export-excel-sch/', views.export_excel_sch, name='export_excel_sch'),
    path('export-excel-ver/', views.export_excel_ver, name='export_excel_ver'),
    path('export-excel-nom/', views.export_excel_nom, name='export_excel_nom'),
    #############################################
    path('export-csv-rac/', views.export_csv_rac, name='export_csv_rac'),
    path('export-csv-sch/', views.export_csv_sch, name='export_csv_sch'),
    path('export-csv-ver/', views.export_csv_ver, name='export_csv_ver'),
    path('export-csv-nom/', views.export_csv_nom, name='export_csv_nom'),
    #############################################
    path('export-xml-rac/', views.export_xml_rac, name='export_xml_rac'),
    path('export-xml-sch/', views.export_xml_sch, name='export_xml_sch'),
    path('export-xml-ver/', views.export_xml_ver, name='export_xml_ver'),
    path('export-xml-nom/', views.export_xml_nom, name='export_xml_nom'),
    ##############################################

    path('parse-excel/', views.Parse_xl, name='Parse_xl'),
    path('parse-txt/', views.Parse_txt, name='Parse_txt'),
    path('parse-xml/', views.Parse_xml, name='Parse_xml'),

    path('display/', views.display, name='display'),

    path('dict-arabe/', views.arabedic, name='arabedic'),
    path('racine/', views.racines, name='racines'),
    path('scheme/', views.scheme, name='scheme'),

    path('search_rac/', views.racine_search, name='racine_search'),
    path('search_sch/<int:id_sch>', views.scheme_search, name='scheme_search'),
    path('search-mot/', views.search_mot, name='search_mot'),


    path('ajouter-rac/', views.ajouter_racine, name='ajouter_racine'),
    path('ajouter-sch/', views.ajouter_scheme, name='ajouter_scheme'),
    path('ajouter-mot/<int:id_m>/', views.ajouter_verb, name='ajouter_verb')

]
