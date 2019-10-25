from django.db import models

#D'Larinhoo mexendo aqui

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#------------------------------------------
    
class Artigo(models.Model):

    cod_artigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30, null=False, blank=False)
    resumo = models.CharField(max_length=3000, null=False, blank=False)
    palavras_chaves = models.CharField(max_length=200, null=False, blank=False)
    area = models.CharField(max_length=100, null=False, blank=False)
    situacao = models.CharField(max_length=30, null=False, blank=False)
    pdf = models.FileField(upload_to='artigos/pdfs')
    autor = models.CharField(max_length=70, null=False, blank=False)

    def __str__(self):
        return self.titulo

    def deletar(self, *args, **kwargs):
        self.pdf.deletar()
        super().deletar(*args, **kwargs)


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
