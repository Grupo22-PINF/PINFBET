# Generated by Django 3.1.2 on 2020-12-21 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20201221_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='grade',
            field=models.IntegerField(blank=True, default=3),
            preserve_default=False,
        ),
    ]
