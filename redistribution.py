#from editions.models import Edition, Inscription
from evaluation_committee.models import EvaluationCommittee, UserCommittee, Evaluation, RatingCriteria, EvaluationRatingCriteria
from django.conf import settings

from django.utils import timezone
#event = Edition.objects.filter(ativo=True, end_of_registrations__gte=timezone.now()).exists()
#if event:

    #event = Edition.objects.get(ativo=True)
    #inscription = Inscription.objects.get(user=request.user, edition=event, campus__name='Picos')
evaluation_committee = EvaluationCommittee.objects.all()
users_committee = UserCommittee.objects.filter(committee=evaluation_committee, interest_area=work.interest_area).exclude(user=request.user)

data = {
    'corrector': users_committee[0].user,
    'evaluations': Evaluation.objects.filter(corrector=users_committee[0].user).count()
}

for corrector in users_committee:
    evaluations = Evaluation.objects.filter(
        corrector=corrector.user
    ).count()
    if evaluations < data['evaluations']:
        data['corrector'] = corrector.user
        data['evaluations'] = evaluations

evaluation = Evaluation.objects.create(work=work, corrector=data['corrector'])
evaluation.save()

rating_criteria_event = RatingCriteria.objects.all()
items = []
for criteria in rating_criteria_event:
    items.append(EvaluationRatingCriteria(criteria=criteria, value=0.0, evaluation=evaluation))

EvaluationRatingCriteria.objects.bulk_create(items)

# html_content = render_to_string('work/send_email.html', {'work': work, 'corrector': data['corrector']})
# text_content = strip_tags(html_content)

# subject = "[SEMEX] Um novo trabalho submetido para avaliação! | SEMEX"
# from_email = "SEMEX <"+ str(settings.EMAIL_HOST_USER)+">"
to = [data['corrector'].email]

# msg = EmailMultiAlternatives(subject, text_content, from_email, to)
# msg.attach_alternative(html_content, "text/html")
# msg.send()

print("mandar email para", to)

pass