# Generated by Django 2.2.5 on 2019-10-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revista', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='artigo',
            name='user_autor',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
