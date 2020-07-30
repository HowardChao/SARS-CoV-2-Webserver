from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View

from .forms import ParametersForm, RunModelForm

from .model import parameters
from .model import person
from .model import vaccine
from .model import model


global data
global labels
data = []
labels = []

def home(request):
    global data
    if request.method == 'POST':
        print("POST!")
        if "parameters_submit_btn" in request.POST:
            print("parameters_submit_btn!")
            form = ParametersForm(request.POST)
            if form.is_valid():
                BMP_IDX_CASE_NUM = form.cleaned_data["BMP_IDX_CASE_NUM"]
                BMP_SIMULATION_DAY = form.cleaned_data["BMP_SIMULATION_DAY"]





        if "run_model" in request.POST:
            print("run_model!")
            form = RunModelForm(request.POST)
            print(form)
            print(form.is_valid())
            if form.is_valid():
                print("Form is valid")
                md = model.VaccineModel()
                transmission_gp = md.transmission_gp
                data.append(len(transmission_gp))
                for i in range(10):
                    md.one_day_passed()
                    transmission_gp = md.transmission_gp
                    data.append(len(transmission_gp))
                    labels.append("Day "+str(i))

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
    global data
    global labels
    # labels = ["Red", "Blue", "Yellow", "Green", "Purple"]
    content = {
        'data': data,
        'labels': labels,
    }
    return JsonResponse(content)
