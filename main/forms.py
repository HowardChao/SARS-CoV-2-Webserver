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

    CR_SAME_GRP = forms.FloatField()
    CR_DIFF_GRP = forms.FloatField()

    VR_YOUTH_RT = forms.FloatField()
    VR_ADULT_RT = forms.FloatField()
    VR_ELDER_RT = forms.FloatField()

    IR_YOUTH_NV_RT = forms.FloatField()
    IR_ADULT_NV_RT = forms.FloatField()
    IR_ELDER_NV_RT = forms.FloatField()
    IR_YOUTH_V_RT = forms.FloatField()
    IR_ADULT_V_RT = forms.FloatField()
    IR_ELDER_V_RT = forms.FloatField()

    STR_YOUTH_RT = forms.FloatField()
    STR_ADULT_RT = forms.FloatField()
    STR_ELDER_RT = forms.FloatField()

    MIR_YOUTH_RT = forms.FloatField()
    MIR_ADULT_RT = forms.FloatField()
    MIR_ELDER_RT = forms.FloatField()

    SR_YOUTH_48_RT = forms.FloatField()
    SR_ADULT_48_RT = forms.FloatField()
    SR_ELDER_48_RT = forms.FloatField()
    SR_YOUTH_N48_RT = forms.FloatField()
    SR_ADULT_N48_RT = forms.FloatField()
    SR_ELDER_N48_RT = forms.FloatField()

    FR_YOUTH_RT = forms.FloatField()
    FR_ADULT_RT = forms.FloatField()
    FR_ELDER_RT = forms.FloatField()
