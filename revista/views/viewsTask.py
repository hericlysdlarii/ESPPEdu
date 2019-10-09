from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from ..entidades.task import task
from ..forms import taskform
from ..services import task_service

@login_required()
def home(request):
    return render(request, 'user/home.html')

@login_required()
def createTask(request):
    if request.method == 'POST':
        formTask = taskform(request.POST)
        if formTask.is_valid():
            name = formTask.cleaned_data["name"]
            about = formTask.cleaned_data["about"]
            date = formTask.cleaned_data["date"]
            priority = formTask.cleaned_data["priority"]
            newTask = task(name=name, about=about, date=date,
                           priority=priority, user=request.user)
            task_service.createTask(newTask)
            return redirect('home')
    else:
        formTask = taskform()
    return render(request, 'user/formTask.html', {'formTask': formTask})

@login_required()
def listTask(request):
    tasks = task_service.listTask(request.user)
    return render(request, 'user/listTask.html', {'tasks': tasks})

@login_required()
def updateTask(request, id):
    taskDB = task_service.listTaskID(id)
    if taskDB.user != request.user:
        return HttpResponse("Não permitido")
    formTask = taskform(request.POST or None, instance=taskDB)
    if formTask.is_valid():
        name = formTask.cleaned_data["name"]
        about = formTask.cleaned_data["about"]
        date = formTask.cleaned_data["date"]
        priority = formTask.cleaned_data["priority"]
        newTask = task(name=name, about=about, date=date,
                       priority=priority, user=request.user)
        task_service.updateTask(taskDB, newTask)
        return redirect('home')
    return render(request, 'user/formTask.html', {'formTask': formTask})

@login_required()
def removeTask(request, id):
    taskDB = task_service.listTaskID(id)
    if request.method == 'POST':
        task_service.removeTask(taskDB)
        return redirect('home')
    return render(request, 'user/deleteTask.html', {'task': taskDB})
