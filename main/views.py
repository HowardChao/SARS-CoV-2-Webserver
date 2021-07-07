from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
from django.conf import settings

from . import utils_func
from . import jobs
from .forms import RunModelForm, AnalysisCodeForm

from .vmodel import parameters
from .vmodel import person
from .vmodel import vaccine
from .vmodel import model

import json
import os
from django_q.tasks import async_task, result, fetch, AsyncTask, result_group, result
from django_q.brokers import get_broker
import django_q

import inspect
import copy
# global data
# global labels
# data = []
# labels = []

def iterate(group, input_json, data):
    in_nput_json = copy.deepcopy(input_json)

    if in_nput_json['id'] == "Index Case":
        in_nput_json['pb'] = "1"
    elif in_nput_json['id'] == "Contact another person":
        in_nput_json['pb'] = "(" + str(data["CR_SAME_GRP"]) + ", " + str(data["CR_DIFF_GRP"]) + ")"
    # elif in_nput_json['id'] == "Vaccinated":
    #     in_nput_json['pb'] = str(data["VR_"+group+"_RT"])
    # elif in_nput_json['id'] == "Infected (vaccinated)":
    #     in_nput_json['pb'] = str(data["IR_"+group+"_Vg1_input_param_file_RT"])
    # elif in_nput_json['id'] == "Not infected (vaccinated)":
    #     in_nput_json['pb'] = str(1 - float(data["IR_"+group+"_V_RT"]))
    # elif in_nput_json['id'] == "Not vaccinated":
    #     in_nput_json['pb'] = str(1 - float(data["VR_"+group+"_RT"]))
    # elif in_nput_json['id'] == "Infected (not vaccinated)":
    #     in_nput_json['pb'] = str(data["IR_"+group+"_NV_RT"])
    # elif in_nput_json['id'] == "Not infected (not vaccinated)":
    #     in_nput_json['pb'] = str(1 - float(data["IR_"+group+"_NV_RT"]))
    # elif in_nput_json['id'] == "Seek medical treatment":
    #     in_nput_json['pb'] = str(data["STR_"+group+"_RT"])
    # elif in_nput_json['id'] == "Taken Antiviral":
    #     in_nput_json['pb'] = str(data["MIR_"+group+"_RT"])
    # elif in_nput_json['id'] == "IPDpitalization (antiviral)":
    #     in_nput_json['pb'] = str(data["SR_"+group+"_48_RT"])
    # elif in_nput_json['id'] == "Death (antiviral, IPD)":
    #     in_nput_json['pb'] = str(data["FR_"+group+"_RT"])
    # elif in_nput_json['id'] == "Recovery (antiviral, IPD)":
    #     in_nput_json['pb'] = str(1 - float(data["FR_"+group+"_RT"]))
    # elif in_nput_json['id'] == "Recovery (antiviral, not IPD)":
    #     in_nput_json['pb'] = str(1 - float(data["SR_"+group+"_48_RT"]))
    # elif in_nput_json['id'] == "Not taken Antiviral":
    #     in_nput_json['pb'] = str(1 - float(data["MIR_"+group+"_RT"]))
    # elif in_nput_json['id'] == "IPDpitalization (no antiviral)":
    #     in_nput_json['pb'] = str(data["SR_"+group+"_N48_RT"])
    # elif in_nput_json['id'] == "Death (no antiviral, IPD)":
    #     in_nput_json['pb'] = str(data["FR_"+group+"_RT"])
    # elif in_nput_json['id'] == "Recovery (no antiviral, IPD)":
    #     in_nput_json['pb'] = str(1 - float(data["FR_"+group+"_RT"]))
    # elif in_nput_json['id'] == "Recovery (no antiviral, not IPD)":
    #     in_nput_json['pb'] = str(1 - float(data["SR_"+group+"_N48_RT"]))
    # print("in_nput_json: ", in_nput_json)
    # if len(in_nput_json['children']) != 0:
    #     for idx, value in enumerate(in_nput_json['children']):
    #         print("   > > > : ", idx)
    #         in_nput_json['children'][idx] = iterate(group, value, data)
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
    ## These values are default inputs.
    content = {
        'analysis_code': "Empty",
        'homepage_status': "pre_running_state",
        'BMP_IDX_CASE_NUM': parameters.IDX_CASE_NUM,
        'BMP_SIMULATION_DAY': parameters.SIMULATION_DAY,
        'BMP_CYCLE_DAYS': parameters.CYCLE_DAYS,
        'BMP_CONTACT_PEOPLE_NUM': parameters.CONTACT_PEOPLE_NUM,

        'AGP_YOUTH_GRP': parameters.AgeGroupPerc.YOUTH_GRP.value,
        'AGP_ADULT_GRP': parameters.AgeGroupPerc.ADULT_GRP.value,
        'AGP_ELDER_GRP': parameters.AgeGroupPerc.ELDER_GRP.value,

        'CP_SMT_YOUTH_Rate_CP': parameters.ContactPersonSeekTreatment_Rate.YOUTH_CP_RT.value,
        'CP_SMT_ADULT_Rate_CP': parameters.ContactPersonSeekTreatment_Rate.ADULT_CP_RT.value,
        'CP_SMT_ELDER_Rate_CP': parameters.ContactPersonSeekTreatment_Rate.ELDER_CP_RT.value,
        'CP_SMT_YOUTH_Rate_ST': parameters.ContactPersonSeekTreatment_Rate.YOUTH_ST_RT.value,
        'CP_SMT_ADULT_Rate_ST': parameters.ContactPersonSeekTreatment_Rate.ADULT_ST_RT.value,
        'CP_SMT_ELDER_Rate_ST': parameters.ContactPersonSeekTreatment_Rate.ELDER_ST_RT.value,

        'CR_SAME_GRP': parameters.ContactGroup_Rate.SAME_GRP.value,
        'CR_DIFF_GRP': parameters.ContactGroup_Rate.DIFF_GRP.value,

        'G1_Vac_YOUTH_Rate_V': parameters.Vaccine_Rate.YOUTH_V_RT.value,
        'G1_Vac_ADULT_Rate_V': parameters.Vaccine_Rate.ADULT_V_RT.value,
        'G1_Vac_ELDER_Rate_V': parameters.Vaccine_Rate.ELDER_V_RT.value,

        'G2_Vac_YOUTH_Rate_V': parameters.Vaccine_Rate.YOUTH_V_RT.value,
        'G2_Vac_ADULT_Rate_V': parameters.Vaccine_Rate.ADULT_V_RT.value,
        'G2_Vac_ELDER_Rate_V': parameters.Vaccine_Rate.ELDER_V_RT.value,

        'G3_Vac_YOUTH_Rate_V': parameters.Vaccine_Rate.YOUTH_V_RT.value,
        'G3_Vac_ADULT_Rate_V': parameters.Vaccine_Rate.ADULT_V_RT.value,
        'G3_Vac_ELDER_Rate_V': parameters.Vaccine_Rate.ELDER_V_RT.value,

        'G4_Vac_YOUTH_Rate_V': parameters.Vaccine_Rate.YOUTH_V_RT.value,
        'G4_Vac_ADULT_Rate_V': parameters.Vaccine_Rate.ADULT_V_RT.value,
        'G4_Vac_ELDER_Rate_V': parameters.Vaccine_Rate.ELDER_V_RT.value,

        'Vac_Infection_YOUTH_Rate_V_I': parameters.Vac_Infection_Rate.YOUTH_V_I_RT.value,
        'Vac_Infection_ADULT_Rate_V_I': parameters.Vac_Infection_Rate.ADULT_V_I_RT.value,
        'Vac_Infection_ELDER_Rate_V_I': parameters.Vac_Infection_Rate.ELDER_V_I_RT.value,
        'Vac_Infection_YOUTH_Rate_V_NI': parameters.Vac_Infection_Rate.YOUTH_V_NI_RT.value,
        'Vac_Infection_ADULT_Rate_V_NI': parameters.Vac_Infection_Rate.ADULT_V_NI_RT.value,
        'Vac_Infection_ELDER_Rate_V_NI': parameters.Vac_Infection_Rate.ELDER_V_NI_RT.value,

        'NoVac_Infection_YOUTH_Rate_NV_I': parameters.NoVac_Infection_Rate.YOUTH_NV_I_RT.value,
        'NoVac_Infection_ADULT_Rate_NV_I': parameters.NoVac_Infection_Rate.ADULT_NV_I_RT.value,
        'NoVac_Infection_ELDER_Rate_NV_I': parameters.NoVac_Infection_Rate.ELDER_NV_I_RT.value,
        'NoVac_Infection_YOUTH_Rate_NV_NI': parameters.NoVac_Infection_Rate.YOUTH_NV_NI_RT.value,
        'NoVac_Infection_ADULT_Rate_NV_NI': parameters.NoVac_Infection_Rate.ADULT_NV_NI_RT.value,
        'NoVac_Infection_ELDER_Rate_NV_NI': parameters.NoVac_Infection_Rate.ELDER_NV_NI_RT.value,

        'SMT_IPDOPD_YOUTH_Rate_IPD': parameters.SMT_IPDOPD_Rate.YOUTH_IPD_RT.value,
        'SMT_IPDOPD_ADULT_Rate_IPD': parameters.SMT_IPDOPD_Rate.ADULT_IPD_RT.value,
        'SMT_IPDOPD_ELDER_Rate_IPD': parameters.SMT_IPDOPD_Rate.ELDER_IPD_RT.value,
        'SMT_IPDOPD_YOUTH_Rate_OPD': parameters.SMT_IPDOPD_Rate.YOUTH_OPD_RT.value,
        'SMT_IPDOPD_ADULT_Rate_OPD': parameters.SMT_IPDOPD_Rate.ADULT_OPD_RT.value,
        'SMT_IPDOPD_ELDER_Rate_OPD': parameters.SMT_IPDOPD_Rate.ELDER_OPD_RT.value,

        'SMT_IPD_Death_YOUTH_Rate_IPD_D': parameters.SMT_IPD_Death_Rate.YOUTH_IPD_D_RT.value,
        'SMT_IPD_Death_ADULT_Rate_IPD_D': parameters.SMT_IPD_Death_Rate.ADULT_IPD_D_RT.value,
        'SMT_IPD_Death_ELDER_Rate_IPD_D': parameters.SMT_IPD_Death_Rate.ELDER_IPD_D_RT.value,
        'SMT_IPD_Death_YOUTH_Rate_IPD_R': parameters.SMT_IPD_Death_Rate.YOUTH_IPD_R_RT.value,
        'SMT_IPD_Death_ADULT_Rate_IPD_R': parameters.SMT_IPD_Death_Rate.ADULT_IPD_R_RT.value,
        'SMT_IPD_Death_ELDER_Rate_IPD_R': parameters.SMT_IPD_Death_Rate.ELDER_IPD_R_RT.value,

        'SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M': parameters.SMT_OPD_MedicineIntake_Rate.YOUTH_OPD_M_RT.value,
        'SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M': parameters.SMT_OPD_MedicineIntake_Rate.ADULT_OPD_M_RT.value,
        'SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M': parameters.SMT_OPD_MedicineIntake_Rate.ELDER_OPD_M_RT.value,
        'SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_NM': parameters.SMT_OPD_MedicineIntake_Rate.YOUTH_OPD_NM_RT.value,
        'SMT_OPD_MedicineIntake_ADULT_Rate_OPD_NM': parameters.SMT_OPD_MedicineIntake_Rate.ADULT_OPD_NM_RT.value,
        'SMT_OPD_MedicineIntake_ELDER_Rate_OPD_NM': parameters.SMT_OPD_MedicineIntake_Rate.ELDER_OPD_NM_RT.value,

        'SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD': parameters.SMT_OPD_M_IPD_Rate.YOUTH_OPD_M_IPD_RT.value,
        'SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD': parameters.SMT_OPD_M_IPD_Rate.ADULT_OPD_M_IPD_RT.value,
        'SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD': parameters.SMT_OPD_M_IPD_Rate.ELDER_OPD_M_IPD_RT.value,
        'SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_R': parameters.SMT_OPD_M_IPD_Rate.YOUTH_OPD_M_R_RT.value,
        'SMT_OPD_M_IPD_ADULT_Rate_OPD_M_R': parameters.SMT_OPD_M_IPD_Rate.ADULT_OPD_M_R_RT.value,
        'SMT_OPD_M_IPD_ELDER_Rate_OPD_M_R': parameters.SMT_OPD_M_IPD_Rate.ELDER_OPD_M_R_RT.value,

        'SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D': parameters.SMT_OPD_M_IPD_Death_Rate.YOUTH_OPD_M_IPD_D_RT.value,
        'SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D': parameters.SMT_OPD_M_IPD_Death_Rate.ADULT_OPD_M_IPD_D_RT.value,
        'SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D': parameters.SMT_OPD_M_IPD_Death_Rate.ELDER_OPD_M_IPD_D_RT.value,
        'SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_R': parameters.SMT_OPD_M_IPD_Death_Rate.YOUTH_OPD_M_IPD_R_RT.value,
        'SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_R': parameters.SMT_OPD_M_IPD_Death_Rate.ADULT_OPD_M_IPD_R_RT.value,
        'SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_R': parameters.SMT_OPD_M_IPD_Death_Rate.ELDER_OPD_M_IPD_R_RT.value,

        'SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD': parameters.SMT_OPD_NM_IPD_Rate.YOUTH_OPD_NM_IPD_RT.value,
        'SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD': parameters.SMT_OPD_NM_IPD_Rate.ADULT_OPD_NM_IPD_RT.value,
        'SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD': parameters.SMT_OPD_NM_IPD_Rate.ELDER_OPD_NM_IPD_RT.value,
        'SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_R': parameters.SMT_OPD_NM_IPD_Rate.YOUTH_OPD_NM_R_RT.value,
        'SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_R': parameters.SMT_OPD_NM_IPD_Rate.ADULT_OPD_NM_R_RT.value,
        'SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_R': parameters.SMT_OPD_NM_IPD_Rate.ELDER_OPD_NM_R_RT.value,

        'SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D': parameters.SMT_OPD_NM_IPD_Death_Rate.YOUTH_OPD_NM_IPD_D_RT.value,
        'SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D': parameters.SMT_OPD_NM_IPD_Death_Rate.ADULT_OPD_NM_IPD_D_RT.value,
        'SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D': parameters.SMT_OPD_NM_IPD_Death_Rate.ELDER_OPD_NM_IPD_D_RT.value,
        'SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_R': parameters.SMT_OPD_NM_IPD_Death_Rate.YOUTH_OPD_NM_IPD_R_RT.value,
        'SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_R': parameters.SMT_OPD_NM_IPD_Death_Rate.ADULT_OPD_NM_IPD_R_RT.value,
        'SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_R': parameters.SMT_OPD_NM_IPD_Death_Rate.ELDER_OPD_NM_IPD_R_RT.value,

        'MC_YOUTH_EARN_LOST_PER_DEATH_Rate': parameters.Mortality_Cost.YOUTH_EARN_LOST_PER_DAY_RT.value,
        'MC_ADULT_EARN_LOST_PER_DEATH_Rate': parameters.Mortality_Cost.ADULT_EARN_LOST_PER_DAY_RT.value,
        'MC_ELDER_EARN_LOST_PER_DEATH_Rate': parameters.Mortality_Cost.ELDER_EARN_LOST_PER_DAY_RT.value,

        'TIC_YOUTH_AVE_STAY_DAY_Rate': parameters.Total_Inpatient_Cost.YOUTH_AVE_STAY_DAY_RT.value,
        'TIC_ADULT_AVE_STAY_DAY_Rate': parameters.Total_Inpatient_Cost.ADULT_AVE_STAY_DAY_RT.value,
        'TIC_ELDER_AVE_STAY_DAY_Rate': parameters.Total_Inpatient_Cost.ELDER_AVE_STAY_DAY_RT.value,
        'TIC_YOUTH_COST_PER_BED_PER_DAY_Rate': parameters.Total_Inpatient_Cost.YOUTH_COST_PER_BED_PER_DAY_RT.value,
        'TIC_ADULT_COST_PER_BED_PER_DAY_Rate': parameters.Total_Inpatient_Cost.ADULT_COST_PER_BED_PER_DAY_RT.value,
        'TIC_ELDER_COST_PER_BED_PER_DAY_Rate': parameters.Total_Inpatient_Cost.ELDER_COST_PER_BED_PER_DAY_RT.value,
        'TIC_YOUTH_HOS_LOSS_PER_DAY_Rate': parameters.Total_Inpatient_Cost.YOUTH_HOS_LOSS_PER_DAY_RT.value,
        'TIC_ADULT_HOS_LOSS_PER_DAY_Rate': parameters.Total_Inpatient_Cost.ADULT_HOS_LOSS_PER_DAY_RT.value,
        'TIC_ELDER_HOS_LOSS_PER_DAY_Rate': parameters.Total_Inpatient_Cost.ELDER_HOS_LOSS_PER_DAY_RT.value,
        'TIC_YOUTH_TRANS_COST_Rate': parameters.Total_Inpatient_Cost.YOUTH_TRANS_COST_RT.value,
        'TIC_ADULT_TRANS_COST_Rate': parameters.Total_Inpatient_Cost.ADULT_TRANS_COST_RT.value,
        'TIC_ELDER_TRANS_COST_Rate': parameters.Total_Inpatient_Cost.ELDER_TRANS_COST_RT.value,

        'TOC_YOUTH_AVE_DAY_LOST_Rate': parameters.Total_Outpatient_Cost.YOUTH_AVE_DAY_LOST_RT.value,
        'TOC_ADULT_AVE_DAY_LOST_Rate': parameters.Total_Outpatient_Cost.ADULT_AVE_DAY_LOST_RT.value,
        'TOC_ELDER_AVE_DAY_LOST_Rate': parameters.Total_Outpatient_Cost.ELDER_AVE_DAY_LOST_RT.value,
        'TOC_YOUTH_TREAT_COST_Rate': parameters.Total_Outpatient_Cost.YOUTH_TREAT_COST_RT.value,
        'TOC_ADULT_TREAT_COST_Rate': parameters.Total_Outpatient_Cost.ADULT_TREAT_COST_RT.value,
        'TOC_ELDER_TREAT_COST_Rate': parameters.Total_Outpatient_Cost.ELDER_TREAT_COST_RT.value,
        'TOC_YOUTH_OPD_LOST_PER_DAY_Rate': parameters.Total_Outpatient_Cost.YOUTH_OPD_LOST_PER_DAY_RT.value,
        'TOC_ADULT_OPD_LOST_PER_DAY_Rate': parameters.Total_Outpatient_Cost.ADULT_OPD_LOST_PER_DAY_RT.value,
        'TOC_ELDER_OPD_LOST_PER_DAY_Rate': parameters.Total_Outpatient_Cost.ELDER_OPD_LOST_PER_DAY_RT.value,
        'TOC_YOUTH_TRANS_COST_Rate': parameters.Total_Outpatient_Cost.YOUTH_TRANS_COST_RT.value,
        'TOC_ADULT_TRANS_COST_Rate': parameters.Total_Outpatient_Cost.ADULT_TRANS_COST_RT.value,
        'TOC_ELDER_TRANS_COST_Rate': parameters.Total_Outpatient_Cost.ELDER_TRANS_COST_RT.value,

        'TVC_YOUTH_VAC_COST_Rate': parameters.Total_Vaccination_Cost.YOUTH_VAC_COST_RT.value,
        'TVC_ADULT_VAC_COST_Rate': parameters.Total_Vaccination_Cost.ADULT_VAC_COST_RT.value,
        'TVC_ELDER_VAC_COST_Rate': parameters.Total_Vaccination_Cost.ELDER_VAC_COST_RT.value,
        'TVC_YOUTH_VAC_LOST_PER_HOUR_Rate': parameters.Total_Vaccination_Cost.YOUTH_VAC_LOST_PER_HOUR_RT.value,
        'TVC_ADULT_VAC_LOST_PER_HOUR_Rate': parameters.Total_Vaccination_Cost.ADULT_VAC_LOST_PER_HOUR_RT.value,
        'TVC_ELDER_VAC_LOST_PER_HOUR_Rate': parameters.Total_Vaccination_Cost.ELDER_VAC_LOST_PER_HOUR_RT.value,
        'TVC_YOUTH_TRANS_COST_Rate': parameters.Total_Vaccination_Cost.YOUTH_TRANS_COST_RT.value,
        'TVC_ADULT_TRANS_COST_Rate': parameters.Total_Vaccination_Cost.ADULT_TRANS_COST_RT.value,
        'TVC_ELDER_TRANS_COST_Rate': parameters.Total_Vaccination_Cost.ELDER_TRANS_COST_RT.value,
        'TVC_YOUTH_EFF': parameters.Total_Vaccination_Cost.YOUTH_EFF.value,
        'TVC_ADULT_EFF': parameters.Total_Vaccination_Cost.ADULT_EFF.value,
        'TVC_ELDER_EFF': parameters.Total_Vaccination_Cost.ELDER_EFF.value,

        'TVSEC_YOUTH_SIDE_EFF_Rate': parameters.Total_Vaccination_Side_Effects_Cost.YOUTH_SIDE_EFF_RT.value,
        'TVSEC_ADULT_SIDE_EFF_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ADULT_SIDE_EFF_RT.value,
        'TVSEC_ELDER_SIDE_EFF_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ELDER_SIDE_EFF_RT.value,
        'TVSEC_YOUTH_MEAN_OPD_FREQ_Rate': parameters.Total_Vaccination_Side_Effects_Cost.YOUTH_MEAN_OPD_FREQ_RT.value,
        'TVSEC_ADULT_MEAN_OPD_FREQ_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ADULT_MEAN_OPD_FREQ_RT.value,
        'TVSEC_ELDER_MEAN_OPD_FREQ_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ELDER_MEAN_OPD_FREQ_RT.value,
        'TVSEC_YOUTH_DIR_OPD_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.YOUTH_DIR_OPD_COST_RT.value,
        'TVSEC_ADULT_DIR_OPD_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ADULT_DIR_OPD_COST_RT.value,
        'TVSEC_ELDER_DIR_OPD_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ELDER_DIR_OPD_COST_RT.value,
        'TVSEC_YOUTH_PROD_OPD_LOSS_Rate': parameters.Total_Vaccination_Side_Effects_Cost.YOUTH_PROD_OPD_LOSS_RT.value,
        'TVSEC_ADULT_PROD_OPD_LOSS_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ADULT_PROD_OPD_LOSS_RT.value,
        'TVSEC_ELDER_PROD_OPD_LOSS_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ELDER_PROD_OPD_LOSS_RT.value,
        'TVSEC_YOUTH_TRANS_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.YOUTH_TRANS_COST_RT.value,
        'TVSEC_ADULT_TRANS_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ADULT_TRANS_COST_RT.value,
        'TVSEC_ELDER_TRANS_COST_Rate': parameters.Total_Vaccination_Side_Effects_Cost.ELDER_TRANS_COST_RT.value,
    }

    if request.method == 'POST':
        print("POST!")
        if "run_model" in request.POST:
            analysis_code = utils_func.analysis_code_generator()
            content = {
                'analysis_code': analysis_code,
                'homepage_status': "pre_running_state",
            }
            utils_func.create_sample_directory(analysis_code)
            datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', analysis_code)
            json_file = os.path.join(datadir, "data.json")
            # transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
            # labels_file = os.path.join(datadir, "labels.json")
            with open(json_file, 'w', encoding="UTF-8") as f:
                json.dump({}, f, ensure_ascii=False)

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
            # print(form)
            print(form.is_valid())
            if form.is_valid():
                input_params_json_file = os.path.join(datadir, "input_params.json")
                print("Form is valid")

                GROUP_NUM = form.cleaned_data["GROUP_NUM"]
                BMP_IDX_CASE_NUM = form.cleaned_data["BMP_IDX_CASE_NUM"]
                BMP_SIMULATION_DAY = form.cleaned_data["BMP_SIMULATION_DAY"]
                BMP_CYCLE_DAYS = form.cleaned_data["BMP_CYCLE_DAYS"]
                BMP_CONTACT_PEOPLE_NUM = form.cleaned_data["BMP_CONTACT_PEOPLE_NUM"]

                AGP_YOUTH_GRP = form.cleaned_data["AGP_YOUTH_GRP"]
                AGP_ADULT_GRP = form.cleaned_data["AGP_ADULT_GRP"]
                AGP_ELDER_GRP = form.cleaned_data["AGP_ELDER_GRP"]

                CR_SAME_GRP = form.cleaned_data["CR_SAME_GRP"]
                CR_DIFF_GRP = form.cleaned_data["CR_DIFF_GRP"]

                G1_Vac_YOUTH_Rate_V = form.cleaned_data["G1_Vac_YOUTH_Rate_V"]
                G1_Vac_ADULT_Rate_V = form.cleaned_data["G1_Vac_ADULT_Rate_V"]
                G1_Vac_ELDER_Rate_V = form.cleaned_data["G1_Vac_ELDER_Rate_V"]

                G2_Vac_YOUTH_Rate_V = form.cleaned_data["G2_Vac_YOUTH_Rate_V"]
                G2_Vac_ADULT_Rate_V = form.cleaned_data["G2_Vac_ADULT_Rate_V"]
                G2_Vac_ELDER_Rate_V = form.cleaned_data["G2_Vac_ELDER_Rate_V"]

                G3_Vac_YOUTH_Rate_V = form.cleaned_data["G3_Vac_YOUTH_Rate_V"]
                G3_Vac_ADULT_Rate_V = form.cleaned_data["G3_Vac_ADULT_Rate_V"]
                G3_Vac_ELDER_Rate_V = form.cleaned_data["G3_Vac_ELDER_Rate_V"]

                G4_Vac_YOUTH_Rate_V = form.cleaned_data["G4_Vac_YOUTH_Rate_V"]
                G4_Vac_ADULT_Rate_V = form.cleaned_data["G4_Vac_ADULT_Rate_V"]
                G4_Vac_ELDER_Rate_V = form.cleaned_data["G4_Vac_ELDER_Rate_V"]


                Vac_Infection_YOUTH_Rate_V_I = form.cleaned_data["Vac_Infection_YOUTH_Rate_V_I"]
                Vac_Infection_ADULT_Rate_V_I = form.cleaned_data["Vac_Infection_ADULT_Rate_V_I"]
                Vac_Infection_ELDER_Rate_V_I = form.cleaned_data["Vac_Infection_ELDER_Rate_V_I"]

                NoVac_Infection_YOUTH_Rate_NV_I = form.cleaned_data["NoVac_Infection_YOUTH_Rate_NV_I"]
                NoVac_Infection_ADULT_Rate_NV_I = form.cleaned_data["NoVac_Infection_ADULT_Rate_NV_I"]
                NoVac_Infection_ELDER_Rate_NV_I = form.cleaned_data["NoVac_Infection_ELDER_Rate_NV_I"]

                CP_SMT_YOUTH_Rate_CP = form.cleaned_data["CP_SMT_YOUTH_Rate_CP"]
                CP_SMT_ADULT_Rate_CP = form.cleaned_data["CP_SMT_ADULT_Rate_CP"]
                CP_SMT_ELDER_Rate_CP = form.cleaned_data["CP_SMT_ELDER_Rate_CP"]
                CP_SMT_YOUTH_Rate_ST = form.cleaned_data["CP_SMT_YOUTH_Rate_ST"]
                CP_SMT_ADULT_Rate_ST = form.cleaned_data["CP_SMT_ADULT_Rate_ST"]
                CP_SMT_ELDER_Rate_ST = form.cleaned_data["CP_SMT_ELDER_Rate_ST"]

                SMT_IPDOPD_YOUTH_Rate_IPD = form.cleaned_data["SMT_IPDOPD_YOUTH_Rate_IPD"]
                SMT_IPDOPD_ADULT_Rate_IPD = form.cleaned_data["SMT_IPDOPD_ADULT_Rate_IPD"]
                SMT_IPDOPD_ELDER_Rate_IPD = form.cleaned_data["SMT_IPDOPD_ELDER_Rate_IPD"]
                SMT_IPDOPD_YOUTH_Rate_OPD = form.cleaned_data["SMT_IPDOPD_YOUTH_Rate_OPD"]
                SMT_IPDOPD_ADULT_Rate_OPD = form.cleaned_data["SMT_IPDOPD_ADULT_Rate_OPD"]
                SMT_IPDOPD_ELDER_Rate_OPD = form.cleaned_data["SMT_IPDOPD_ELDER_Rate_OPD"]

                # SMT_IPD_Death_YOUTH_Rate_IPD_D = form.cleaned_data["SMT_IPD_Death_YOUTH_Rate_IPD_D"]
                # SMT_IPD_Death_ADULT_Rate_IPD_D = form.cleaned_data["SMT_IPD_Death_ADULT_Rate_IPD_D"]
                # SMT_IPD_Death_ELDER_Rate_IPD_D = form.cleaned_data["SMT_IPD_Death_ELDER_Rate_IPD_D"]

                SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M = form.cleaned_data["SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M"]
                SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M = form.cleaned_data["SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M"]
                SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M = form.cleaned_data["SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M"]

                SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD = form.cleaned_data["SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD"]
                SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD = form.cleaned_data["SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD"]
                SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD = form.cleaned_data["SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD"]

                SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D = form.cleaned_data["SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D"]
                SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D = form.cleaned_data["SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D"]
                SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D = form.cleaned_data["SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D"]

                SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD = form.cleaned_data["SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD"]
                SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD = form.cleaned_data["SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD"]
                SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD = form.cleaned_data["SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD"]

                SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D = form.cleaned_data["SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D"]
                SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D = form.cleaned_data["SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D"]
                SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D = form.cleaned_data["SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D"]

                MC_YOUTH_EARN_LOST_PER_DEATH_Rate = form.cleaned_data["MC_YOUTH_EARN_LOST_PER_DEATH_Rate"]
                MC_ADULT_EARN_LOST_PER_DEATH_Rate = form.cleaned_data["MC_ADULT_EARN_LOST_PER_DEATH_Rate"]
                MC_ELDER_EARN_LOST_PER_DEATH_Rate = form.cleaned_data["MC_ELDER_EARN_LOST_PER_DEATH_Rate"]

                TIC_YOUTH_AVE_STAY_DAY_Rate = form.cleaned_data["TIC_YOUTH_AVE_STAY_DAY_Rate"]
                TIC_ADULT_AVE_STAY_DAY_Rate = form.cleaned_data["TIC_ADULT_AVE_STAY_DAY_Rate"]
                TIC_ELDER_AVE_STAY_DAY_Rate = form.cleaned_data["TIC_ELDER_AVE_STAY_DAY_Rate"]
                TIC_YOUTH_COST_PER_BED_PER_DAY_Rate = form.cleaned_data["TIC_YOUTH_COST_PER_BED_PER_DAY_Rate"]
                TIC_ADULT_COST_PER_BED_PER_DAY_Rate = form.cleaned_data["TIC_ADULT_COST_PER_BED_PER_DAY_Rate"]
                TIC_ELDER_COST_PER_BED_PER_DAY_Rate = form.cleaned_data["TIC_ELDER_COST_PER_BED_PER_DAY_Rate"]
                TIC_YOUTH_HOS_LOSS_PER_DAY_Rate = form.cleaned_data["TIC_YOUTH_HOS_LOSS_PER_DAY_Rate"]
                TIC_ADULT_HOS_LOSS_PER_DAY_Rate = form.cleaned_data["TIC_ADULT_HOS_LOSS_PER_DAY_Rate"]
                TIC_ELDER_HOS_LOSS_PER_DAY_Rate = form.cleaned_data["TIC_ELDER_HOS_LOSS_PER_DAY_Rate"]
                TIC_YOUTH_TRANS_COST_Rate = form.cleaned_data["TIC_YOUTH_TRANS_COST_Rate"]
                TIC_ADULT_TRANS_COST_Rate = form.cleaned_data["TIC_ADULT_TRANS_COST_Rate"]
                TIC_ELDER_TRANS_COST_Rate = form.cleaned_data["TIC_ELDER_TRANS_COST_Rate"]

                TOC_YOUTH_AVE_DAY_LOST_Rate = form.cleaned_data["TOC_YOUTH_AVE_DAY_LOST_Rate"]
                TOC_ADULT_AVE_DAY_LOST_Rate = form.cleaned_data["TOC_ADULT_AVE_DAY_LOST_Rate"]
                TOC_ELDER_AVE_DAY_LOST_Rate = form.cleaned_data["TOC_ELDER_AVE_DAY_LOST_Rate"]
                TOC_YOUTH_TREAT_COST_Rate = form.cleaned_data["TOC_YOUTH_TREAT_COST_Rate"]
                TOC_ADULT_TREAT_COST_Rate = form.cleaned_data["TOC_ADULT_TREAT_COST_Rate"]
                TOC_ELDER_TREAT_COST_Rate = form.cleaned_data["TOC_ELDER_TREAT_COST_Rate"]
                TOC_YOUTH_OPD_LOST_PER_DAY_Rate = form.cleaned_data["TOC_YOUTH_OPD_LOST_PER_DAY_Rate"]
                TOC_ADULT_OPD_LOST_PER_DAY_Rate = form.cleaned_data["TOC_ADULT_OPD_LOST_PER_DAY_Rate"]
                TOC_ELDER_OPD_LOST_PER_DAY_Rate = form.cleaned_data["TOC_ELDER_OPD_LOST_PER_DAY_Rate"]
                TOC_YOUTH_TRANS_COST_Rate = form.cleaned_data["TOC_YOUTH_TRANS_COST_Rate"]
                TOC_ADULT_TRANS_COST_Rate = form.cleaned_data["TOC_ADULT_TRANS_COST_Rate"]
                TOC_ELDER_TRANS_COST_Rate = form.cleaned_data["TOC_ELDER_TRANS_COST_Rate"]

                TVC_YOUTH_VAC_COST_Rate = form.cleaned_data["TVC_YOUTH_VAC_COST_Rate"]
                TVC_ADULT_VAC_COST_Rate = form.cleaned_data["TVC_ADULT_VAC_COST_Rate"]
                TVC_ELDER_VAC_COST_Rate = form.cleaned_data["TVC_ELDER_VAC_COST_Rate"]
                TVC_YOUTH_VAC_LOST_PER_HOUR_Rate = form.cleaned_data["TVC_YOUTH_VAC_LOST_PER_HOUR_Rate"]
                TVC_ADULT_VAC_LOST_PER_HOUR_Rate = form.cleaned_data["TVC_ADULT_VAC_LOST_PER_HOUR_Rate"]
                TVC_ELDER_VAC_LOST_PER_HOUR_Rate = form.cleaned_data["TVC_ELDER_VAC_LOST_PER_HOUR_Rate"]
                TVC_YOUTH_TRANS_COST_Rate = form.cleaned_data["TVC_YOUTH_TRANS_COST_Rate"]
                TVC_ADULT_TRANS_COST_Rate = form.cleaned_data["TVC_ADULT_TRANS_COST_Rate"]
                TVC_ELDER_TRANS_COST_Rate = form.cleaned_data["TVC_ELDER_TRANS_COST_Rate"]
                TVC_YOUTH_EFF = form.cleaned_data["TVC_YOUTH_EFF"]
                TVC_ADULT_EFF = form.cleaned_data["TVC_ADULT_EFF"]
                TVC_ELDER_EFF = form.cleaned_data["TVC_ELDER_EFF"]

                TVSEC_YOUTH_SIDE_EFF_Rate = form.cleaned_data["TVSEC_YOUTH_SIDE_EFF_Rate"]
                TVSEC_ADULT_SIDE_EFF_Rate = form.cleaned_data["TVSEC_ADULT_SIDE_EFF_Rate"]
                TVSEC_ELDER_SIDE_EFF_Rate = form.cleaned_data["TVSEC_ELDER_SIDE_EFF_Rate"]
                TVSEC_YOUTH_MEAN_OPD_FREQ_Rate = form.cleaned_data["TVSEC_YOUTH_MEAN_OPD_FREQ_Rate"]
                TVSEC_ADULT_MEAN_OPD_FREQ_Rate = form.cleaned_data["TVSEC_ADULT_MEAN_OPD_FREQ_Rate"]
                TVSEC_ELDER_MEAN_OPD_FREQ_Rate = form.cleaned_data["TVSEC_ELDER_MEAN_OPD_FREQ_Rate"]
                TVSEC_YOUTH_DIR_OPD_COST_Rate = form.cleaned_data["TVSEC_YOUTH_DIR_OPD_COST_Rate"]
                TVSEC_ADULT_DIR_OPD_COST_Rate = form.cleaned_data["TVSEC_ADULT_DIR_OPD_COST_Rate"]
                TVSEC_ELDER_DIR_OPD_COST_Rate = form.cleaned_data["TVSEC_ELDER_DIR_OPD_COST_Rate"]
                TVSEC_YOUTH_PROD_OPD_LOSS_Rate = form.cleaned_data["TVSEC_YOUTH_PROD_OPD_LOSS_Rate"]
                TVSEC_ADULT_PROD_OPD_LOSS_Rate = form.cleaned_data["TVSEC_ADULT_PROD_OPD_LOSS_Rate"]
                TVSEC_ELDER_PROD_OPD_LOSS_Rate = form.cleaned_data["TVSEC_ELDER_PROD_OPD_LOSS_Rate"]
                TVSEC_YOUTH_TRANS_COST_Rate = form.cleaned_data["TVSEC_YOUTH_TRANS_COST_Rate"]
                TVSEC_ADULT_TRANS_COST_Rate = form.cleaned_data["TVSEC_ADULT_TRANS_COST_Rate"]
                TVSEC_ELDER_TRANS_COST_Rate = form.cleaned_data["TVSEC_ELDER_TRANS_COST_Rate"]

                global_json = os.path.join(settings.STATIC_MAIN_APP, 'main/topology.json')
                with open(global_json, 'r', encoding="UTF-8") as f:
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

                with open(YOUTH_json_file, 'w', encoding="UTF-8") as f:
                    json.dump(YOUTH_json_new, f, ensure_ascii=False)
                with open(ADULT_json_file, 'w', encoding="UTF-8") as f:
                    json.dump(ADULT_json_new, f, ensure_ascii=False)
                with open(ELDER_json_file, 'w', encoding="UTF-8") as f:
                    json.dump(ELDER_json_new, f, ensure_ascii=False)

                # This is for the final input parameter storage!!
                with open(input_params_json_file, 'w', encoding="UTF-8") as f:
                    json.dump({
                        "YOUTH_json_file": YOUTH_json_file,
                        "ADULT_json_file": ADULT_json_file,
                        "ELDER_json_file": ELDER_json_file,
                        "GROUP_NUM": GROUP_NUM,
                        "BMP_IDX_CASE_NUM": BMP_IDX_CASE_NUM,
                        "BMP_SIMULATION_DAY": BMP_SIMULATION_DAY,
                        "BMP_CYCLE_DAYS": BMP_CYCLE_DAYS,
                        "BMP_CONTACT_PEOPLE_NUM": BMP_CONTACT_PEOPLE_NUM,

                        "AGP_YOUTH_GRP": AGP_YOUTH_GRP,
                        "AGP_ADULT_GRP": AGP_ADULT_GRP,
                        "AGP_ELDER_GRP": AGP_ELDER_GRP,

                        "CR_SAME_GRP": CR_SAME_GRP,
                        "CR_DIFF_GRP": CR_DIFF_GRP,



                        "G1_Vac_YOUTH_Rate_V": G1_Vac_YOUTH_Rate_V,
                        "G1_Vac_ADULT_Rate_V": G1_Vac_ADULT_Rate_V,
                        "G1_Vac_ELDER_Rate_V": G1_Vac_ELDER_Rate_V,

                        "G2_Vac_YOUTH_Rate_V": G2_Vac_YOUTH_Rate_V,
                        "G2_Vac_ADULT_Rate_V": G2_Vac_ADULT_Rate_V,
                        "G2_Vac_ELDER_Rate_V": G2_Vac_ELDER_Rate_V,

                        "G3_Vac_YOUTH_Rate_V": G3_Vac_YOUTH_Rate_V,
                        "G3_Vac_ADULT_Rate_V": G3_Vac_ADULT_Rate_V,
                        "G3_Vac_ELDER_Rate_V": G3_Vac_ELDER_Rate_V,

                        "G4_Vac_YOUTH_Rate_V": G4_Vac_YOUTH_Rate_V,
                        "G4_Vac_ADULT_Rate_V": G4_Vac_ADULT_Rate_V,
                        "G4_Vac_ELDER_Rate_V": G4_Vac_ELDER_Rate_V,



                        "Vac_Infection_YOUTH_Rate_V_I": Vac_Infection_YOUTH_Rate_V_I,
                        "Vac_Infection_ADULT_Rate_V_I": Vac_Infection_ADULT_Rate_V_I,
                        "Vac_Infection_ELDER_Rate_V_I": Vac_Infection_ELDER_Rate_V_I,

                        "NoVac_Infection_YOUTH_Rate_NV_I": NoVac_Infection_YOUTH_Rate_NV_I,
                        "NoVac_Infection_ADULT_Rate_NV_I": NoVac_Infection_ADULT_Rate_NV_I,
                        "NoVac_Infection_ELDER_Rate_NV_I": NoVac_Infection_ELDER_Rate_NV_I,

                        "CP_SMT_YOUTH_Rate_CP": CP_SMT_YOUTH_Rate_CP,
                        "CP_SMT_ADULT_Rate_CP": CP_SMT_ADULT_Rate_CP,
                        "CP_SMT_ELDER_Rate_CP": CP_SMT_ELDER_Rate_CP,
                        "CP_SMT_YOUTH_Rate_ST": CP_SMT_YOUTH_Rate_ST,
                        "CP_SMT_ADULT_Rate_ST": CP_SMT_ADULT_Rate_ST,
                        "CP_SMT_ELDER_Rate_ST": CP_SMT_ELDER_Rate_ST,

                        "SMT_IPDOPD_YOUTH_Rate_IPD": SMT_IPDOPD_YOUTH_Rate_IPD,
                        "SMT_IPDOPD_ADULT_Rate_IPD": SMT_IPDOPD_ADULT_Rate_IPD,
                        "SMT_IPDOPD_ELDER_Rate_IPD": SMT_IPDOPD_ELDER_Rate_IPD,
                        "SMT_IPDOPD_YOUTH_Rate_OPD": SMT_IPDOPD_YOUTH_Rate_OPD,
                        "SMT_IPDOPD_ADULT_Rate_OPD": SMT_IPDOPD_ADULT_Rate_OPD,
                        "SMT_IPDOPD_ELDER_Rate_OPD": SMT_IPDOPD_ELDER_Rate_OPD,

                        # "SMT_IPD_Death_YOUTH_Rate_IPD_D": SMT_IPD_Death_YOUTH_Rate_IPD_D,
                        # "SMT_IPD_Death_ADULT_Rate_IPD_D": SMT_IPD_Death_ADULT_Rate_IPD_D,
                        # "SMT_IPD_Death_ELDER_Rate_IPD_D": SMT_IPD_Death_ELDER_Rate_IPD_D,

                        "SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M": SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M,
                        "SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M": SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M,
                        "SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M": SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M,

                        "SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD": SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD,
                        "SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD": SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD,
                        "SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD": SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD,

                        "SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D": SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D,
                        "SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D": SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D,
                        "SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D": SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D,

                        "SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD": SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD,
                        "SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD": SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD,
                        "SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD": SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD,

                        "SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D": SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D,
                        "SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D": SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D,
                        "SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D": SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D,

                        "MC_YOUTH_EARN_LOST_PER_DEATH_Rate": MC_YOUTH_EARN_LOST_PER_DEATH_Rate,
                        "MC_ADULT_EARN_LOST_PER_DEATH_Rate": MC_ADULT_EARN_LOST_PER_DEATH_Rate,
                        "MC_ELDER_EARN_LOST_PER_DEATH_Rate": MC_ELDER_EARN_LOST_PER_DEATH_Rate,

                        "TIC_YOUTH_AVE_STAY_DAY_Rate": TIC_YOUTH_AVE_STAY_DAY_Rate,
                        "TIC_ADULT_AVE_STAY_DAY_Rate": TIC_ADULT_AVE_STAY_DAY_Rate,
                        "TIC_ELDER_AVE_STAY_DAY_Rate": TIC_ELDER_AVE_STAY_DAY_Rate,
                        "TIC_YOUTH_COST_PER_BED_PER_DAY_Rate": TIC_YOUTH_COST_PER_BED_PER_DAY_Rate,
                        "TIC_ADULT_COST_PER_BED_PER_DAY_Rate": TIC_ADULT_COST_PER_BED_PER_DAY_Rate,
                        "TIC_ELDER_COST_PER_BED_PER_DAY_Rate": TIC_ELDER_COST_PER_BED_PER_DAY_Rate,
                        "TIC_YOUTH_HOS_LOSS_PER_DAY_Rate": TIC_YOUTH_HOS_LOSS_PER_DAY_Rate,
                        "TIC_ADULT_HOS_LOSS_PER_DAY_Rate": TIC_ADULT_HOS_LOSS_PER_DAY_Rate,
                        "TIC_ELDER_HOS_LOSS_PER_DAY_Rate": TIC_ELDER_HOS_LOSS_PER_DAY_Rate,
                        "TIC_YOUTH_TRANS_COST_Rate": TIC_YOUTH_TRANS_COST_Rate,
                        "TIC_ADULT_TRANS_COST_Rate": TIC_ADULT_TRANS_COST_Rate,
                        "TIC_ELDER_TRANS_COST_Rate": TIC_ELDER_TRANS_COST_Rate,

                        "TOC_YOUTH_AVE_DAY_LOST_Rate": TOC_YOUTH_AVE_DAY_LOST_Rate,
                        "TOC_ADULT_AVE_DAY_LOST_Rate": TOC_ADULT_AVE_DAY_LOST_Rate,
                        "TOC_ELDER_AVE_DAY_LOST_Rate": TOC_ELDER_AVE_DAY_LOST_Rate,
                        "TOC_YOUTH_TREAT_COST_Rate": TOC_YOUTH_TREAT_COST_Rate,
                        "TOC_ADULT_TREAT_COST_Rate": TOC_ADULT_TREAT_COST_Rate,
                        "TOC_ELDER_TREAT_COST_Rate": TOC_ELDER_TREAT_COST_Rate,
                        "TOC_YOUTH_OPD_LOST_PER_DAY_Rate": TOC_YOUTH_OPD_LOST_PER_DAY_Rate,
                        "TOC_ADULT_OPD_LOST_PER_DAY_Rate": TOC_ADULT_OPD_LOST_PER_DAY_Rate,
                        "TOC_ELDER_OPD_LOST_PER_DAY_Rate": TOC_ELDER_OPD_LOST_PER_DAY_Rate,
                        "TOC_YOUTH_TRANS_COST_Rate": TOC_YOUTH_TRANS_COST_Rate,
                        "TOC_ADULT_TRANS_COST_Rate": TOC_ADULT_TRANS_COST_Rate,
                        "TOC_ELDER_TRANS_COST_Rate": TOC_ELDER_TRANS_COST_Rate,


                        "TVC_YOUTH_VAC_COST_Rate": TVC_YOUTH_VAC_COST_Rate,
                        "TVC_ADULT_VAC_COST_Rate": TVC_ADULT_VAC_COST_Rate,
                        "TVC_ELDER_VAC_COST_Rate": TVC_ELDER_VAC_COST_Rate,
                        "TVC_YOUTH_VAC_LOST_PER_HOUR_Rate": TVC_YOUTH_VAC_LOST_PER_HOUR_Rate,
                        "TVC_ADULT_VAC_LOST_PER_HOUR_Rate": TVC_ADULT_VAC_LOST_PER_HOUR_Rate,
                        "TVC_ELDER_VAC_LOST_PER_HOUR_Rate": TVC_ELDER_VAC_LOST_PER_HOUR_Rate,
                        "TVC_YOUTH_TRANS_COST_Rate": TVC_YOUTH_TRANS_COST_Rate,
                        "TVC_ADULT_TRANS_COST_Rate": TVC_ADULT_TRANS_COST_Rate,
                        "TVC_ELDER_TRANS_COST_Rate": TVC_ELDER_TRANS_COST_Rate,
                        "TVC_YOUTH_EFF": TVC_YOUTH_EFF,
                        "TVC_ADULT_EFF": TVC_ADULT_EFF,
                        "TVC_ELDER_EFF": TVC_ELDER_EFF,

                        "TVSEC_YOUTH_SIDE_EFF_Rate": TVSEC_YOUTH_SIDE_EFF_Rate,
                        "TVSEC_ADULT_SIDE_EFF_Rate": TVSEC_ADULT_SIDE_EFF_Rate,
                        "TVSEC_ELDER_SIDE_EFF_Rate": TVSEC_ELDER_SIDE_EFF_Rate,
                        "TVSEC_YOUTH_MEAN_OPD_FREQ_Rate": TVSEC_YOUTH_MEAN_OPD_FREQ_Rate,
                        "TVSEC_ADULT_MEAN_OPD_FREQ_Rate": TVSEC_ADULT_MEAN_OPD_FREQ_Rate,
                        "TVSEC_ELDER_MEAN_OPD_FREQ_Rate": TVSEC_ELDER_MEAN_OPD_FREQ_Rate,
                        "TVSEC_YOUTH_DIR_OPD_COST_Rate": TVSEC_YOUTH_DIR_OPD_COST_Rate,
                        "TVSEC_ADULT_DIR_OPD_COST_Rate": TVSEC_ADULT_DIR_OPD_COST_Rate,
                        "TVSEC_ELDER_DIR_OPD_COST_Rate": TVSEC_ELDER_DIR_OPD_COST_Rate,
                        "TVSEC_YOUTH_PROD_OPD_LOSS_Rate": TVSEC_YOUTH_PROD_OPD_LOSS_Rate,
                        "TVSEC_ADULT_PROD_OPD_LOSS_Rate": TVSEC_ADULT_PROD_OPD_LOSS_Rate,
                        "TVSEC_ELDER_PROD_OPD_LOSS_Rate": TVSEC_ELDER_PROD_OPD_LOSS_Rate,
                        "TVSEC_YOUTH_TRANS_COST_Rate": TVSEC_YOUTH_TRANS_COST_Rate,
                        "TVSEC_ADULT_TRANS_COST_Rate": TVSEC_ADULT_TRANS_COST_Rate,
                        "TVSEC_ELDER_TRANS_COST_Rate": TVSEC_ELDER_TRANS_COST_Rate,
                    }, f, ensure_ascii=False)

                for group_idx in range(1, GROUP_NUM+1):
                    a = async_task(jobs.start_analysis, datadir, BMP_SIMULATION_DAY, group_idx, task_name="id_"+analysis_code+"_"+str(group_idx))
                    print("Group ", group_idx)
                    print("!!!! A: ", a)

                content = {
                    'analysis_code': analysis_code,
                    'homepage_status': "running_state",
                    "YOUTH_json_file": os.path.join('media', 'tmp', analysis_code, "YOUTH.json"),
                    "ADULT_json_file": os.path.join('media', 'tmp', analysis_code, "ADULT.json"),
                    "ELDER_json_file": os.path.join('media', 'tmp', analysis_code, "ELDER.json"),
                }
    return render(request, template, content)


# # hooks.py
# def print_result(task):
#     print("&&&&&& THIS IS THE RESULT !!!: ", task.result)


# def check_task_status(analysis_code):

def find_view(request):
    template = "main/find.html"

    form = AnalysisCodeForm(request.POST or None)
    print("### form: ", form)
    inside_or_outside = False
    # print("form.is_valid(): ", form.is_valid())
    data = {
        'labels': [],
        'totalInfected_sz': [],
        'currentInfected_sz': [],
        'newInfected_sz': [],
        'totalSeekMed_sz': [],
        'currentSeekMed_sz': [],
        'newSeekMed_sz': [],
        'totalDeath_sz': [],
        'newDeath_sz': [],
        'totalRecovery_sz': [],
        'newRecovery_sz': [],
        'totalReachDay_sz': [],
        'newReachDay_sz': [],
    }
    analysis_code = ""
    if form.is_valid():
        # print("*** form['your_analysis_code'].value: ", form['your_analysis_code'].value())
        analysis_code = form['your_analysis_code'].value()
        # task_result = fetch('id_' + analysis_code)
        # # print("@@@@@ task_result: ", task_result)
        # if task_result != None:
        datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', form['your_analysis_code'].value())
        data_json_file = os.path.join(datadir, "data.json")
        input_params_json_file = os.path.join(datadir, "input_params.json")
        if os.path.isfile(data_json_file) and os.path.isfile(input_params_json_file):
            print("Not None!!!")
            template = "main/home.html"

        else:
            print("None!!!")
        print("&&&&& data: ", data)
    content = {
        'analysis_code': analysis_code,
        'homepage_status': "post_running_state",
        "YOUTH_json_file": os.path.join('media', 'tmp', analysis_code, "YOUTH.json"),
        "ADULT_json_file": os.path.join('media', 'tmp', analysis_code, "ADULT.json"),
        "ELDER_json_file": os.path.join('media', 'tmp', analysis_code, "ELDER.json"),
    }

    return render(request, template, content)



    if request.method == 'POST':
        print("POST!")
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

def get_data(request, slug_analysis_code, *args, **kwargs):
    # labels = ["Red", "Blue", "Yellow", "Green", "Purple"]
    datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', slug_analysis_code)

    g1_input_param_file = os.path.join(datadir, "input_params.json")

    if os.path.isfile(g1_input_param_file):
        with open(g1_input_param_file, encoding="UTF-8") as f:
            input_param_data = json.load(f)
        group_num = input_param_data["GROUP_NUM"]
        # print("&&&& group_num: ", group_num)

    json_files = []
    all_data = {}
    if group_num >= 1:
        g1_json_file = os.path.join(datadir, "G1_data.json")
        json_files.append(g1_json_file)
    if group_num >= 2:
        g2_json_file = os.path.join(datadir, "G2_data.json")
        json_files.append(g2_json_file)
    if group_num >= 3:
        g3_json_file = os.path.join(datadir, "G3_data.json")
        json_files.append(g3_json_file)
    if group_num >= 4:
        g4_json_file = os.path.join(datadir, "G4_data.json")
        json_files.append(g4_json_file)

    # transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
    # labels_file = os.path.join(datadir, "labels.json")

    for gp_idx, json_file in enumerate(json_files):
        if os.path.isfile(json_file):
            with open(json_file, encoding="UTF-8") as f:
                data = json.load(f)
            # json.dump({}, f)
        else:
            data = {
                'labels': [],
                'totalInfected_sz': [],
                'currentInfected_sz': [],
                'newInfected_sz': [],
                'totalSeekMed_sz': [],
                'currentSeekMed_sz': [],
                'newSeekMed_sz': [],
                'totalDeath_sz': [],
                'newDeath_sz': [],
                'totalRecovery_sz': [],
                'newRecovery_sz': [],
                'totalReachDay_sz': [],
                'newReachDay_sz': [],
            }
        all_data["Group_"+str(gp_idx+1)] = data

    # print("^^^^^^ slug_analysis_code: ", slug_analysis_code)
    # print("^^^^^^ data: ", all_data)

    all_data['analysis_code'] = slug_analysis_code
    # print("^^^^^^ new data: ", all_data)

    # print("django_q_tasks.objects(): ", django_q_tasks.Success)

    # taskr = fetch("267d724c903f49cba48c9d0f835a70e5", cached=True)
    # print("$$$$$$$$$$$$", "267d724c903f49cba48c9d0f835a70e5", "   ", taskr)
    success = django_q.models.Success.objects
    success_all = success.all()
    task_status_ls = []

    for group_idx in range(1, group_num+1):
        task_status = False
        for success_itr in success_all:
            if ("id_"+slug_analysis_code+"_"+str(group_idx) == success_itr.name):
                task_status = True
                break
            else:
                task_status = False
        task_status_ls.append(task_status)

    print("task_status_ls: ", task_status_ls)
    all_data['task_status'] = all(task_status_ls)
    print("task_status: ", all(task_status_ls))

    # check_task_status(slug_analysis_code)

    # content = {
    #     'analysis_code': slug_analysis_code,
    #     'data': data,
    #     'labels': labels,
    # }
    return JsonResponse(all_data)

def get_params_data(request, slug_analysis_code, *args, **kwargs):
    datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', slug_analysis_code)
    input_params_json_file = os.path.join(datadir, "input_params.json")
    print("input_params_json_file: ", input_params_json_file)

    if os.path.isfile(input_params_json_file):
        with open(input_params_json_file, encoding="UTF-8") as f:
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
