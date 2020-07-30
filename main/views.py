from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View

def home(request):
    template = "main/home.html"
    return render(request, template)

def help_view(request):
    template = "main/help.html"
    return render(request, template)

def about_view(request):
    template = "main/about.html"
    return render(request, template)

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chart.html', {})

def get_data(request, *args, **kwargs):
    data = [1, 2, 3, 4, 5]
    labels = ["Red", "Blue", "Yellow", "Green", "Purple"]
    content = {
        'data': data,
        'labels': labels,
    }
    return JsonResponse(content)
