from django.urls import path
from .views import *

app_name = "website"

urlpatterns = [
    path('', home, name='home'), # Pagina inicial
    #path('programacoes/', schedule, name='schedule'), # Programações
    path('ajuda/', ajuda, name='ajuda'), # Normas
    #path('inscricao/', ParticipantsCreate.as_view(), name='inscricao'), # Inscricao
    path('resultado_submissoes/', submission_result, name='submission_result'), # resultado sumissoes
]
