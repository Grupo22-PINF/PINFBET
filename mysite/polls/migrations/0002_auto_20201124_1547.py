# Generated by Django 3.1.2 on 2020-11-24 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=20)),
                ('coins', models.IntegerField(default=0)),
                ('grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Apuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=8)),
                ('amount', models.IntegerField()),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=100)),
                ('grade', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
