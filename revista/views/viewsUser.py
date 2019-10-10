from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 

def createUser(request):
    if request.method == 'POST':
        formUser = UserCreationForm(request.POST)
        if formUser.is_valid():
            formUser.save()
            return redirect('home')
    else:
        formUser = UserCreationForm()
    return render(request, 'users/formUser.html', {'formUser': formUser})

def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'As credenciais do usuário estão incorretas')
            return redirect('loginUser')
    else:
        formLogin = AuthenticationForm()
    return render(request, 'users/login.html', {'formLogin': formLogin})

def logoutUser(request):
    logout(request)
    return redirect('loginUser')