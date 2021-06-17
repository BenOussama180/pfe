from datetime import datetime
import re
from django import http
from django.contrib.messages.api import error
from django.db.models.query import QuerySet, RawQuerySet
from django.template import context
from pyexcel_io.constants import SKIP_DATA
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
from django.http import HttpResponseRedirect


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


######################################################################################
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
    Racines = data["Worksheet"]
    if (len(Racines) > 1):
        for Worksheet in Racines:
            if (len(Worksheet) > 0):
                if (Worksheet[0] != "id"):
                    if (len(Worksheet) < 5):
                        i = len(Worksheet)
                        while (i < 5):
                            Worksheet.append("")
                            i += 1
                    c = Racine.objects.filter(rac=Worksheet[1])
                    bools = isinstance(Worksheet[2], (int, float))
                    if bools != True:
                        Worksheet[2] = 3
                    if (c.count() == 0):
                        Racine.objects.create(
                            rac=Worksheet[1],
                            type_rac=Worksheet[2],
                            classe_rac=Worksheet[3]
                        )
    messages.success(request, 'Votre base de donnée a bien été Sauvegardé!')
    return render(request, 'users/import-db.html')


def Parse_txt(request, format=None):
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
            Racine.objects.create(
                rac=fields[1].decode(),
                type_rac=fields[2].decode(),
                classe_rac=fields[3].decode()
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
            Racine.objects.create(
                rac=recorde.find("field[@name='rac']").text,
                type_rac=recorde.find("field[@name='type_rac']").text,
                classe_rac=recorde.find("field[@name='classe_rac']").text,
            )
        messages.success(
            request, 'Votre base de donnée a bien été Sauvegardé!!!')
        return render(request, 'users/import-db.html')
    else:
        messages.info(request, 'Veuillez importer un fichier de type XML')
        return render(request, 'users/import-db.html')
#######################################################################################
# def Parse_xl_scheme(request):
#     try:
#         excel_file = request.FILES['myfile_sch']
#     except MultiValueDictKeyError:
#         messages.error(request, 'Votre Upload a mal tourné')
#         return render(request, 'users/importdb.html')

#     if (str(excel_file).split('.')[-1] == "xls"):
#         data = xls_get(excel_file, column_limit=5)
#     elif (str(excel_file).split('.')[-1] == "xlsx"):
#         data = xlsx_get(excel_file, column_limit=5)
#     else:
#         messages.info(request, 'Veuillez importer un fichier de type Excel')
#         return render(request, 'users/importdb.html')
#     Racines = data["Worksheet"]
#     if (len(Racines) > 1):
#         for Worksheet in Racines:
#             if (len(Worksheet) > 0):
#                 if (Worksheet[0] != "id"):
#                     if (len(Worksheet) < 5):
#                         i = len(Worksheet)
#                         while (i < 5):
#                             Worksheet.append("")
#                             i += 1
#                     c = Racine.objects.filter(rac=Worksheet[1])
#                     bools = isinstance(Worksheet[2], (int, float))
#                     if bools != True:
#                         Worksheet[2] = 3
#                     if (c.count() == 0):
#                         Racine.objects.create(
#                             rac=Worksheet[1],
#                             type_rac=Worksheet[2],
#                             classe_rac=Worksheet[3]
#                         )
#     messages.success(request, 'Votre base de donnée a bien été Sauvegardé!')
#     return render(request, 'users/import-db.html')


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

###########################################################


def arabedic(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'POST':
        if not request.POST.get('mot_t'):
            messages.error(request, "Choisir Verbe/Nom: 'كلمة/فعل' ")
            return redirect(request.META.get('HTTP_REFERER', 'users/racine.html'))

        if request.POST.get('mot_t') == 'كلمة':
            nom_i = request.POST.get('mot')
            rac_nom_i = request.POST.get('rac_mot')
            sch_nom_i = request.POST.get('sch_mot')
            if not rac_nom_i or not sch_nom_i:
                messages.error(request, "Erreur d'insertion ")
                return redirect(request.META.get('HTTP_REFERER', 'users/racine.html'))

            noms = Nom.objects.filter(Q(nom__icontains=nom_i) | Q(
                scheme_nom__scheme__icontains=sch_nom_i), Q(racine_nom__rac__icontains=rac_nom_i))
            mylist = noms
            if not mylist:
                messages.warning(
                    request, "il y'a pas du nom avec ces caractéristique")
                return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))

        else:
            ver_i = request.POST.get('mot')
            rac_ver_i = request.POST.get('rac_mot')
            sch_ver_i = request.POST.get('sch_mot')
            verbs = Verbe.objects.filter(
                Q(verbe__icontains=ver_i) | Q(scheme_ver__scheme__icontains=sch_ver_i) | Q(racine_ver__rac__icontains=rac_ver_i))
            mylist = verbs
            if not mylist:
                messages.warning(
                    request, "il y'a pas du verbe avec ces caractéristique")
                return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))

    if request.method == 'GET':
        lverbs = Verbe.objects.all()
        lnoms = Nom.objects.all()
        mylist = chain(lverbs, lnoms)
        mylist = list(mylist)

    paginated_lmots = Paginator(mylist, 1)
    page_num = request.GET.get('page')
    lmots_obj = paginated_lmots.get_page(page_num)
    context = {
        'lmots_obj': lmots_obj
    }
    return render(request, 'users/dict-arabe.html', context)


def search_mot(request):
    if request.method != 'GET':
        raise Http404

    list_scheme = Scheme.objects.all()
    list_racine = Racine.objects.all()

    context = {

        'list_scheme': list_scheme,
        'list_racine': list_racine
    }
    return render(request, 'users/search-mot.html', context)
###############################


def racines(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'POST':

        type = request.POST.get('type_rac', -1)
        racine = request.POST.get('rac', -1)

        racines = Racine.objects.filter(Q(type_rac__iexact=type) | Q(
            rac__icontains=racine)).order_by('id_rac')
        if not racines:
            messages.warning(
                request, "il ya pas des racines avec ces caracteristique")
            return redirect(request.META.get('HTTP_REFERER', 'users/racine.html'))

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

####################################################


def scheme(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'GET':
        schemes = Scheme.objects.all()

    if request.method == 'POST':
        sch = request.POST.get('sch')
        type_sch = request.POST.get('type_scheme')
        # classe_sch = request.POST.get('classe_sch')
        nb = request.POST.get('nb')
        unit = request.POST.get('unit')
        ora = request.POST.get('ora')
        conj = request.POST.get('conj')
        typ = request.POST.get('typ')
        schemes = Scheme.objects.filter(Q(scheme__icontains=sch), Q(unit__icontains=unit) | Q(nombre__icontains=nb) | Q(
                                        ora__icontains=ora) | Q(conj__icontains=conj) | Q(typ__icontains=typ) | Q(type_scheme__iexact=type_sch)).order_by('id_sch')
        if not schemes:
            schemes = Scheme.objects.all()
            messages.error(
                request, "il y'a pas des schemes avec ces conditions")
            return render(request, 'users/scheme.html')
    paginated_schemes = Paginator(schemes, 1)
    page_num = request.GET.get('page')
    schemes = paginated_schemes.get_page(page_num)

    context = {
        'schemes': schemes,
    }
    return render(request, 'users/scheme.html', context)


def scheme_search(request, id_sch):
    if request.method != 'GET':
        raise Http404
    try:
        scheme = Scheme.objects.get(id_sch=id_sch)
    except Scheme.DoesNotExist:
        messages.error("on a pas trouvée ce scheme")

    nombres = Scheme._meta.get_field('nombre').choices
    units = Scheme._meta.get_field('unit').choices
    oras = Scheme._meta.get_field('ora').choices
    conjs = Scheme._meta.get_field('conj').choices
    typs = Scheme._meta.get_field('typ').choices

    context = {
        'scheme': scheme,
        'nombres': nombres,
        'units': units,
        'oras': oras,
        'conjs': conjs,
        'typs': typs
    }
    return render(request, 'users/search_sch.html', context)


def ajouter_racine(request):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    if request.method == 'GET':
        return render(request, 'users/ajouter-racine.html')
    if request.method == 'POST':
        racine_rac = request.POST.get('racine_rac')
        type = request.POST.get('racine_type_rac')
        classe = request.POST.get('racine_classe')

        if not type or not racine_rac or not classe:
            messages.error(request, "Erreur d'insertion")
            return redirect(request.META.get('HTTP_REFERER', 'users/racine.html'))

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
        typs = Scheme._meta.get_field('typ').choices

        context = {
            'nombres': nombres,
            'units': units,
            'oras': oras,
            'conjs': conjs,
            'typs': typs

        }
        return render(request, 'users/ajouter-scheme.html', context)

    if request.method == 'POST':
        scheme_i = request.POST.get('scheme_sch')
        nombre_i = request.POST.get('nb_choice')
        scheme_ti = request.POST.get('type')
        scheme_cli = request.POST.get('classe')
        if not scheme_cli:
            messages.warning(request, "La classe est obligatoire")
            return redirect(request.META.get('HTTP_REFERER', 'users/scheme.html'))

        if not scheme_ti:
            messages.warning(request, "Donner le type")
            return redirect(request.META.get('HTTP_REFERER', 'users/scheme.html'))

        if not scheme_i and not nombre_i and not scheme_cli and not scheme_cli:
            messages.error(request, "Erreur d'insertion")
            return redirect(request.META.get('HTTP_REFERER', 'users/scheme.html'))

        scheme = Scheme(scheme=request.POST.get('scheme_sch'), sch_cons=request.POST.get('sch_cons'), sch_voy=request.POST.get('sch_voy'), nombre=request.POST.get('nb_choice'), unit=request.POST.get(
            'unit_choice'), ora=request.POST.get('ora_choice'), conj=request.POST.get('conj_choice'), type_scheme=request.POST.get('type'), classe_sch=request.POST.get('classe'), typ=request.POST.get('typ_choice'))
        scheme.save()
        messages.success(request, "Vous avez ajouter un scheme avec succes")
        return redirect('/')


def ajouter_verb(request, id_m):

    if request.method != 'GET' and request.method != 'POST':
        raise Http404

    if request.method == 'POST':
        if id_m == 1:
            scheme_v = request.POST.get('arg_schverb')
            racine_v = request.POST.get('arg_racverb')
            verb_i = request.POST.get('ver')
            if not scheme_v or not racine_v or not verb_i:
                messages.error(request, "error d'insertion")
                return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))

            verb = Verbe(verbe=request.POST.get('ver'), ver_cons=request.POST.get('ver_c'),
                         ver_voy=request.POST.get('ver_v'), scheme_ver=Scheme.objects.get(id_sch=scheme_v), racine_ver=Racine.objects.get(id_rac=racine_v))
            verb.save()
            messages.success(request, "Vous avez ajouter un verbe avec succes")

        elif id_m == 2:
            scheme_n = request.POST.get('arg_schnom')
            racine_n = request.POST.get('arg_racnom')
            nom_i = request.POST.get('nom')
            if not scheme_n or not racine_n or not nom_i:
                messages.error(request, "error d'insertion:")
                return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))

            nom = Nom(nom=request.POST.get('nom'), nom_cons=request.POST.get('nom_c'),
                      nom_voy=request.POST.get('nom_v'), scheme_nom=Scheme.objects.get(id_sch=scheme_n),
                      racine_nom=Racine.objects.get(id_rac=racine_n))
            nom.save()
            messages.success(request, "Vous avez ajouter un nom avec succes")

    context = {
        'list_verbs_scheme': Scheme.objects.filter(type_scheme=1),
        'list_nom_scheme': Scheme.objects.filter(type_scheme=2),
        'list_racines': Racine.objects.all()
    }

    return render(request, 'users/ajouter-mot.html', context)

##########################################################


def edit_racine(request, id_rac):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    racine = None
    try:
        racine = Racine.objects.get(id_rac=id_rac)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cette utilisateur n'existe pas"})
    if request.method == 'GET':
        return render(request, 'users/edit-racine.html', {'racine': racine})
    if request.method == 'POST':
        racine.rac = request.POST['e_rac']
        racine.type_rac = request.POST['e_rac_t']
        racine.classe_rac = request.POST['e_rac_c']
        racine.save()
        messages.info(request, "Vous avez modifier avec succes")
        return render(request, 'users/edit-racine.html', {'racine': racine})


def edit_scheme(request, id_sch):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    try:
        scheme = Scheme.objects.get(id_sch=id_sch)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cette utilisateur n'existe pas"})
    if request.method == 'GET':
        nombres = Scheme._meta.get_field('nombre').choices
        units = Scheme._meta.get_field('unit').choices
        oras = Scheme._meta.get_field('ora').choices
        conjs = Scheme._meta.get_field('conj').choices
        typs = Scheme._meta.get_field('typ').choices
        context = {
            'scheme': scheme,
            'nombres': nombres,
            'units': units,
            'oras': oras,
            'conjs': conjs,
            'typs': typs,
        }
        return render(request, 'users/edit-scheme.html', context)

    if request.method == 'POST':

        scheme.scheme = request.POST['sch_e']
        scheme.type_scheme = request.POST['sch_t_e']
        scheme.classe_sch = request.POST['sch_c_e']
        scheme.nombre = request.POST['nb_choice_e']
        scheme.unit = request.POST['unit_choice_e']
        scheme.ora = request.POST['ora_choice_e']
        scheme.conj = request.POST['conj_choice_e']
        scheme.typ = request.POST['typ_choice_e']
        scheme.save()

        messages.info(request, "Vous avez modifier avec succes")

        nombres = Scheme._meta.get_field('nombre').choices
        units = Scheme._meta.get_field('unit').choices
        oras = Scheme._meta.get_field('ora').choices
        conjs = Scheme._meta.get_field('conj').choices
        typs = Scheme._meta.get_field('typ').choices
        context = {
            'nombres': nombres,
            'units': units,
            'oras': oras,
            'conjs': conjs,
            'typs': typs,
            'scheme': scheme
        }
        return render(request, 'users/edit-scheme.html', context)


def edit_verbe(request, id_ver):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    try:
        verb = Verbe.objects.get(id_ver=id_ver)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cet verbe n'existe pas"})

    if request.method == 'GET':
        context = {
            'verb': verb
        }
        return render(request, 'users/edit-verbe.html', context)
    if request.method == 'POST':
        scheme_v = request.POST.get('sch_ver_ed')
        racine_v = request.POST.get('rac_ver_ed')
        scheme_e = Scheme.objects.filter(scheme=scheme_v)
        racine_e = Racine.objects.filter(rac=racine_v)
        if not scheme_e or not racine_e:
            messages.error(
                request, "Vous ne pouvez pas utiliser ce schème ou racine (n'existe pas)")
            return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))
        verb.verbe = request.POST['v_ed']
        verb.ver_cons = request.POST['v_con_ed']
        verb.ver_voy = request.POST['v_voy_ed']
        verb.scheme_ver = scheme_e
        verb.racine_ver = racine_e
        verb.save()
        messages.success(request, "Vous avez modifier ce verbe avec succes")
        return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))


def edit_nom(request, id_nom):
    if request.method != 'GET' and request.method != 'POST':
        raise Http404
    try:
        nom = Nom.objects.get(id_nom=id_nom)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "Cet nom n'existe pas"})

    if request.method == 'GET':
        context = {
            'nom': nom
        }
        return render(request, 'users/edit-nom.html', context)

    if request.method == 'POST':
        scheme_n = request.POST['sch_nom_ed']
        racine_n = request.POST['rac_nom_ed']
        print('here again: ')
        print(scheme_n)
        print(racine_n)
        scheme_n_e = Scheme.objects.filter(scheme=scheme_n)
        racine_n_e = Racine.objects.filter(rac=racine_n)
        if not scheme_n_e or not racine_n_e:
            messages.error(
                request, "Vous ne pouvez pas utiliser ce schème ou racine (n'existe pas)")
            return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))

        nom.nom = request.POST['n_ed']
        nom.scheme_ver = scheme_n_e
        nom.racine_ver = racine_n_e
        nom.nom_cons = request.POST['n_con_ed']
        nom.nom_voy = request.POST['n_voy_ed']
        nom.save()
        messages.success(request, "Vous avez modifier ce nom avec succes")
        return redirect(request.META.get('HTTP_REFERER', 'users/dict-arabe.html'))
