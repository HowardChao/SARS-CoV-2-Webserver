import random
from .parameters import RouteStatus, AgeGroup, ContactRate, VaccineRate, InfectionRate


class Person():
    def __init__(self, age):
        self.age = age
        self.age_group = self.set_age_group(age)
        self.route_status = RouteStatus.TRANSMISSION
        # self.vaccome_status
        self.vaccine_status = bool(random.getrandbits(1))

        self.youth_contact_rate = self.set_contact_rate(age, 'youth')
        self.adult_contact_rate = self.set_contact_rate(age, 'adult')
        self.elder_contact_rate = self.set_contact_rate(age, 'elder')
        self.vaccine_rate = self.set_vaccine_rate(age)
        # Initial get_vaccine is unknown


        self.infection_rate = self.set_infection_rate(age, self.get_vaccine)


    def route_status_rand(self):
        if self.route_status is RouteStatus.TRANSMISSION:
            rand_dice = bool(random.getrandbits(1))
            if rand_dice is True:
                pass
            elif rand_dice is False:
                self.route_status = RouteStatus.HOSPITALISED
        elif self.route_status is RouteStatus.HOSPITALISED:
            pass

    def set_age_group(self, age):
        if age <= 18:
            return AgeGroup.YOUTH_GRP
        elif age > 18 and age <65:
            return AgeGroup.ADULT_GRP
        elif age >= 65:
            return AgeGroup.ELDER_GRP

    def set_contact_rate(self, age, category):
        if age <= 18:
            if category is 'youth':
                return ContactRate.SAME_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif age > 18 and age <65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.SAME_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif age >= 65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.SAME_GRP

    def set_vaccine_rate(self, age):
        if age <= 18:
            return VaccineRate.YOUTH_RT
        elif age > 18 and age <65:
            return VaccineRate.ADULT_RT
        elif age >= 65:
            return VaccineRate.ELDER_RT

    def vaccine_status_rand(self):
        if self.vaccine_status is True:
            pass
        elif self.vaccine_status is False:
            self.vaccine_status = bool(random.getrandbits(1))

    def set_infection_rate(self, age, get_vaccine):
        if get_vaccine is True:
            if age <= 18:
                return InfectionRate.YOUTH_V_RT
            elif age > 18 and age <65:
                return InfectionRate.ADULT_V_RT
            elif age >= 65:
                return InfectionRate.ELDER_V_RT
        elif get_vaccine is False:
            if age <= 18:
                return InfectionRate.YOUTH_NV_RT
            elif age > 18 and age <65:
                return InfectionRate.ADULT_NV_RT
            elif age >= 65:
                return InfectionRate.ELDER_NV_RT



def HealthPerson(Person):
    def __init__(self, age, vaccine_rate, affected_rate):
        Person(age, vaccine_rate, infection_rate)

def IdxCasePerson(Person):
    def __init__(self, age, vaccine_rate, affected_rate, hosp_status, sever_rate, mortality_rate, symptom):
        Person(age, vaccine_rate, infection_rate)
        self.hosp_status = hosp_status
        self.sever_rate = sever_rate
        self.mortality_rate = mortality_rate
        self.symptom = symptom
