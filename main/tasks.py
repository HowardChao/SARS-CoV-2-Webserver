from celery import shared_task
import delegator
import logging
import os
import json

from .model import model

logger = logging.getLogger(__name__)

@shared_task
def start_analysis(datadir):
    # print("Inside start_analysis: ", start_analysis)
    transmission_gp_sz_file = os.path.join(datadir, "transmission_gp_sz.json")
    labels_file = os.path.join(datadir, "labels.json")

    transmission_gp_sz = []
    labels = []
    md = model.VaccineModel()
    transmission_gp_sz.append(len(md.transmission_gp))
    labels.append("Day 0")
    for i in range(10):
        md.one_day_passed()

        transmission_gp_sz.append(len(md.transmission_gp))
        with open(transmission_gp_sz_file, 'w') as f:
            json.dump(transmission_gp_sz, f)

        labels.append("Day "+str(i+1))
        with open(labels_file, 'w') as f:
            json.dump(labels, f)
