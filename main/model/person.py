import uuid
import random
from .parameters import CurrStatus, RouteStatus, AgeGroup, ContactPersonSeekTreatment_Rate, ContactGroup_Rate, Vaccine_Rate, Vac_Infection_Rate, NoVac_Infection_Rate, SMT_HospitalizedOPD_Rate, SMT_Hospitalized_Death_Rate, SMT_OPD_MedicineIntake_Rate, SMT_OPD_M_Hospitalized_Rate, SMT_OPD_M_Hospitalized_Death_Rate, SMT_OPD_NM_Hospitalized_Rate, SMT_OPD_NM_Hospitalized_Death_Rate, effectiveness

class Person():
    def __init__(self, age, initial_idx_case=False):
        self.id = str(uuid.uuid1())
        self.initial_idx_case = initial_idx_case
        self.person_status = [-1, -1, -1, -1, -1]
        self.curr_status = CurrStatus.IN_MODEL
        self.day = 0
        self.age = age
        self.age_group = self.set_age_group()
        self.contactperson_rate, self.seektreatment_rate = self.set_contactperson_seektreatment_rate()

        self.youth_contact_rate = self.set_contact_rate('youth')
        self.adult_contact_rate = self.set_contact_rate('adult')
        self.elder_contact_rate = self.set_contact_rate('elder')
        self.vaccine_rate, self.n_vaccine_rate = self.set_vaccine_rate()
        self.vac_infection_rate, self.vac_n_infection_rate = self.set_vac_infection_rate()
        self.n_vac_infection_rate, self.n_vac_n_infection_rate = self.set_n_vac_infection_rate()

        # Initialization
        self.vaccine_status = self.set_vaccine_status()
        self.set_initial_idx_case()

        self.smt_hospitalized_rate, self.smt_opd_rate = self.set_smt_hospitalized_opd_rate()
        self.smt_hospitalized_death_rate, self.smt_hospitalized_recovery_rate = self.set_smt_hospitalized_death_rate()
        self.smt_opd_medicine_rate, self.smt_opd_n_medicine_rate = self.set_smt_opd_medicineintake_rate()
        self.smt_opd_m_hospitalized_rate, self.smt_opd_m_recovery_rate = self.set_smt_opd_m_hospitalized_rate()
        self.smt_opd_m_hospitalized_death_rate, self.smt_opd_m_hospitalized_recovery_rate = self.set_smt_opd_m_hospitalized_death_rate()
        self.smt_opd_nm_hospitalized_rate, self.smt_opd_nm_recovery_rate = self.set_smt_opd_nm_hospitalized_rate()
        self.smt_opd_nm_hospitalized_death_rate, self.smt_opd_nm_recovery_death_rate = self.set_smt_opd_nm_hospitalized_death_rate()
        # self.infection_rate = self.set_infection_rate()
        # self.infection_status = self.set_infection_status(initial_idx_case)
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

    ##################
    # Initialization #
    ##################
    def set_vaccine_status(self):
        if self.curr_status.value == 'in_model':
            rand_dice = random.random() < self.vaccine_rate.value
            if rand_dice:
                self.vaccine_status = True
            else:
                self.vaccine_status = False

    def set_initial_idx_case(self):
        if self.curr_status.value == 'in_model':
            if self.initial_idx_case == True:
                self.infection_status = True
                self.person_status[0] = 1
            else:
                self.infection_status = False

    ##################
    # When the new infected person contact another person
    ##################
    def set_infection_status(self):
        # Only set infection status when it's false
        if self.curr_status.value == 'in_model' and self.infection_status == False:
            if self.initial_idx_case == True:
                self.infection_status = True
            else:
                if self.vaccine_status == True:
                    rand_dice = random.random() < self.vac_infection_rate.value
                    if rand_dice:
                        self.infection_status = True
                    else:
                        self.infection_status = False
                else:
                    rand_dice = random.random() < self.n_vac_infection_rate.value
                    if rand_dice:
                        self.infection_status = True
                    else:
                        self.infection_status = False

    ##################
    # All the infected people need to choose their route everytime
    ##################
    def set_route_status(self):
        # Only need to check when the person hasn't contact another person
        if self.curr_status.value == 'in_model' and self.infection_status == True:
            rand_dice = random.random() < self.contactperson_rate.value
            if rand_dice:
                self.person_status[0] = 1
            else:
                self.person_status[0] = 0

    ##################
    # After the infected people choose their route. Run their own path
    ##################
    def contact_people(self):
        if self.curr_status.value == 'in_model' and self.person_status[0] == 1:
            infected_people_ls = []
            non_infected_people_ls = []
            for _ in range(6):
                rand_age = np.random.choice(
                            [ random.randint(0, 18), random.randint(19, 64), random.randint(65, 100)],
                            1,
                            p=[self.youth_contact_rate.value,self.adult_contact_rate.value, self.elder_contact_rate.value]
                           )[0]
                p = Person(rand_age)
                # InfectionRate
                p.set_infection_status()
                if p.infection_status == True:
                    infected_people_ls.append(p)
                else:
                    non_infected_people_ls.append(p)
            return infected_people_ls, non_infected_people_ls
        else:
            return [], []

    def seek_medical_treatment(self):
        if self.curr_status.value == 'in_model' and self.person_status[0] == 0:
            death_ls = []
            recovery_ls = []
            reached_ls = []
            self.set_smt_hospitalized_opd_status()
            if self.person_status[1] == 1:
                self.set_smt_hospitalized_death_status()
                if self.person_status[2] == 1:
                    self.death()
                elif self.person_status[2] == 0:
                    self.recovery()
            elif self.person_status[1] == 0:
                self.set_smt_opd_medicineintake_status()
                if self.person_status[2] == 1:
                    self.set_smt_opd_m_hospitalized_status()
                    if self.person_status[3] == 1:
                        self.set_smt_opd_m_hospitalized_death_status()
                        if self.person_status[4] == 1:
                            self.death()
                        elif self.person_status[4] == 0:
                            self.recovery()
                    elif self.person_status[3] == 0:
                        self.recovery()
                elif self.person_status[2] == 0:
                    self.set_smt_opd_nm_hospitalized_status()
                    if self.person_status[3] == 1:
                        self.set_smt_opd_nm_hospitalized_death_status()
                        if self.person_status[4] == 1:
                            self.death()
                        elif self.person_status[4] == 0:
                            self.recovery()
                    elif self.person_status[3] == 0:
                        self.recovery()


    def death(self):
        self.curr_status = CurrStatus.DEATH

    def recovery(self):
        self.curr_status = CurrStatus.RECOVERY

    ## static
    def set_contactperson_seektreatment_rate(self):
        if self.age <= 18:
            return ContactPersonSeekTreatment_Rate.YOUTH_CP_RT, ContactPersonSeekTreatment_Rate.YOUTH_ST_RT
        elif self.age > 18 and self.age <65:
            return ContactPersonSeekTreatment_Rate.ADULT_CP_RT, ContactPersonSeekTreatment_Rate.ADULT_ST_RT
        elif self.age >= 65:
            return ContactPersonSeekTreatment_Rate.ELDER_CP_RT, ContactPersonSeekTreatment_Rate.ELDER_ST_RT

    ## static
    def set_age_group(self):
        if self.age <= 18:
            return AgeGroup.YOUTH_GRP
        elif self.age > 18 and self.age <65:
            return AgeGroup.ADULT_GRP
        elif self.age >= 65:
            return AgeGroup.ELDER_GRP

    ## static
    def set_contact_rate(self, category):
        if self.age <= 18:
            if category is 'youth':
                return ContactGroup_Rate.SAME_GRP
            elif category is 'adult':
                return ContactGroup_Rate.DIFF_GRP
            elif category is 'elder':
                return ContactGroup_Rate.DIFF_GRP
        elif self.age > 18 and self.age <65:
            if category is 'youth':
                return ContactGroup_Rate.DIFF_GRP
            elif category is 'adult':
                return ContactGroup_Rate.SAME_GRP
            elif category is 'elder':
                return ContactGroup_Rate.DIFF_GRP
        elif self.age >= 65:
            if category is 'youth':
                return ContactGroup_Rate.DIFF_GRP
            elif category is 'adult':
                return ContactGroup_Rate.DIFF_GRP
            elif category is 'elder':
                return ContactGroup_Rate.SAME_GRP

    def set_vaccine_rate(self):
        if self.age <= 18:
            return Vaccine_Rate.YOUTH_V_RT, Vaccine_Rate.YOUTH_NV_RT
        elif self.age > 18 and self.age <65:
            return Vaccine_Rate.ADULT_V_RT, Vaccine_Rate.ADULT_NV_RT
        elif self.age >= 65:
            return Vaccine_Rate.ELDER_V_RT, Vaccine_Rate.ELDER_NV_RT

    def set_vac_infection_rate(self):
        if self.age <= 18:
            return Vac_Infection_Rate.YOUTH_V_I_RT, Vac_Infection_Rate.YOUTH_V_NI_RT
        elif self.age > 18 and self.age <65:
            return Vac_Infection_Rate.ADULT_V_I_RT, Vac_Infection_Rate.ADULT_V_NI_RT
        elif self.age >= 65:
            return Vac_Infection_Rate.ELDER_V_I_RT, Vac_Infection_Rate.ELDER_V_NI_RT

    def set_n_vac_infection_rate(self):
        if self.age <= 18:
            return NoVac_Infection_Rate.YOUTH_NV_I_RT, NoVac_Infection_Rate.YOUTH_NV_NI_RT
        elif self.age > 18 and self.age <65:
            return NoVac_Infection_Rate.ADULT_NV_I_RT, NoVac_Infection_Rate.ADULT_NV_NI_RT
        elif self.age >= 65:
            return NoVac_Infection_Rate.ELDER_NV_I_RT, NoVac_Infection_Rate.ELDER_NV_NI_RT

    def set_smt_hospitalized_opd_rate(self):
        if self.age <= 18:
            return SMT_HospitalizedOPD_Rate.YOUTH_HOS_RT, SMT_HospitalizedOPD_Rate.YOUTH_OPD_RT
        elif self.age > 18 and self.age <65:
            return SMT_HospitalizedOPD_Rate.ADULT_HOS_RT, SMT_HospitalizedOPD_Rate.ADULT_OPD_RT
        elif self.age >= 65:
            return SMT_HospitalizedOPD_Rate.ELDER_HOS_RT, SMT_HospitalizedOPD_Rate.ELDER_OPD_RT

    def set_smt_hospitalized_death_rate(self):
        if self.age <= 18:
            return SMT_Hospitalized_Death_Rate.YOUTH_HOS_D_RT, SMT_Hospitalized_Death_Rate.YOUTH_HOS_R_RT
        elif self.age > 18 and self.age <65:
            return SMT_Hospitalized_Death_Rate.ADULT_HOS_D_RT, SMT_Hospitalized_Death_Rate.ADULT_HOS_R_RT
        elif self.age >= 65:
            return SMT_Hospitalized_Death_Rate.ELDER_HOS_D_RT, SMT_Hospitalized_Death_Rate.ELDER_HOS_R_RT


    def set_smt_opd_medicineintake_rate(self):
        if self.age <= 18:
            return SMT_OPD_MedicineIntake_Rate.YOUTH_OPD_M_RT, SMT_OPD_MedicineIntake_Rate.YOUTH_OPD_NM_RT
        elif self.age > 18 and self.age <65:
            return SMT_OPD_MedicineIntake_Rate.ADULT_OPD_M_RT, SMT_OPD_MedicineIntake_Rate.ADULT_OPD_NM_RT
        elif self.age >= 65:
            return SMT_OPD_MedicineIntake_Rate.ELDER_OPD_M_RT, SMT_OPD_MedicineIntake_Rate.ELDER_OPD_NM_RT

    def set_smt_opd_m_hospitalized_rate(self):
        if self.age <= 18:
            return SMT_OPD_M_Hospitalized_Rate.YOUTH_OPD_M_HOS_RT, SMT_OPD_M_Hospitalized_Rate.YOUTH_OPD_M_R_RT
        elif self.age > 18 and self.age <65:
            return SMT_OPD_M_Hospitalized_Rate.ADULT_OPD_M_HOS_RT, SMT_OPD_M_Hospitalized_Rate.ADULT_OPD_M_R_RT
        elif self.age >= 65:
            return SMT_OPD_M_Hospitalized_Rate.ELDER_OPD_M_HOS_RT, SMT_OPD_M_Hospitalized_Rate.ELDER_OPD_M_R_RT

    def set_smt_opd_m_hospitalized_death_rate(self):
        if self.age <= 18:
            return SMT_OPD_M_Hospitalized_Death_Rate.YOUTH_OPD_M_HOS_D_RT, SMT_OPD_M_Hospitalized_Death_Rate.YOUTH_OPD_M_HOS_R_RT
        elif self.age > 18 and self.age <65:
            return SMT_OPD_M_Hospitalized_Death_Rate.ADULT_OPD_M_HOS_D_RT, SMT_OPD_M_Hospitalized_Death_Rate.ADULT_OPD_M_HOS_R_RT
        elif self.age >= 65:
            return SMT_OPD_M_Hospitalized_Death_Rate.ELDER_OPD_M_HOS_D_RT, SMT_OPD_M_Hospitalized_Death_Rate.ELDER_OPD_M_HOS_R_RT

    def set_smt_opd_nm_hospitalized_rate(self):
        if self.age <= 18:
            return SMT_OPD_NM_Hospitalized_Rate.YOUTH_OPD_NM_HOS_RT, SMT_OPD_NM_Hospitalized_Rate.YOUTH_OPD_NM_R_RT
        elif self.age > 18 and self.age <65:
            return SMT_OPD_NM_Hospitalized_Rate.ADULT_OPD_NM_HOS_RT, SMT_OPD_NM_Hospitalized_Rate.ADULT_OPD_NM_R_RT
        elif self.age >= 65:
            return SMT_OPD_NM_Hospitalized_Rate.ELDER_OPD_NM_HOS_RT, SMT_OPD_NM_Hospitalized_Rate.ELDER_OPD_NM_R_RT

    def set_smt_opd_nm_hospitalized_death_rate(self):
        if self.age <= 18:
            return SMT_OPD_NM_Hospitalized_Death_Rate.YOUTH_OPD_NM_HOS_D_RT, SMT_OPD_NM_Hospitalized_Death_Rate.YOUTH_OPD_NM_HOS_R_RT
        elif self.age > 18 and self.age <65:
            return SMT_OPD_NM_Hospitalized_Death_Rate.ADULT_OPD_NM_HOS_D_RT, SMT_OPD_NM_Hospitalized_Death_Rate.ADULT_OPD_NM_HOS_R_RT
        elif self.age >= 65:
            return SMT_OPD_NM_Hospitalized_Death_Rate.ELDER_OPD_NM_HOS_D_RT, SMT_OPD_NM_Hospitalized_Death_Rate.ELDER_OPD_NM_HOS_R_RT

    ##########################
    ## Outside Calling func ##
    ##########################
    def day_preprocessing(self):
        self.set_route_status()

    def day_postprocessing(self):
        if self.curr_status.value == 'in_model':
            self.set_infection_status()
            self.day += 1
            if self.day > 7:
                self.curr_status = CurrStatus.CYCLE_REACHED


    def day_passed(self):
        if self.curr_status.value == 'in_model':
            self.day += 1
            # 1. Check whether the person get infected
            self.set_infection_status()
            # 2. Check whether the person go into transmission cycle
            self.set_route_status()

        # if self.day > 7:
        #     self.cycle_reached()
        # if self.curr_status is not CurrStatus.DEATH:
        #     self.recovery()






    # ## The status of this function is dynamic
    # def set_vaccine_status(self):
    #     if self.route_status is RouteStatus.TRANSMISSION:
    #         rand_dice = random.random() < self.vaccine_rate.value
    #         if rand_dice:
    #             return True
    #         else:
    #             return False
    #
    # ## dynamic
    # def set_infection_rate(self):
    #     if self.vaccine_status is True:
    #         if self.age <= 18:
    #             return InfectionRate.YOUTH_V_RT
    #         elif self.age > 18 and self.age <65:
    #             return InfectionRate.ADULT_V_RT
    #         elif self.age >= 65:
    #             return InfectionRate.ELDER_V_RT
    #     elif self.vaccine_status is False:
    #         if self.age <= 18:
    #             return InfectionRate.YOUTH_NV_RT
    #         elif self.age > 18 and self.age <65:
    #             return InfectionRate.ADULT_NV_RT
    #         elif self.age >= 65:
    #             return InfectionRate.ELDER_NV_RT
    #
    # def set_infection_status(self, initial_idx_case):
    #     if initial_idx_case is True:
    #         return True
    #     rand_dice = random.random() < self.infection_rate.value
    #     if rand_dice:
    #         return True
    #     else:
    #         return False
    #
    # ## static
    # def set_medicine_intake_rate(self):
    #     if self.age <= 18:
    #         return MedicineIntakeRate.YOUTH_RT
    #     elif self.age > 18 and self.age <65:
    #         return MedicineIntakeRate.ADULT_RT
    #     elif self.age >= 65:
    #         return MedicineIntakeRate.ELDER_RT
    #
    # def set_medicine_intake_status(self):
    #     if self.seek_treatment_status is True:
    #         rand_dice = random.random() < self.medicine_intake_rate.value
    #         if rand_dice:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    #
    # def set_severe_rate(self):
    #     if self.medicine_intake_status is True:
    #         if self.age <= 18:
    #             return SevereRate.YOUTH_48_RT
    #         elif self.age > 18 and self.age <65:
    #             return SevereRate.ADULT_48_RT
    #         elif self.age >= 65:
    #             return SevereRate.ELDER_48_RT
    #     elif self.medicine_intake_status is False:
    #         if self.age <= 18:
    #             return SevereRate.YOUTH_N48_RT
    #         elif self.age > 18 and self.age <65:
    #             return SevereRate.ADULT_N48_RT
    #         elif self.age >= 65:
    #             return SevereRate.ELDER_N48_RT
    #
    # def set_severe_status(self):
    #     if self.seek_treatment_status is True:
    #         rand_dice = random.random() < self.severe_rate.value
    #         if rand_dice:
    #             return True
    #         else:
    #             self.recovery()
    #             return False
    #     else:
    #         return False
    #
    # def set_fatality_rate(self):
    #     if self.age <= 18:
    #         return FatalityRate.YOUTH_RT
    #     elif self.age > 18 and self.age <65:
    #         return FatalityRate.ADULT_RT
    #     elif self.age >= 65:
    #         return FatalityRate.ELDER_RT
    #
    # def in_model(self):
    #     self.curr_status = CurrStatus.IN_MODEL
    #
    # def recovery(self):
    #     self.curr_status = CurrStatus.RECOVERY
    #
    # def death(self):
    #     self.curr_status = CurrStatus.DEATH
    #
    # def cycle_reached(self):
    #     self.curr_status = CurrStatus.CYCLE_REACHED
    #
    # def set_current_status(self):
    #     if self.route_status is RouteStatus.TRANSMISSION:
    #         if self.day > 7:
    #             self.cycle_reached()
    #         else:
    #             self.in_model()
    #     elif self.route_status is RouteStatus.SEEKTREATMENT:
    #         if self.severe_status:
    #             rand_dice = random.random() < self.fatality_rate.value
    #             if rand_dice:
    #                 self.death()
    #             else:
    #                 self.recovery()
    #         else:
    #             self.recovery()
    #
    # ##########################
    # ## Outside Calling func ##
    # ##########################
    # def day_passed(self):
    #     self.day += 1
    #     self.set_current_status()
    #     # if self.day > 7:
    #     #     self.cycle_reached()
    #     # if self.curr_status is not CurrStatus.DEATH:
    #     #     self.recovery()


# def HealthPerson(Person):
#     def __init__(self, age, vaccine_rate, affected_rate):
#         Person(age, vaccine_rate, infection_rate)
#
# def IdxCasePerson(Person):
#     def __init__(self, age, vaccine_rate, affected_rate, hosp_status, sever_rate, mortality_rate, symptom):
#         Person(age, vaccine_rate, infection_rate)
#         self.hosp_status = hosp_status
#         self.sever_rate = sever_rate
#         self.mortality_rate = mortality_rate
#         self.symptom = symptom
