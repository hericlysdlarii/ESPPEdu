from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from accounts.models import User
from accounts.forms import UserAdminCreationForm, UserCreationForm
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError, transaction
#from editions.models import Edition , Inscription
from datetime import datetime , date
from evaluation_committee.models import *
#from editions.models import *

# Página inicial
def home(request):
  return render(request, 'website/index.html')

# Programações
def schedule(request):
  return render(request, 'website/schedule.html')

# Normas
def standards(request):
  return render(request, 'website/standards.html')

# resultado das submissoes
# def submission_result(request):

#   picos = []
#   parnaiba = []
#   floriano = []
#   teresina = []
#   bj = []

#   # i_picos = Inscription.objects.filter(campus=4)
#   # i_parnaiba = Inscription.objects.filter(campus=1)
#   # i_floriano = Inscription.objects.filter(campus=5)
#   # i_teresina = Inscription.objects.filter(campus=2)
#   # i_bj = Inscription.objects.filter(campus=3)


#   trabalhos = Evaluation.objects.all()

#   for i in i_picos:
#     evt =  Evaluation.objects.filter(work__submission_user=i.user)
#     if evt:
#       for user in evt:
#         if user.average >=7:
#           picos.append(user.work.title)
  

#   for i in i_parnaiba:
#     evt =  Evaluation.objects.filter(work__submission_user=i.user)
#     if evt:
#       for user in evt:
#         if user.average >=7:
#           parnaiba.append(user.work.title)


#   for i in i_floriano:
#     evt =  Evaluation.objects.filter(work__submission_user=i.user)
#     if evt:
#       for user in evt:
#         if user.average >=7:
#           floriano.append(user.work.title)

#   for i in i_teresina:
#     evt =  Evaluation.objects.filter(work__submission_user=i.user)
#     if evt:
#       for user in evt:
#         if user.average >=7:
#           teresina.append(user.work.title)

#   for i in i_bj:
#     evt =  Evaluation.objects.filter(work__submission_user=i.user)
#     if evt:
#       for user in evt:
#         if user.average >=7:
#           bj.append(user.work.title)

#   contexto = {
#       'picos': picos,
#       'teresina': teresina,
#       'parnaiba': parnaiba,
#       'bomjesus': bj,
#       'floriano': floriano
#   }


#   return render(request, 'website/submission_result.html',contexto)

#Inscrição
# class ParticipantsCreate(CreateView):
#   model = User
#   template_name = 'website/inscricao.html'
#   form_class = UserCreationForm

#   def form_valid(self, form):
#       try:
#           with transaction.atomic():
#               participant = form.save()

#               messages.success(self.request, 'Participante cadastrado com sucesso.')

#       except IntegrityError: #If the transaction failed
#           messages.error(
#               self.request, 'Ocorreu um erro ao salvar o participante.')

#       return HttpResponseRedirect(self.get_success_url())

#   def form_invalid(self, form):
#       return self.render_to_response(
#           self.get_context_data(
#                   form=form,
#               )
#           )
#   def get_success_url(self):
#       return reverse('accounts:login')
