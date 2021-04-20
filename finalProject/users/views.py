

from datetime import datetime
from .forms import userForm
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, response
from .models import Users
from django.core.paginator import Paginator
from django.contrib import messages
from .filters import userFilter
from email_validator import validate_email, EmailNotValidError
import xlwt
import csv
from django.core import serializers
import xml

# Create your views here.


def index(request):

    users = Users.objects.all()
    #search users
    myFilter = userFilter(request.GET, queryset=users)
    users = myFilter.qs
    #pagination
    paginator = Paginator(users, 1)
    # the ('',1) sets the page number to 1 if the page number isnt available
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)
    context = {
        'users': users,
        'myFilter': myFilter,
        'paginator': paginator,
        #converting page to an integer so we can compare the ' i '(which is an integer) 
        #compare the 'i' with page in index.html to highlight the page number we are in
        'page' : int(page)
    }
    return render(request, 'users/index.html', context)


def details(request, id):
    user = Users.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'users/details.html', context)

def about(request):
    return render(request, 'users/about.html')

def export(request):
    return render(request, 'users/exportdb.html')

def registerUser(request):
    if request.method == 'POST':
        user = Users(
        name=request.POST['name'], prenom=request.POST['prenom'] ,email=request.POST['email'], city=request.POST['city'])
        try:
             user.email = validate_email(request.POST.get('email'))
             user.email=request.POST.get('email')
             user.save()
             messages.success(request,'Vous avez Ajouter un utilisateur avec succés')
             return redirect('/')
        except EmailNotValidError:
            messages.error(request, 'email est pas valide')
            return render(request, 'users/form.html')     
    else:
        return render(request, 'users/form.html')

def editUser(request, id):
     user = Users.objects.get(id=id)
     form = userForm(request.POST,instance=user)
     if form.is_valid():
         form.save()
         messages.success(request,'Vous avez Modifier un utilisateur avec succés')
         return redirect('/')
     context = {
         'user' : user
     }      
     return render(request, 'users/edit.html', context)   


def deleteUser(request, id):
    user = Users.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request,'Vous avez Supprimer un utilisateur avec succés')
        return redirect('/')
    context = {
        'user' : user
    }
    return render(request, 'users/delete.html', context)  


def export_excel(request):
    #tellin browser how to handle file ( as excel )
    response=HttpResponse(content_type='application/ms-excel')
    #adding to file name
    response['Content-Disposition']='attachement; filename=Users'+ \
         str(datetime.now())+'.xls'
    #creating work book
    wb=xlwt.Workbook(encoding='utf-8')
    #work sheet name
    ws=wb.add_sheet('Users')
    #define row number
    row_num= 0
    font_style=xlwt.XFStyle()
    #making first row bold
    font_style.font.bold= True

    columns=['Nom', 'Prenom', 'Email', 'Ville']

    #inserting columns in the rows
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style= xlwt.XFStyle()

    rows=Users.objects.filter().values_list('name', 'prenom','email','city')

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prenom', 'Email', 'ville'])
    #loopin through data and foreach one writing it 
    
    for user in Users.objects.all().values_list('name','prenom','email','city'):
        writer.writerow(user)

    response['Content-Disposition'] = 'attachement; filename="users.csv"'
    return response


def export_xml(request):
    response = HttpResponse(content_type='application/xml')
    user = Users.objects.all()
    user = serializers.serialize('xml', user)
    response['Content-Disposition'] = 'attachement; filename="users.xml"'

    return HttpResponse(user, response )



 





          



