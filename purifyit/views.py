from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import subprocess
import os
import shutil
# Create your views here.

def index(request):
    if request.method == "POST":
        free_storage()
        uploaded_img = request.FILES['img']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_img.name, uploaded_img)
        url = fs.url(file_name)
        print(file_name)
        print(url)
        script_name = 'GFPGAN/inference_gfpgan.py'
        command_to_run = 'python ' + script_name + ' -i ' + "static/purifyit/media/"+ file_name + ' -o static/purifyit/results -v 1.3 -s 2'
        
        try:
            output = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            output = e.output
        print(output)
        return render(request, 'purifyit/index.html', {
            "og_img" : file_name,
            "restored_img": file_name
        })
    return render(request, 'purifyit/index.html')

def free_storage():

    media_path = r"static/purifyit/media/"
    for file_name in os.listdir(media_path):
        # construct full file path
        file_path = media_path + file_name
        if os.path.isfile(file_path):
            print('Deleting file:', file_name)
            os.remove(file_path)
        
    path = r"static/purifyit/results/"
    for dir_name in os.listdir(path):
        # construct full directory path
        dir_path = path + dir_name
        if os.path.isdir(dir_path):
            print('Deleting Dir:', dir_name)
            shutil.rmtree(dir_path)
