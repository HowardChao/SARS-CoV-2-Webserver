from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def home(request):
    template = "main/home.html"
    return render(request, template)

def help_view(request):
    template = "main/help.html"
    return render(request, template)

def about_view(request):
    template = "main/about.html"
    return render(request, template)
