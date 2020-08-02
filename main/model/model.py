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
        self.transmission_gp = []
        ## In model group
        # self.treatment_gp = []
        self.death_gp = []
        self.recovery_gp = []
        self.cycle_reached_gp = []

        # self.youth_vaccine = []
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
            p.day_passed()
            self.transmission_gp.append(p)
        for i in range(adult_pop):
            age = random.randrange(19, 64)
            p = Person(age, initial_idx_case=True)
            p.day_passed()
            self.transmission_gp.append(p)
        for i in range(elder_pop):
            age = random.randrange(65, 100)
            p = Person(age, initial_idx_case=True)
            p.day_passed()
            self.transmission_gp.append(p)
        self.day += 1



    def one_day_passed(self):
        print("##################")
        print("## Day ", str(self.day), " ##")
        print("##################")
        print('@@ Starting transmission_gp size: ', len(self.transmission_gp))
        # print('treatment_gp size: ', len(self.treatment_gp))

        ## Step 1: choose route option
        Ori_transmission_gp = []
        new_transmission_gp = []
        new_death_gp = []
        new_recovery_gp = []
        new_cycle_reached_gp = []
        for _p in self.transmission_gp:
            _p.choose_route()
            if _p.route_status is RouteStatus.TRANSMISSION:
                for contact_idx in range(6):
                    rand_age = np.random.choice(
                                [ random.randint(0, 18), random.randint(19, 64), random.randint(65, 100)],
                                1,
                                p=[_p.youth_contact_rate.value,
                                _p.adult_contact_rate.value, _p.elder_contact_rate.value]
                               )[0]
                    p = Person(rand_age)
                    # InfectionRate
                    if p.infection_status is True and _p.curr_status == CurrStatus.IN_MODEL:
                        p.day_passed()
                        new_transmission_gp.append(p)
                        # self.transmission_gp.append(p)

                _p.day_passed()
                if _p.curr_status == CurrStatus.IN_MODEL:
                    Ori_transmission_gp.append(_p)

                elif _p.curr_status == CurrStatus.CYCLE_REACHED:
                    new_cycle_reached_gp.append(_p)
                    # self.transmission_gp.remove(_p)

            elif _p.route_status is RouteStatus.SEEKTREATMENT:
                _p.day_passed()
                if _p.curr_status == CurrStatus.DEATH:
                    new_death_gp.append(_p)
                elif _p.curr_status == CurrStatus.RECOVERY:
                    new_recovery_gp.append(_p)
                # self.transmission_gp.remove(_p)
        self.transmission_gp = Ori_transmission_gp + new_transmission_gp
        self.death_gp = self.death_gp + new_death_gp
        self.recovery_gp = self.recovery_gp + new_recovery_gp
        self.cycle_reached_gp = self.cycle_reached_gp + new_cycle_reached_gp

        print('     Ori_transmission_gp size      : ', len(Ori_transmission_gp))
        print('     new_transmission_gp size      : ', len(new_transmission_gp))

        print('         self.transmission_gp size : ', len(self.transmission_gp))

        print('     new_death_gp                  : ', len(new_death_gp))
        print('         self.death_gp size        : ', len(self.death_gp))
        print('     new_recovery_gp               : ', len(new_recovery_gp))
        print('         self.recovery_gp size     : ', len(self.recovery_gp))
        print('     new_cycle_reached_gp          : ', len(new_cycle_reached_gp))
        print('         self.cycle_reached_gp size: ', len(self.cycle_reached_gp))
        self.day += 1

        # for _p in self.transmission_gp:
        #     if _p
