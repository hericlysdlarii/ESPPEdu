from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from dal import autocomplete
from pycpfcnpj import cpfcnpj
from django.contrib.auth import get_user_model

from .models import User


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'name', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff']


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'email']



class PasswordResetForm(PasswordResetForm):
    def clean_email(self):
        amount = get_user_model()._default_manager.filter(
            email__iexact=self.cleaned_data.get('email'), is_active=True).count()
        if(amount < 1):
            raise forms.ValidationError('Lamentamos, mas não reconhecemos esse endereço de e-mail.')
        return self.cleaned_data.get('email')


class UserCreationForm(UserCreationForm):
    """
    Formulário para criaçao de usuário.
    """
    username =  forms.CharField(initial='')
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'cpf', 'sex', 'phone', 'is_whatsapp']


class UpdateUserForm(forms.ModelForm):
    """
    Formulário para ediçaão de usuário.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'cpf', 'sex', 'phone', 'is_whatsapp']

