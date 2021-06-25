from typing import Pattern
from unicodedata import name
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),

    path('edit/<int:id>/', views.edituser, name='edit'),
    ###########################################################
    path('edit-racine/<int:id_rac>/', views.edit_racine, name='edit_racine'),
    path('edit-scheme/<int:id_sch>/', views.edit_scheme, name='edit_scheme'),
    path('edit-verbe/<int:id_ver>/', views.edit_verbe, name='edit_verbe'),
    path('edit-nom/<int:id_nom>/', views.edit_nom, name='edit_nom'),
    ###########################################################
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
    path('import2/', views.import2, name='import2'),
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
    path('parse-excel_rac/', views.Parse_xl_rac, name='Parse_xl_rac'),
    path('parse-txt_rac/', views.Parse_txt_rac, name='Parse_txt_rac'),
    path('parse-xml_rac/', views.Parse_xml_rac, name='Parse_xml_rac'),
    ########################################################
    ##############################################
    path('parse-excel_sch/', views.Parse_xl_sch, name='Parse_xl_sch'),
    path('parse-txt_sch/', views.Parse_txt_sch, name='Parse_txt_sch'),
    # path('parse-xml_sch/', views.Parse_xml_sch, name='Parse_xml_sch'),
    ########################################################
    ##############################################
    path('parse-excel_nom/', views.Parse_xl_nom, name='Parse_xl_nom'),
    path('parse-txt_nom/', views.Parse_txt_nom, name='Parse_txt_nom'),
    # path('parse-xml_nom/', views.Parse_xml_nom, name='Parse_xml_nom'),
    ########################################################
    ##############################################
    path('parse-excel_ver/', views.Parse_xl_ver, name='Parse_xl_ver'),
    path('parse-txt_ver/', views.Parse_txt_ver, name='Parse_txt_ver'),
    # path('parse-xml_ver/', views.Parse_xml_ver, name='Parse_xml_ver'),
    ########################################################
    path('parse-excel/', views.Parse_xl, name='Parse_xl'),
    path('parse-txt/', views.Parse_txt, name='Parse_txt'),
    path('parse-xml/', views.Parse_xml, name='Parse_xml'),
    ######################################################

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
