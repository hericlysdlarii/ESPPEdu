# -*- coding: utf-8 -*-

import re
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class AuditModel(models.Model):

    created_on = models.DateTimeField('Criado em', auto_now_add=True)
    updated_on = models.DateTimeField('Autalizado em', auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, AuditModel):

    username = models.CharField(
        'Usuário', max_length=255, default=uuid.uuid4, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )

    name = models.CharField('Nome', max_length=100, blank=False, null=False)
    email = models.EmailField('E-mail',max_length=255,unique=True, blank=False, null=False)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    is_superuser = models.BooleanField('Super-Usuário', default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    cpf = models.CharField('CPF', max_length=14, blank=True, null=True)
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = ((MALE, 'Masculino'), (FEMALE, 'Feminino'),)
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, default=FEMALE)

    phone = models.CharField('Celular', max_length=16, blank=True, null=True)
    is_whatsapp = models.BooleanField('O celular é WhatsApp?', default=False)
    
    avatar = ThumbnailerImageField(
        upload_to="avatar",
        blank=True,
        resize_source=dict(size=(215, 215), crop=True)
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['name']

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]

    # propriedade para saber se o usuário faz parte do comitê avaliador
    @property
    def is_evaluation_committee(self):
        #from editions.models import Edition
        from evaluation_committee.models import EvaluationCommittee
        from evaluation_committee.models import UserCommittee
        from datetime import datetime

        try:
            #edition = Edition.objects.get(ativo=True, start_of_registrations__lte=datetime.now(), end_of_registrations__gte=datetime.now())
            if UserCommittee.objects.filter(user=self).exists(): #, committee__edition=edition
                return True

            return False
        
        except:
            return False


    # @property
    # def is_organizer(self):
    #     #from editions.models import Edition

    #     try:
    #         #edition = Edition.objects.get(ativo=True)
    #         if self in edition.organizers.all():
    #             return True
            
    #         return False
    #     except:
    #         return False:

 
    # propriedade para saber se o usuário eh um partcicipante
    @property
    def is_participant(self):
        if not self.is_evaluation_committee and not self.is_superuser:
            return True

        return False

