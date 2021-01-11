import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Alumno(models.Model):
    uid = models.CharField(max_length=12)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    email = models.CharField(max_length=50,default="dsada@gmail.com")
    coins = models.IntegerField(default=500)
    career = models.CharField(max_length=50)
    exp = models.FileField(blank=True,null=True)

    def __str__(self):
        return self.uid

class Asignatura(models.Model):
    sid = models.CharField(max_length=8)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AlumAsig(models.Model):
    uid = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    sid = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    nminima = models.IntegerField(default=0)
    grade = models.FloatField(default=0)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return   self.sid.sid + self.uid.uid

class Amistad(models.Model):
    solicitud = models.IntegerField(default=-1)
    uid1 = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="Alumno1")
    uid2 = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="Alumno2")

    def __str__(self):
        return self.uid1.uid + self.uid2.uid

class Publicidad(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()
    image = models.ImageField()

    def __str__(self):
        return self.name
