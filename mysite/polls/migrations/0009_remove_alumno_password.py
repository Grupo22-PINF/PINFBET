# Generated by Django 3.1.2 on 2020-12-01 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_alumno_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno',
            name='password',
        ),
    ]