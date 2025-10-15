from django.shortcuts import render, redirect
from .forms import FileConvertForm
import tempfile
from .utils import convert_doc_to_pdf, convert_to_png, supported_image_formats
from django.http import FileResponse, Http404
import os
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import subprocess


# Create your views here.

def about(request):
    return render(request, 'about.html')

def placeholder(request):
    return render(request, 'placeholder.html')
def index(request):
    form = FileConvertForm()
    

    return render(request, 'index.html', {"form": form})

def result(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'converted', filename)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    file_url = os.path.join(settings.MEDIA_URL, 'converted', filename)
    form = FileConvertForm()
    return render(request, 'result.html', {
        'file_url': file_url,
        'filename': filename,
        'form': form
    })




def convert(request):
    if request.method != 'POST':
        return redirect('index')

    form = FileConvertForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Invalid form submission.")
        return redirect('index')

    uploaded_file = form.cleaned_data['input_file']
    conversion_type = form.cleaned_data['convert_to']

    try:
        if conversion_type == 'pdf':
            pdf_relative_path = convert_doc_to_pdf(uploaded_file)
        elif conversion_type == 'png':
            if uploaded_file.name.endswith(supported_image_formats):
                pdf_relative_path = convert_to_png(uploaded_file)
            else:
                messages.error(request, "Your file type is not supported for conversion to PNG.")
                return redirect('index')

        filename = os.path.basename(pdf_relative_path)
        return redirect('result', filename=filename)

    except subprocess.CalledProcessError:
        messages.error(request, "Conversion failed: LibreOffice error.")
        return redirect('index')

    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return redirect('index')
    
    
    
    
def serve_converted_file(request, filename, key):
    # check secret key
    if key != DOWNLOAD_SECRET_KEY:
        raise Http404("File not found")

    file_path = os.path.join(settings.MEDIA_ROOT, 'converted', filename)
    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(open(file_path, 'rb'), as_attachment=True)