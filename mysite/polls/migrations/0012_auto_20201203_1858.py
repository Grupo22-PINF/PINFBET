# Generated by Django 3.1.2 on 2020-12-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_alumasig'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumasig',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Apuesta',
        ),
    ]
