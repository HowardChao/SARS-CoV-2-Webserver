from django import forms

# class ParametersForm(forms.Form):
            # <input class="form-control" type="number" value="5000" id="BMP_IDX_CASE_NUM">



class RunModelForm(forms.Form):
    # try_ = forms.IntegerField()

    BMP_IDX_CASE_NUM = forms.IntegerField()
    BMP_SIMULATION_DAY = forms.IntegerField()
    BMP_SIMULATION_TIME = forms.IntegerField()
    BMP_CYCLE_DAYS = forms.IntegerField()

    AGP_YOUTH_GRP = forms.FloatField()
    AGP_ADULT_GRP = forms.FloatField()
    AGP_ELDER_GRP = forms.FloatField()

    CP_SMT_YOUTH_Rate_CP = forms.FloatField()
    CP_SMT_ADULT_Rate_CP = forms.FloatField()
    CP_SMT_ELDER_Rate_CP = forms.FloatField()
    CP_SMT_YOUTH_Rate_ST = forms.FloatField()
    CP_SMT_ADULT_Rate_ST = forms.FloatField()
    CP_SMT_ELDER_Rate_ST = forms.FloatField()

    CR_SAME_GRP = forms.FloatField()
    CR_DIFF_GRP = forms.FloatField()

    Vac_YOUTH_Rate_V = forms.FloatField()
    Vac_ADULT_Rate_V = forms.FloatField()
    Vac_ELDER_Rate_V = forms.FloatField()
    Vac_YOUTH_Rate_NV = forms.FloatField()
    Vac_ADULT_Rate_NV = forms.FloatField()
    Vac_ELDER_Rate_NV = forms.FloatField()

    Vac_Infection_YOUTH_Rate_V_I = forms.FloatField()
    Vac_Infection_ADULT_Rate_V_I = forms.FloatField()
    Vac_Infection_ELDER_Rate_V_I = forms.FloatField()
    Vac_Infection_YOUTH_Rate_V_NI = forms.FloatField()
    Vac_Infection_ADULT_Rate_V_NI = forms.FloatField()
    Vac_Infection_ELDER_Rate_V_NI = forms.FloatField()

    NoVac_Infection_YOUTH_Rate_NV_I = forms.FloatField()
    NoVac_Infection_ADULT_Rate_NV_I = forms.FloatField()
    NoVac_Infection_ELDER_Rate_NV_I = forms.FloatField()
    NoVac_Infection_YOUTH_Rate_NV_NI = forms.FloatField()
    NoVac_Infection_ADULT_Rate_NV_NI = forms.FloatField()
    NoVac_Infection_ELDER_Rate_NV_NI = forms.FloatField()

    SMT_HospitalizedOPD_YOUTH_Rate_HOS = forms.FloatField()
    SMT_HospitalizedOPD_ADULT_Rate_HOS = forms.FloatField()
    SMT_HospitalizedOPD_ELDER_Rate_HOS = forms.FloatField()
    SMT_HospitalizedOPD_YOUTH_Rate_OPD = forms.FloatField()
    SMT_HospitalizedOPD_ADULT_Rate_OPD = forms.FloatField()
    SMT_HospitalizedOPD_ELDER_Rate_OPD = forms.FloatField()

    SMT_Hospitalized_Death_YOUTH_Rate_HOS_D = forms.FloatField()
    SMT_Hospitalized_Death_ADULT_Rate_HOS_D = forms.FloatField()
    SMT_Hospitalized_Death_ELDER_Rate_HOS_D = forms.FloatField()
    SMT_Hospitalized_Death_YOUTH_Rate_HOS_R = forms.FloatField()
    SMT_Hospitalized_Death_ADULT_Rate_HOS_R = forms.FloatField()
    SMT_Hospitalized_Death_ELDER_Rate_HOS_R = forms.FloatField()

    SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M = forms.FloatField()
    SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M = forms.FloatField()
    SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M = forms.FloatField()
    SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_NM = forms.FloatField()
    SMT_OPD_MedicineIntake_ADULT_Rate_OPD_NM = forms.FloatField()
    SMT_OPD_MedicineIntake_ELDER_Rate_OPD_NM = forms.FloatField()

    SMT_OPD_M_Hospitalized_YOUTH_Rate_OPD_M_HOS = forms.FloatField()
    SMT_OPD_M_Hospitalized_ADULT_Rate_OPD_M_HOS = forms.FloatField()
    SMT_OPD_M_Hospitalized_ELDER_Rate_OPD_M_HOS = forms.FloatField()
    SMT_OPD_M_Hospitalized_YOUTH_Rate_OPD_M_R = forms.FloatField()
    SMT_OPD_M_Hospitalized_ADULT_Rate_OPD_M_R = forms.FloatField()
    SMT_OPD_M_Hospitalized_ELDER_Rate_OPD_M_R = forms.FloatField()

    SMT_OPD_M_Hospitalized_Death_YOUTH_Rate_OPD_M_HOS_D = forms.FloatField()
    SMT_OPD_M_Hospitalized_Death_ADULT_Rate_OPD_M_HOS_D = forms.FloatField()
    SMT_OPD_M_Hospitalized_Death_ELDER_Rate_OPD_M_HOS_D = forms.FloatField()
    SMT_OPD_M_Hospitalized_Death_YOUTH_Rate_OPD_M_HOS_R = forms.FloatField()
    SMT_OPD_M_Hospitalized_Death_ADULT_Rate_OPD_M_HOS_R = forms.FloatField()
    SMT_OPD_M_Hospitalized_Death_ELDER_Rate_OPD_M_HOS_R = forms.FloatField()

    SMT_OPD_NM_Hospitalized_YOUTH_Rate_OPD_NM_HOS = forms.FloatField()
    SMT_OPD_NM_Hospitalized_ADULT_Rate_OPD_NM_HOS = forms.FloatField()
    SMT_OPD_NM_Hospitalized_ELDER_Rate_OPD_NM_HOS = forms.FloatField()
    SMT_OPD_NM_Hospitalized_YOUTH_Rate_OPD_NM_R = forms.FloatField()
    SMT_OPD_NM_Hospitalized_ADULT_Rate_OPD_NM_R = forms.FloatField()
    SMT_OPD_NM_Hospitalized_ELDER_Rate_OPD_NM_R = forms.FloatField()

    SMT_OPD_NM_Hospitalized_Death_YOUTH_Rate_OPD_NM_HOS_D = forms.FloatField()
    SMT_OPD_NM_Hospitalized_Death_ADULT_Rate_OPD_NM_HOS_D = forms.FloatField()
    SMT_OPD_NM_Hospitalized_Death_ELDER_Rate_OPD_NM_HOS_D = forms.FloatField()
    SMT_OPD_NM_Hospitalized_Death_YOUTH_Rate_OPD_NM_HOS_R = forms.FloatField()
    SMT_OPD_NM_Hospitalized_Death_ADULT_Rate_OPD_NM_HOS_R = forms.FloatField()
    SMT_OPD_NM_Hospitalized_Death_ELDER_Rate_OPD_NM_HOS_R = forms.FloatField()
