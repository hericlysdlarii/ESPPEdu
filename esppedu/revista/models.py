from django.db import models
from django.contrib.auth.models import User

    
class Artigo(models.Model):

    cod_artigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30, null=False, blank=False)
    resumo = models.CharField(max_length=3000, null=False, blank=False)
    palavras_chaves = models.CharField(max_length=200, null=False, blank=False)
    area = models.CharField(max_length=100, null=False, blank=False)
    situacao = models.CharField(max_length=30, null=False, blank=False)
    pdf = models.FileField(upload_to='artigos/pdfs')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def deletar(self, *args, **kwargs):
        self.pdf.deletar()
        super().deletar(*args, **kwargs)


# Create your models here.
