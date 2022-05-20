from tkinter import Image
from django.conf import settings
from django.shortcuts import redirect, render
from subprocess import run, PIPE

from .forms import Imageforms
import sys
from django.core.files.storage import FileSystemStorage

def Home(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        fileurl = fs.open(filename)
        templateurl = fs.url(filename)
        image = run([sys.executable, 'Model.py', str(fileurl), str(filename)], shell=False, stdout=PIPE)
        gurl = image.stdout
        gurl = gurl.decode("utf-8")
        context = {'in_img':templateurl, 'out_img':gurl, 'form':Imageforms()}
        return render(request, 'index.html', context )

    context = {}
    context['form'] = Imageforms()

    return render(request, 'index.html', context)
