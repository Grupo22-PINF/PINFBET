# Generated by Django 3.1.2 on 2020-11-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20201124_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='career',
            field=models.CharField(default='GII', max_length=5),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='career',
            field=models.CharField(default='GII', max_length=5),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='surname',
            field=models.CharField(max_length=30),
        ),
    ]
