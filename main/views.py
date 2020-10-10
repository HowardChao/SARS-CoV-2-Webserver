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
import copy
# global data
# global labels
# data = []
# labels = []

def iterate(group, input_json, data):
    in_nput_json = copy.deepcopy(input_json)

# STR_YOUTH_RT = form.cleaned_data["STR_YOUTH_RT"]
# STR_ADULT_RT = form.cleaned_data["STR_ADULT_RT"]
# STR_ELDER_RT = form.cleaned_data["STR_ELDER_RT"]
#
# MIR_YOUTH_RT = form.cleaned_data["MIR_YOUTH_RT"]
# MIR_ADULT_RT = form.cleaned_data["MIR_ADULT_RT"]
# MIR_ELDER_RT = form.cleaned_data["MIR_ELDER_RT"]
#
# SR_YOUTH_48_RT = form.cleaned_data["SR_YOUTH_48_RT"]
# SR_ADULT_48_RT = form.cleaned_data["SR_ADULT_48_RT"]
# SR_ELDER_48_RT = form.cleaned_data["SR_ELDER_48_RT"]
# SR_YOUTH_N48_RT = form.cleaned_data["SR_YOUTH_N48_RT"]
# SR_ADULT_N48_RT = form.cleaned_data["SR_ADULT_N48_RT"]
# SR_ELDER_N48_RT = form.cleaned_data["SR_ELDER_N48_RT"]
#
# FR_YOUTH_RT = form.cleaned_data["FR_YOUTH_RT"]
# FR_ADULT_RT = form.cleaned_data["FR_ADULT_RT"]
# FR_ELDER_RT = form.cleaned_data["FR_ELDER_RT"]

    if in_nput_json['id'] == "Index Case":
        in_nput_json['pb'] = "1"
    elif in_nput_json['id'] == "Contact another person":
        in_nput_json['pb'] = "(" + str(data["CR_SAME_GRP"]) + ", " + str(data["CR_DIFF_GRP"]) + ")"
    elif in_nput_json['id'] == "Vaccinated":
        in_nput_json['pb'] = str(data["VR_"+group+"_RT"])
    elif in_nput_json['id'] == "Infected (vaccinated)":
        in_nput_json['pb'] = str(data["IR_"+group+"_V_RT"])
    elif in_nput_json['id'] == "Not infected (vaccinated)":
        in_nput_json['pb'] = str(1 - float(data["IR_"+group+"_V_RT"]))
    elif in_nput_json['id'] == "Not vaccinated":
        in_nput_json['pb'] = str(1 - float(data["VR_"+group+"_RT"]))
    elif in_nput_json['id'] == "Infected (not vaccinated)":
        in_nput_json['pb'] = str(data["IR_"+group+"_NV_RT"])
    elif in_nput_json['id'] == "Not infected (not vaccinated)":
        in_nput_json['pb'] = str(1 - float(data["IR_"+group+"_NV_RT"]))
    elif in_nput_json['id'] == "Seek medical treatment":
        in_nput_json['pb'] = str(data["STR_"+group+"_RT"])
    elif in_nput_json['id'] == "Taken Antiviral":
        in_nput_json['pb'] = str(data["MIR_"+group+"_RT"])
    elif in_nput_json['id'] == "Hospitalization (antiviral)":
        in_nput_json['pb'] = str(data["SR_"+group+"_48_RT"])
    elif in_nput_json['id'] == "Death (antiviral, hospitalized)":
        in_nput_json['pb'] = str(data["FR_"+group+"_RT"])
    elif in_nput_json['id'] == "Recovery (antiviral, hospitalized)":
        in_nput_json['pb'] = str(1 - float(data["FR_"+group+"_RT"]))
    elif in_nput_json['id'] == "Recovery (antiviral, not hospitalized)":
        in_nput_json['pb'] = str(1 - float(data["SR_"+group+"_48_RT"]))
    elif in_nput_json['id'] == "Not taken Antiviral":
        in_nput_json['pb'] = str(1 - float(data["MIR_"+group+"_RT"]))
    elif in_nput_json['id'] == "Hospitalization (no antiviral)":
        in_nput_json['pb'] = str(data["SR_"+group+"_N48_RT"])
    elif in_nput_json['id'] == "Death (no antiviral, hospitalized)":
        in_nput_json['pb'] = str(data["FR_"+group+"_RT"])
    elif in_nput_json['id'] == "Recovery (no antiviral, hospitalized)":
        in_nput_json['pb'] = str(1 - float(data["FR_"+group+"_RT"]))
    elif in_nput_json['id'] == "Recovery (no antiviral, not hospitalized)":
        in_nput_json['pb'] = str(1 - float(data["SR_"+group+"_N48_RT"]))
    print("in_nput_json: ", in_nput_json)
    if len(in_nput_json['children']) != 0:
        for idx, value in enumerate(in_nput_json['children']):
            print("   > > > : ", idx)
            in_nput_json['children'][idx] = iterate(group, value, data)
    return in_nput_json

    # for (k, v) in input_json.items():
    #     print("      Key: " + k)
    #     if k == "name":
    #         print("      v", v)
    #     elif k == "Vaccinated":
    #         pass
    #     elif k == "Vaccinated":
    #         pass
    #     elif k == "Contact another person":
    #         pass
    #     elif k == "Contact another person":
    #         pass
    #     elif k == "Contact another person":
    #         pass
    #     elif k == "Contact another person":
    #         pass
    #     elif k == "Contact another person":
    #         pass
    #     elif k == "children":
    #         for elem in v:
    #             iterate(elem)


def home(request):
    template = "main/home.html"
    # analysis_code = utils_func.analysis_code_generator()
    # print("analysis_code: ", analysis_code)
    content = {
        'analysis_code': "Empty",
        'button_clicked': "False",
        'BMP_IDX_CASE_NUM': parameters.IDX_CASE_NUM,
        'BMP_SIMULATION_DAY': parameters.SIMULATION_DAY,
        'BMP_SIMULATION_TIME': parameters.SIMULATION_TIME,
        'BMP_CYCLE_DAYS': parameters.CYCLE_DAYS,

        'AGP_YOUTH_GRP': parameters.AgeGroupPerc.YOUTH_GRP.value,
        'AGP_ADULT_GRP': parameters.AgeGroupPerc.ADULT_GRP.value,
        'AGP_ELDER_GRP': parameters.AgeGroupPerc.ELDER_GRP.value,

        'CR_SAME_GRP': parameters.ContactRate.SAME_GRP.value,
        'CR_DIFF_GRP': parameters.ContactRate.DIFF_GRP.value,

        'VR_YOUTH_RT': parameters.VaccineRate.YOUTH_RT.value,
        'VR_ADULT_RT': parameters.VaccineRate.ADULT_RT.value,
        'VR_ELDER_RT': parameters.VaccineRate.ELDER_RT.value,

        'IR_YOUTH_NV_RT': parameters.InfectionRate.YOUTH_NV_RT.value,
        'IR_ADULT_NV_RT': parameters.InfectionRate.ADULT_NV_RT.value,
        'IR_ELDER_NV_RT': parameters.InfectionRate.ELDER_NV_RT.value,
        'IR_YOUTH_V_RT': parameters.InfectionRate.YOUTH_V_RT.value,
        'IR_ADULT_V_RT': parameters.InfectionRate.ADULT_V_RT.value,
        'IR_ELDER_V_RT': parameters.InfectionRate.ELDER_V_RT.value,

        'STR_YOUTH_RT': parameters.SeekTreatmentRate.YOUTH_RT.value,
        'STR_ADULT_RT': parameters.SeekTreatmentRate.ADULT_RT.value,
        'STR_ELDER_RT': parameters.SeekTreatmentRate.ELDER_RT.value,

        'MIR_YOUTH_RT': parameters.MedicineIntakeRate.YOUTH_RT.value,
        'MIR_ADULT_RT': parameters.MedicineIntakeRate.ADULT_RT.value,
        'MIR_ELDER_RT': parameters.MedicineIntakeRate.ELDER_RT.value,

        'SR_YOUTH_48_RT': parameters.SevereRate.YOUTH_48_RT.value,
        'SR_ADULT_48_RT': parameters.SevereRate.ADULT_48_RT.value,
        'SR_ELDER_48_RT': parameters.SevereRate.ELDER_48_RT.value,
        'SR_YOUTH_N48_RT': parameters.SevereRate.YOUTH_N48_RT.value,
        'SR_ADULT_N48_RT': parameters.SevereRate.ADULT_N48_RT.value,
        'SR_ELDER_N48_RT': parameters.SevereRate.ELDER_N48_RT.value,

        'FR_YOUTH_RT': parameters.FatalityRate.YOUTH_RT.value,
        'FR_ADULT_RT': parameters.FatalityRate.ADULT_RT.value,
        'FR_ELDER_RT': parameters.FatalityRate.ELDER_RT.value,
    }

    if request.method == 'POST':
        print("POST!")
        if "run_model" in request.POST:
            analysis_code = utils_func.analysis_code_generator()
            content = {
                'analysis_code': analysis_code,
                'button_clicked': "False",
            }
            utils_func.create_sample_directory(analysis_code)
            datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', analysis_code)

            json_file = os.path.join(datadir, "data.json")
            # transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
            # labels_file = os.path.join(datadir, "labels.json")
            with open(json_file, 'w') as f:
                json.dump({}, f)

            # for (k, v) in YOUTH_json.items():
            #     print("      Key: " + k)
            #     if k == "name":
            #         print("  v", v)
            #     elif k == "children":
            #         pass

                #   "name":"Index Case",
                #   "edge_name":"Index Case",
                #   "pb":"[0.5]",
                # # print("      Value: " + v)
                # # print("      Value: " + str(v))
            # with open(YOUTH_json, 'w') as f:
            #     json.dump({}, f)

            # with open(ADULT_json, 'w') as f:
            #     json.dump({}, f)
            #
            # with open(ELDER_json, 'w') as f:
            #     json.dump({}, f)

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
                BMP_SIMULATION_TIME = form.cleaned_data["BMP_SIMULATION_TIME"]
                BMP_CYCLE_DAYS = form.cleaned_data["BMP_CYCLE_DAYS"]

                AGP_YOUTH_GRP = form.cleaned_data["AGP_YOUTH_GRP"]
                AGP_ADULT_GRP = form.cleaned_data["AGP_ADULT_GRP"]
                AGP_ELDER_GRP = form.cleaned_data["AGP_ELDER_GRP"]

                CR_SAME_GRP = form.cleaned_data["CR_SAME_GRP"]
                CR_DIFF_GRP = form.cleaned_data["CR_DIFF_GRP"]

                VR_YOUTH_RT = form.cleaned_data["VR_YOUTH_RT"]
                VR_ADULT_RT = form.cleaned_data["VR_ADULT_RT"]
                VR_ELDER_RT = form.cleaned_data["VR_ELDER_RT"]

                IR_YOUTH_NV_RT = form.cleaned_data["IR_YOUTH_NV_RT"]
                IR_ADULT_NV_RT = form.cleaned_data["IR_ADULT_NV_RT"]
                IR_ELDER_NV_RT = form.cleaned_data["IR_ELDER_NV_RT"]
                IR_YOUTH_V_RT = form.cleaned_data["IR_YOUTH_V_RT"]
                IR_ADULT_V_RT = form.cleaned_data["IR_ADULT_V_RT"]
                IR_ELDER_V_RT = form.cleaned_data["IR_ELDER_V_RT"]

                STR_YOUTH_RT = form.cleaned_data["STR_YOUTH_RT"]
                STR_ADULT_RT = form.cleaned_data["STR_ADULT_RT"]
                STR_ELDER_RT = form.cleaned_data["STR_ELDER_RT"]

                MIR_YOUTH_RT = form.cleaned_data["MIR_YOUTH_RT"]
                MIR_ADULT_RT = form.cleaned_data["MIR_ADULT_RT"]
                MIR_ELDER_RT = form.cleaned_data["MIR_ELDER_RT"]

                SR_YOUTH_48_RT = form.cleaned_data["SR_YOUTH_48_RT"]
                SR_ADULT_48_RT = form.cleaned_data["SR_ADULT_48_RT"]
                SR_ELDER_48_RT = form.cleaned_data["SR_ELDER_48_RT"]
                SR_YOUTH_N48_RT = form.cleaned_data["SR_YOUTH_N48_RT"]
                SR_ADULT_N48_RT = form.cleaned_data["SR_ADULT_N48_RT"]
                SR_ELDER_N48_RT = form.cleaned_data["SR_ELDER_N48_RT"]

                FR_YOUTH_RT = form.cleaned_data["FR_YOUTH_RT"]
                FR_ADULT_RT = form.cleaned_data["FR_ADULT_RT"]
                FR_ELDER_RT = form.cleaned_data["FR_ELDER_RT"]

                global_json = os.path.join(settings.STATIC_MAIN_APP, 'main/topology.json')
                with open(global_json, 'r') as f:
                    data = json.load(f)
                    YOUTH_json = copy.deepcopy(data)
                    ADULT_json = copy.deepcopy(data)
                    ELDER_json = copy.deepcopy(data)

                YOUTH_json_file = os.path.join(datadir, "YOUTH.json")
                ADULT_json_file = os.path.join(datadir, "ADULT.json")
                ELDER_json_file = os.path.join(datadir, "ELDER.json")

                YOUTH_json_new = iterate("YOUTH", YOUTH_json, form.cleaned_data)
                ADULT_json_new = iterate("ADULT", ADULT_json, form.cleaned_data)
                ELDER_json_new = iterate("ELDER", ELDER_json, form.cleaned_data)

                with open(YOUTH_json_file, 'w') as f:
                    json.dump(YOUTH_json_new, f)
                with open(ADULT_json_file, 'w') as f:
                    json.dump(ADULT_json_new, f)
                with open(ELDER_json_file, 'w') as f:
                    json.dump(ELDER_json_new, f)

                with open(input_params_json_file, 'w') as f:
                    json.dump({
                        "YOUTH_json_file": YOUTH_json_file,
                        "ADULT_json_file": ADULT_json_file,
                        "ELDER_json_file": ELDER_json_file,
                        "BMP_IDX_CASE_NUM": BMP_IDX_CASE_NUM,
                        "BMP_SIMULATION_DAY": BMP_SIMULATION_DAY,
                        "BMP_SIMULATION_TIME": BMP_SIMULATION_TIME,
                        "BMP_CYCLE_DAYS": BMP_CYCLE_DAYS,
                        "AGP_YOUTH_GRP": AGP_YOUTH_GRP,
                        "AGP_ADULT_GRP": AGP_ADULT_GRP,
                        "AGP_ELDER_GRP": AGP_ELDER_GRP,
                        "CR_SAME_GRP": CR_SAME_GRP,
                        "CR_DIFF_GRP": CR_DIFF_GRP,
                        "VR_YOUTH_RT":  VR_YOUTH_RT,
                        "VR_ADULT_RT": VR_ADULT_RT,
                        "VR_ELDER_RT": VR_ELDER_RT,
                        "IR_YOUTH_NV_RT": IR_YOUTH_NV_RT,
                        "IR_ADULT_NV_RT": IR_ADULT_NV_RT,
                        "IR_ELDER_NV_RT": IR_ELDER_NV_RT,
                        "IR_YOUTH_V_RT": IR_YOUTH_V_RT,
                        "IR_ADULT_V_RT": IR_ADULT_V_RT,
                        "IR_ELDER_V_RT": IR_ELDER_V_RT,
                        "STR_YOUTH_RT": STR_YOUTH_RT,
                        "STR_ADULT_RT": STR_ADULT_RT,
                        "STR_ELDER_RT": STR_ELDER_RT,
                        "MIR_YOUTH_RT": MIR_YOUTH_RT,
                        "MIR_ADULT_RT": MIR_ADULT_RT,
                        "MIR_ELDER_RT": MIR_ELDER_RT,
                        "SR_YOUTH_48_RT": SR_YOUTH_48_RT,
                        "SR_ADULT_48_RT": SR_ADULT_48_RT,
                        "SR_ELDER_48_RT": SR_ELDER_48_RT,
                        "SR_YOUTH_N48_RT": SR_YOUTH_N48_RT,
                        "SR_ADULT_N48_RT": SR_ADULT_N48_RT,
                        "SR_ELDER_N48_RT": SR_ELDER_N48_RT,
                        "FR_YOUTH_RT": FR_YOUTH_RT,
                        "FR_ADULT_RT": FR_ADULT_RT,
                        "FR_ELDER_RT": FR_ELDER_RT,
                    }, f)

                a = async_task(tasks.start_analysis, datadir, BMP_SIMULATION_DAY, task_name="id_"+analysis_code)
                print("!!!! A: ", a)
                content = {
                    'analysis_code': analysis_code,
                    'button_clicked': "True",
                    "YOUTH_json_file": os.path.join('media', 'tmp', analysis_code, "YOUTH.json"),
                    "ADULT_json_file": os.path.join('media', 'tmp', analysis_code, "ADULT.json"),
                    "ELDER_json_file": os.path.join('media', 'tmp', analysis_code, "ELDER.json"),
                }
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
