import os
from django.http import HttpResponse, HttpResponseBadRequest
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .forms import TableroForm, ArchivoForm
from .problema_caballos import ProblemaCaballos, mostrar_tableros

def index(request):
    return render(request, 'index.html')

def resolver_tablero(request):
    if request.method == 'POST':
        form = TableroForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            problema = ProblemaCaballos(n)
            max_caballos, soluciones = problema.resolver()

            generated_dir = os.path.join('media', 'generated')
            os.makedirs(generated_dir, exist_ok=True)

            if n <= 9:
                file_name = os.path.join(generated_dir, f"CABAL_0{n}.html")
            else:
                file_name = os.path.join(generated_dir, f"CABAL_{n}.html")

            with open(file_name, "w") as archivo:
                archivo.write("<html><body>\n")
                archivo.write(f"<h1>Resultados para tablero de tamaño {n}x{n}</h1>\n")
                archivo.write(f"<p>Número máximo de caballos colocados: {max_caballos}</p>\n")
                archivo.write(f"<p>Número de soluciones: {len(soluciones)}</p>\n")

                for solution in soluciones:
                    mostrar_tableros(solution, archivo)
                    archivo.write("<br><br>\n")  # Salto de línea entre tableros

                archivo.write("</body></html>\n")

            return render(request, 'resultado.html', {
                'form': form,
                'max_caballos': max_caballos,
                'soluciones': soluciones,
                'n': n,
                'file_name': file_name,
            })
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
