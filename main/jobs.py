import delegator
import logging
import os
import json

from .vmodel import model

logger = logging.getLogger(__name__)

def start_analysis(datadir, cycle_days, group_idx):
    print("@@@@@@@ group_idx: ", group_idx)
    print("Inside start_analysis: ", start_analysis)
    # totalInfected_sz_file = os.path.join(datadir, "totalInfected_sz.json")
    # currentInfected_sz_file = os.path.join(datadir, "currentInfected_sz.json")
    # newInfected_sz_file = os.path.join(datadir, "newInfected_sz.json")
    # totalDeath_sz_file = os.path.join(datadir, "totalDeath_sz.json")
    # newDeath_sz_file = os.path.join(datadir, "newDeath_sz.json")
    # totalRecovery_sz_file = os.path.join(datadir, "totalRecovery_sz.json")
    # newRecovery_sz_file = os.path.join(datadir, "newRecovery_sz.json")
    # totalReachDay_sz_file = os.path.join(datadir, "totalReachDay_sz.json")
    # newReachDay_sz_file = os.path.join(datadir, "newReachDay_sz.json")
    #
    # labels_file = os.path.join(datadir, "labels.json")
    json_file = os.path.join(datadir, "G"+str(group_idx)+"_data.json")
    input_params_file = os.path.join(datadir, "input_params.json")

    # model_results = {
    #     "Group_1": {},
    #     "Group_2": {},
    #     "Group_3": {},
    #     "Group_4": {}
    # }

    # for group_idx in range(1, group_num+1):
    labels = []
    labels.append("Day 0")
    md = model.VaccineModel(params_file_path=input_params_file, group_idx=group_idx)
    totalInfected_sz = md.totalInfected
    currentInfected_sz = md.currentInfected
    newInfected_sz = md.newInfected
    totalSeekMed_sz = md.totalSeekMed
    currentSeekMed_sz = md.currentSeekMed
    newSeekMed_sz = md.newSeekMed
    totalDeath_sz = md.totalDeath
    newDeath_sz = md.newDeath
    # totalRecovery_sz = md.totalRecovery
    # newRecovery_sz = md.newRecovery
    totalRecovery_sz = md.totalRecovery + md.totalReachDay
    newRecovery_sz = md.newRecovery + md.newReachDay
    totalReachDay_sz = md.totalReachDay
    newReachDay_sz =  md.newReachDay

    cost_labels = ["Vaccination Cost", "Vaccination Side Effects Cost", "Mortality Cost", "Inpatient Cost", "Outpatient Cost"]
    total_expanse_sz = md.totalExpanse
    cost_results_sz = [md.vac_cost, md.vac_side_effect_cost, md.mortality_cost, md.hospitalization_cost, md.outpatient_cost]

    json_data = {
        'labels': labels,
        'totalInfected_sz': totalInfected_sz,
        'currentInfected_sz': currentInfected_sz,
        'newInfected_sz': newInfected_sz,
        'totalSeekMed_sz': totalSeekMed_sz,
        'currentSeekMed_sz': currentSeekMed_sz,
        'newSeekMed_sz': newSeekMed_sz,
        'totalDeath_sz': totalDeath_sz,
        'newDeath_sz': newDeath_sz,
        'totalRecovery_sz': totalRecovery_sz,
        'newRecovery_sz': newRecovery_sz,
        'totalReachDay_sz': totalReachDay_sz,
        'newReachDay_sz': newReachDay_sz,
        'cost_labels': cost_labels,
        'total_expanse_sz': total_expanse_sz,
        'cost_results_sz': cost_results_sz
    }
    # model_results["Group_"+str(group_idx)] = json_data



    for i in range(cycle_days):
        md.one_day_passed()
        totalInfected_sz = md.totalInfected
        currentInfected_sz = md.currentInfected
        newInfected_sz = md.newInfected
        totalSeekMed_sz = md.totalSeekMed
        currentSeekMed_sz = md.currentSeekMed
        newSeekMed_sz = md.newSeekMed
        totalDeath_sz = md.totalDeath
        newDeath_sz = md.newDeath
        # totalRecovery_sz = md.totalRecovery
        # newRecovery_sz = md.newRecovery
        totalRecovery_sz = md.totalRecovery + md.totalReachDay
        newRecovery_sz = md.newRecovery + md.newReachDay
        totalReachDay_sz = md.totalReachDay
        newReachDay_sz =  md.newReachDay

        total_expanse_sz = md.totalExpanse
        cost_results_sz = [md.vac_cost, md.vac_side_effect_cost, md.mortality_cost, md.hospitalization_cost, md.outpatient_cost]


        labels.append("Day "+str(i+1))
        json_data = {
            'labels': labels,
            'totalInfected_sz': totalInfected_sz,
            'currentInfected_sz': currentInfected_sz,
            'newInfected_sz': newInfected_sz,
            'totalSeekMed_sz': totalSeekMed_sz,
            'currentSeekMed_sz': currentSeekMed_sz,
            'newSeekMed_sz': newSeekMed_sz,
            'totalDeath_sz': totalDeath_sz,
            'newDeath_sz': newDeath_sz,
            'totalRecovery_sz': totalRecovery_sz,
            'newRecovery_sz': newRecovery_sz,
            'totalReachDay_sz': totalReachDay_sz,
            'newReachDay_sz': newReachDay_sz,
            'cost_labels': cost_labels,
            'total_expanse_sz': total_expanse_sz,
            'cost_results_sz': cost_results_sz
        }
        # model_results["Group_"+str(group_idx)] = json_data

        print("json_data: ", json_data)
        with open(json_file, 'w') as f:
            json.dump(json_data, f)

        # with open(labels_file, 'w') as f:
        #     json.dump(labels, f)
