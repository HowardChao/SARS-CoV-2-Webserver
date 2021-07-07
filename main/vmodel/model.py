import random
import copy
import numpy as np
import json

from .parameters import IDX_CASE_NUM, SIMULATION_DAY, CYCLE_DAYS, CONTACT_PEOPLE_NUM, AgeGroupPerc, RouteStatus, CurrStatus
from .person import Person

class VaccineModel:
    def __init__(self, params_file_path, group_idx):
        with open(params_file_path, 'r', encoding="UTF-8") as f:
            params_data = json.load(f)
        # print("*** params_data[BMP_IDX_CASE_NUM]: ", params_data["BMP_IDX_CASE_NUM"])
        self.params_file_path = params_file_path
        self.group_idx = group_idx
        self.idx_case_num = params_data["BMP_IDX_CASE_NUM"]
        self.sim_day = params_data["BMP_SIMULATION_DAY"]
        self.day = 0
        self.cycle_days = params_data["BMP_CYCLE_DAYS"]
        self.contact_people_num = params_data["BMP_CONTACT_PEOPLE_NUM"]

        ## In_model group
        self.transmission_gp = []
        self.seek_med_gp = []

        ## Leave model group
        self.death_gp = []
        self.recovery_gp = []
        self.cycle_reached_gp = []

        ## Plotting Params
        self.totalInfected = []
        self.currentInfected = []
        self.newInfected = []

        self.totalSeekMed = []
        self.currentSeekMed = []
        self.newSeekMed = []

        self.totalDeath = []
        self.newDeath = []

        self.totalRecovery = []
        self.newRecovery = []

        self.totalReachDay = []
        self.newReachDay = []

        self.initial_model()

        self.totalExpanse = 0
        self.vac_cost = 0
        self.vac_side_effect_cost = 0
        self.mortality_cost = 0
        self.hospitalization_cost = 0
        self.outpatient_cost = 0

        # Mortality cost
        # Transportation cost + Total hospitalization cost
        # Transportation cost + Total outpatient cost





    # Day 1
    def initial_model(self):
        print("##################")
        print("## Day ", str(self.day), " ##")
        print("##################")
        youth_pop = int((AgeGroupPerc.YOUTH_GRP.value)*self.idx_case_num)
        adult_pop = int((AgeGroupPerc.ADULT_GRP.value)*self.idx_case_num)
        elder_pop = self.idx_case_num - youth_pop - adult_pop
        # int((AgeGroupPerc.ELDER_GRP.value)*self.idx_case_num)
        for i in range(youth_pop):
            age = random.randrange(0, 18)
            p = Person(age, initial_idx_case=True, params_file_path=self.params_file_path, group_idx=self.group_idx)
            self.transmission_gp.append(p)
        for i in range(adult_pop):
            age = random.randrange(19, 64)
            p = Person(age, initial_idx_case=True, params_file_path=self.params_file_path, group_idx=self.group_idx)
            self.transmission_gp.append(p)
        for i in range(elder_pop):
            age = random.randrange(65, 100)
            p = Person(age, initial_idx_case=True, params_file_path=self.params_file_path, group_idx=self.group_idx)
            self.transmission_gp.append(p)

        self.day += 1

        self.totalInfected.append(self.idx_case_num)
        self.currentInfected.append(self.idx_case_num)
        self.newInfected.append(0)

        self.totalSeekMed.append(0)
        self.currentSeekMed.append(0)
        self.newSeekMed.append(0)

        self.totalDeath.append(0)
        self.newDeath.append(0)

        self.totalRecovery.append(0)
        self.newRecovery.append(0)

        self.totalReachDay.append(0)
        self.newReachDay.append(0)


    def one_day_passed(self):
        print("##################")
        print("## Day ", str(self.day), " ##")
        print("##################")
        print('@@ Starting transmission_gp size: ', len(self.transmission_gp))

        new_transmission_gp = []
        trans_gp_2_seek_med_gp = []
        new_seek_med_gp = []
        new_death_gp = []
        new_recovery_gp = []
        new_cycle_reached_gp = []

        # total_infected_num = 0
        new_infected_num = 0
        # current_infected_num = 0
        new_seek_med_num = 0

        #####################################
        ### Transmission group processing ###
        #####################################
        for _p in self.transmission_gp:
            # cycle reached pre-check
            _p.in_trans_day += 1
            if _p.in_trans_day > 7:
                _p.trans_cycle_reached()

            if _p.curr_status == CurrStatus.TRANS_CYCLE_REACHED:
                new_cycle_reached_gp.append(_p)
            else:
                _p.trans_people_set_route_status()

            if _p.curr_status == CurrStatus.IN_TRANS_MODEL and _p.person_status[0] == 1:
                ##############################################
                ### Person stays in the transmission model ###
                ##############################################
                infected_ls = _p.contact_people(self.contact_people_num)
                new_infected_num += len(infected_ls)
                new_transmission_gp.append(_p)
                new_transmission_gp = new_transmission_gp + infected_ls
            elif _p.curr_status == CurrStatus.IN_MED_MODEL and _p.person_status[0] == 0:
                ########################################
                ### Person is in the seek med model ####
                ########################################
                # In the seektreatment path
                # _p.seek_medical_treatment()
                new_seek_med_num += 1
                trans_gp_2_seek_med_gp.append(_p)
            # print('%%%%%% in_trans_day       : ', _p.in_trans_day)
            # print('%%%%%% in_med_day         : ', _p.in_med_day)
            # print('%%%%%% SMT_IPD_day        : ', _p.SMT_IPD_day)
            # print('%%%%%% SMT_OPD_day        : ', _p.SMT_OPD_day)
            # print('%%%%%% SMT_OPD_M_day      : ', _p.SMT_OPD_M_day)
            # print('%%%%%% SMT_OPD_M_IPD_day  : ', _p.SMT_OPD_M_IPD_day)
            # print('%%%%%% SMT_OPD_NM_day     : ', _p.SMT_OPD_NM_day)
            # print('%%%%%% SMT_OPD_NM_IPD_day : ', _p.SMT_OPD_NM_IPD_day)


            ## Day post-processing
            # _p.trans_gp_day_postprocessing()
            ## Filter out reached people (_p can only be 'IN_TRANS_MODEL' or 'CYCLE_REACHED'.)
            # if _p.curr_status == CurrStatus.CYCLE_REACHED:
            #     new_cycle_reached_gp.append(_p)

        self.transmission_gp = new_transmission_gp
        self.seek_med_gp = self.seek_med_gp + trans_gp_2_seek_med_gp

        ###########################################
        ### Seek med treatment group processing ###
        ###########################################
        for _p in self.seek_med_gp:
            _p.in_med_day += 1
            # print('*** _p.in_med_day: ', _p.in_med_day)
            if _p.in_med_day == 1:
                _p.seek_medical_treatment()

        # self.totalExpanse = 0
        # self.vac_cost = 0
        # self.vac_side_effect_cost = 0
        # self.mortality_cost = 0
        # self.hospitalization_cost = 0
        # self.outpatient_cost = 0

            if _p.person_status[1] == 1:
                # Patient is IPD
                if _p.in_med_day > _p.SMT_IPD_day:
                    # Cost for IPD
                    self.hospitalization_cost += _p.SMT_IPD_day*(_p.tic_cost_per_bed_per_day_rate+_p.tic_hos_loss_per_day_rate)+ _p.tic_trans_cost_rate
                    self.outpatient_cost += 0
                    if _p.person_status[2] == 1:
                        # Patient is IPD death
                        _p.death()

                    elif _p.person_status[2] == 0:
                        # Patient is IPD recovery
                        _p.recovery()

            elif _p.person_status[1] == 0:
                # Patient is OPD
                if _p.in_med_day > _p.SMT_OPD_day:
                    if _p.person_status[2] == 1:
                        # Patient is OPD, medicine
                        if _p.in_med_day > _p.SMT_OPD_day+_p.SMT_OPD_M_day:
                            if _p.person_status[3] == 1:
                                # Patient is OPD, medicine, IPD
                                if _p.in_med_day > _p.SMT_OPD_day+_p.SMT_OPD_M_day+_p.SMT_OPD_M_IPD_day:

                                    self.hospitalization_cost += _p.SMT_OPD_M_IPD_day*(_p.tic_cost_per_bed_per_day_rate+_p.tic_hos_loss_per_day_rate)+ _p.tic_trans_cost_rate
                                    self.outpatient_cost += _p.toc_treat_cost_rate + _p.SMT_OPD_day*_p.toc_opd_lost_per_day_rate + _p.toc_trans_cost_rate

                                    if _p.person_status[4] == 1:
                                        # Patient is OPD, medicine, IPD, death
                                        _p.death()
                                    elif _p.person_status[4] == 0:
                                        # Patient is OPD, medicine, IPD, recovery
                                        _p.recovery()
                            elif _p.person_status[3] == 0:
                                # Patient is OPD, medicine, recoveory
                                self.hospitalization_cost += 0
                                self.outpatient_cost += _p.toc_treat_cost_rate + _p.SMT_OPD_day*_p.toc_opd_lost_per_day_rate + _p.toc_trans_cost_rate
                                _p.recovery()

                    elif _p.person_status[2] == 0:
                        # Patient is OPD, no medicine
                        if _p.in_med_day > _p.SMT_OPD_day+_p.SMT_OPD_NM_day:
                            if _p.person_status[3] == 1:
                                # Patient is OPD, no medicine, IPD
                                if _p.in_med_day > _p.SMT_OPD_day+_p.SMT_OPD_NM_day+_p.SMT_OPD_NM_IPD_day:

                                    self.hospitalization_cost += _p.SMT_OPD_M_IPD_day*(_p.tic_cost_per_bed_per_day_rate+_p.tic_hos_loss_per_day_rate)+ _p.tic_trans_cost_rate
                                    self.outpatient_cost += _p.toc_treat_cost_rate + _p.SMT_OPD_day*_p.toc_opd_lost_per_day_rate + _p.toc_trans_cost_rate

                                    # print("_p.tic_cost_per_bed_per_day_rate: ", _p.tic_cost_per_bed_per_day_rate)

                                    if _p.person_status[4] == 1:
                                        # Patient is OPD, no medicine, IPD, death
                                        _p.death()
                                    elif _p.person_status[4] == 0:
                                        # Patient is OPD, no medicine, IPD, recovery
                                        _p.recovery()
                            elif _p.person_status[3] == 0:
                                # Patient is OPD, no medicine, recovery
                                self.hospitalization_cost += 0
                                self.outpatient_cost += _p.toc_treat_cost_rate + _p.SMT_OPD_day*_p.toc_opd_lost_per_day_rate + _p.toc_trans_cost_rate
                                _p.recovery()


            if _p.curr_status == CurrStatus.IN_MED_MODEL and _p.person_status[0] == 0:
                new_seek_med_gp.append(_p)
            elif _p.curr_status == CurrStatus.DEATH:
                # Cost for IPD
                self.vac_cost += _p.vac_cost
                self.vac_side_effect_cost += _p.vac_side_effect_cost
                new_death_gp.append(_p)
                # Cost for death
                self.mortality_cost += _p.mc_earn_lost_per_death_rate
            elif _p.curr_status == CurrStatus.RECOVERY:
                # Cost for IPD
                self.vac_cost += _p.vac_cost
                self.vac_side_effect_cost += _p.vac_side_effect_cost
                new_recovery_gp.append(_p)
            # print('&&&&&& in_trans_day       : ', _p.in_trans_day)
            # print('&&&&&& in_med_day         : ', _p.in_med_day)
            # print('&&&&&& SMT_IPD_day        : ', _p.SMT_IPD_day)
            # print('&&&&&& SMT_OPD_day        : ', _p.SMT_OPD_day)
            # print('&&&&&& SMT_OPD_M_day      : ', _p.SMT_OPD_M_day)
            # print('&&&&&& SMT_OPD_M_IPD_day  : ', _p.SMT_OPD_M_IPD_day)
            # print('&&&&&& SMT_OPD_NM_day     : ', _p.SMT_OPD_NM_day)
            # print('&&&&&& SMT_OPD_NM_IPD_day : ', _p.SMT_OPD_NM_IPD_day)


        self.seek_med_gp = new_seek_med_gp
        self.death_gp = self.death_gp + new_death_gp
        self.recovery_gp = self.recovery_gp + new_recovery_gp
        self.cycle_reached_gp = self.cycle_reached_gp + new_cycle_reached_gp
        self.day += 1
        self.totalExpanse = self.vac_cost + self.vac_side_effect_cost + self.mortality_cost + self.hospitalization_cost + self.outpatient_cost
        print("$$ self.vac_cost             : ", self.vac_cost)
        print("$$ self.vac_side_effect_cost : ", self.vac_side_effect_cost)
        print("$$ self.mortality_cost       : ", self.mortality_cost)
        print("$$ self.hospitalization_cost : ", self.hospitalization_cost)
        print("$$ self.outpatient_cost      : ", self.outpatient_cost)
        print("$$ self.totalExpanse         : ", self.totalExpanse)

        # print('     new_transmission_gp size      : ', len(new_transmission_gp))
        # print('         self.transmission_gp size : ', len(self.transmission_gp))
        # print('     new_seek_med_gp size          : ', len(new_seek_med_gp))
        # print('         self.seek_med_gp size     : ', len(self.seek_med_gp))
        # print('     new_death_gp                  : ', len(new_death_gp))
        # print('         self.death_gp size        : ', len(self.death_gp))
        # print('     new_recovery_gp               : ', len(new_recovery_gp))
        # print('         self.recovery_gp size     : ', len(self.recovery_gp))
        # print('     new_cycle_reached_gp          : ', len(new_cycle_reached_gp))
        # print('         self.cycle_reached_gp size: ', len(self.cycle_reached_gp))
        #########################
        ## update model params ##
        #########################
        self.totalInfected.append(len(self.transmission_gp) + len(self.seek_med_gp) + len(self.death_gp) + len(self.recovery_gp) + len(self.cycle_reached_gp))
        self.currentInfected.append(len(self.transmission_gp))
        self.newInfected.append(new_infected_num)


        self.totalSeekMed.append(len(self.seek_med_gp) + len(self.death_gp) + len(self.recovery_gp))
        self.currentSeekMed.append(len(self.seek_med_gp))
        self.newSeekMed.append(new_seek_med_num)


        self.totalDeath.append(len(self.death_gp))
        self.newDeath.append(len(new_death_gp))

        self.totalRecovery.append(len(self.recovery_gp))
        self.newRecovery.append(len(new_recovery_gp))

        self.totalReachDay.append(len(self.cycle_reached_gp))
        self.newReachDay.append(len(new_cycle_reached_gp))

        # print('     totalInfected size        : ', self.totalInfected)
        # print('     currentInfected size      : ', self.currentInfected)
        # print('     newInfected size          : ', self.newInfected)
        #
        # print('     totalSeekMed size         : ', self.totalSeekMed)
        # print('     currentSeekMed size       : ', self.currentSeekMed)
        # print('     newSeekMed size           : ', self.newSeekMed)
        #
        # print('     totalDeath size           : ', self.totalDeath)
        # print('     newDeath size             : ', self.newDeath)
        #
        # print('     totalRecovery size        : ', self.totalRecovery)
        # print('     newRecovery size          : ', self.newRecovery)
        #
        # print('     totalReachDay size        : ', self.totalReachDay)
        # print('     newReachDay size          : ', self.newReachDay)
