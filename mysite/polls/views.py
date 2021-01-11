from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
from django.db.models import Q
import PyPDF2
from .funciones import ImportExp, ImportMatricula, ImportAsignaturas, GenAd
from .forms import AlumnoForm
from .models import Alumno,Asignatura,AlumAsig,Amistad
import logging


def index(request):
    publi=GenAd()
    usuario=request.user.username
    latest_apuesta_list = AlumAsig.objects.filter(uid__uid=usuario,passed=False).exclude(amount=0)
    latest_apuestaamigo_list=AlumAsig.objects.filter(uid__uid=None).exclude(amount=0)
    ## SACAMOS APUESTAS DE AMIGOS QUE SE ENCUENTRAN EN EL UID2 DE LA CLASE AMISTAD
    friends = Amistad.objects.filter(uid1__uid=usuario,solicitud=1)
    friends=friends.values_list('uid2_id', flat=True)
    for f in friends:
        try:
            amigo=Alumno.objects.get(id=f)
            latest_fapuesta_list = AlumAsig.objects.filter(uid__uid=amigo,passed=False).exclude(amount=0)
            latest_apuestaamigo_list=latest_apuestaamigo_list | latest_fapuesta_list
        except:
            pass
    ## SACAMOS APUESTAS DE AMIGOS QUE SE ENCUENTRAN EN EL UID1 DE LA CLASE AMISTAD Y LAS ENLAZAMOS CON LAS ANTERIORES
    friends = Amistad.objects.filter(uid2__uid=usuario,solicitud=1)
    friends=friends.values_list('uid1_id', flat=True)
    for f in friends:
        try:
            amigo=Alumno.objects.get(id=f)
            latest_fapuesta_list = AlumAsig.objects.filter(uid__uid=amigo,passed=False).exclude(amount=0)
            latest_apuestaamigo_list=latest_apuestaamigo_list | latest_fapuesta_list
        except:
            pass
    context = {'latest_apuesta_list': latest_apuesta_list, 'latest_apuestaamigo_list':latest_apuestaamigo_list, 'publi':publi}
    #ImportAsignaturas()     ##ACTIVAR SOLO PARA DAR SOPORTE A CARRERAS NUEVAS
    return render(request,'polls/index.html',context)

def detail(request, sid, uid):
    publi=GenAd()
    if request.user.is_authenticated:
        apuesta=get_object_or_404(AlumAsig,sid__sid=sid,uid__uid=uid)
        context = {'apuesta': apuesta,'publi':publi}
        return render(request,'polls/detalle.html',context)
    else:
        redirect('polls:login')

def apostar(request):
    publi=GenAd()
    if request.user.is_authenticated:
        usuario=Alumno.objects.get(uid=request.user.username)
        latest_asignatura_list=AlumAsig.objects.filter(uid=usuario,passed=False)
        context = {'latest_asignatura_list': latest_asignatura_list,'publi':publi}
        return render(request,'polls/menuapuesta.html',context)

    return redirect('polls:login')

def apostarasig(request, sid):
    publi=GenAd()
    if request.method == "POST":
        try:
            apuesta = get_object_or_404(AlumAsig,uid__uid=request.user.username,sid__sid=sid)
            alumno = Alumno.objects.get(uid=request.user.username)
            monedas     = int(request.POST['ncoins'])
            nota      = request.POST['nminima']

            if(monedas>(alumno.coins+apuesta.amount)):
                return render(request,'polls/apuesta.html',{'error_message':"No tienes suficientes monedas para realizar esa apuesta.",'asignatura':apuesta.sid,'publi':publi})
            if(monedas<=0):
                return render(request,'polls/apuesta.html',{'error_message':"Introduce un número de monedas superior a cero.",'asignatura':apuesta.sid,'publi':publi})

            else:
                alumno.coins = alumno.coins + apuesta.amount - monedas
                alumno.save()
                apuesta.amount = monedas
                apuesta.nminima = nota
                apuesta.save()
                
                return redirect('polls:detail',sid=sid,uid=request.user.username)
            
        except ValueError:
            return render(request,'polls/apuesta.html',{'error_message':"No has introducido un valor de monedas válido.",'asignatura':apuesta.sid,'publi':publi})

    if request.user.is_authenticated:
        asignatura=get_object_or_404(Asignatura,sid=sid)
        context = {'asignatura': asignatura,'publi':publi}
        return render(request,'polls/apuesta.html',context)

    return redirect('polls:login')

def registro(request):
    publi=GenAd()
    if request.method == "POST":
        logging.debug(request.POST['ac_politica'])
        usuario     = request.POST['usuario']
        nombre      = request.POST['nombre']
        apellidos    = request.POST['apellidos']
        email       = request.POST['email']
        contrasena  = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']
        carrera     = request.POST['carrera']

        if(contrasena!=contrasena2):
            return render(request,'polls/registro.html',{'error_message':"Las contraseñas no coinciden.",'publi':publi})

        if(User.objects.filter(username=usuario).exists()):
            return render(request,'polls/registro.html',{'error_message':"Ese nombre de usuario ya está en uso.",'publi':publi})
        else:
            if(User.objects.filter(email=email).exists()):
                return render(request,'polls/registro.html',{'error_message':"Ese correo electrónico ya está en uso.",'publi':publi})
            else:
                    user = User.objects.create_user(usuario,email,contrasena)
                    user.save()

        alum=Alumno.objects.create(
            uid = usuario,
            name = nombre,
            surname = apellidos,
            email = email,
            career = carrera,
        )
        alum.save()
        return redirect('polls:login')

    return render(request, 'polls/registro.html', {'publi':publi})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('polls:index')

def login(request):
    publi=GenAd()
    if request.method == "POST":
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        user = authenticate(username=usuario,password=contrasena)
        if user is not None:
            do_login(request, user)
            return redirect('polls:index')
        else:
            return render(request,'polls/iniciosesion.html',{'error_message':"Nombre de usuario o contraseña incorrectos.",'publi':publi})
    return render(request, "polls/iniciosesion.html",{'publi':publi})

def profile(request):
    publi=GenAd()
    if request.user.is_authenticated:
        usuario=request.user.username
        alumno=get_object_or_404(Alumno,uid=usuario)
        latest_asignatura_list = AlumAsig.objects.filter(uid__uid=usuario, passed=False)
        context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list,'publi':publi}
        return render(request,'polls/perfil.html',context)
    else:
        redirect('polls:login')

def SubirExpediente(request):
    publi=GenAd()
    if request.user.is_authenticated:
        usuario=request.user.username
        alumno=get_object_or_404(Alumno,uid=usuario)
        latest_asignatura_list = AlumAsig.objects.filter(uid__uid=usuario, passed=False)
        if request.method == 'POST':
            form = AlumnoForm(request.POST,request.FILES, instance=alumno)
            if form.is_valid():
                form.save()
                if (alumno.exp):
                    reward = ImportExp(str(alumno.exp.path),alumno)
                    if reward==-1:
                        context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi, 'error_message':"Has subido un expediente no válido."}
                        return render(request, 'polls/subirfichero.html', context)
                    else:
                        monedas = alumno.coins
                        alumno.coins = monedas+reward
                        alumno.save()
                        if (alumno.coins == 0):
                            alumno.coins=100                ## EL ALUMNO DEBE PODER SEGUIR JUGANDO.
                            alumno.save()
                        return redirect('polls:profile')
                else:
                    context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi, 'error_message':"No has subido ningún archivo."}
                    return render(request, 'polls/subirfichero.html', context)
        else:
            form = AlumnoForm()
        context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi}
        return render(request, 'polls/subirfichero.html', context)
    else:
        redirect('polls:login')

def SubirMatricula(request):
    publi=GenAd()
    if request.user.is_authenticated:
        usuario=request.user.username
        alumno=get_object_or_404(Alumno,uid=usuario)
        latest_asignatura_list = AlumAsig.objects.filter(uid__uid=usuario, passed=False)
        if request.method == 'POST':
            form = AlumnoForm(request.POST,request.FILES, instance=alumno)
            if form.is_valid():
                form.save()
                if (alumno.exp):
                    status = ImportMatricula(str(alumno.exp.path),alumno)
                    if status==0:
                        return redirect('polls:profile')
                    if status==1:
                        context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi, 'error_message':"Has subido una matrícula no válida."}
                        return render(request, 'polls/subirmatricula.html', context)
                else:
                    context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi, 'error_message':"No has subido ningún archivo."}
                    return render(request, 'polls/subirmatricula.html', context)
        else:
            form = AlumnoForm()
        context = {'alumno': alumno, 'latest_asignatura_list': latest_asignatura_list, 'form':form,'publi':publi}
        return render(request, 'polls/subirmatricula.html', context)
    else:
        redirect('polls:login')


def delete(request):
    publi=GenAd()
    if request.user.is_authenticated:
        if request.method == "POST":
            password1 = request.POST['password1']   # Contraseña
            password2 = request.POST['password2']   # Verificar contraseña
            user = request.user.username
            user = authenticate(username=user, password=password1)

            if password1 == password2:
                if user is not None:
                    u = Alumno.objects.get(uid=user)
                    user.delete()
                    u.delete()
                    do_logout(request)
                    return render(request,'polls/cuentaeliminada.html')
                    #return redirect('polls:cuentaeliminada')
                else:
                    return render(request,'polls/eliminarcuenta.html',{'error_message':"Contraseña incorrecta.",'publi':publi})   
            else: return render(request, 'polls/eliminarcuenta.html',{'error_message':"Las contraseñas que usted ha introducido no coinciden",'publi':publi})    
        
        return render(request,'polls/eliminarcuenta.html',{'publi':publi})
    else:
        redirect('polls:login')

def buscador(request):
    publi=GenAd()
    if request.user.is_authenticated:
        if request.method == "POST":
            u = request.POST['user']
            usuario = Alumno.objects.filter(uid__istartswith=u)
            user=Alumno.objects.get(uid=request.user.username)

            return render(request, 'polls/mostrarusuario.html', {"usuario":usuario,'publi':publi})
            
        return render(request,'polls/buscarusuario.html',{'publi':publi})

    else:
        return redirect('polls:login')


def solicitar(request):
    publi=GenAd()
    if request.user.is_authenticated:
        if request.method == "POST":
            usuario = request.POST['usuario']

            user=request.user.username

            uid1 = Alumno.objects.get(uid=user)
            uid2 = Alumno.objects.get(uid=usuario)

            Amistad.objects.create(
                solicitud = 0,      #pendiente de aceptar
                uid1 = uid1,
                uid2 = uid2,
            )

            if request.POST['perfil']=="perfil":
                return redirect('polls:perfilext',usuario=uid2.uid)

            return redirect('polls:buscarusuario')
        
        return render(request, 'polls/mostrarusuario.html', {"usuario":usuario,'publi':publi})

    else:
        return redirect('polls:login')


def aceptar(request):
    publi=GenAd()
    if request.user.is_authenticated:
        user = request.user.username
        amistad = Amistad.objects.filter(uid2__uid=user, solicitud=0)
        if request.method == "POST":
            agregar = request.POST['agregar']
            emisor = request.POST['emisor']
            amigo = Amistad.objects.get(uid1__uid=emisor, uid2__uid=user)
            
            if agregar == "Aceptar":
                amigo.solicitud = 1
                amigo.save()

            else:
                amigo.delete()

            amistad = Amistad.objects.filter(uid2__uid=user,solicitud=0)
            return render(request,'polls/notificaciones.html', {"amistad":amistad,'publi':publi})

        return render(request,'polls/notificaciones.html', {"amistad":amistad,'publi':publi})
    else:
        return redirect('polls:login')

def buscador_amigo(request):
    publi=GenAd()
    if request.user.is_authenticated:
        user = request.user.username
        amistad1 = Amistad.objects.filter(solicitud=1,uid1__uid=user)
        amistad2 = Amistad.objects.filter(solicitud=1,uid2__uid=user)
        if request.method ==  "POST":
            amigo = request.POST['amigo']     
            usuario = Alumno.objects.get(uid=amigo)

            return redirect('polls:perfilext',usuario=usuario.uid)

        return render(request,'polls/veramigos.html',{"amistad1":amistad1,"amistad2":amistad2,'publi':publi})

    else:
        return redirect('polls:login')

def perfilext(request,usuario):
    publi=GenAd()
    if request.user.is_authenticated:
        usuario=Alumno.objects.get(uid=usuario)
        user = request.user.username
        amistad1 = Amistad.objects.filter(uid1__uid=user,uid2__uid=usuario.uid).exists()
        amistad2 = Amistad.objects.filter(uid2__uid=user,uid1__uid=usuario.uid).exists()
        latest_asignatura_list = AlumAsig.objects.filter(uid__uid=usuario, passed=False)
        if (amistad1 or amistad2):
            noamistad=False
        else:
            noamistad=True
        
        return render(request,'polls/perfilext.html',{"alumno":usuario,"noamistad":noamistad,"latest_asignatura_list":latest_asignatura_list,'publi':publi})

    else:
        return redirect('polls:login')


def politica(request):
    publi=GenAd()
    return render(request,'polls/politicaprivacidad.html',{'publi':publi})

def aboutus(request):
    publi=GenAd()
    return render(request,'polls/aboutus.html',{'publi':publi})

def contactanos(request):
    publi=GenAd()
    return render(request,'polls/contacto.html',{'publi':publi})

