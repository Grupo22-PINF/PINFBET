import PyPDF2
import xlrd, tabula
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
import os, logging
from random import randint
from tabula import convert_into

from .models import Alumno,Asignatura,AlumAsig,Publicidad

def ImportExp(ruta,usuario): 
        # Creating a pdf file object
	try:
                convert_into(ruta,'media/conversion.csv', pages='all')
                safe = pd.read_csv('media/conversion.csv',encoding='latin-1')
                logging.debug(str(safe.columns[0]))
                if (str(safe.columns[0])=='CÃ³digo  AsignaturaCred Dur Tip AÃ±o'):
                        file = pd.read_csv('media/conversion.csv',encoding='latin-1')
                        file.to_excel('media/conversion.xls', index = False,header=False) 
                        loc = 'media/conversion.xls'
                        wb = xlrd.open_workbook(loc)
                        sheet = wb.sheet_by_index(0)
                        count = 0;
                        for i in range(sheet.nrows):
                                if (sheet.cell_value(i,1) != 'SUSPENSO') and (sheet.cell_value(i,1) != 'NO PRESENTADO') and (sheet.cell_value(i,1) != 'Unnamed: 2'):
                                        code = str(sheet.cell_value(i,0))[0:8]
                                        logging.debug(code)
                                        asig = Asignatura.objects.filter(sid=code)
                                        if asig.exists():                                       ##ASIGNATURA SOPORTADA POR LA PLATAFORMA
                                                asig=Asignatura.objects.get(sid=code)
                                                logging.debug("Asignatura OK")
                                                nota = float(str(sheet.cell_value(i,3))[0])+(float(str(sheet.cell_value(i,3))[2])/10.0)
                                                AlAs=AlumAsig.objects.filter(uid=usuario,sid=asig,passed=False)
                                                if AlAs.exists():                                ##ALUMNO YA MATRICULADO, ASIGNATURA POR APROBAR
                                                        logging.debug('Relacion existente')
                                                        AlAs=AlumAsig.objects.get(uid=usuario,sid=asig)
                                                        if AlAs.nminima<=nota:
                                                                logging.debug('Aprobado')
                                                                AlAs.grade=nota
                                                                AlAs.passed=True
                                                                AlAs.save()
                                                                count=((AlAs.nminima)*(AlAs.grade/10)*AlAs.amount+AlAs.amount)+count
                                                        else:
                                                                logging.debug('Suspenso')
                                                                AlAs.grade=0
                                                                AlAs.amount=0
                                                                AlAs.save()
                                                else:                                           ##ASIGNATURA DE CURSOS ANTERIORES, YA APROBADAS
                                                        AlAs=AlumAsig.objects.filter(uid=usuario,sid=asig,passed=True)
                                                        if AlAs.exists():                       ##EVITAMOS DUPLICAR LA RELACIÓN
                                                                logging.debug('Relacion existente, ya aprobada')
                                                        else:
                                                                logging.debug('No existe esta relacion aun')
                                                                new = AlumAsig.objects.create(
                                                                        uid = usuario,
                                                                        sid = asig,
                                                                        amount = 0,
                                                                        grade = nota,
                                                                        passed = True,
                                                                )
                                                                count=count+100
                                                                new.save()
                        os.remove(ruta)
                        os.remove('media/conversion.csv')
                        os.remove('media/conversion.xls')
                        usuario.doc = None
                        usuario.save()
                        logging.debug(count)
                        return count

                else:
                        logging.debug("Expediente no válido")
                        os.remove(ruta)
                        os.remove('media/conversion.csv')
                        usuario.doc = None
                        usuario.save()
                        return -1

	except Exception as e:
		logging.debug("Expediente no válido (EXCEPCION)")
		logging.exception(e)
		os.remove(ruta)
		usuario.doc = None
		usuario.save()
		return -1

def ImportMatricula(ruta,usuario):
        # Creating a pdf file object
        try:
                convert_into(ruta,'media/conversion.csv', pages='all')
                safe = pd.read_csv('media/conversion.csv',encoding='latin-1')
                logging.debug(str(safe.columns[2]))
                if (str(safe.columns[2])=='DATOS DE MATRICULA'):
                        file = pd.read_csv('media/conversion.csv',encoding='latin-1')
                        file.to_excel('media/conversion.xls', index = False,header=False) 
                        loc = 'media/conversion.xls'
                        wb = xlrd.open_workbook(loc)
                        sheet = wb.sheet_by_index(0)

                        for i in range(sheet.nrows):
                                code = str(sheet.cell_value(i,0))[0:8]
                                logging.debug(code)
                                asig = Asignatura.objects.filter(sid=code)
                                if asig.exists():                                       ##ASIGNATURA SOPORTADA POR LA PLATAFORMA
                                        asig=Asignatura.objects.get(sid=code)
                                        logging.debug("Asignatura OK")
                                        AlAs=AlumAsig.objects.filter(uid=usuario,sid=asig,passed=False)
                                        logging.debug(AlAs.exists())
                                        if not AlAs.exists():                                ##ALUMNO YA MATRICULADO
                                                logging.debug(code)
                                                logging.debug('No existe esta relacion aun')
                                                new = AlumAsig.objects.create(
                                                        uid = usuario,
                                                        sid = asig,
                                                        amount = 0,
                                                        grade = 0,
                                                        passed = False,
                                                )
                                                new.save()
                                        else:
                                                logging.debug("Alumno ya matriculado de esta asignatura.")


                        os.remove(ruta)
                        os.remove('media/conversion.csv')
                        os.remove('media/conversion.xls')
                        usuario.doc = None;
                        usuario.save()
                        return 0
                else:
                    logging.debug("Matrícula no válida")
                    os.remove(ruta)
                    os.remove('media/conversion.csv')
                    usuario.doc = None;
                    usuario.save()
                    return 1
        except Exception as e:
                logging.debug("Matrícula no válida (EXCEPCION)")
                logging.exception(e)
                os.remove(ruta)
                usuario.doc = None
                usuario.save()
                return 1

#### METODO USADO PARA DAR SOPORTE A NUEVAS CARRERAS.
#### SUBIR EN FORMATO .PDF LA PÁGINA DE ASIGNATURAS DE UNA CARRERA DADA, OBTENIDA EN http://asignaturas2.uca.es/
def ImportAsignaturas():
        # Creating a pdf file object
        tabula.io.convert_into('media/asigs.pdf','media/conversion.csv', pages='all')
        file = pd.read_csv('media/conversion.csv',encoding='latin-1')
        file.to_excel('media/conversion.xls', index = False,header=False)
        input("") ## Limpiar conversion.xls de forma manual. Asegurar que cada fila contiene nombre y código.
        loc = 'media/conversion.xls'
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        logging.debug(sheet.nrows)

        for i in range(sheet.nrows):
               code = str(sheet.cell_value(i,1))[0:8]
               logging.debug(code)
               if code:
                        asig = Asignatura.objects.filter(sid=code)
                        if not asig.exists():                                       ##ASIGNATURA SOPORTADA POR LA PLATAFORMA
                                new = Asignatura.objects.create(
                                        sid = code,
                                        name = str(sheet.cell_value(i,0)),
                                )
                                new.save()
                        else:
                                logging.debug("Asignatura existente.")

        os.remove('media/asigs.pdf')
        os.remove('media/conversion.csv')
        os.remove('media/conversion.xls')
        return 0

def GenAd():
        count=Publicidad.objects.count()
        publi=Publicidad.objects.all()[randint(0,count-1)]

        return publi