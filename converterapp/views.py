from django.shortcuts import render, redirect
from .forms import FileConvertForm
import os
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.

def about(request):
    return render(request, 'about.html')

def index(request):
    form = FileConvertForm()
    
    context = {
        'form': form
    }
    return render(request, 'index.html', {"form": form})

def convert(request):
    if request.method != 'POST':
        return redirect('index')
        
    if request.method == 'POST':
        form = FileConvertForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['input_file']
            convert_to = form.cleaned_data['convert_to']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = fs.path(filename)
            messages.success(request, 'File uploaded successfully.')
            
            
            try:
                # 🚨 TO-DO: Call your conversion function here, writing to output_file_path
                # Example: run_conversion(uploaded_file_path, output_file_path, target_format)
                
                # Assuming the conversion function is successful and writes the file:
                # ... Your conversion code here ...
                
                # Clean up the original uploaded file (CRITICAL STEP)
                fs.delete(filename) 
                
                # Redirect to the new download URL with the filename
                return redirect('download', filename=output_filename)
                
                
            except Exception as e:
                fs.delete(filename)
                messages.error(request, f"conversion failed:{e}")
                return redirect('index')
                
                
          
    else:
       return redirect('index')