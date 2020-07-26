import random
import copy
import numpy as np
from .parameters import IDX_CASE_NUM, SIMULATION_DAY, SIMULATION_TIME, CYCLE_DAYS, AgeGroupPerc, RouteStatus, CurrStatus

from .person import Person

class VaccineModel():
    def __init__(self):
        self.idx_case_num = IDX_CASE_NUM
        self.sim_day = SIMULATION_DAY
        self.sim_time = SIMULATION_TIME
        self.day = 0
        self.cycle_days = CYCLE_DAYS
        ## In model group
        self.transmission_gp = {}

        ## In model group
        self.treatment_gp = {}

        self.death_gp = {}
        self.recovery_gp = {}
        self.cycle_reached_gp = {}
        self.initial_model()

    # Day 1
    def initial_model(self):
        print("##################")
        print("## Day ", str(self.day), " ##")
        print("##################")
        youth_pop = int((AgeGroupPerc.YOUTH_GRP.value)*self.idx_case_num)
        adult_pop = int((AgeGroupPerc.ADULT_GRP.value)*self.idx_case_num)
        elder_pop = int((AgeGroupPerc.ELDER_GRP.value)*self.idx_case_num)
        for i in range(youth_pop):
            age = random.randrange(0, 18)
            p = Person(age, initial_idx_case=True)
            self.transmission_gp[p.id] = p
        for i in range(adult_pop):
            age = random.randrange(19, 64)
            p = Person(age, initial_idx_case=True)
            self.transmission_gp[p.id] = p
        for i in range(elder_pop):
            age = random.randrange(65, 100)
            p = Person(age, initial_idx_case=True)
            self.transmission_gp[p.id] = p
        self.day += 1



    def one_day_passed(self):
        print("##################")
        print("## Day ", str(self.day), " ##")
        print("##################")
        print('transmission_gp size: ', len(self.transmission_gp))
        print('treatment_gp size: ', len(self.treatment_gp))
        transmission_gp_route = copy.deepcopy(self.transmission_gp)

        ## Step 1: choose route option
        for id, indv in transmission_gp_route.items():
            indv.route_status_rand()
            if indv.route_status is RouteStatus.TRANSMISSION:
                pass
            elif indv.route_status is RouteStatus.HOSPITALISED:
                del self.transmission_gp[id]
                self.treatment_gp[id] = indv
        print('     transmission_gp size: ', len(self.transmission_gp))
        print('     treatment_gp size: ', len(self.treatment_gp))

        ## Step 2: Transmission path
        transmission_gp_contact = copy.deepcopy(self.transmission_gp)
        for id, indv in transmission_gp_contact.items():
            for contact_idx in range(6):
                rand_age = np.random.choice(
                            [ random.randint(0, 18), random.randint(19, 64), random.randint(65, 100)],
                            1,
                            p=[indv.youth_contact_rate.value, indv.adult_contact_rate.value, indv.elder_contact_rate.value]
                           )[0]
                p = Person(rand_age)

                # InfectionRate
                if p.infection_status is True:
                    self.transmission_gp[p.id] = p
        print('     transmission_gp size: ', len(self.transmission_gp))
        print('     treatment_gp size: ', len(self.treatment_gp))

        ## Step 3: Seek help path
        treatment_gp_seek = copy.deepcopy(self.treatment_gp)
        for id, indv in treatment_gp_seek.items():
            if indv.curr_status == CurrStatus.DEATH:
                del self.treatment_gp[id]
                self.death_gp[id] = indv
            elif indv.curr_status == CurrStatus.RECOVERY:
                del self.treatment_gp[id]
                self.recovery_gp[id] = indv

        ## Step 4: Remove people that stay in model more than cycle limit
        transmission_gp_reach = copy.deepcopy(self.transmission_gp)
        for id, indv in transmission_gp_reach.items():
            if indv.curr_status == CurrStatus.CYCLE_REACHED:
                del self.transmission_gp[id]
                self.cycle_reached_gp[id] = indv
        print('transmission_gp size: ', len(self.transmission_gp))
        print('treatment_gp size: ', len(self.treatment_gp))
        print('death_gp size: ', len(self.death_gp))
        print('recovery_gp size: ', len(self.recovery_gp))
        print('cycle_reached_gp size: ', len(self.cycle_reached_gp))
        self.day += 1
