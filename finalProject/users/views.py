from datetime import datetime
from django.contrib.messages.api import error
from django.db.models.query import QuerySet
from .forms import PersonForm
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, response
from .models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import django_filters
from .filters import PersonFilter
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


def details(request, id):
    if request.method != 'GET':
        raise Http404
    person = None
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "The person does not exist"})
    context = {
        'person': person
    }
    return render(request, 'users/details.html', context)


def about(request):
    return render(request, 'users/about.html')


def export(request):
    return render(request, 'users/export-db.html')


def registerUser(request):
    if request.method !='GET' and request.method !='POST':
        # print(f'{request.method}')
        raise Http404
    if request.method =='GET':
        return render(request, 'users/form.html')
    form = PersonForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, 'You are registred succeefully')
        return redirect('/')
    return render(request, 'users/form.html',{'form':form})


def editUser(request, id):
    if request.method !='GET' and request.method !='POST':
        raise Http404
    person = None
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "The person does not exist"})

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


def deleteUser(request, id):
    if request.method !='GET':
        raise Http404
    person = None
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return render(request, '/', {'error',  "The person does not exist"})
    print(person.id)
    person.delete()
    messages.info(request, 'Vous avez Supprimer un utilisateur avec succés')
    return redirect('/')


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
    # loopin through data and foreach one writing it
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


def import_(request):
    return render(request, 'users/importdb.html')


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
    if (len(Clients) > 1):  # We have company data
        for Worksheet in Clients:
            if (len(Worksheet) > 0):  # The row is not blank
                if (Worksheet[0] != "id"):  # This is not header
                    # Fill ending columns with blank
                    if (len(Worksheet) < 5):
                        i = len(Worksheet)
                        while (i < 5):
                            Worksheet.append("")
                            i += 1
                            # Check if Client exist
                            # Assume that Client name is unique
                    c = Person.objects.filter(name=Worksheet[1])
                    if (c.count() == 0):
                        Person.objects.create(
                            name=Worksheet[1],
                            prenom=Worksheet[2],
                            email=Worksheet[4],
                            city=Worksheet[3]
                        )
    messages.success(request, 'Votre base de donnée a bien été Sauvegardé!')
    return render(request, 'users/importdb.html')


def Parse_txt(request, format=None):
    Clients_all = Person.objects.all()
    try:
        txt_file = request.FILES['file_txt']
    except MultiValueDictKeyError:
        messages.error(request, 'Votre Upload a mal tourné')
        return render(request, 'users/importdb.html')
    if (str(request.FILES['file_txt']).split('.')[-1] == "txt"):
        # lines = f.readlines()
        # with open("txt_file", "r") as fileopened:
        lines = txt_file.readlines()
        glines = (line.strip() for line in lines)
        for line in glines:
            fields = line.split(";".encode())
            Person.objects.create(
                name=fields[1].decode(),
                prenom=fields[2].decode(),
                email=fields[3].decode(),
                city=fields[4].decode()
            )
        messages.success(
            request, 'Votre base de donnée a bien été Sauvegardé!')
        return render(request, 'users/importdb.html')

    else:
        messages.info(request, 'Veuillez importer un fichier de type Text')
        return render(request, 'users/importdb.html')


def Parse_xml(request):
    try:
        file_xml = request.FILES['xml_file']
    except MultiValueDictKeyError:
        messages.error(request, 'Votre Upload a mal tourné')
        return render(request, 'users/importdb.html')

    if (str(request.FILES['xml_file']).split('.')[-1] == "xml"):
        doc = ET.parse(request.FILES['xml_file'])
        # records=doc.getElementsByTagName("record")
        myroot = doc.getroot()
        for recorde in myroot.findall('record'):
            Person.objects.create(
                name=recorde.find('nom').text,
                prenom=recorde.find('prenom').text,
                city=recorde.find('ville').text,
                email=recorde.find('email').text
            )
        messages.success(
            request, 'Votre base de donnée a bien été Sauvegardé!!!')
        return render(request, 'users/importdb.html')
    else:
        messages.info(request, 'Veuillez importer un fichier de type XML')
        return render(request, 'users/importdb.html')
