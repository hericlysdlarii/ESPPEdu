from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.contrib import messages
from dal import autocomplete
from .models import *
#from editions.models import *
from django.contrib.auth.decorators import login_required
from .forms import*
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# def ajuda(request):
#     # mostrar os trabalhos de determinado campus e area de intersse que não foram avaliados
    
#     # i = Inscription.objects.filter(campus__name='Teresina')
#     # users = [x.user for x in i]
#     # interest_area = InterestArea.objects.get(name='Ensino de Ciências')
#     # works_users = UserWork.objects.filter(user__in=users, work__interest_area=interest_area)

#     # works = [x.work for x in works_users]

#     # for w in works:
#     #     if not Evaluation.objects.filter(work=w).exists():
#     #         print("======", w)

#     # mostrar trabalhos repetidos de determinado campus

#     i = Inscription.objects.filter(campus__name='Teresina')
#     users = [x.user for x in i]
#     works_users = UserWork.objects.filter(user__in=users)

#     works = [x.work for x in works_users]

#     trabalhos = []

#     for w in works:
#         if w in trabalhos:
#             print("======", w)
#         else:
#             trabalhos.append(w)




# Função para remanejar os trabalhos para os avaliadores
# def atualizar(request):
    
#     campus = Campus.objects.get(name=request.GET['campus'])

#     work_list = []

#     works = Work.objects.all()

#     from django.utils import timezone
#     event = Edition.objects.filter(ativo=True).exists()
#     if event:

#         # print("========== entrou")

#         event = Edition.objects.get(ativo=True)
#         inscription = Inscription.objects.filter(edition=event, campus=campus)
#         inscription_users = [x.user for x in inscription]

#         edition = Edition.objects.get(ativo=True)
#         inscriptions = Inscription.objects.filter(edition=edition, campus=campus)
#         users = [x.user for x in inscriptions]
#         workAuthor = UserWork.objects.filter(user__in=users)
#         works_id = [w.work.id for w in workAuthor]
#         works = Work.objects.filter(id__in=works_id)
        

#         for work in works:
#             evaluation_committee = EvaluationCommittee.objects.get(edition=event, campus=campus)

#             users_work_id = [x.user.id for x in workAuthor if x.work == work]
            
#             users_committee = UserCommittee.objects.filter(committee=evaluation_committee, interest_area=work.interest_area).exclude(user__id__in=users_work_id)

#             data = {
#                 'corrector': users_committee[0].user,
#                 'evaluations': Evaluation.objects.filter(created_on__gte=event.start_of_registrations, corrector=users_committee[0].user).count()
#             }    
            
#             if not Evaluation.objects.filter(work=work).exists():
#                 data = {
#                     'corrector': users_committee[0].user,
#                     'evaluations': Evaluation.objects.filter(created_on__gte=event.start_of_registrations, corrector=users_committee[0].user).count()
#                 }

#                 for corrector in users_committee:
#                     evaluations = Evaluation.objects.filter(
#                         created_on__gte=event.start_of_registrations, 
#                         corrector=corrector.user
#                     ).count()
#                     if evaluations < data['evaluations']:
#                         data['corrector'] = corrector.user
#                         data['evaluations'] = evaluations

#                 evaluation = Evaluation.objects.create(work=work, corrector=data['corrector'])
#                 evaluation.save()
                
#                 rating_criteria_event = RatingCriteria.objects.filter(edition=event)
#                 items = []
#                 for criteria in rating_criteria_event:
#                     items.append(EvaluationRatingCriteria(criteria=criteria, value=0.0, evaluation=evaluation))

#                 EvaluationRatingCriteria.objects.bulk_create(items)

#                 to = [data['corrector'].email]

#                 html_content = render_to_string('work/send_email.html', {'work': work, 'corrector': data['corrector']})
#                 text_content = strip_tags(html_content)

#                 subject = "[SEMEX] Um novo trabalho submetido para avaliação! | SEMEX"
#                 from_email = "SEMEX <"+ str(settings.EMAIL_HOST_USER)+">"
#                 to = [data['corrector'].email]

#                 msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#                 msg.attach_alternative(html_content, "text/html")

#                 msg.send()

#         pass

# View para Autocomplete de User
class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs


# View para Autocomplete de User
class CorrectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = User.objects.all()
        aux = []

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
            for q in qs:
                if q.is_evaluation_committee:
                    aux.append(q)

        return aux


# View para Autocomplete de Work
class WorkAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Work.objects.all()

        if self.q:
            qs = qs.filter(Q(title__icontains=self.q))

        return qs


# View para Autocomplete de InterestArea
class InterestAreaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = InterestArea.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs


# View para Autocomplete de InterestArea
# class CriteriaAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):

#         qs = RatingCriteria.objects.all()

#         if self.q:
#             qs = qs.filter(Q(name__icontains=self.q))

#         return qs


# Views para Model EvaluationCommittee
@method_decorator(login_required, name='dispatch')
class CreateEvaluationCommittee(CreateView):
    """
    ClassView para Criação de objeto EvaluationCommittee
    """
    model = EvaluationCommittee
    form_class = EvaluationCommitteeForm
    template_name = 'evaluation-committee/add.html'

    def get(self, request, *args, **kwargs):
        self.usercommittee_formset = UserCommitteFormSet()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.usercommittee_formset = UserCommitteFormSet(self.request.POST)
        form = self.get_form()
        if form.is_valid() and self.usercommittee_formset.is_valid():
            return self.form_valid(form)
        else:
            self.object=None
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        self.usercommittee_formset.instance=self.object
        self.usercommittee_formset.save()

        return HttpResponseRedirect(reverse('evaluation_committee:list_evaluation_committee'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usercommittee_formset']=self.usercommittee_formset
        return context


@method_decorator(login_required, name='dispatch')
class UpdateEvaluationCommittee(UpdateView):
    """
    ClassView para edição de objeto EvaluationCommittee
    """
    model = EvaluationCommittee
    form_class = EvaluationCommitteeForm
    template_name = 'evaluation-committee/add.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.usercommittee_formset = UserCommitteFormSet(instance=self.object)
        self.usercommittee_formset.extra=0
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.usercommittee_formset = UserCommitteFormSet(self.request.POST, instance=self.object)
        form = self.get_form()
        if form.is_valid() and self.usercommittee_formset.is_valid():
            return self.form_valid(form)
        else:
            print(self.usercommittee_formset.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.usercommittee_formset.save()        
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('evaluation_committee:list_evaluation_committee')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usercommittee_formset']=self.usercommittee_formset
        return context


@login_required
def evaluation_committee_delete(request, pk):
    """
    View para exclusão de objeto EvaluationCommittee
    """
    evaluation_committee= get_object_or_404(EvaluationCommittee, pk=pk)
    evaluation_committee.delete()
    return JsonResponse({'msg': "Comitê Avaliador excluido com sucesso!", 'code': "1"})


@method_decorator(login_required, name='dispatch')
class ListEvaluationCommittee(ListView):
    """
    ClassView para lista dos objetos EvaluationCommittee
    """
    model = EvaluationCommittee
    http_method_names = ['get']
    template_name = 'evaluation-committee/list.html'
    context_object_name = 'evaluation_committee'
    paginate_by = 25

    # def get_queryset(self):
    #     self.queryset = super(ListEvaluationCommittee, self).get_queryset()
    #     if self.request.GET.get('search_box', False):
    #         self.queryset=self.queryset.filter(edition__name__icontains = self.request.GET['search_box'])
    #     return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListEvaluationCommittee, self)
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


# Views para Model InterestArea
@method_decorator(login_required, name='dispatch')
class CreateInterestArea(CreateView):
    """
    ClassView para Criação de objeto InterestArea
    """
    model = InterestArea
    form_class = InterestAreaForm
    template_name = 'interest-area/add.html'


@method_decorator(login_required, name='dispatch')
class UpdateInterestArea(UpdateView):
    """
    ClassView para edição de objeto InterestArea
    """
    model = InterestArea
    form_class = InterestAreaForm
    template_name = 'interest-area/add.html'


@login_required
def interest_area_delete(request, pk):
    """
    View para exclusão de objeto InterestArea
    """
    interest_area= get_object_or_404(InterestArea, pk=pk)
    interest_area.delete()
    return JsonResponse({'msg': "Área de Interesse excluida com sucesso!", 'code': "1"})


@method_decorator(login_required, name='dispatch')
class ListInterestArea(ListView):
    """
    ClassView para listagem de objetos InterestArea
    """
    model = InterestArea
    http_method_names = ['get']
    template_name = 'interest-area/list.html'
    context_object_name = 'interest_area'
    paginate_by = 25

    def get_queryset(self):
        self.queryset = super(ListInterestArea, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(name__icontains = self.request.GET['search_box'])
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListInterestArea, self)
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


# Views para Model RatingCriteria
# ition matching query does not exist.

# Função para enviar email para avaliador com menos trabalhos
# def send_work(request, work):
#     from django.utils import timezone
#     event = Edition.objects.filter(ativo=True, end_of_registrations__gte=timezone.now()).exists()
#     if event:

#         event = Edition.objects.get(ativo=True)
#         inscription = Inscription.objects.get(user=request.user, edition=event)
#         evaluation_committee = EvaluationCommittee.objects.get(edition=event, campus=inscription.campus)
#         workAuthor = workAuthor.objects.filter(work=work)
#         users_work_id = [x.user.id for x in workAuthor if x.work == work]
#         users_committee = UserCommittee.objects.filter(committee=evaluation_committee, interest_area=work.interest_area).exclude(user__id__in=users_work_id)
        
#         data = {
#             'corrector': users_committee[0].user,
#             'evaluations': Evaluation.objects.filter(correction_date__lte=event.start_of_registrations, corrector=users_committee[0].user).count()
#         }

#         for corrector in users_committee:
#             evaluations = Evaluation.objects.filter(
#                 correction_date__lte=event.start_of_registrations, 
#                 corrector=corrector.user
#             ).count()
#             if evaluations < data['evaluations']:
#                 data['corrector'] = corrector.user
#                 data['evaluations'] = evaluations

#         evaluation = Evaluation.objects.create(work=work, corrector=data['corrector'])
#         evaluation.save()
        
#         rating_criteria_event = RatingCriteria.objects.filter(edition=event)
#         items = []
#         for criteria in rating_criteria_event:
#             items.append(EvaluationRatingCriteria(criteria=criteria, value=0.0, evaluation=evaluation))

#         EvaluationRatingCriteria.objects.bulk_create(items)

#         html_content = render_to_string('work/send_email.html', {'work': work, 'corrector': data['corrector']})
#         text_content = strip_tags(html_content)

#         subject = "[SEMEX] Um novo trabalho submetido para avaliação! | SEMEX"
#         from_email = "SEMEX <"+ str(settings.EMAIL_HOST_USER)+">"
#         to = [data['corrector'].email]

#         msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

#         pass

# Views para Model Work
@method_decorator(login_required, name='dispatch')
class CreateWork(CreateView):
    """
    ClassView para Criação de objeto Work
    """
    model = Work
    form_class = WorkForm
    template_name = 'work/add.html' 

    def get(self, request, *args, **kwargs):
        self.userwork_formset = UserWorkFormSet(initial=[{'name':self.request.user.name,'email':self.request.user.email, 'is_coordinator': False}])
        self.userwork_formset.extra=1
        return super(CreateWork,self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.userwork_formset = UserWorkFormSet(self.request.POST)
        form = self.get_form()
        if form.is_valid() and self.userwork_formset.is_valid():
            return self.form_valid(form)
        else:
            self.object=None
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        self.object.submission_user = self.request.user
        self.object.save()
        
        for i,user_form in enumerate(self.userwork_formset):
            if 'name' in user_form.cleaned_data and 'email' in user_form.cleaned_data:            
                try:
                    user  = User.objects.get(email=user_form.cleaned_data.get('email'))
                except:
                    user = User(username=user_form.cleaned_data.get('email'), 
                        email=user_form.cleaned_data.get('email'),
                        name=user_form.cleaned_data.get('name')
                    )
                    user.set_password('teste')
                    user.save()
                
                from django.utils import timezone
                user_work = UserWork(user=user,work=self.object,order=i+1, is_coordinator=user_form.cleaned_data['is_coordinator'], created_on=timezone.now(), updated_on=timezone.now())
                user_work.save()
        # try:
        #     send_work(self.request, self.object)
        # except:
        #     pass
        return HttpResponseRedirect(reverse('evaluation_committee:list_work'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userwork_formset']=self.userwork_formset
        #from django.utils import timezone
        #event = Edition.objects.filter(ativo=True, start_submissions__lte=timezone.now(), end_submissions__gte=timezone.now()).exists()
        #context['event']=event
        return context


@method_decorator(login_required, name='dispatch')
class UpdateWork(UpdateView):
    """
    ClassView para edição de objeto Work
    """
    model = Work
    form_class = WorkForm
    template_name = 'work/add.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        userwork_data = []
        for userwork in UserWork.objects.filter(work=self.object):
            userwork_data.append({'name':userwork.user.name,'email':userwork.user.email, 'is_coordinator': userwork.is_coordinator})
        self.userwork_formset = UserWorkFormSet(initial=userwork_data)
        self.userwork_formset.extra=1
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.userwork_formset = UserWorkFormSet(self.request.POST)
        if self.object.file_word and self.request.FILES.get('file_word', False):
            self.object.file_word.delete()

        if self.object.file_pdf and self.request.FILES.get('file_pdf', False):
            self.object.file_pdf.delete()

        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid() and self.userwork_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()

        for item in UserWork.objects.filter(work=self.object):
            item.delete()

        for i,user_form in enumerate(self.userwork_formset):
            if 'name' in user_form.cleaned_data and 'email' in user_form.cleaned_data:
                try:
                    user  = User.objects.get(email=user_form.cleaned_data['email'])
                except:
                    user = User(username=user_form.cleaned_data.get('email'), 
                        email=user_form.cleaned_data.get('email'),
                        name=user_form.cleaned_data.get('name')
                    )
                    user.set_password('teste')
                    user.save()
                from django.utils import timezone
                user_work = UserWork(user=user,work=self.object,order=i+1, is_coordinator=user_form.cleaned_data['is_coordinator'], created_on=timezone.now(), updated_on=timezone.now())
                user_work.save()

        
        # if not Evaluation.objects.filter(work=self.object).exists():
        #     try:
        #         send_work(self.request, self.object)
        #     except:
        #         pass

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('evaluation_committee:list_work')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userwork_formset']=self.userwork_formset
        #from django.utils import timezone
        #event = Edition.objects.filter(ativo=True, start_submissions__lte=timezone.now(), end_submissions__gte=timezone.now()).exists()
        #context['event']=event

        return context


@login_required
def work_delete(request, pk):
    """
    View para exclusão de objeto Work
    """
    work= get_object_or_404(Work, pk=pk)
    work.delete()
    return JsonResponse({'msg': "Trabalho excluido com sucesso!", 'code': "1"})


@method_decorator(login_required, name='dispatch')
class ListWork(ListView):
    """
    ClassView para listagem de objetos Work
    """
    model = Work
    http_method_names = ['get']
    template_name = 'work/list.html'
    context_object_name = 'work'
    paginate_by = 25

    def get_queryset(self):
        if not self.request.user.is_evaluation_committee and not self.request.user.is_superuser:
            workAuthor = UserWork.objects.filter(user=self.request.user)
            works_id = [w.work.id for w in workAuthor]
            self.queryset = Work.objects.filter(id__in=works_id)
        else:
            self.queryset = super(ListWork, self).get_queryset()

        if self.request.GET.get('search_box', False):
            #edition = Edition.objects.get(ativo=True)
            try:
                #campus = Campus.objects.get(name__contains=self.request.GET['search_box'])
                #inscriptions = Inscription.objects.filter(campus__name__icontains=self.request.GET['search_box'])
                #users = [x.user for x in inscriptions]
                workAuthor = UserWork.objects.filter(user__in=users)
                works_id = [w.work.id for w in workAuthor]
                self.queryset=self.queryset.filter(Q(id__in=works_id))
            except:
                pass
            #inscriptions = Inscription.objects.filter(campus__name__icontains=self.request.GET['search_box'])
            #users = [x.user for x in inscriptions]
            workAuthor = UserWork.objects.filter(user__in=users)
            works_id = [w.work.id for w in workAuthor]
            self.queryset=self.queryset.filter(Q(title__icontains = self.request.GET['search_box']) | Q(id__in=works_id))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListWork, self)
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
        from django.utils import timezone
        #event = Edition.objects.filter(ativo=True, start_submissions__lte=timezone.now(), end_submissions__gte=timezone.now()).exists()
        context.update({
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': num_pages not in page_numbers,
        #'event': event
            })
        return context


# Views para Model Evaluation
@method_decorator(login_required, name='dispatch')
class CreateEvaluation(CreateView):
    """
    ClassView para Criação de objeto Evaluation
    """
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluation/add.html'

    def get(self, request, *args, **kwargs):
        # edition = Edition.objects.get(ativo=True)
        # self.rating_criteria_event = RatingCriteria.objects.filter(edition=edition)
        # items = []
        # for criteria in self.rating_criteria_event:
        #     items.append({'criteria': criteria, 'value': 0.0 ,})

        
        # self.evaluation_rating_criteria = EvaluationRatingCriteriaFormSet(initial=items)

        return super(CreateEvaluation,self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        #self.evaluation_rating_criteria = EvaluationRatingCriteriaFormSet(self.request.POST)
        if form.is_valid():  #and self.evaluation_rating_criteria.is_valid()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        #self.evaluation_rating_criteria.instance=self.object
        #self.evaluation_rating_criteria.save()
        #edition = Edition.objects.get(ativo=True)
        #self.rating_criteria_event = RatingCriteria.objects.filter(edition=edition)
    
        # for criteria in self.rating_criteria_event:
        #     name = "criteria-" + str(criteria.id)
        #     value = float(self.request.POST[name])
        #     evaluation_rating_criteria = EvaluationRatingCriteria.objects.create(criteria=criteria, evaluation=evaluation, value=value)
        #     evaluation_rating_criteria.save()

        return HttpResponseRedirect(reverse('evaluation_committee:list_evaluation'))

    def get_context_data(self, **kwargs):
        context = super(CreateEvaluation,self).get_context_data(**kwargs)
        #context['rating_criteria_event'] = self.rating_criteria_event
        #context['evaluation_rating_criteria'] = self.evaluation_rating_criteria
        return context


@method_decorator(login_required, name='dispatch')
class UpdateEvaluation(UpdateView):
    """
    ClassView para edição de objeto Evaluation
    """
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluation/add.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # self.evaluation_rating_criteria = EvaluationRatingCriteria.objects.filter(evaluation=self.object)
        #self.evaluation_rating_criteria = EvaluationRatingCriteriaFormSet(instance=self.object)
        return super(UpdateEvaluation,self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, instance=self.object)
        #self.evaluation_rating_criteria = EvaluationRatingCriteriaFormSet(self.request.POST, instance=self.object)
        if form.is_valid(): #and self.evaluation_rating_criteria.is_valid()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save()
        #self.evaluation_rating_criteria.save()
        return HttpResponseRedirect(reverse('evaluation_committee:list_evaluation'))

    def get_context_data(self, **kwargs):
        #self.evaluation_rating_criteria.extra=0
        context = super(UpdateEvaluation,self).get_context_data(**kwargs)
        #context['evaluation_rating_criteria'] = self.evaluation_rating_criteria
        return context


@login_required
def evaluation_delete(request, pk):
    """
    View para exclusão de objeto Evaluation
    """
    evaluation= get_object_or_404(Evaluation, pk=pk)
    evaluation.delete()
    return JsonResponse({'msg': "Avaliação excluida com sucesso!", 'code': "1"})


@method_decorator(login_required, name='dispatch')
class ListEvaluation(ListView):
    """
    ClassView para listagem de objetos Evaluation
    """
    model = Evaluation
    http_method_names = ['get']
    template_name = 'evaluation/list.html'
    context_object_name = 'evaluation'
    paginate_by = 25

    def get_queryset(self):
        if not self.request.user.is_evaluation_committee and not self.request.user.is_superuser:
            workAuthor = UserWork.objects.filter(user=self.request.user)
            works_id = [w.work.id for w in workAuthor]
            works = Work.objects.filter(id__in=works_id)
            works_id = [x.id for x in works]
            self.queryset = Evaluation.objects.filter(work__id__in=works_id)
        elif not self.request.user.is_evaluation_committee:
            self.queryset = super(ListEvaluation, self).get_queryset()    
        else:
            self.queryset = Evaluation.objects.filter(corrector=self.request.user) 

        if self.request.GET.get('search_box', False):

            self.queryset=self.queryset.filter(Q(work__title__icontains = self.request.GET['search_box'])| Q(corrector__username__icontains=self.request.GET['search_box']))

            self.queryset=self.queryset.filter(Q(work__title__icontains = self.request.GET['search_box']) | Q(corrector__name__icontains=self.request.GET['search_box']) | Q(corrector__username__icontains=self.request.GET['search_box']) |Q(work__interest_area__name__icontains = self.request.GET['search_box']))

        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListEvaluation, self)
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
class GetEvaluation(DetailView):
    """
    ClassView para visualizacao de objeto Evaluation
    """
    model = Evaluation
    http_method_names = ['get']
    template_name = 'evaluation/detail.html'
    context_object_name = 'evaluation'
    
    def get_context_data(self, **kwargs):
        context = super(GetEvaluation,self).get_context_data(**kwargs)
        #context['rating_criteria'] = EvaluationRatingCriteria.objects.filter(evaluation=self.object)
        context['authors'] = UserWork.objects.filter(work=self.object.work)
        return context


@method_decorator(login_required, name='dispatch')
class DetailWork(DetailView):
    """
    ClassView para visualizacao de objeto Evaluation
    """
    model = Work
    http_method_names = ['get']
    template_name = 'work/detail.html'
    context_object_name = 'work'
    
    def get_context_data(self, **kwargs):
        context = super(DetailWork,self).get_context_data(**kwargs)
        context['authors'] = UserWork.objects.filter(work=self.get_object())
        return context