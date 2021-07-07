import uuid
import random
import numpy as np
import scipy.stats
import json
from .parameters import CurrStatus, RouteStatus, AgeGroup, ContactPersonSeekTreatment_Rate, ContactGroup_Rate, Vaccine_Rate, Vac_Infection_Rate, NoVac_Infection_Rate, SMT_IPDOPD_Rate, SMT_IPD_Death_Rate, SMT_OPD_MedicineIntake_Rate, SMT_OPD_M_IPD_Rate, SMT_OPD_M_IPD_Death_Rate, SMT_OPD_NM_IPD_Rate, SMT_OPD_NM_IPD_Death_Rate, effectiveness, Total_Vaccination_Cost

from .parameters import SMT_IPD_DIST, SMT_OPD_DIST, SMT_OPD_M_DIST, SMT_OPD_M_IPD_DIST, SMT_OPD_NM_DIST, SMT_OPD_NM_IPD_DIST


class Person:
    def __init__(self, age, initial_idx_case=False, params_file_path="", group_idx=0):
        self.params_file_path = params_file_path
        self.group_idx = group_idx
        self.id = str(uuid.uuid1())
        self.initial_idx_case = initial_idx_case
        self.person_status = [-1, -1, -1, -1, -1]

    # INITIAL = 'initial'
    # IN_TRANS_MODEL = 'in_trans_model'
    # TRANS_CYCLE_REACHED = 'trans_cycle_reached'
    # IN_MED_MODEL = 'in_med_model'
    # RECOVERY = 'recovery'
    # DEATH = 'death'
        self.vac_cost = 0
        self.vac_side_effect_cost = 0

        self.curr_status = CurrStatus.INITIAL
        self.in_trans_day = 0
        self.in_med_day = 0

        self.SMT_IPD_day = 0
        self.SMT_OPD_day = 0
        self.SMT_OPD_M_day = 0
        self.SMT_OPD_M_IPD_day = 0
        self.SMT_OPD_NM_day = 0
        self.SMT_OPD_NM_IPD_day = 0

        self.age = age
        with open(params_file_path, 'r', encoding="UTF-8") as f:
            params_data = json.load(f)
        self.params_data = params_data
        self.age_group = self.set_age_group()
        self.contactperson_rate, self.seektreatment_rate = self.set_contactperson_seektreatment_rate()
        self.youth_contact_rate = self.set_contact_rate('youth')
        self.adult_contact_rate = self.set_contact_rate('adult')
        self.elder_contact_rate = self.set_contact_rate('elder')
        self.vaccine_rate, self.n_vaccine_rate = self.set_vaccine_rate()
        self.vac_infection_rate, self.vac_n_infection_rate = self.set_vac_infection_rate()
        self.n_vac_infection_rate, self.n_vac_n_infection_rate = self.set_n_vac_infection_rate()

        # Initialization
        self.tvc_vac_cost_rate, self.tvc_vac_lost_per_hour_rate, self.tvc_trans_cost_rate, self.tvc_eff = self.set_vaccination_cost_param()
        self.tvsec_side_eff_rate, self.tvsec_mean_opd_freq_rate, self.tvsec_dir_opd_cost_rate, self.tvsec_prod_opd_loss_rate, self.tvsec_trans_cost_rate = self.set_vaccine_side_effect_cost_param()
        self.mc_earn_lost_per_death_rate= self.set_mortality_cost_param()
        self.tic_ave_stay_day_rate, self.tic_cost_per_bed_per_day_rate, self.tic_hos_loss_per_day_rate, self.tic_trans_cost_rate = self.set_hospitalization_cost_param()
        self.toc_ave_day_lost_rate, self.toc_treat_cost_rate, self.toc_opd_lost_per_day_rate, self.toc_trans_cost_rate = self.set_outpatient_cost_param()

        self.set_vaccine_status()
        self.infection_status = False
        self.set_initial_idx_case()



        self.smt_ipd_rate, self.smt_opd_rate = self.set_smt_ipd_opd_rate()
        self.smt_ipd_death_rate, self.smt_ipd_recovery_rate = self.set_smt_ipd_death_rate()
        self.smt_opd_medicine_rate, self.smt_opd_n_medicine_rate = self.set_smt_opd_medicineintake_rate()
        self.smt_opd_m_ipd_rate, self.smt_opd_m_recovery_rate = self.set_smt_opd_m_ipd_rate()
        self.smt_opd_m_ipd_death_rate, self.smt_opd_m_ipd_recovery_rate = self.set_smt_opd_m_ipd_death_rate()
        self.smt_opd_nm_ipd_rate, self.smt_opd_nm_recovery_rate = self.set_smt_opd_nm_ipd_rate()
        self.smt_opd_nm_ipd_death_rate, self.smt_opd_nm_ipd_recovery_rate = self.set_smt_opd_nm_ipd_death_rate()

        # print("$$ self.vac_cost = 0", self.vac_cost)
        # print("$$ self.vac_side_effect_cost = 0", self.vac_side_effect_cost)

        # self.infection_rate = self.set_infection_rate()
        #
        # self.seek_treatment_rate = self.set_seek_treatment_rate()
        #
        # self.seek_treatment_status = False
        #
        # self.medicine_intake_rate = self.set_medicine_intake_rate()
        # self.medicine_intake_status = False
        #
        # self.severe_rate = self.set_severe_rate()
        # self.severe_status = False
        #
        # self.fatality_rate = self.set_fatality_rate()
        # self.effectiveness_mild = effectiveness.MILD
        # self.effectiveness_severe = effectiveness.SEVERE
        # self.effectiveness_death = effectiveness.DEATH

        #    Total vaccination cost
        #    Total costs of vaccine side effects
        # print("%%%%%%%%%%% self.vaccine_status: ", self.vaccine_status)



    ## Cost calculation setting
    def set_vaccination_cost_param(self):
        if self.age <= 18:
            return self.params_data["MC_YOUTH_EARN_LOST_PER_DEATH_Rate"], self.params_data["TVC_YOUTH_VAC_LOST_PER_HOUR_Rate"], self.params_data["TVC_YOUTH_TRANS_COST_Rate"], self.params_data["TVC_YOUTH_EFF"]
        elif self.age > 18 and self.age <65:
            return self.params_data["TVC_ADULT_VAC_COST_Rate"], self.params_data["TVC_ADULT_VAC_LOST_PER_HOUR_Rate"], self.params_data["TVC_ADULT_TRANS_COST_Rate"], self.params_data["TVC_ADULT_EFF"]
        elif self.age >= 65:
            return self.params_data["TVC_ELDER_VAC_COST_Rate"], self.params_data["TVC_ELDER_VAC_LOST_PER_HOUR_Rate"], self.params_data["TVC_ELDER_TRANS_COST_Rate"], self.params_data["TVC_ELDER_EFF"]

    def set_vaccine_side_effect_cost_param(self):
        if self.age <= 18:
            return self.params_data["TVSEC_YOUTH_SIDE_EFF_Rate"], self.params_data["TVSEC_YOUTH_MEAN_OPD_FREQ_Rate"], self.params_data["TVSEC_YOUTH_DIR_OPD_COST_Rate"], self.params_data["TVSEC_YOUTH_PROD_OPD_LOSS_Rate"], self.params_data["TVSEC_YOUTH_TRANS_COST_Rate"]
        elif self.age > 18 and self.age <65:
            return self.params_data["TVSEC_ADULT_SIDE_EFF_Rate"], self.params_data["TVSEC_ADULT_MEAN_OPD_FREQ_Rate"], self.params_data["TVSEC_ADULT_DIR_OPD_COST_Rate"], self.params_data["TVSEC_ADULT_PROD_OPD_LOSS_Rate"], self.params_data["TVSEC_ADULT_TRANS_COST_Rate"]
        elif self.age >= 65:
            return self.params_data["TVSEC_ELDER_SIDE_EFF_Rate"], self.params_data["TVSEC_ELDER_MEAN_OPD_FREQ_Rate"], self.params_data["TVSEC_ELDER_DIR_OPD_COST_Rate"], self.params_data["TVSEC_ELDER_PROD_OPD_LOSS_Rate"], self.params_data["TVSEC_ELDER_TRANS_COST_Rate"]


    def set_mortality_cost_param(self):
        if self.age <= 18:
            return self.params_data["MC_YOUTH_EARN_LOST_PER_DEATH_Rate"]
        elif self.age > 18 and self.age <65:
            return self.params_data["MC_ADULT_EARN_LOST_PER_DEATH_Rate"]
        elif self.age >= 65:
            return self.params_data["MC_ELDER_EARN_LOST_PER_DEATH_Rate"]

    def set_hospitalization_cost_param(self):
        if self.age <= 18:
            return self.params_data["TIC_YOUTH_AVE_STAY_DAY_Rate"], self.params_data["TIC_YOUTH_COST_PER_BED_PER_DAY_Rate"], self.params_data["TIC_YOUTH_HOS_LOSS_PER_DAY_Rate"], self.params_data["TIC_YOUTH_TRANS_COST_Rate"]
        elif self.age > 18 and self.age <65:
            return self.params_data["TIC_ADULT_AVE_STAY_DAY_Rate"], self.params_data["TIC_ADULT_COST_PER_BED_PER_DAY_Rate"], self.params_data["TIC_ADULT_HOS_LOSS_PER_DAY_Rate"], self.params_data["TIC_ADULT_TRANS_COST_Rate"]
        elif self.age >= 65:
            return self.params_data["TIC_ELDER_AVE_STAY_DAY_Rate"], self.params_data["TIC_ELDER_COST_PER_BED_PER_DAY_Rate"], self.params_data["TIC_ELDER_HOS_LOSS_PER_DAY_Rate"], self.params_data["TIC_ELDER_TRANS_COST_Rate"]

    def set_outpatient_cost_param(self):
        if self.age <= 18:
            return self.params_data["TOC_YOUTH_AVE_DAY_LOST_Rate"], self.params_data["TOC_YOUTH_TREAT_COST_Rate"], self.params_data["TOC_YOUTH_OPD_LOST_PER_DAY_Rate"], self.params_data["TOC_YOUTH_TRANS_COST_Rate"]
        elif self.age > 18 and self.age <65:
            return self.params_data["TOC_ADULT_AVE_DAY_LOST_Rate"], self.params_data["TOC_ADULT_TREAT_COST_Rate"], self.params_data["TOC_ADULT_OPD_LOST_PER_DAY_Rate"], self.params_data["TOC_ADULT_TRANS_COST_Rate"]
        elif self.age >= 65:
            return self.params_data["TOC_ELDER_AVE_DAY_LOST_Rate"], self.params_data["TOC_ELDER_TREAT_COST_Rate"], self.params_data["TOC_ELDER_OPD_LOST_PER_DAY_Rate"], self.params_data["TOC_ELDER_TRANS_COST_Rate"]


    ##################
    # Initialization #
    ##################
    def set_vaccine_status(self):
        if self.curr_status == CurrStatus.INITIAL:
            if self.initial_idx_case == True:
                self.vaccine_status = False
            else:
                rand_dice = random.random() < self.vaccine_rate
                if rand_dice:
                    self.vaccine_status = True
                    # print("%%%%%%%%%%% self.vaccine_status: ", self.vaccine_status)
                else:
                    self.vaccine_status = False
                    # print("%%%%%%%%%%% self.vaccine_status: ", self.vaccine_status)

        if self.vaccine_status == True:
            self.vac_cost = self.tvc_vac_cost_rate + self.tvc_vac_lost_per_hour_rate*16 + self.tvc_trans_cost_rate
            rand_dice = random.random() < self.tvsec_side_eff_rate
            if rand_dice:
                self.vac_side_effect_cost = self.tvsec_mean_opd_freq_rate * self.tvsec_dir_opd_cost_rate + self.tvsec_prod_opd_loss_rate + self.tvsec_trans_cost_rate
            else:
                self.vac_side_effect_cost = 0

    def set_initial_idx_case(self):
        if self.curr_status == CurrStatus.INITIAL:
            if self.initial_idx_case == True:
                self.curr_status = CurrStatus.IN_TRANS_MODEL
                self.infection_status = True
                self.person_status[0] = 1
            else:
                self.infection_status = False

    ##################
    # When the new infected person contact another person
    ##################
    def set_infection_status(self):
        # Only set infection status when it's false
        if self.infection_status == False:
            if self.initial_idx_case == True:
                self.infection_status = True
                self.curr_status = CurrStatus.IN_TRANS_MODEL
                self.person_status[0] = 1
            else:
                if self.vaccine_status == True:
                    rand_dice = random.random() < self.vac_infection_rate
                    if rand_dice:
                        self.infection_status = True
                        self.curr_status = CurrStatus.IN_TRANS_MODEL
                        self.person_status[0] = 1
                    else:
                        self.infection_status = False
                else:
                    rand_dice = random.random() < self.n_vac_infection_rate
                    if rand_dice:
                        self.infection_status = True
                        self.curr_status = CurrStatus.IN_TRANS_MODEL
                        self.person_status[0] = 1
                    else:
                        self.infection_status = False

    ##################
    # All the infected people need to choose their route everytime
    ##################
    def trans_people_set_route_status(self):
        # Only need to check when the person hasn't contact another person
        if self.curr_status == CurrStatus.IN_TRANS_MODEL and self.person_status[0] == 1 and self.infection_status == True:
            rand_dice = random.random() < self.contactperson_rate
            if rand_dice:
                self.person_status[0] = 1
                self.curr_status = CurrStatus.IN_TRANS_MODEL
            else:
                self.person_status[0] = 0
                self.curr_status = CurrStatus.IN_MED_MODEL

    ##################
    # After the infected people choose their route. Run their own path
    ##################
    def contact_people(self, ave_contacted_people_num):
        infected_people_ls = []
        # non_infected_people_ls = []
        for _ in range(ave_contacted_people_num):
            rand_age = np.random.choice(
                        [ random.randint(0, 18), random.randint(19, 64), random.randint(65, 100)],
                        1,
                        p=[self.youth_contact_rate,self.adult_contact_rate, self.elder_contact_rate]
                       )[0]
            p = Person(age=rand_age, params_file_path=self.params_file_path, group_idx=self.group_idx)
            # InfectionRate
            p.set_infection_status()
            if p.infection_status == True:
                infected_people_ls.append(p)
            # else:
            #     non_infected_people_ls.append(p)
        return infected_people_ls
            # , non_infected_people_ls


    def seek_medical_treatment(self):
        # Only run for first timer!!!!
        if self.curr_status == CurrStatus.IN_MED_MODEL and self.person_status[0] == 0:
            # print("*** Inside seek_medical_treatment:!!!")
            self.set_smt_IPD_opd_status()
            if self.person_status[1] == 1:
                # Patient is IPD
                self.set_smt_IPD_death_status()
                if self.person_status[2] == 1:
                    # self.death()
                    pass
                elif self.person_status[2] == 0:
                    # self.recovery()
                    pass
            elif self.person_status[1] == 0:
                # Patient is OPD
                self.set_smt_opd_medicineintake_status()
                if self.person_status[2] == 1:
                    self.set_smt_opd_m_IPD_status()
                    if self.person_status[3] == 1:
                        self.set_smt_opd_m_IPD_death_status()
                        if self.person_status[4] == 1:
                            # self.death()
                            pass
                        elif self.person_status[4] == 0:
                            # self.recovery()
                            pass
                    elif self.person_status[3] == 0:
                        # self.recovery()
                        pass
                elif self.person_status[2] == 0:
                    self.set_smt_opd_nm_IPD_status()
                    if self.person_status[3] == 1:
                        self.set_smt_opd_nm_IPD_death_status()
                        if self.person_status[4] == 1:
                            # self.death()
                            pass
                        elif self.person_status[4] == 0:
                            # self.recovery()
                            pass
                    elif self.person_status[3] == 0:
                        # self.recovery()
                        pass


    def set_smt_IPD_opd_status(self):
        rand_dice = random.random() < self.smt_ipd_rate
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0

    def set_smt_IPD_death_status(self):
        rand_dice = random.random() < self.smt_ipd_death_rate
        lower = SMT_IPD_DIST.SMT_IPD_DIST_LOWER.value
        upper = SMT_IPD_DIST.SMT_IPD_DIST_UPPER.value
        mu = SMT_IPD_DIST.SMT_IPD_DIST_MU.value
        sigma = SMT_IPD_DIST.SMT_IPD_DIST_SIGMA.value
        N = 1
        self.SMT_IPD_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])

        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 1
            self.person_status[2] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 1
            self.person_status[2] = 0

    def set_smt_opd_medicineintake_status(self):
        rand_dice = random.random() < self.smt_opd_medicine_rate
        lower = SMT_OPD_DIST.SMT_OPD_DIST_LOWER.value
        upper = SMT_OPD_DIST.SMT_OPD_DIST_UPPER.value
        mu = SMT_OPD_DIST.SMT_OPD_DIST_MU.value
        sigma = SMT_OPD_DIST.SMT_OPD_DIST_SIGMA.value
        N = 1
        self.SMT_OPD_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 0

    def set_smt_opd_m_IPD_status(self):
        rand_dice = random.random() < self.smt_opd_m_ipd_rate
        lower = SMT_OPD_M_DIST.SMT_OPD_M_DIST_LOWER.value
        upper = SMT_OPD_M_DIST.SMT_OPD_M_DIST_UPPER.value
        mu = SMT_OPD_M_DIST.SMT_OPD_M_DIST_MU.value
        sigma = SMT_OPD_M_DIST.SMT_OPD_M_DIST_SIGMA.value
        N = 1
        self.SMT_OPD_M_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 1
            self.person_status[3] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 1
            self.person_status[3] = 0

    def set_smt_opd_m_IPD_death_status(self):
        rand_dice = random.random() < self.smt_opd_m_ipd_death_rate
        lower = SMT_OPD_M_IPD_DIST.SMT_OPD_M_IPD_DIST_LOWER.value
        upper = SMT_OPD_M_IPD_DIST.SMT_OPD_M_IPD_DIST_UPPER.value
        mu = SMT_OPD_M_IPD_DIST.SMT_OPD_M_IPD_DIST_MU.value
        sigma = SMT_OPD_M_IPD_DIST.SMT_OPD_M_IPD_DIST_SIGMA.value
        N = 1
        self.SMT_OPD_M_IPD_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])
        # print("### self.SMT_OPD_M_IPD_day: ", self.SMT_OPD_M_IPD_day)
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 1
            self.person_status[3] = 1
            self.person_status[4] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 1
            self.person_status[3] = 1
            self.person_status[4] = 0

    def set_smt_opd_nm_IPD_status(self):
        rand_dice = random.random() < self.smt_opd_nm_ipd_rate
        lower = SMT_OPD_NM_DIST.SMT_OPD_NM_DIST_LOWER.value
        upper = SMT_OPD_NM_DIST.SMT_OPD_NM_DIST_UPPER.value
        mu = SMT_OPD_NM_DIST.SMT_OPD_NM_DIST_MU.value
        sigma = SMT_OPD_NM_DIST.SMT_OPD_NM_DIST_SIGMA.value
        N = 1
        self.SMT_OPD_NM_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 0
            self.person_status[3] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 0
            self.person_status[3] = 0

    def set_smt_opd_nm_IPD_death_status(self):
        rand_dice = random.random() < self.smt_opd_nm_ipd_death_rate
        lower = SMT_OPD_NM_IPD_DIST.SMT_OPD_NM_IPD_DIST_LOWER.value
        upper = SMT_OPD_NM_IPD_DIST.SMT_OPD_NM_IPD_DIST_UPPER.value
        mu = SMT_OPD_NM_IPD_DIST.SMT_OPD_NM_IPD_DIST_MU.value
        sigma = SMT_OPD_NM_IPD_DIST.SMT_OPD_NM_IPD_DIST_SIGMA.value
        N = 1
        self.SMT_OPD_NM_IPD_day = int(np.around(scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N))[0])
        if rand_dice:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 0
            self.person_status[3] = 1
            self.person_status[4] = 1
        else:
            self.person_status[0] = 0
            self.person_status[1] = 0
            self.person_status[2] = 0
            self.person_status[3] = 1
            self.person_status[4] = 0

    def trans_cycle_reached(self):
        self.curr_status = CurrStatus.TRANS_CYCLE_REACHED

    def death(self):
        self.curr_status = CurrStatus.DEATH

    def recovery(self):
        self.curr_status = CurrStatus.RECOVERY

    ## static
    def set_contactperson_seektreatment_rate(self):
        if self.age <= 18:
            return self.params_data["CP_SMT_YOUTH_Rate_CP"], self.params_data["CP_SMT_YOUTH_Rate_ST"]
        elif self.age > 18 and self.age <65:
            return self.params_data["CP_SMT_ADULT_Rate_CP"], self.params_data["CP_SMT_ADULT_Rate_ST"]
        elif self.age >= 65:
            return self.params_data["CP_SMT_ELDER_Rate_CP"], self.params_data["CP_SMT_ELDER_Rate_ST"]

    ## static
    def set_age_group(self):
        if self.age <= 18:
            return self.params_data["AGP_YOUTH_GRP"]
        elif self.age > 18 and self.age <65:
            return self.params_data["AGP_ADULT_GRP"]
        elif self.age >= 65:
            return self.params_data["AGP_ELDER_GRP"]

    ## static
    def set_contact_rate(self, category):
        if self.age <= 18:
            if category is 'youth':
                return self.params_data["CR_SAME_GRP"]
            elif category is 'adult':
                return self.params_data["CR_DIFF_GRP"]
            elif category is 'elder':
                return self.params_data["CR_DIFF_GRP"]
        elif self.age > 18 and self.age <65:
            if category is 'youth':
                return self.params_data["CR_DIFF_GRP"]
            elif category is 'adult':
                return self.params_data["CR_SAME_GRP"]
            elif category is 'elder':
                return self.params_data["CR_DIFF_GRP"]
        elif self.age >= 65:
            if category is 'youth':
                return self.params_data["CR_DIFF_GRP"]
            elif category is 'adult':
                return self.params_data["CR_DIFF_GRP"]
            elif category is 'elder':
                return self.params_data["CR_SAME_GRP"]

    def set_vaccine_rate(self):
        if self.group_idx == 1:
            if self.age <= 18:
                return self.params_data["G1_Vac_YOUTH_Rate_V"], 1-self.params_data["G1_Vac_YOUTH_Rate_V"]
            elif self.age > 18 and self.age <65:
                return self.params_data["G1_Vac_ADULT_Rate_V"], 1-self.params_data["G1_Vac_ADULT_Rate_V"]
            elif self.age >= 65:
                return self.params_data["G1_Vac_ELDER_Rate_V"], 1-self.params_data["G1_Vac_ELDER_Rate_V"]
        elif self.group_idx == 2:
            if self.age <= 18:
                return self.params_data["G2_Vac_YOUTH_Rate_V"], 1-self.params_data["G2_Vac_YOUTH_Rate_V"]
            elif self.age > 18 and self.age <65:
                return self.params_data["G2_Vac_ADULT_Rate_V"], 1-self.params_data["G2_Vac_ADULT_Rate_V"]
            elif self.age >= 65:
                return self.params_data["G2_Vac_ELDER_Rate_V"], 1-self.params_data["G2_Vac_ELDER_Rate_V"]
        elif self.group_idx == 3:
            if self.age <= 18:
                return self.params_data["G3_Vac_YOUTH_Rate_V"], 1-self.params_data["G3_Vac_YOUTH_Rate_V"]
            elif self.age > 18 and self.age <65:
                return self.params_data["G3_Vac_ADULT_Rate_V"], 1-self.params_data["G3_Vac_ADULT_Rate_V"]
            elif self.age >= 65:
                return self.params_data["G3_Vac_ELDER_Rate_V"], 1-self.params_data["G3_Vac_ELDER_Rate_V"]
        elif self.group_idx == 4:
            if self.age <= 18:
                return self.params_data["G4_Vac_YOUTH_Rate_V"], 1-self.params_data["G4_Vac_YOUTH_Rate_V"]
            elif self.age > 18 and self.age <65:
                return self.params_data["G4_Vac_ADULT_Rate_V"], 1-self.params_data["G4_Vac_ADULT_Rate_V"]
            elif self.age >= 65:
                return self.params_data["G4_Vac_ELDER_Rate_V"], 1-self.params_data["G4_Vac_ELDER_Rate_V"]

        # if self.age <= 18:
        #     return self.params_data["Vac_YOUTH_Rate_V"], 1-self.params_data["Vac_YOUTH_Rate_V"]
        # elif self.age > 18 and self.age <65:
        #     return self.params_data["Vac_ADULT_Rate_V"], 1-self.params_data["Vac_ADULT_Rate_V"]
        # elif self.age >= 65:
        #     return self.params_data["Vac_ELDER_Rate_V"], 1-self.params_data["Vac_ELDER_Rate_V"]

    def set_vac_infection_rate(self):
        if self.age <= 18:
            return self.params_data["Vac_Infection_YOUTH_Rate_V_I"], 1-self.params_data["Vac_Infection_YOUTH_Rate_V_I"]
        elif self.age > 18 and self.age <65:
            return self.params_data["Vac_Infection_ADULT_Rate_V_I"], 1-self.params_data["Vac_Infection_ADULT_Rate_V_I"]
        elif self.age >= 65:
            return self.params_data["Vac_Infection_ELDER_Rate_V_I"], 1-self.params_data["Vac_Infection_ELDER_Rate_V_I"]

    def set_n_vac_infection_rate(self):
        if self.age <= 18:
            return self.params_data["NoVac_Infection_YOUTH_Rate_NV_I"], 1-self.params_data["NoVac_Infection_YOUTH_Rate_NV_I"]
        elif self.age > 18 and self.age <65:
            return self.params_data["NoVac_Infection_ADULT_Rate_NV_I"], 1-self.params_data["NoVac_Infection_ADULT_Rate_NV_I"]
        elif self.age >= 65:
            return self.params_data["NoVac_Infection_ELDER_Rate_NV_I"], 1-self.params_data["NoVac_Infection_ELDER_Rate_NV_I"]

    def set_smt_ipd_opd_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_IPDOPD_YOUTH_Rate_IPD"], self.params_data["SMT_IPDOPD_YOUTH_Rate_OPD"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_IPDOPD_ADULT_Rate_IPD"], self.params_data["SMT_IPDOPD_ADULT_Rate_OPD"]
        elif self.age >= 65:
            return self.params_data["SMT_IPDOPD_ELDER_Rate_IPD"], self.params_data["SMT_IPDOPD_ELDER_Rate_OPD"]

    def set_smt_ipd_death_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D"]


    def set_smt_opd_medicineintake_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M"], 1-self.params_data["SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M"], 1-self.params_data["SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M"], 1-self.params_data["SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M"]

    def set_smt_opd_m_ipd_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD"], 1-self.params_data["SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD"], 1-self.params_data["SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD"], 1-self.params_data["SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD"]

    def set_smt_opd_m_ipd_death_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D"], 1-self.params_data["SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D"]

    def set_smt_opd_nm_ipd_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD"], 1-self.params_data["SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD"], 1-self.params_data["SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD"], 1-self.params_data["SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD"]

    def set_smt_opd_nm_ipd_death_rate(self):
        if self.age <= 18:
            return self.params_data["SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D"], 1-self.params_data["SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D"]
        elif self.age > 18 and self.age <65:
            return self.params_data["SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D"], 1-self.params_data["SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D"]
        elif self.age >= 65:
            return self.params_data["SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D"], 1-self.params_data["SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D"]

    ##########################
    ## Outside Calling func ##
    ##########################
    def trans_gp_day_preprocessing(self):
        self.in_trans_day += 1
        if self.in_trans_day > 7:
            self.trans_cycle_reached()
        if self.curr_status == CurrStatus.TRANS_CYCLE_REACHED:
            pass
        if self.curr_status == CurrStatus.IN_TRANS_MODEL and self.person_status[0] == 1:
            self.trans_people_set_route_status()

    def seek_med_gp_day_preprocessing(self):
        if self.curr_status == CurrStatus.IN_MED_MODEL and self.person_status[0] == 0:
            pass

    def trans_gp_day_postprocessing(self):
        if self.curr_status == CurrStatus.IN_TRANS_MODEL and self.person_status[0] == 1:
            #########################################
            ### Transmission model one day pass!! ###
            #########################################
            self.in_trans_day += 1
            if self.in_trans_day == 7:
                self.trans_cycle_reached()

    # def seek_med_gp_day_postprocessing(self):
    #     if self.curr_status == CurrStatus.IN_MED_MODEL and self.person_status[0] == 0:
    #         print("*** Inside seek_med_gp_day_postprocessing:!!!")
    #         ############################################
    #         ### Medical seeking model one day pass!! ###
    #         ############################################
    #         if self.person_status[1] == 1:
    #             # Patient is IPD
    #             if self.in_med_day > self.SMT_IPD_day:
    #                 if self.person_status[2] == 1:
    #                     # Patient is IPD death
    #                     self.death()
    #                 elif self.person_status[2] == 0:
    #                     # Patient is IPD recovery
    #                     self.recovery()
    #
    #         elif self.person_status[1] == 0:
    #             # Patient is OPD
    #             if self.in_med_day > self.SMT_OPD_day:
    #                 if self.person_status[2] == 1:
    #                     # Patient is OPD, medicine
    #                     if self.in_med_day > self.SMT_OPD_day+self.SMT_OPD_M_day:
    #                         if self.person_status[3] == 1:
    #                             # Patient is OPD, medicine, IPD
    #                             if self.in_med_day > self.SMT_OPD_day+self.SMT_OPD_M_day+self.SMT_OPD_M_IPD_day:
    #                                 if self.person_status[4] == 1:
    #                                     # Patient is OPD, medicine, IPD, death
    #                                     self.death()
    #                                 elif self.person_status[4] == 0:
    #                                     # Patient is OPD, medicine, IPD, recovery
    #                                     self.recovery()
    #                         elif self.person_status[3] == 0:
    #                             # Patient is OPD, medicine, recoveory
    #                             self.recovery()
    #                 elif self.person_status[2] == 0:
    #                     # Patient is OPD, no medicine
    #                     if self.in_med_day > self.SMT_OPD_day+self.SMT_OPD_NM_day:
    #                         if self.person_status[3] == 1:
    #                             # Patient is OPD, no medicine, IPD
    #                             if self.in_med_day > self.SMT_OPD_day+self.SMT_OPD_NM_day+self.SMT_OPD_NM_IPD_day:
    #                                 if self.person_status[4] == 1:
    #                                     # Patient is OPD, no medicine, IPD, death
    #                                     self.death()
    #                                 elif self.person_status[4] == 0:
    #                                     # Patient is OPD, no medicine, IPD, recovery
    #                                     self.recovery()
    #                         elif self.person_status[3] == 0:
    #                             # Patient is OPD, no medicine, recovery
    #                             self.recovery()
