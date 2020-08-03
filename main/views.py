from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
from django.conf import settings

from . import utils_func
from . import tasks
from .forms import RunModelForm

from .model import parameters
from .model import person
from .model import vaccine
from .model import model

import json
import os
from django_q.tasks import async_task, result, fetch, AsyncTask, result_group
import django_q

import inspect
# global data
# global labels
# data = []
# labels = []

def home(request):
    template = "main/home.html"
    # analysis_code = utils_func.analysis_code_generator()
    # print("analysis_code: ", analysis_code)
    content = {
        'analysis_code': "Empty",
    }

    if request.method == 'POST':
        print("POST!")
        if "run_model" in request.POST:
            analysis_code = utils_func.analysis_code_generator()
            content = {
                'analysis_code': analysis_code,
            }
            utils_func.create_sample_directory(analysis_code)
            datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', analysis_code)

            json_file = os.path.join(datadir, "data.json")
            # transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
            # labels_file = os.path.join(datadir, "labels.json")
            with open(json_file, 'w') as f:
                json.dump({}, f)
            # with open(transmission_gp_sz_file, 'w') as f:
            #     json.dump([], f)
            # with open(labels_file, 'w') as f:
            #     json.dump([], f)
            print("run_model!")
            form = RunModelForm(request.POST)
            print(form)
            print(form.is_valid())
            if form.is_valid():

                input_params_json_file = os.path.join(datadir, "input_params.json")
                print("Form is valid")
                BMP_IDX_CASE_NUM = form.cleaned_data["BMP_IDX_CASE_NUM"]
                BMP_SIMULATION_DAY = form.cleaned_data["BMP_SIMULATION_DAY"]
                with open(input_params_json_file, 'w') as f:
                    json.dump({
                        "BMP_IDX_CASE_NUM": BMP_IDX_CASE_NUM,
                        "BMP_SIMULATION_DAY": BMP_SIMULATION_DAY,
                    }, f)
                # a = AsyncTask(tasks.start_analysis, datadir, group="id_"+analysis_code)
                # print("!!!! A: ", a)
                a = async_task(tasks.start_analysis, datadir, task_name="id_"+analysis_code)
                print("!!!! A: ", a)
    return render(request, template, content)

# def check_task_status(analysis_code):


def help_view(request):
    template = "main/help.html"
    return render(request, template)

def about_view(request):
    template = "main/about.html"
    return render(request, template)

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chart.html', {})

def get_data(request, slug_analysis_code, *args, **kwargs):
    # labels = ["Red", "Blue", "Yellow", "Green", "Purple"]
    datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', slug_analysis_code)

    json_file = os.path.join(datadir, "data.json")

    # transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
    # labels_file = os.path.join(datadir, "labels.json")

    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = json.load(f)
            # json.dump({}, f)
    else:
        data = {
            'labels': [],
            'totalInfected_sz': [],
            'currentInfected_sz': [],
            'newInfected_sz': [],
            'totalDeath_sz': [],
            'newDeath_sz': [],
            'totalRecovery_sz': [],
            'newRecovery_sz': [],
            'totalReachDay_sz': [],
            'newReachDay_sz': [],
        }

    # if os.path.isfile(transmission_gp_sz_file):
    #     with open(transmission_gp_sz_file) as f:
    #         data = json.load(f)
    # else:
    #     data = []
    #
    # if os.path.isfile(labels_file):
    #     with open(labels_file) as f:
    #         labels = json.load(f)
    # else:
    #     labels = []

    print("slug_analysis_code: ", slug_analysis_code)
    print("data: ", data)

    data['analysis_code'] = slug_analysis_code
    print("new data: ", data)

    # print("django_q_tasks.objects(): ", django_q_tasks.Success)

    # taskr = fetch("267d724c903f49cba48c9d0f835a70e5", cached=True)
    # print("$$$$$$$$$$$$", "267d724c903f49cba48c9d0f835a70e5", "   ", taskr)
    success = django_q.models.Success.objects
    success_all = success.all()
    task_status = False
    for success_itr in success_all:
        if ("id_"+slug_analysis_code == success_itr.name):
            task_status = True
            break
    data['task_status'] = task_status
    print("task_status: ", task_status)

    # check_task_status(slug_analysis_code)

    # content = {
    #     'analysis_code': slug_analysis_code,
    #     'data': data,
    #     'labels': labels,
    # }
    return JsonResponse(data)

def get_params_data(request, slug_analysis_code, *args, **kwargs):
    datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', slug_analysis_code)
    input_params_json_file = os.path.join(datadir, "input_params.json")

    if os.path.isfile(input_params_json_file):
        with open(input_params_json_file) as f:
            data = json.load(f)
    else:
        data = {
            'BMP_IDX_CASE_NUM': 0,
            'BMP_SIMULATION_DAY': 0,
        }

    # content = {
    #     'analysis_code': slug_analysis_code,
    #     'data': data,
    #     'labels': labels,
    # }
    return JsonResponse(data)
