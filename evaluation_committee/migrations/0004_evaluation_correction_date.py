# Generated by Django 2.2.4 on 2019-11-26 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation_committee', '0003_remove_evaluation_correction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='correction_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Data de correção'),
        ),
    ]
