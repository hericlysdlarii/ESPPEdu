from django import forms
from .models import Artigo





# D'Lariinhoo mexendo aqui

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#--------------------------------------------------
#teste = User.get_username()
class ArtigoForm(forms.ModelForm):
    #Não mexa aqui
    ##autor = forms.CharField(max_length=4, disabled=True, initial=teste)
    class Meta:
        model = Artigo 
        fields = ('autor','cod_artigo','titulo','resumo', 'palavras_chaves', 'area','pdf')





class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

