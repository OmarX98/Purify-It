from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import subprocess
# Create your views here.

def index(request):
    if request.method == "POST":
        uploaded_img = request.FILES['img']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_img.name, uploaded_img)
        url = fs.url(file_name)
        print(file_name)
        script_name = 'GFPGAN/inference_gfpgan.py'
        command_to_run = 'python ' + script_name + ' -i ' + url[1:] + ' -o results -v 1.3 -s 2'
        
        try:
            output = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            output = e.output
        print(output)
        return render(request, 'purifyit/index.html', {
            "og_img" : file_name
        })
    return render(request, 'purifyit/index.html')