import os
from django.http import HttpResponse, HttpResponseBadRequest
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .forms import TableroForm, ArchivoForm
from .problema_caballos import ProblemaCaballos, mostrar_tableros
from .problema_reinas import ProblemaReinas, mostrar_tableros_reinas
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def resolver_tablero(request):
    if request.method == 'POST':
        form = TableroForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            estilo = request.POST.get('estilo', 'normal')
            problema = ProblemaCaballos(n)
            max_caballos, soluciones = problema.resolver()

            generated_dir = os.path.join('media', 'generated')
            os.makedirs(generated_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = os.path.join(generated_dir, f"CABAL_{n:02}_{timestamp}.html")

            with open(file_name, "w") as archivo:
                archivo.write("<html><body>\n")
                archivo.write(f"<h1>Resultados para tablero de tamaño {n}x{n}</h1>\n")
                archivo.write(f"<p>Número máximo de caballos colocados: {max_caballos}</p>\n")
                archivo.write(f"<p>Número de soluciones: {len(soluciones)}</p>\n")

                for solution in soluciones:
                    mostrar_tableros(solution, archivo, estilo)
                    archivo.write("<br><br>\n")

                archivo.write("</body></html>\n")

            context = {
                'form': form,
                'max_caballos': max_caballos,
                'soluciones': soluciones,
                'n': n,
                'file_name': file_name,
            }

            if 'download_pdf' in request.POST:
                return generar_pdf(file_name)
            else:
                return render(request, 'resultado.html', context)
    else:
        form = TableroForm()

    return render(request, 'resolver_tablero.html', {'form': form})

def generar_pdf(html_file_path):
    with open(html_file_path, "r") as archivo_html:
        html_content = archivo_html.read()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultados_caballos.pdf"'

    pisa_status = pisa.CreatePDF(
        src=BytesIO(html_content.encode('utf-8')),
        dest=response,
    )

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response

#Tarjetas
from django.core.files.storage import FileSystemStorage
from .tarjetas import cards_problem, leer_archivo, cargar_archivo

def cargar_archivo_view(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            # Verifica que el archivo tenga la extensión .in
            if not archivo.name.endswith('.in'):
                return HttpResponseBadRequest('Error: El archivo debe tener la extensión .in')
            
            try:
                # Leer y validar el contenido del archivo
                arreglo = leer_archivo(archivo)

                # Resolver el problema con las tarjetas
                nuevos_indices = cards_problem(arreglo)

                # Preparar las tarjetas para mostrarlas
                tarjetas = [{'valor': arreglo[i], 'estado': 'conservada' if i in nuevos_indices else 'eliminada'} for i in range(len(arreglo))]

                return render(request, 'resultado_tarjetas.html', {'tarjetas': tarjetas})

            except ValueError as e:
                # Captura errores relacionados con el formato del archivo
                return HttpResponseBadRequest(f'Error en el archivo: {e}')
            except Exception as e:
                # Captura cualquier otro tipo de error inesperado
                return HttpResponseBadRequest(f'Error inesperado al procesar el archivo: {e}')
        else:
            return HttpResponseBadRequest('Error: Formulario inválido')
    
    else:
        form = ArchivoForm()
    
    return render(request, 'cargar_archivo.html', {'form': form})

def descargar_archivo_view(request):
    file_name = request.GET.get('file')
    fs = FileSystemStorage()
    if fs.exists(file_name):
        with fs.open(file_name) as archivo:
            response = HttpResponse(archivo, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    return redirect('cargar_archivo')

def generar_pdf_tarjetas(tarjetas):
    template_path = 'resultado_pdf.html'
    
    # Añadimos más datos al contexto, como la fecha de generación
    context = {
        'tarjetas': tarjetas,
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
    }
    
    # Convertir la plantilla HTML a cadena
    html = render_to_string(template_path, context)

    # Crear respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tarjetas.pdf"'
    
    # Crear el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si hay errores, devolver mensaje de error
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: {}'.format(pisa_status.err))
    
    # Retornar el archivo PDF si todo salió bien
    return response

def descargar_pdf_view(request):
    if request.method == 'POST':
        tarjetas_json = request.POST.get('tarjetas')
        if tarjetas_json:
            try:
                tarjetas = json.loads(tarjetas_json)
                return generar_pdf_tarjetas(tarjetas)
            except json.JSONDecodeError as e:
                return HttpResponseBadRequest(f'Error al decodificar JSON: {str(e)}')
        else:
            return HttpResponseBadRequest('No se recibieron datos de tarjetas.')
    return HttpResponseBadRequest('Método no permitido')


#Reinas

def resolver_reinas(request):
    if request.method == 'POST':
        form = TableroForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            estilo = request.POST.get('estilo', 'normal')
            problema = ProblemaReinas(n)
            num_soluciones, soluciones = problema.resolver()

            generated_dir = os.path.join('media', 'generated')
            os.makedirs(generated_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = os.path.join(generated_dir, f"REINA_{n:02}_{timestamp}.html")

            with open(file_name, "w") as archivo:
                archivo.write("<html><body>\n")
                archivo.write(f"<h1>Resultados para tablero de tamaño {n}x{n}</h1>\n")
                archivo.write(f"<p>Número de soluciones: {num_soluciones}</p>\n")

                for solution in soluciones:
                    mostrar_tableros_reinas(solution, archivo, estilo)
                    archivo.write("<br><br>\n")

                archivo.write("</body></html>\n")

            if 'download_pdf' in request.POST:
                return generar_pdf_reinas(file_name)

            return render(request, 'resultado_reinas.html', {
                'form': form,
                'num_soluciones': num_soluciones,
                'soluciones': soluciones,
                'n': n,
                'file_name': file_name,
            })
    else:
        form = TableroForm()

    return render(request, 'resolver_reinas.html', {'form': form})

def generar_pdf_reinas(html_file_path):
    with open(html_file_path, "r") as archivo_html:
        html_content = archivo_html.read()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultados_reinas.pdf"'

    pisa_status = pisa.CreatePDF(
        src=BytesIO(html_content.encode('utf-8')),
        dest=response,
    )

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response