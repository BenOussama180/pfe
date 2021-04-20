

from .forms import userForm
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .models import Users
from django.core.paginator import Paginator
from django.contrib import messages
from .filters import userFilter
from email_validator import validate_email, EmailNotValidError


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
          



