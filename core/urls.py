# URL APP CORE

from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'), # Pagina inicial
    #path('ranking/', ranking, name='ranking'),
]
