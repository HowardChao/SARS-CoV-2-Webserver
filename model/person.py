import uuid
import random
from .parameters import CurrStatus, RouteStatus, AgeGroup, ContactRate, VaccineRate, InfectionRate, MedicineIntakeRate, SevereRate, FatalityRate, effectiveness


class Person():
    def __init__(self, age):

        # RECOVERY = 'recovery'
        # DEATH = 'death'
        # CYCLE_REACHED
        self.id = str(uuid.uuid1())
        self.curr_status = CurrStatus.IN_MODEL
        self.age = age
        self.age_group = self.set_age_group()
        self.route_status = RouteStatus.TRANSMISSION
        self.vaccine_status = bool(random.getrandbits(1))
        self.medicine_48 = bool(random.getrandbits(1))
        self.youth_contact_rate = self.set_contact_rate('youth')
        self.adult_contact_rate = self.set_contact_rate('adult')
        self.elder_contact_rate = self.set_contact_rate('elder')
        self.vaccine_rate = self.set_vaccine_rate()
        self.infection_rate = self.set_infection_rate()
        self.medicine_intake_rate = self.set_medicine_intake_rate()
        self.severe_rate = self.set_severe_rate()
        self.fatality_rate = self.set_fatality_rate()
        self.effectiveness_mild = effectiveness.MILD
        self.effectiveness_severe = effectiveness.SEVERE
        self.effectiveness_death = effectiveness.DEATH

    ## The status of this function is dynamic
    def route_status_rand(self):
        if self.route_status is RouteStatus.TRANSMISSION:
            rand_dice = bool(random.getrandbits(1))
            if rand_dice is True:
                pass
            elif rand_dice is False:
                self.route_status = RouteStatus.HOSPITALISED
        elif self.route_status is RouteStatus.HOSPITALISED:
            pass

    ## The status of this function is dynamic
    def vaccine_status_rand(self):
        if self.vaccine_status is True:
            pass
        elif self.vaccine_status is False:
            self.vaccine_status = bool(random.getrandbits(1))
            if self.vaccine_status is True:
                self.infection_rate = self.set_infection_rate()

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
                return ContactRate.SAME_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif self.age > 18 and self.age <65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.SAME_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif self.age >= 65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.SAME_GRP

    ## static
    def set_vaccine_rate(self):
        if self.age <= 18:
            return VaccineRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return VaccineRate.ADULT_RT
        elif self.age >= 65:
            return VaccineRate.ELDER_RT

    ## dynamic
    def set_infection_rate(self):
        if self.vaccine_status is True:
            if self.age <= 18:
                return InfectionRate.YOUTH_V_RT
            elif self.age > 18 and self.age <65:
                return InfectionRate.ADULT_V_RT
            elif self.age >= 65:
                return InfectionRate.ELDER_V_RT
        elif self.vaccine_status is False:
            if self.age <= 18:
                return InfectionRate.YOUTH_NV_RT
            elif self.age > 18 and self.age <65:
                return InfectionRate.ADULT_NV_RT
            elif self.age >= 65:
                return InfectionRate.ELDER_NV_RT

    ## static
    def set_medicine_intake_rate(self):
        if self.age <= 18:
            return MedicineIntakeRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return MedicineIntakeRate.ADULT_RT
        elif self.age >= 65:
            return MedicineIntakeRate.ELDER_RT

    def set_severe_rate(self):
        if self.medicine_48 is True:
            if self.age <= 18:
                return SevereRate.YOUTH_48_RT
            elif self.age > 18 and self.age <65:
                return SevereRate.ADULT_48_RT
            elif self.age >= 65:
                return SevereRate.ELDER_48_RT
        elif self.medicine_48 is False:
            if self.age <= 18:
                return SevereRate.YOUTH_N48_RT
            elif self.age > 18 and self.age <65:
                return SevereRate.ADULT_N48_RT
            elif self.age >= 65:
                return SevereRate.ELDER_N48_RT

    def set_fatality_rate(self):
        if self.age <= 18:
            return FatalityRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return FatalityRate.ADULT_RT
        elif self.age >= 65:
            return FatalityRate.ELDER_RT

    def death(self):
        self.curr_status = CurrStatus.DEATH

    def recovery(self):
        self.curr_status = CurrStatus.RECOVERY


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
