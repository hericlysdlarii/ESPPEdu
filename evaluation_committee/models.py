from django.db import models
from accounts.models import User
from accounts.models import AuditModel
#from editions.models import Campus, Edition
from django.urls import reverse

# Models para Pacote de Comitê Avaliador.
class InterestArea(AuditModel):
    """
    Modelo de classe para Área de Interese que irá se relacionar com o comitê 
    avaliador e trabalhos postados.
    """
    name = models.CharField('Nome', blank=False, null=False, unique=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('evaluation_committee:list_interest_area')

    class Meta:
        verbose_name = 'Área de interesse'
        verbose_name_plural = 'Áreas de interesse'
        ordering = ['id']


class Work(AuditModel):
    """
    Modelo de classe para trabalho submetido na plataforma para análise.
    """
    title = models.CharField('Título', blank=False, null=False, max_length=255)
    interest_area = models.ForeignKey(InterestArea, verbose_name='área de interesse', blank=True, on_delete=models.CASCADE)
    key_words = models.CharField('Palavras-chave', blank=True, null=True, max_length=255)
    file_word = models.FileField('Arquivo Word', blank=True, null=True, upload_to='uploads/%Y/%m/%d/')
    file_pdf = models.FileField('Arquivo PDF', blank=True, null=True, upload_to='uploads/%Y/%m/%d/')
    submission_user = models.ForeignKey(User, verbose_name='Usuário que submeteu', blank=True, null=True, on_delete=models.DO_NOTHING)
    
    
    @property
    def author(self):
        author = UserWork.objects.get(work=self, order=1)
        return author.user

    @property
    def has_evaluation(self):
        try:
            Evaluation.objects.get(work=self)
            return True
        except:
            return False
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('evaluation_committee:list_work')

    class Meta:
        verbose_name = 'Trabalho'
        verbose_name_plural = 'Trabalhos'
        ordering = ['id']


class Evaluation(AuditModel):
    """
    Modelo de classe para cadastro de avaliação de trabalho
    """
    work = models.ForeignKey(Work, verbose_name='trabalho', on_delete=models.CASCADE)
    corrector = models.ForeignKey(User, verbose_name="Avaliador(a)", on_delete=models.CASCADE)
    correction_date = models.DateField('Data de correção', blank=True, null=True, auto_now_add=True)
    observation = models.TextField('Observação', blank=True, null=True)

    def __str__(self):
        return 'Avaliação: {}'.format(self.work.title)

    def get_absolute_url(self):
        return reverse('evaluation_committee:list_evaluation')

    # @property
    # def average(self):
    #     notes = EvaluationRatingCriteria.objects.filter(evaluation=self)
    #     final = 0
    #     for note in notes:
    #         final += float(note.value)
        
    #     try:  
    #         return float(final/notes.count())
    #     except ZeroDivisionError:
    #         return 0.0

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['id']


# class RatingCriteria(AuditModel):
#     """
#     Modelo de classe para cadastro de critério de avaliação.
#     """
#     #edition = models.ForeignKey(Edition, verbose_name='edição', on_delete=models.CASCADE)
#     name = models.CharField('Nome', blank=False, null=False, max_length=255)
#     weight = models.DecimalField('Peso', max_digits=4, decimal_places=2, blank=True, null=True)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('evaluation_committee:list_rating_criteria')

#     class Meta:
#         verbose_name = 'Critério de Avaliação'
#         verbose_name_plural = 'Critérios de Avaliação'
#         ordering = ['id']


# class EvaluationRatingCriteria(AuditModel):
#     """
#     Modelo de classe para cadastro de nota (0-10) do critério de avaliação para o 
#     trabalho especificado. 
#     """
#     criteria = models.ForeignKey(RatingCriteria, verbose_name='critério', on_delete=models.CASCADE)
#     evaluation = models.ForeignKey(Evaluation, verbose_name='avaliação', on_delete=models.CASCADE)
#     value = models.DecimalField('Valor', max_digits=4, decimal_places=2, blank=False, null=False)

#     def __str__(self):
#         return 'Avaliação do critério {} do trabalho {}'.format(self.criteria.name, self.evaluation.work.title)

#     def get_absolute_url(self):
#         pass
#         # return reverse('evaluation_committee:rating_criteria_list')

#     class Meta:
#         verbose_name = 'Avaliação do critério'
#         verbose_name_plural = 'Avaliações dos critérios'
#         ordering = ['id'] 


class EvaluationCommittee(AuditModel):
    """
    Modelo de classe para cadastro de comissão avaliadora da edição do evento.
    """
    #campus = models.ForeignKey(Campus, verbose_name='campus', on_delete=models.CASCADE, blank=False, null=False)
    #edition = models.ForeignKey(Edition, verbose_name='edição', on_delete=models.CASCADE, blank=False, null=False)

    # def __str__(self):
    #     return "Comitê científico do campus {}".format(self.campus.name)

    def get_absolute_url(self):
        return reverse('evaluation_committee:list_evaluation_committee')


    class Meta:
        verbose_name = 'Comitê Avaliador'
        verbose_name_plural = 'Comitês Avaliadores'
        ordering = ['id'] 


class UserCommittee(AuditModel):
    """
    Modelo de classe para relacionar o Usuário, o comitê avaliador e sua área de intersse
    """
    user = models.ForeignKey(User, verbose_name="usuário", on_delete=models.CASCADE, blank=False, null=False)
    committee = models.ForeignKey(EvaluationCommittee, verbose_name="comitê avaliador", on_delete=models.CASCADE, blank=False, null=False)
    interest_area = models.ForeignKey(InterestArea, verbose_name='área de interesse', on_delete=models.CASCADE, blank=False, null=False)

    # def __str__(self):
    #     return "Comitê científico do campus {}".format(self.committee.campus.name)

    def get_absolute_url(self):
        return reverse('evaluation_committee:list_evaluation_committee')
        pass

    class Meta:
        ordering = ['id'] 


class UserWork(AuditModel):
    """
    Modelo de classe que permite que o participante adicione mais de um autor do trabalho.
    """
    order = models.IntegerField('Ordem', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='usuário', on_delete=models.CASCADE, blank=False, null=False)
    work = models.ForeignKey(Work, verbose_name='trabalho', on_delete=models.CASCADE, blank=False, null=False)
    is_coordinator = models.BooleanField('É o Coordenador?', blank=True, null=True, default=False)

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        pass
        # return reverse('evaluation_committee:rating_criteria_list')

    class Meta:
        verbose_name = 'Usuário com Trabalho'
        verbose_name_plural = 'Usuários com Trabalhos'
        ordering = ['order'] 
