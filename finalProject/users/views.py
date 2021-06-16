from datetime import datetime
import re
from django import http
from django.contrib.messages.api import error
from django.db.models.query import QuerySet, RawQuerySet
from django.template import context
from .forms import PersonForm, RacineForm
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, response
from .models import Nom, Person, Racine, Verbe, Scheme
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import django_filters
from .filters import PersonFilter, SchemeFilter, VerbeFilter, NomFilter, RacineFilter, SchemeFilter
from . import filters
from email_validator import validate_email, EmailNotValidError
import xlwt
import csv
from django.core import serializers
from .resources import PersonResource
from tablib import Dataset
from django.utils.datastructures import MultiValueDictKeyError
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from xml.etree import ElementTree as ET
from django.http import Http404
from itertools import chain
from django.db.models import Q


# Index page
# TODO which method needs to be suppoted GET pr POST or both ?
def index(request):
    if request.method != 'GET':
        raise Http404
    filtered_qs = PersonFilter(
        request.GET,
        queryset=Person.objects.all()
    )
    paginated_filtered_users = Paginator(filtered_qs.qs, 1)
    page_num = request.GET.get('page')
    user_page_obj = paginated_filtered_users.get_page(page_num)
    return render(request, 'users/index.html', {'filtered_qs': filtered_qs, 'user_page_obj': user_page_obj})


def search(request):
    if request.method != 'GET':
        raise Http404
    return render(request, 'users/search.html', {'filtered_qs': PersonFilter()})


def about(request):
    return render(request, 'users/about.html')


def export(request):
    return render(request, 'users/export-db.html')


def registeruser(request):
    if request.method != 'GET' and request.method != 'POST':
        # print(f'{request.method}')
        raise Http404
    if request.method == 'GET':
        return render(request, 'users/form.html')
    form = PersonForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, 'You are registred succeefully')
        return redirect('/')
    return render(request, 'users/form.html', {'form': form})


def edituser(request, id):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    person = None
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cette utilisateur n'existe pas"})

    if request.method == 'GET':
        return render(request, 'users/edit.html', {'user': person})
    else:
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.info(
                request, 'Vous avez Modifier un utilisateur avec succés')
            return redirect('/')
            # {% for key, value in form.errors.items %}
        return render(request, 'users/edit.html', {'user': person})


def deleteuser(request, id):
    if request.method != 'POST' and request.method != 'GET':
        raise Http404
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cette utilisateur n'existe pas"})
    if request.method == 'POST':
        person.delete()
        messages.error(
            request, 'Vous avez Supprimer un utilisateur avec succés')
        return redirect('/')
    else:
        context = {
            'user': person
        }
    return render(request, 'users/delete.html', context)


def export_excel(request):
    # tellin browser how to handle file ( as excel )
    response = HttpResponse(content_type='application/ms-excel')
    # adding to file name
    response['Content-Disposition'] = 'attachement; filename=Users' + \
        str(datetime.now())+'.xls'
    # creating work book
    wb = xlwt.Workbook(encoding='utf-8')
    # work sheet name
    ws = wb.add_sheet('Worksheet')
    # define row number
    row_num = 0
    font_style = xlwt.XFStyle()
    # making first row bold
    font_style.font.bold = True

    columns = ['Id', 'Nom', 'Prenom', 'Email', 'Ville']

    # inserting columns in the rows
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Person.objects.filter().values_list(
        'id', 'name', 'prenom', 'email', 'city')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Id', 'Nom', 'Prenom', 'Email', 'ville'])
    for person in Person.objects.all().values_list('id', 'name', 'prenom', 'email', 'city'):
        writer.writerow(person)

    response['Content-Disposition'] = 'attachement; filename="users.csv"'
    return response


def export_xml(request):
    response = HttpResponse(content_type='application/xml')
    person = Person.objects.all()
    person = serializers.serialize('xml', person)
    response['Content-Disposition'] = 'attachement; filename="users.xml"'

    return HttpResponse(person, response)


def import_db(request):
    return render(request, 'users/import-db.html')


def Parse_xl(request, format=None):
    try:
        excel_file = request.FILES['myfile']
    except MultiValueDictKeyError:
        messages.error(request, 'Votre Upload a mal tourné')
        return render(request, 'users/importdb.html')
    if (str(excel_file).split('.')[-1] == "xls"):
        data = xls_get(excel_file, column_limit=5)
    elif (str(excel_file).split('.')[-1] == "xlsx"):
        data = xlsx_get(excel_file, column_limit=5)
    else:
        messages.info(request, 'Veuillez importer un fichier de type Excel')
        return render(request, 'users/importdb.html')
    Clients = data["Worksheet"]
    if (len(Clients) > 1):
        for Worksheet in Clients:
            if (len(Worksheet) > 0):
                if (Worksheet[0] != "id"):
                    if (len(Worksheet) < 5):
                        i = len(Worksheet)
                        while (i < 5):
                            Worksheet.append("")
                            i += 1
                    c = Person.objects.filter(name=Worksheet[1])
                    if (c.count() == 0):
                        Person.objects.create(
                            name=Worksheet[1],
                            prenom=Worksheet[2],
                            email=Worksheet[3],
                            city=Worksheet[4]
                        )
    messages.success(request, 'Votre base de donnée a bien été Sauvegardé!')
    return render(request, 'users/import-db.html')


def Parse_txt(request, format=None):
    Clients_all = Person.objects.all()
    try:
        txt_file = request.FILES['file_txt']
    except MultiValueDictKeyError:
        messages.error(request, 'Votre Upload a mal tourné')
        return render(request, 'users/import-db.html')
    if (str(request.FILES['file_txt']).split('.')[-1] == "txt"):
        lines = txt_file.readlines()
        glines = (line.strip() for line in lines)
        for line in glines:
            fields = line.split(";".encode())
            try:
                valid = validate_email(fields[4].decode())
            except EmailNotValidError:
                messages.error(request, 'Cet email est pas valide!')
                continue
            Person.objects.create(
                name=fields[1].decode(),
                prenom=fields[2].decode(),
                email=valid.email,
                city=fields[3].decode()
            )
        messages.success(
            request, 'Votre base de donnée a bien été Sauvegardé!')
        return render(request, 'users/import-db.html')

    else:
        messages.info(request, 'Veuillez importer un fichier de type Text')
        return render(request, 'users/import-db.html')


def Parse_xml(request):
    try:
        file_xml = request.FILES['xml_file']
    except MultiValueDictKeyError:
        messages.error(request, 'Votre Upload a mal tourné')
        return render(request, 'users/import-db.html')

    if (str(request.FILES['xml_file']).split('.')[-1] == "xml"):
        doc = ET.parse(request.FILES['xml_file'])
        myroot = doc.getroot()
        for recorde in myroot.findall('object'):
            # try:
            #     valid = validate_email(recorde.find("field[@name='email']").text)
            # except EmailNotValidError:
            #     messages.error(request, 'Cet email est pas valide!')
            #     continue
            Person.objects.create(
                name=recorde.find("field[@name='name']").text,
                prenom=recorde.find("field[@name='prenom']").text,
                city=recorde.find("field[@name='city']").text,
                # email=valid.email
                email=recorde.find("field[@name='email']").text
            )
        messages.success(
            request, 'Votre base de donnée a bien été Sauvegardé!!!')
        return render(request, 'users/import-db.html')
    else:
        messages.info(request, 'Veuillez importer un fichier de type XML')
        return render(request, 'users/import-db.html')


def display(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    results = []

    if request.method == 'POST':
        scheme = request.POST.get('arg_lverb', -1)
        racines = request.POST.get('arg_lverb_racines', -1)
        results = Verbe.objects.filter(
            scheme_ver__id_sch=scheme, racine_ver__id_rac=racines)

    context = {
        'ver_filter': '',
        'verb_obj': results,
        'nom_filter': '',
        'nom_obj': '',
        'list_verbs_scheme': Scheme.objects.filter(type_scheme=1),
        'list_names_scheme': Scheme.objects.filter(type_scheme=2),
        'list_verbs_racine': Racine.objects.all()
    }
    return render(request, 'users/display.html', context)


def arabedic(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    lverbs = Verbe.objects.all()
    lnoms = Nom.objects.all()

    mylist = chain(lverbs, lnoms)

    paginated_lmots = Paginator(list(mylist), 1)
    page_num = request.GET.get('page')
    lmots_obj = paginated_lmots.get_page(page_num)

    context = {
        'lmots_obj': lmots_obj
    }
    return render(request, 'users/dict-arabe.html', context)


def racines(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    if request.method == 'POST':

        type = request.POST.get('type_rac', -1)
        racine = request.POST.get('rac', -1)
        # id_r = request.POST.get('id_rac', -1)
        if not type:
            messages.error(request, "donner le type")
        racines = Racine.objects.filter(Q(type_rac__iexact=type), Q(
            rac__icontains=racine)).order_by('id_rac')

    if request.method == 'GET':
        racines = Racine.objects.all()

    paginated_racines = Paginator(racines, 1)
    page_num = request.GET.get('page')
    racines = paginated_racines.get_page(page_num)
    context = {
        'racines': racines
    }

    return render(request, 'users/racine.html', context)


def racine_search(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    return render(request, 'users/search_rac.html')


def scheme(request):
    if request.method != 'GET':
        raise Http404

    schemes = Scheme.objects.all()
    paginated_schemes = Paginator(schemes, 1)
    page_num = request.GET.get('page')
    schemes = paginated_schemes.get_page(page_num)

    return render(request, 'users/scheme.html', {'schemes': schemes})


def scheme_search(request, id_sch):
    if request.method != 'GET':
        raise Http404
    try:
        scheme = Scheme.objects.get(id_sch=id_sch)
    except Scheme.DoesNotExist:
        messages.error("on a pas trouvée ce scheme")
    context = {
        'scheme': scheme
    }
    return render(request, 'users/search_sch.html', context)

# 3
# Ajout works for everything pretty sure


def ajouter_racine(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    if request.method == 'GET':
        return render(request, 'users/ajouter-racine.html')
    if request.method == 'POST':
        racine_rac = request.POST.get('racine_rac')
        type = request.POST.get('racine_type_rac')
        classe = request.POST.get('racine_classe')

        if not type:
            messages.warning(request, "le type est obligatoire")
            if not racine_rac and not classe:
                messages.warning(request, "donner des valeurs")

        else:
            racine = Racine(rac=racine_rac, type_rac=type, classe_rac=classe)
            racine.save()
            messages.success(
                request, "vous avez ajouter un racine avec succes")
            return render(request, 'users/racine.html')
    return redirect('/')


def ajouter_scheme(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'GET':
        # schemes = Scheme.objects.all()

        nombres = Scheme._meta.get_field('nombre').choices
        units = Scheme._meta.get_field('unit').choices
        oras = Scheme._meta.get_field('ora').choices
        conjs = Scheme._meta.get_field('conj').choices

        context = {
            'nombres': nombres,
            'units': units,
            'oras': oras,
            'conjs': conjs
        }
        return render(request, 'users/ajouter-scheme.html', context)

    if request.method == 'POST':

        scheme = Scheme(scheme=request.POST.get('scheme_sch'), sch_cons=request.POST.get('sch_cons'), sch_voy=request.POST.get('sch_voy'), nombre=request.POST.get('nb_choice'), unit=request.POST.get(
            'unit_choice'), ora=request.POST.get('ora_choice'), conj=request.POST.get('conj_choice'), type_scheme=request.POST.get('type'), classe_sch=request.POST.get('classe'))
        scheme.save()
        messages.success(request, "Vous avez ajouter un scheme avec succes")
        return redirect('/')


def ajouter_verb(request, id_m):

    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'GET':

        context = {
            'list_verbs_scheme': Scheme.objects.all(),
            'list_nom_scheme': Scheme.objects.all(),
            'list_racines': Racine.objects.all()
        }

        return render(request, 'users/ajouter-mot.html', context)
    if request.method == 'POST':
        if id_m == 1:
            scheme_v = request.POST.get('arg_schverb')
            racine_v = request.POST.get('arg_racverb')
            verb = Verbe(verbe=request.POST.get('ver'), ver_cons=request.POST.get('ver_c'),
                         ver_voy=request.POST.get('ver_v'), scheme_ver=Scheme.objects.get(id_sch=scheme_v), racine_ver=Racine.objects.get(id_rac=racine_v))
            verb.save()
            messages.success(request, "Vous avez ajouter un verbe avec succes")

        elif id_m == 2:
            nom = Nom(nom=request.POST.GET('nom'), nom_cons=request.POST.GET('nom_c'),
                      nom_voy=request.POST.GET('nom_v'), scheme_nom=request.POST.GET('arg_schnom'),
                      racine_nom=request.POST.GET('arg_racnom'))
            nom.save()
            messages.success(request, "Vous avez ajouter un nom avec succes")
