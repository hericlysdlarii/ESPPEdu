from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.contrib import messages
from dal import autocomplete
from .models import (
    User)
from .forms import (
    UpdateUserForm,
    UserCreationForm)

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

@method_decorator(login_required, name='dispatch')
class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('core:index')

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('core:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)


class CreateUser(CreateView):
    model = User
    template_name = 'accounts/add.html'
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object=None
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        self.object.is_superuser = False
        self.object.save()
        
        return HttpResponseRedirect(reverse('accounts:list_user'))


@method_decorator(login_required, name='dispatch')
class CreateUserAdmin(CreateView):
    model = User
    template_name = 'accounts/add-superuser.html'
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object=None
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        self.object.is_superuser = True
        self.object.save()
        
        return HttpResponseRedirect(reverse('accounts:list_user_admin'))


@method_decorator(login_required, name='dispatch')
class ListUserAdmin(ListView):
    """
    ClassView para listagem dos Usuários
    """
    model = User
    http_method_names = ['get']
    template_name = 'accounts/list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.queryset = User.objects.filter(is_superuser=True)
        
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(name__icontains = self.request.GET['search_box'])
        
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListUserAdmin, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context['page_obj'].number
        num_pages = context['paginator'].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= num_pages]
        context.update({
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': num_pages not in page_numbers,
            })
        return context


@method_decorator(login_required, name='dispatch')
class ListUser(ListView):
    """
    ClassView para listagem dos Usuários
    """
    model = User
    http_method_names = ['get']
    template_name = 'accounts/list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.queryset = User.objects.filter(is_superuser=False)
        
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(name__icontains = self.request.GET['search_box'])
        
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListUser, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context['page_obj'].number
        num_pages = context['paginator'].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= num_pages]
        context.update({
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': num_pages not in page_numbers,
            })
        return context


@method_decorator(login_required, name='dispatch')
class EditUser(UpdateView):
    """
    ClassView para edição de Usuário
    """
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/add.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('accounts:list_user'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def user_delete(request, pk):
    """
    View para exclusão de um Usuário
    """
    if request.user.is_superuser:
        user= get_object_or_404(User, pk=pk)
        user.delete()
        return JsonResponse({'msg': "Avaliação excluida com sucesso!", 'code': "1"})


# # Autocomplete Specialty
# @method_decorator(login_required, name='dispatch')
# class SpecialtyAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !

#         qs = Specialty.objects.all()

#         if self.q:
#             qs = qs.filter(description__icontains=self.q)

#         return qs

# @method_decorator(login_required, name='dispatch')
# class ListSpecialtyView(ListView):
#     model = Specialty
#     template_name = 'specialty/list.html'
#     http_method_names = ['get']
#     # muda o nome do product_list gerado por padrao pela classe
#     context_object_name = 'object_list'
#     paginate_by = 25

#     def get_queryset(self):
#         self.queryset = super(ListSpecialtyView, self).get_queryset()
#         if self.request.GET.get('search_box', False) :
#             self.queryset = self.queryset.filter(description__icontains = self.request.GET['search_box'])
#         return self.queryset

#     def get_context_data(self, **kwargs):
#         _super = super(ListSpecialtyView, self)
#         context = _super.get_context_data(**kwargs)
#         adjacent_pages = 3
#         page_number = context['page_obj'].number
#         num_pages = context['paginator'].num_pages
#         startPage = max(page_number - adjacent_pages, 1)
#         if startPage <= 5:
#             startPage = 1
#         endPage = page_number + adjacent_pages + 1
#         if endPage >= num_pages - 1:
#             endPage = num_pages + 1
#         page_numbers = [n for n in range(startPage, endPage) \
#                         if n > 0 and n <= num_pages]

#         context.update({
#             'page_numbers': page_numbers,
#             'show_first': 1 not in page_numbers,
#             'show_last': num_pages not in page_numbers,
#             })
#         return context

# @method_decorator(login_required, name='dispatch')
# class CreateSpecialtyView(CreateView):
#     model = Specialty
#     template_name = 'specialty/add.html'
#     form_class = SpecialtyForm

# @method_decorator(login_required, name='dispatch')
# class UpdateSpecialtyView(UpdateView):
#     model = Specialty
#     template_name = 'specialty/add.html'
#     form_class = SpecialtyForm

# @method_decorator(login_required, name='dispatch')
# class DetailSpecialtyView(DetailView):
#     model = Specialty
#     template_name = 'specialty/details.html'


# # specialty DELETE JSON
# @login_required
# def delete_specialty(request, pk):
#     specialty = get_object_or_404(Specialty, pk=pk)
#     specialty.delete()
#     return JsonResponse({'msg': "Especialidade excluida com sucesso!", 'code': "1"})
