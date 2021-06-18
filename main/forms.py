from django import forms

# class ParametersForm(forms.Form):
            # <input class="form-control" type="number" value="5000" id="BMP_IDX_CASE_NUM">


class AnalysisCodeForm(forms.Form):
    your_analysis_code = forms.CharField(max_length=100)

class RunModelForm(forms.Form):
    # try_ = forms.IntegerField()

    BMP_IDX_CASE_NUM = forms.IntegerField()
    BMP_SIMULATION_DAY = forms.IntegerField()
    BMP_CYCLE_DAYS = forms.IntegerField()
    BMP_CONTACT_PEOPLE_NUM = forms.IntegerField()

    AGP_YOUTH_GRP = forms.FloatField()
    AGP_ADULT_GRP = forms.FloatField()
    AGP_ELDER_GRP = forms.FloatField()

    CR_SAME_GRP = forms.FloatField()
    CR_DIFF_GRP = forms.FloatField()

    Vac_YOUTH_Rate_V = forms.FloatField()
    Vac_ADULT_Rate_V = forms.FloatField()
    Vac_ELDER_Rate_V = forms.FloatField()

    Vac_Infection_YOUTH_Rate_V_I = forms.FloatField()
    Vac_Infection_ADULT_Rate_V_I = forms.FloatField()
    Vac_Infection_ELDER_Rate_V_I = forms.FloatField()

    NoVac_Infection_YOUTH_Rate_NV_I = forms.FloatField()
    NoVac_Infection_ADULT_Rate_NV_I = forms.FloatField()
    NoVac_Infection_ELDER_Rate_NV_I = forms.FloatField()

    CP_SMT_YOUTH_Rate_CP = forms.FloatField()
    CP_SMT_ADULT_Rate_CP = forms.FloatField()
    CP_SMT_ELDER_Rate_CP = forms.FloatField()
    CP_SMT_YOUTH_Rate_ST = forms.FloatField()
    CP_SMT_ADULT_Rate_ST = forms.FloatField()
    CP_SMT_ELDER_Rate_ST = forms.FloatField()

    SMT_IPDOPD_YOUTH_Rate_IPD = forms.FloatField()
    SMT_IPDOPD_ADULT_Rate_IPD = forms.FloatField()
    SMT_IPDOPD_ELDER_Rate_IPD = forms.FloatField()
    SMT_IPDOPD_YOUTH_Rate_OPD = forms.FloatField()
    SMT_IPDOPD_ADULT_Rate_OPD = forms.FloatField()
    SMT_IPDOPD_ELDER_Rate_OPD = forms.FloatField()

    # SMT_IPD_Death_YOUTH_Rate_IPD_D = forms.FloatField()
    # SMT_IPD_Death_ADULT_Rate_IPD_D = forms.FloatField()
    # SMT_IPD_Death_ELDER_Rate_IPD_D = forms.FloatField()

    SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M = forms.FloatField()
    SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M = forms.FloatField()
    SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M = forms.FloatField()

    SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD = forms.FloatField()
    SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD = forms.FloatField()
    SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD = forms.FloatField()

    SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D = forms.FloatField()
    SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D = forms.FloatField()
    SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D = forms.FloatField()

    SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD = forms.FloatField()
    SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD = forms.FloatField()
    SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD = forms.FloatField()

    SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D = forms.FloatField()
    SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D = forms.FloatField()
    SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D = forms.FloatField()

    MC_YOUTH_EARN_LOST_PER_DAY_Rate = forms.FloatField()
    MC_ADULT_EARN_LOST_PER_DAY_Rate = forms.FloatField()
    MC_ELDER_EARN_LOST_PER_DAY_Rate = forms.FloatField()

    TIC_YOUTH_AVE_STAY_DAY_Rate = forms.FloatField()
    TIC_ADULT_AVE_STAY_DAY_Rate = forms.FloatField()
    TIC_ELDER_AVE_STAY_DAY_Rate = forms.FloatField()
    TIC_YOUTH_COST_PER_BED_PER_DAY_Rate = forms.FloatField()
    TIC_ADULT_COST_PER_BED_PER_DAY_Rate = forms.FloatField()
    TIC_ELDER_COST_PER_BED_PER_DAY_Rate = forms.FloatField()
    TIC_YOUTH_HOS_LOSS_PER_DAY_Rate = forms.FloatField()
    TIC_ADULT_HOS_LOSS_PER_DAY_Rate = forms.FloatField()
    TIC_ELDER_HOS_LOSS_PER_DAY_Rate = forms.FloatField()
    TIC_YOUTH_TRANS_COST_Rate = forms.FloatField()
    TIC_ADULT_TRANS_COST_Rate = forms.FloatField()
    TIC_ELDER_TRANS_COST_Rate = forms.FloatField()

    TOC_YOUTH_AVE_DAY_LOST_Rate = forms.FloatField()
    TOC_ADULT_AVE_DAY_LOST_Rate = forms.FloatField()
    TOC_ELDER_AVE_DAY_LOST_Rate = forms.FloatField()
    TOC_YOUTH_TREAT_COST_Rate = forms.FloatField()
    TOC_ADULT_TREAT_COST_Rate = forms.FloatField()
    TOC_ELDER_TREAT_COST_Rate = forms.FloatField()
    TOC_YOUTH_OPD_LOST_PER_DAY_Rate = forms.FloatField()
    TOC_ADULT_OPD_LOST_PER_DAY_Rate = forms.FloatField()
    TOC_ELDER_OPD_LOST_PER_DAY_Rate = forms.FloatField()
    TOC_YOUTH_TRANS_COST_Rate = forms.FloatField()
    TOC_ADULT_TRANS_COST_Rate = forms.FloatField()
    TOC_ELDER_TRANS_COST_Rate = forms.FloatField()

    TVC_YOUTH_VAC_COST_Rate = forms.FloatField()
    TVC_ADULT_VAC_COST_Rate = forms.FloatField()
    TVC_ELDER_VAC_COST_Rate = forms.FloatField()
    TVC_YOUTH_VAC_LOST_PER_HOUR_Rate = forms.FloatField()
    TVC_ADULT_VAC_LOST_PER_HOUR_Rate = forms.FloatField()
    TVC_ELDER_VAC_LOST_PER_HOUR_Rate = forms.FloatField()
    TVC_YOUTH_TRANS_COST_Rate = forms.FloatField()
    TVC_ADULT_TRANS_COST_Rate = forms.FloatField()
    TVC_ELDER_TRANS_COST_Rate = forms.FloatField()
    TVC_YOUTH_EFF = forms.FloatField()
    TVC_ADULT_EFF = forms.FloatField()
    TVC_ELDER_EFF = forms.FloatField()

    TVSEC_YOUTH_SIDE_EFF_Rate = forms.FloatField()
    TVSEC_ADULT_SIDE_EFF_Rate = forms.FloatField()
    TVSEC_ELDER_SIDE_EFF_Rate = forms.FloatField()
    TVSEC_YOUTH_MEAN_OPD_FREQ_Rate = forms.FloatField()
    TVSEC_ADULT_MEAN_OPD_FREQ_Rate = forms.FloatField()
    TVSEC_ELDER_MEAN_OPD_FREQ_Rate = forms.FloatField()
    TVSEC_YOUTH_DIR_OPD_COST_Rate = forms.FloatField()
    TVSEC_ADULT_DIR_OPD_COST_Rate = forms.FloatField()
    TVSEC_ELDER_DIR_OPD_COST_Rate = forms.FloatField()
    TVSEC_YOUTH_PROD_OPD_LOSS_Rate = forms.FloatField()
    TVSEC_ADULT_PROD_OPD_LOSS_Rate = forms.FloatField()
    TVSEC_ELDER_PROD_OPD_LOSS_Rate = forms.FloatField()
    TVSEC_YOUTH_TRANS_COST_Rate = forms.FloatField()
    TVSEC_ADULT_TRANS_COST_Rate = forms.FloatField()
    TVSEC_ELDER_TRANS_COST_Rate = forms.FloatField()
