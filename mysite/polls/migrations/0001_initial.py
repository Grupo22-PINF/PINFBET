# Generated by Django 3.1.5 on 2021-01-13 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=30)),
                ('email', models.CharField(default='dsada@gmail.com', max_length=50)),
                ('coins', models.IntegerField(default=500)),
                ('career', models.CharField(max_length=50)),
                ('doc', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publicidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Amistad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitud', models.IntegerField(default=-1)),
                ('uid1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Alumno1', to='polls.alumno')),
                ('uid2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Alumno2', to='polls.alumno')),
            ],
        ),
        migrations.CreateModel(
            name='AlumAsig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('nminima', models.IntegerField(default=0)),
                ('grade', models.FloatField(default=0)),
                ('passed', models.BooleanField(default=False)),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.asignatura')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.alumno')),
            ],
        ),
    ]
