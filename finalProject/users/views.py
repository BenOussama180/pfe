

from .forms import userForm
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .models import Users
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.


def index(request):

    # show only first 10 users
    users = Users.objects.all()[:10]

    context = {
        'users': users
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
        name=request.POST['name'], email=request.POST['email'], city=request.POST['city'])
        user.save()
        messages.success(request,'Vous avez Ajouter un utilisateur avec succés')
        return redirect('/')
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
          



