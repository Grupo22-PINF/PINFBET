from django.contrib import admin
from .models import Alumno,Asignatura,AlumAsig,Amistad,Publicidad

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Asignatura)
admin.site.register(AlumAsig)
admin.site.register(Amistad)
admin.site.register(Publicidad)