from django.shortcuts import render
from django.http import HttpResponse
from .db import ConexionDB

def inicio(request):
    return render(request, 'mi_app/inicio.html')

def registroC(request):
    return render(request, 'mi_app/registroC.html')

def registroP(request):
    return render(request, 'mi_app/registroP.html')
def panel_admin(request):
    conexion = ConexionDB()
    # Consultamos ambas tablas
    conductores = conexion.consultar("SELECT * FROM conductor")
    pasajeros = conexion.consultar("SELECT * FROM pasajero")
    
    contexto = {
        'conductores': conductores,
        'pasajeros': pasajeros
    }
    return render(request, 'mi_app/panel.html', contexto)

def procesar(request):
    if request.method == 'POST':
        # 1. Capturar los datos del formulario
        run = request.POST.get('txt_run')
        nombres = request.POST.get('txt_nombres')
        apellidos = request.POST.get('txt_apellidos')
        correo = request.POST.get('txt_correo')
        clave = request.POST.get('txt_clave')
        tipo = request.POST.get('tipo_registro')

        # 2. Seguridad: Validar que el tipo sea estrictamente uno de los permitidos
        if tipo not in ('conductor', 'pasajero'):
            return HttpResponse('Tipo de registro inválido', status=400)

        # 3. Definir la tabla y plantilla según el tipo
        tabla = 'conductor' if tipo == 'conductor' else 'pasajero'
        plantilla = 'mi_app/registroC.html' if tipo == 'conductor' else 'mi_app/registroP.html'

        conexion = ConexionDB()
        
        # 4. Verificar si el RUN ya existe
        sintaxisValidar = f"SELECT 1 FROM {tabla} WHERE run = %s"
        
        if conexion.verificar(sintaxisValidar, (run,)):
            contexto = {
                'msg': 'Casi... Existe un Registro asociado a este RUN',
                'color': 'red'
            }
            return render(request, plantilla, contexto)

        # 5. Insertar el nuevo registro
        sintaxisSQL = f"""
            INSERT INTO {tabla} (run, clave, nombres, apellidos, correo) 
            VALUES (%s, %s, %s, %s, %s)
        """
        conexion.ejecutar(sintaxisSQL, (run, clave, nombres, apellidos, correo))

        contexto = {
            'msg': '¡Registro Insertado Correctamente!',
            'color': 'green'
        }
        return render(request, plantilla, contexto)

    # Si entran por GET, los mandamos al registro por defecto
    return render(request, 'mi_app/registroC.html')