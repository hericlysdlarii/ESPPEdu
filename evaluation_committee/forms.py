from django import forms
from dal import autocomplete
from accounts.models import User

from .models import *


class EvaluationCommitteeForm(forms.ModelForm):
    """
    Formulário para criação e edição do model EvaluationCommittee 
    """
    class Meta:
        model = EvaluationCommittee
        fields = '__all__'


class InterestAreaForm(forms.ModelForm):
    """
    Formulário para criação e edição do model InterestArea
    """
    class Meta:
        model = InterestArea
        fields = '__all__'


# class RatingCriteriaForm(forms.ModelForm):
#     """
#     Formulário para criação e edição do model RatingCriteria
#     """
#     class Meta:
#         model = RatingCriteria
#         exclude = ('weight',)


class UserWorkForm(forms.Form):
    """
    Formulário para criação e edição do model UserWork
    """
    name = forms.CharField()
    email = forms.EmailField()
    is_coordinator = forms.BooleanField(required=False)
        

class WorkForm(forms.ModelForm):
    """
    Formulário para criação e edição do model Work
    """
    interest_area = forms.ModelChoiceField(
		required=True,
		queryset = InterestArea.objects.all(),
		label = "Área de Interesse",
		widget = autocomplete.ModelSelect2(url='evaluation_committee:interest_area_autocomplete',attrs={'style': 'height: auto'})
	)
    class Meta:
        model = Work
        exclude = ('submission_user',)


# Formset para adicionar os autores do trabalho
UserWorkFormSet = forms.formset_factory(UserWorkForm)


class EvaluationForm(forms.ModelForm):
    """
    Formulário para criação e edição do model Evaluation
    """
    work = forms.ModelChoiceField(
		required=True,
		queryset = Work.objects.all(),
		label = "Trabalho",
		widget = autocomplete.ModelSelect2(url='evaluation_committee:work_autocomplete',attrs={'style': 'height: auto'})
	)
    corrector = forms.ModelChoiceField(
		required=True,
		queryset = User.objects.all(),
		label = "Corretor",
		widget = autocomplete.ModelSelect2(url='evaluation_committee:corrector_autocomplete',attrs={'style': 'height: auto'})
	)
    class Meta:
        model = Evaluation
        fields = ['work', 'corrector', 'observation',]


# class EvaluationRatingCriteriaForm(forms.ModelForm):
#     """
#     Formulário para criação e edição do model Evaluation Rating Criteria
#     """
#     value = forms.DecimalField(max_value=10.00)
#     class Meta:
#         model = EvaluationRatingCriteria
#         fields = ['criteria','value',]
#         # widgets = {'criteria':autocomplete.ModelSelect2(url='evaluation_committee:criteria_autocomplete',attrs={'style': 'height: auto'})}


# # Formset para adicionar os autores do trabalho
# EvaluationRatingCriteriaFormSet = forms.inlineformset_factory(
#     Evaluation, EvaluationRatingCriteria, form=EvaluationRatingCriteriaForm)


class UserCommitteeForm(forms.ModelForm):
    """
    Formulário para criação e edição do model Work
    """
    user = forms.ModelChoiceField(queryset=User.objects.all(),to_field_name='username',widget=forms.TextInput())
    class Meta:
        model = UserCommittee
        fields = ['user', 'interest_area']
        # widgets = {'user': forms.TextInput()}

    def __init__(self,data=None,*args,**kwargs):
        super().__init__(data=data,*args,**kwargs)
        if 'user' in self.initial:
            self.initial['user']=User.objects.get(pk=self.initial['user']).username

# Formset para adicionar os autores do trabalho
UserCommitteFormSet = forms.inlineformset_factory(EvaluationCommittee,UserCommittee,form=UserCommitteeForm, extra=1)
