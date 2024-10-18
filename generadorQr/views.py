import random
import string
import qrcode
from PIL import Image
from django.shortcuts import render
import os
from django.conf import settings
import json

# Función para generar un código alfanumérico complejo de 12 dígitos
def generate_random_code(length=12):
    letters = string.ascii_letters  # Letras (mayúsculas y minúsculas)
    digits = string.digits  # Números
    special_characters = "!@#$%^&"  # Caracteres especiales
    all_characters = letters + digits + special_characters  # Combina todos los caracteres

    # Asegurarse de que el código tenga al menos un carácter de cada tipo
    code = [
        random.choice(letters),           # Al menos una letra
        random.choice(digits),            # Al menos un número
        random.choice(special_characters), # Al menos un carácter especial
    ]

    # Rellenar el resto del código hasta alcanzar la longitud deseada
    code += random.choices(all_characters, k=length - 3)

    # Mezclar los caracteres para que el patrón sea aleatorio
    random.shuffle(code)

    return ''.join(code)

# Función para guardar el código en un archivo JSON
def save_to_json(qr_code, qr_image_url, pdf_url):
    json_file_path = os.path.join(settings.BASE_DIR, 'qr_codes_data.json')

    # Verificar si el archivo JSON ya existe y tiene contenido válido
    if os.path.exists(json_file_path):
        try:
            # Intentar cargar el contenido del archivo
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
        except (json.JSONDecodeError, ValueError):
            # Si el archivo está vacío o mal formado, inicializar una lista vacía
            data = []
    else:
        # Si el archivo no existe, inicializar una lista vacía
        data = []

    # Añadir el nuevo código QR al archivo JSON
    data.append({
        "code": qr_code,
        "qr_image": qr_image_url,
        "pdf": pdf_url,
    })

    # Guardar los datos actualizados en el archivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_qr_code(request):
    # Generar un código alfanumérico de 12 dígitos
    random_code = generate_random_code()

    # Crear el código QR con el código alfanumérico
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(random_code)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill='black', back_color='white').convert('RGB')
    qr_code_image = qr_code_image.resize((371, 348))

    # Abrir la imagen base donde vas a insertar el QR
    base_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'entrada.jpg')
    base_image = Image.open(base_image_path)  # Abre la imagen

    # Pegar el QR en la imagen base
    base_image.paste(qr_code_image, (143, 180))

    # Guardar la imagen resultante en una carpeta de imágenes
    output_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')  # Cambiado para usar MEDIA_ROOT
    os.makedirs(output_folder, exist_ok=True)  # Crea la carpeta si no existe
    output_file = os.path.join(output_folder, f'qr_{random_code}.png')
    base_image.save(output_file)

    # Generar la URL para la imagen
    qr_image_url = f'{settings.MEDIA_URL}qr_codes/qr_{random_code}.png'  # Cambiado para usar MEDIA_URL

    # Guardar el PDF en otra carpeta específica para PDFs
    pdf_output_folder = os.path.join(settings.MEDIA_ROOT, 'qr_pdfs')
    os.makedirs(pdf_output_folder, exist_ok=True)  # Crea la carpeta si no existe
    pdf_output_file = os.path.join(pdf_output_folder, f'qr_{random_code}.pdf')
    
    # Verificar si la imagen tiene canal alfa (transparencia) y convertirla a RGB si es necesario
    if base_image.mode == "RGBA":
        base_image = base_image.convert("RGB")

    # Guardar la imagen como PDF
    base_image.save(pdf_output_file, "PDF", resolution=100.0)

    # Generar la URL para el PDF
    pdf_url = f'{settings.MEDIA_URL}qr_pdfs/qr_{random_code}.pdf'

    # Guardar el código QR y la URL en un archivo JSON
    save_to_json(random_code, qr_image_url, pdf_url)

    # Pasar el código, la URL de la imagen y la URL del PDF a la plantilla
    return render(request, 'generadorQr/success.html', {
        'random_code': random_code,
        'qr_image_url': qr_image_url,
        'pdf_file': pdf_url,
    })
