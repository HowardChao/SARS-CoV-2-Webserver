from enum import Enum

IDX_CASE_NUM = 5000
SIMULATION_DAY = 3
SIMULATION_TIME = 1000
CYCLE_DAYS = 7

HEALTH_LIFE_EXP = 71.2
SEVERE_AVG_DEATH_AGE = 40

# IDX_SEEK_TREATMENT_PROB = 0.1
# IDX_INTAKE_MED_48_PROB = 0.5


class AgeGroupPerc(Enum):
    YOUTH_GRP = 0.15
    ADULT_GRP = 0.70
    ELDER_GRP = 0.15

class RouteStatus(Enum):
    TRANSMISSION = 'transmission'
    SEEKTREATMENT = 'seektreatment'

class CurrStatus(Enum):
    IN_MODEL = 'in_model'
    RECOVERY = 'recovery'
    DEATH = 'death'
    CYCLE_REACHED = 'cycle_reached'

class AliveDeath(Enum):
    ALIVE = 'alive'
    DEATH = 'death'

class AgeGroup(Enum):
    YOUTH_GRP = 'youth'
    ADULT_GRP = 'adult'
    ELDER_GRP = 'elder'

class ContactPersonSeekTreatment_Rate(Enum):
    YOUTH_CP_RT = 0.8
    ADULT_CP_RT = 0.8
    ELDER_CP_RT = 0.8
    YOUTH_ST_RT = 1 - YOUTH_CP_RT
    ADULT_ST_RT = 1 - ADULT_CP_RT
    ELDER_ST_RT = 1 - ELDER_CP_RT

class ContactGroup_Rate(Enum):
    SAME_GRP = 0.8
    DIFF_GRP = 1 - SAME_GRP

class Vaccine_Rate(Enum):
    YOUTH_V_RT = 0.646
    ADULT_V_RT = 0.093
    ELDER_V_RT = 0.445
    YOUTH_NV_RT = 1 - YOUTH_V_RT
    ADULT_NV_RT = 1 - ADULT_V_RT
    ELDER_NV_RT = 1 - ELDER_V_RT

class Vac_Infection_Rate(Enum):
    YOUTH_V_I_RT = 0.088
    ADULT_V_I_RT = 0.022
    ELDER_V_I_RT = 0.032
    YOUTH_V_NI_RT = 1 - YOUTH_V_I_RT
    ADULT_V_NI_RT = 1 - ADULT_V_I_RT
    ELDER_V_NI_RT = 1 - ELDER_V_I_RT

class NoVac_Infection_Rate(Enum):
    YOUTH_NV_I_RT = 0.146
    ADULT_NV_I_RT = 0.037
    ELDER_NV_I_RT = 0.053
    YOUTH_NV_NI_RT = 1 - YOUTH_NV_I_RT
    ADULT_NV_NI_RT = 1 - ADULT_NV_I_RT
    ELDER_NV_NI_RT = 1 - ELDER_NV_I_RT

# # Should be removed
# class InfectionRate(Enum):
#     YOUTH_NV_RT = 0.146
#     ADULT_NV_RT = 0.037
#     ELDER_NV_RT = 0.053
#     YOUTH_V_RT = 0.088
#     ADULT_V_RT = 0.022
#     ELDER_V_RT = 0.032


class SMT_HospitalizedOPD_Rate(Enum):
    YOUTH_HOS_RT = 0.1
    ADULT_HOS_RT = 0.1
    ELDER_HOS_RT = 0.1
    YOUTH_OPD_RT = 1 - YOUTH_HOS_RT
    ADULT_OPD_RT = 1 - YOUTH_HOS_RT
    ELDER_OPD_RT = 1 - ELDER_HOS_RT

class SMT_Hospitalized_Death_Rate(Enum):
    YOUTH_HOS_D_RT = 0.12
    ADULT_HOS_D_RT = 0.14
    ELDER_HOS_D_RT = 0.14
    YOUTH_HOS_R_RT = 1 - YOUTH_HOS_D_RT
    ADULT_HOS_R_RT = 1 - ADULT_HOS_D_RT
    ELDER_HOS_R_RT = 1 - ELDER_HOS_D_RT

# This should be renamed
class SMT_OPD_MedicineIntake_Rate(Enum):
    YOUTH_OPD_M_RT = 0.5
    ADULT_OPD_M_RT = 0.5
    ELDER_OPD_M_RT = 0.5
    YOUTH_OPD_NM_RT = 1 - YOUTH_OPD_M_RT
    ADULT_OPD_NM_RT = 1 - ADULT_OPD_M_RT
    ELDER_OPD_NM_RT = 1 - ELDER_OPD_M_RT

class SMT_OPD_M_Hospitalized_Rate(Enum):
    YOUTH_OPD_M_HOS_RT = 0.000075
    ADULT_OPD_M_HOS_RT = 0.000425
    ELDER_OPD_M_HOS_RT = 0.0016
    YOUTH_OPD_M_R_RT = 1 - YOUTH_OPD_M_HOS_RT
    ADULT_OPD_M_R_RT = 1 - ADULT_OPD_M_HOS_RT
    ELDER_OPD_M_R_RT = 1 - ELDER_OPD_M_HOS_RT

class SMT_OPD_M_Hospitalized_Death_Rate(Enum):
    YOUTH_OPD_M_HOS_D_RT = 0.12
    ADULT_OPD_M_HOS_D_RT = 0.14
    ELDER_OPD_M_HOS_D_RT = 0.14
    YOUTH_OPD_M_HOS_R_RT = 1 - YOUTH_OPD_M_HOS_D_RT
    ADULT_OPD_M_HOS_R_RT = 1 - ADULT_OPD_M_HOS_D_RT
    ELDER_OPD_M_HOS_R_RT = 1 - ELDER_OPD_M_HOS_D_RT

class SMT_OPD_NM_Hospitalized_Rate(Enum):
    YOUTH_OPD_NM_HOS_RT = 0.000225
    ADULT_OPD_NM_HOS_RT = 0.001275
    ELDER_OPD_NM_HOS_RT = 0.0048
    YOUTH_OPD_NM_R_RT = 1 - YOUTH_OPD_NM_HOS_RT
    ADULT_OPD_NM_R_RT = 1 - ADULT_OPD_NM_HOS_RT
    ELDER_OPD_NM_R_RT = 1 - ELDER_OPD_NM_HOS_RT

class SMT_OPD_NM_Hospitalized_Death_Rate(Enum):
    YOUTH_OPD_NM_HOS_D_RT = 0.12
    ADULT_OPD_NM_HOS_D_RT = 0.14
    ELDER_OPD_NM_HOS_D_RT = 0.14
    YOUTH_OPD_NM_HOS_R_RT = 1 - YOUTH_OPD_NM_HOS_D_RT
    ADULT_OPD_NM_HOS_R_RT = 1 - ADULT_OPD_NM_HOS_D_RT
    ELDER_OPD_NM_HOS_R_RT = 1 - ELDER_OPD_NM_HOS_D_RT










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
