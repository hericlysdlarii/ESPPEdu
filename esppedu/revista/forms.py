from django import forms
from .models import Artigo

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo 
        exclude = ('user', )
        fields = ('cod_artigo','titulo','resumo', 'palavras_chaves', 'area','pdf')

       