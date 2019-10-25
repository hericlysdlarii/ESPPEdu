from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from .forms import ArtigoForm
from .models import Artigo

# D'Lariinhoo

from django.contrib.auth import login, authenticate
from .forms import SignUpForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string

#--------------------------------
variavel = None

def retorna():
    return variavel

def home(request):
    variavel = request.user
    print("Variavel do usuario", variavel)
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

@login_required
def artigos_lista(request):
    artigos = Artigo.objects.all()
    return render(request,'artigo_lista.html',{
        'artigos': artigos
    })

@login_required
def artigos_upload(request):
    if request.method == 'POST':
        print ("POst ",request.POST, "FILES ", request.FILES)
        form = ArtigoForm(request.POST, request.FILES)
       
        if form.is_valid():
            form.autor = variavel
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

################################### LOGIN ############################################# 

def activation_sent_view(request):
    return render(request, 'activation/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation/activation_invalid.html')

def retorna_usuario_autenticado():
    return variavel

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('activation/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

#################################################################################################
