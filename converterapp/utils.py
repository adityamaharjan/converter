import os
import subprocess
from PIL import Image
from django.conf import settings


base_format = ['JPG', 'jpeg', 'png', 'gif', 'bmp', 'webp']

supported_image_formats = tuple(format.upper() for format in base_format) + tuple(format.lower() for format in base_format)
def convert_doc_to_pdf(uploaded_file):


    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'converted')

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # uploaded file
    input_path = os.path.join(upload_dir, uploaded_file.name)
    with open(input_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # conversion
    subprocess.run([
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', output_dir,
        input_path
    ], check=True)

    base_name, _ = os.path.splitext(uploaded_file.name)
    output_pdf = base_name + '.pdf'
    output_pdf_path = os.path.join(output_dir, output_pdf)

    # remove file
    os.remove(input_path)

    if not os.path.exists(output_pdf_path):
        raise FileNotFoundError("Converted PDF not found after conversion.")

    # relative path
    return os.path.relpath(output_pdf_path, settings.MEDIA_ROOT)


def convert_to_png(uploaded_file):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'converted')

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    base_name, _ = os.path.splitext(uploaded_file.name)
    output_png = base_name + '.png'
    output_png_path = os.path.join(output_dir, output_png)

    # uploaded file
    input_path = os.path.join(upload_dir, uploaded_file.name)
    with open(input_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # conversion
    img = Image.open(input_path)
    img = img.convert('RGBA')  # Ensure image is in RGBA mode
    img.save(output_png_path, 'PNG')
    

    # remove file
    # os.remove(input_path)

    if not os.path.exists(output_png_path):
        raise FileNotFoundError("Converted PNG not found after conversion.")

    # relative path
    return os.path.relpath(output_png_path, settings.MEDIA_ROOT)