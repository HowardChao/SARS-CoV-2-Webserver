import delegator
import logging
import os
import json

from .model import model

logger = logging.getLogger(__name__)

def start_analysis(datadir):
    # print("Inside start_analysis: ", start_analysis)
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
    json_file = os.path.join(datadir, "data.json")


    labels = []
    labels.append("Day 0")
    md = model.VaccineModel()
    totalInfected_sz = md.totalInfected
    currentInfected_sz = md.currentInfected
    newInfected_sz = md.newInfected
    totalDeath_sz = md.totalDeath
    newDeath_sz = md.newDeath
    totalRecovery_sz = md.totalRecovery
    newRecovery_sz = md.newRecovery
    totalReachDay_sz = md.totalReachDay
    newReachDay_sz =  md.newReachDay

    json_data = {
        'labels': labels,
        'totalInfected_sz': totalInfected_sz,
        'currentInfected_sz': currentInfected_sz,
        'newInfected_sz': newInfected_sz,
        'totalDeath_sz': totalDeath_sz,
        'newDeath_sz': newDeath_sz,
        'totalRecovery_sz': totalRecovery_sz,
        'newRecovery_sz': newRecovery_sz,
        'totalReachDay_sz': totalReachDay_sz,
        'newReachDay_sz': newReachDay_sz,
    }

    for i in range(5):
        md.one_day_passed()
        totalInfected_sz = md.totalInfected
        currentInfected_sz = md.currentInfected
        newInfected_sz = md.newInfected
        totalDeath_sz = md.totalDeath
        newDeath_sz = md.newDeath
        totalRecovery_sz = md.totalRecovery
        newRecovery_sz = md.newRecovery
        totalReachDay_sz = md.totalReachDay
        newReachDay_sz =  md.newReachDay
        labels.append("Day "+str(i+1))
        json_data = {
            'labels': labels,
            'totalInfected_sz': totalInfected_sz,
            'currentInfected_sz': currentInfected_sz,
            'newInfected_sz': newInfected_sz,
            'totalDeath_sz': totalDeath_sz,
            'newDeath_sz': newDeath_sz,
            'totalRecovery_sz': totalRecovery_sz,
            'newRecovery_sz': newRecovery_sz,
            'totalReachDay_sz': totalReachDay_sz,
            'newReachDay_sz': newReachDay_sz,
        }

        print("json_data: ", json_data)
        with open(json_file, 'w') as f:
            json.dump(json_data, f)

        # with open(labels_file, 'w') as f:
        #     json.dump(labels, f)
