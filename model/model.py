import random
from .parameters import IDX_CASE_NUM, SIMULATION_DAY, SIMULATION_TIME, CYCLE_DAYS, AgeGroupPerc

from .person import Person

class VaccineModel():
    def __init__(self):
        self.idx_case_num = IDX_CASE_NUM
        self.sim_day = SIMULATION_DAY
        self.sim_time = SIMULATION_TIME
        self.cycle_days = CYCLE_DAYS
        ## In model group
        self.transmission_gp = {}

        ## In model group
        self.treatment_gp = {}

        self.death_gp = {}
        self.recovery_gp = {}
        self.initial_model()


    def initial_model(self):
        youth_pop = int((AgeGroupPerc.YOUTH_GRP.value)*self.idx_case_num)
        adult_pop = int((AgeGroupPerc.ADULT_GRP.value)*self.idx_case_num)
        elder_pop = int((AgeGroupPerc.ELDER_GRP.value)*self.idx_case_num)
        for i in range(youth_pop):
            age = random.randrange(0, 18)
            p = Person(age)
            self.transmission_gp[p.id] = p
        for i in range(adult_pop):
            age = random.randrange(19, 64)
            p = Person(age)
            self.transmission_gp[p.id] = p
        for i in range(elder_pop):
            age = random.randrange(65, 100)
            p = Person(age)
            self.transmission_gp[p.id] = p

    def one_day_passed(self):
