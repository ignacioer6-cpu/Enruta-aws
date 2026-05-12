from django.shortcuts import render
from django.http import HttpResponse
from .db import ConexionDB

def inicio(request):
    return render(request,'mi_app/inicio.html')

def registroC(request):
    return render(request,'mi_app/registroC.html')

def registroP(request):
    return render(request,'mi_app/registroP.html')

def procesar(request):
    if request.method == 'POST':
        run = request.POST.get('txt_run')
        nombres = request.POST.get('txt_nombres')
        apellidos = request.POST.get('txt_apellidos')
        correo = request.POST.get('txt_correo')
        clave = request.POST.get('txt_clave')
        tipo = request.POST.get('tipo_registro')

        if tipo not in ('conductor', 'pasajero'):
            return HttpResponse('Tipo de registro inválido', status=400)

        tabla = 'conductor' if tipo == 'conductor' else 'pasajero'
        plantilla = 'mi_app/registroC.html' if tipo == 'conductor' else 'mi_app/registroP.html'

        conexion = ConexionDB()
        sintaxisValidar = f"""
            select 1 from {tabla} where run=%s
        """
        if conexion.verificar(sintaxisValidar, (run,)):
            contexto = {
                'msg': 'Casi... Existe un Registro asociado',
                'color': 'red'
            }
            return render(request, plantilla, contexto)

        sintaxisSQL = f"""
            insert into {tabla} (run, clave, nombres, apellidos, correo) values(%s,%s,%s,%s,%s)
        """
        conexion.ejecutar(sintaxisSQL, (run, clave, nombres, apellidos, correo))

        contexto = {
            'msg': 'Registro Insertado Correctamente!',
            'color': 'green'
        }
        return render(request, plantilla, contexto)

    return render(request, 'mi_app/registroC.html')