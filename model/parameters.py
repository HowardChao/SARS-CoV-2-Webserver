from enum import Enum

IDX_CASE_NUM = 5000
SIMULATION_DAY = 180
SIMULATION_TIME = 1000
CYCLE_DAYS = 7

HEALTH_LIFE_EXP = 71.2
SEVERE_AVG_DEATH_AGE = 40

class AgeGroupPerc(Enum):
    YOUTH_GRP = 0.15
    ADULT_GRP = 0.70
    ELDER_GRP = 0.15

class RouteStatus(Enum):
    TRANSMISSION = 'transmission'
    HOSPITALISED = 'hospitalised'

class CurrStatus(Enum):
    IN_MODEL = 'in_model'
    RECOVERY = 'recovery'
    DEATH = 'death'
    CYCLE_REACHED = 'cycle_reached'

class ContactRate(Enum):
    SAME_GRP = 0.6
    DIFF_GRP = 0.2

class AgeGroup(Enum):
    YOUTH_GRP = 'youth'
    ADULT_GRP = 'adult'
    ELDER_GRP = 'elder'

class VaccineRate(Enum):
    YOUTH_RT = 0.646
    ADULT_RT = 0.093
    ELDER_RT = 0.445

class InfectionRate(Enum):
    YOUTH_NV_RT = 0.146
    ADULT_NV_RT = 0.037
    ELDER_NV_RT = 0.053
    YOUTH_V_RT = 0.088
    ADULT_V_RT = 0.022
    ELDER_V_RT = 0.032

class MedicineIntakeRate(Enum):
    YOUTH_RT = 0.5
    ADULT_RT = 0.5
    ELDER_RT = 0.5

class SevereRate(Enum):
    YOUTH_48_RT = 0.000075
    ADULT_48_RT = 0.000425
    ELDER_48_RT = 0.0016
    YOUTH_N48_RT = 0.000225
    ADULT_N48_RT = 0.001275
    ELDER_N48_RT = 0.0048

class FatalityRate(Enum):
    YOUTH_RT = 0.12
    ADULT_RT = 0.14
    ELDER_RT = 0.14

class effectiveness(Enum):
    MILD = (-0.88)*7/365
    SEVERE = (-0.88)*7/365 + (-0.98)*5.4/365
    DEATH = (-0.88)*7/365 + (-0.98)*5.4/365 + (-1)*(HEALTH_LIFE_EXP-SEVERE_AVG_DEATH_AGE)

class VaccineExpen(Enum):
    YOUTH_TRIVALENT_VAC = 500
    ADULT_TRIVALENT_VAC = 500
    ELDER_TRIVALENT_VAC = 500
    YOUTH_HIGH_DOSE_VAC = 0
    ADULT_HIGH_DOSE_VAC = 0
    ELDER_HIGH_DOSE_VAC = 1656
    YOUTH_ADJUVANTED_VAC = 0
    ADULT_ADJUVANTED_VAC = 0
    ELDER_ADJUVANTED_VAC = 1696

class HealthExpen(Enum):
    YOUTH_OUTPATIENT = 371
    ADULT_OUTPATIENT = 372
    ELDER_OUTPATIENT = 401
    YOUTH_ANTI_VIRUS = 950
    ADULT_ANTI_VIRUS = 950
    ELDER_ANTI_VIRUS = 950
    YOUTH_HOSPITALIZED = 45935
    ADULT_HOSPITALIZED = 45935
    ELDER_HOSPITALIZED = 45935
