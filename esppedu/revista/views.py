from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from .forms import ArtigoForm
from .models import Artigo

def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })

@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

# def artigos_lista(request):
#     artigos = Artigo.objects.all()
#     return render(request,'artigo_lista.html',{
#         'artigos': artigos
#     })


def listar_artigos(request):
    artigos = Artigo.objects.all()
    return render(request,'artigo_lista.html',{
        'artigos': artigos
    })

@login_required
def artigos_upload(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artigo_lista')
    else:
        form = ArtigoForm()
    return render(request,'artigo_upload.html', {
        'form':form
    })

@login_required
def artigos_delete(request, pk):
    if request.method == 'POST':
        artigo = Artigo.objects.get(pk=pk)
        artigo.delete()
    return redirect('artigo_lista')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('secret_page.html')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def secret_page(request):
    artigos = Artigo.objects.all()
    return render(request,'artigo_lista.html',{
        'artigos': artigos
    })


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'
