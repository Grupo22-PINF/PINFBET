from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('menuapuesta', views.apostar, name='apuesta'),
    path('apostar/<str:sid>/', views.apostarasig, name='apostarasig'),
    path('<str:sid>/<str:uid>/', views.detail, name='detail'),
    path('registro/', views.registro, name='registro'),
    path('logout',views.logout, name='logout'),
    path('login',views.login, name="login"),
    path('perfil',views.profile, name="profile"),
    path('expediente',views.SubirExpediente, name="subirexpediente"),
    path('matricula',views.SubirMatricula, name="subirmatricula"),
    path('eliminarcuenta',views.delete,name="eliminarcuenta"),
    path('buscarusuario',views.buscador,name="buscarusuario"),
    path('mostrarusuario',views.solicitar,name="mostrarusuario"),
    path('notificaciones',views.aceptar,name="notificaciones"),
    path('veramigos',views.buscador_amigo,name="veramigos"),
    path('perfil/<str:usuario>',views.perfilext,name="perfilext"),
    path('politica',views.politica,name="politica"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('contacto',views.contactanos,name="contactanos"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)