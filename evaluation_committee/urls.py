# URL APP EVALUATION COMMITTEE

from django.urls import path
from .views import *
from evaluation_committee.views import ListEvaluation

app_name = 'evaluation_committee'

urlpatterns = [
    # Evaluation Committee
    path('list/', ListEvaluationCommittee.as_view(), name='list_evaluation_committee',),
    path('add/', CreateEvaluationCommittee.as_view(), name='add_evaluation_committee',),
    path('edit/<int:pk>/', UpdateEvaluationCommittee.as_view(), name='edit_evaluation_committee',),
    path('delete/<int:pk>/', evaluation_committee_delete, name='delete_evaluation_committee',),

    # InterestArea
    path('interest-area/list/', ListInterestArea.as_view(), name='list_interest_area',),
    path('interest-area/add/', CreateInterestArea.as_view(), name='add_interest_area',),
    path('interest-area/edit/<int:pk>/', UpdateInterestArea.as_view(), name='edit_interest_area',),
    path('interest-area/delete/<int:pk>/', interest_area_delete, name='delete_interest_area',),

    # # RatingCriteria
    # path('rating-criteria/list/', ListRatingCriteria.as_view(), name='list_rating_criteria',),
    # path('rating-criteria/add/', CreateRatingCriteria.as_view(), name='add_rating_criteria',),
    # path('rating-criteria/edit/<int:pk>/', UpdateRatingCriteria.as_view(), name='edit_rating_criteria',),
    # path('rating-criteria/delete/<int:pk>/', rating_criteria_delete, name='delete_rating_criteria',),

    # Work
    path('work/list/', ListWork.as_view(), name='list_work',),
    path('work/get/<int:pk>/', DetailWork.as_view(), name='get_work',),
    path('work/add/', CreateWork.as_view(), name='add_work',),
    path('work/edit/<int:pk>/', UpdateWork.as_view(), name='edit_work',),
    path('work/delete/<int:pk>/', work_delete, name='delete_work',),

    # Evaluation
    path('evaluation/list/', ListEvaluation.as_view(), name='list_evaluation',),
    path('evaluation/get/<int:pk>/', GetEvaluation.as_view(), name='get_evaluation',),
    path('evaluation/add/', CreateEvaluation.as_view(), name='add_evaluation',),
    path('evaluation/edit/<int:pk>/', UpdateEvaluation.as_view(), name='edit_evaluation',),
    path('evaluation/delete/<int:pk>/', evaluation_delete, name='delete_evaluation',),

    # Autocomplete
 	path('user/autocomplete/', UserAutocomplete.as_view(), name='user_autocomplete',),
 	path('work/autocomplete/', WorkAutocomplete.as_view(), name='work_autocomplete',),
 	path('corrector/autocomplete/', CorrectorAutocomplete.as_view(), name='corrector_autocomplete',),
 	path('interest-area/autocomplete/', InterestAreaAutocomplete.as_view(), name='interest_area_autocomplete',),
 	#path('criteria/autocomplete/', CriteriaAutocomplete.as_view(), name='criteria_autocomplete',),


 	#path('atualizar/', atualizar, name='atualizar',),
 	# path('avisar/', avisar, name='avisar',),

   
]
