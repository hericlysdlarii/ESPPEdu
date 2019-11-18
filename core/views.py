from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from accounts.models import User
from evaluation_committee.models import EvaluationCommittee, UserCommittee, Evaluation, UserWork
#from editions.models import Inscription, Campus

# Página inicial
@login_required
def index(request):
    # Inscritos
    # Admin
    # Trabalhos por campus
    # inscriptions = Inscription.objects.filter(edition__ativo=True).count()
    admins = User.objects.filter(is_superuser=True).count()
    # campus = Campus.objects.all()
    data = []
    # for c in campus:
    #     try:
    #         committee = EvaluationCommittee.objects.get(edition__ativo=True, campus=c)
    #         user_committee = User
    #         users_committe = UserCommittee.objects.filter(committee=committee)
    #         users_id = [i.user.id for i in users_committe]
            
    #         evaluations = Evaluation.objects.filter(corrector__in=users_id).count()
    #         data.append({
    #             #'campus': c,
    #             'works' :  evaluations
    #         })
    #     except:
    #         data.append({
    #             #'campus': c,
    #             'works' :  0
    #         })

    return render(request, 'index.html', {'admins': admins, 'data': data})


# @login_required
# def ranking(request):
#     search = None
#     campus = Campus.objects.all()
#     data = []
#     total = 0
#     if request.GET.get('search_box') and request.GET['search_box'] != '':
#         search = request.GET['search_box']
#         campus = Campus.objects.filter(name__icontains=search)

#         for c in campus:
#             inscriptions = Inscription.objects.filter(campus=c)
#             users = [x.user for x in inscriptions]
#             works = UserWork.objects.filter(user__in=users)

#             works_id = [x.work.id for x in works]

#             evaluations = Evaluation.objects.filter(work__id__in=works_id)
                
#             x = sorted(evaluations, key=lambda t: t.average, reverse=True)
#             total += evaluations.count()
#             data.append({
#                 'campus': c,
#                 'works' :  x
#             })

#     return render(request, 'ranking.html', {'object_list': data, 'search_box': search, 'total': total})
