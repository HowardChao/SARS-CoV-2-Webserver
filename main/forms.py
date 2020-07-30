from django import forms

class ParametersForm(forms.Form):
            # <input class="form-control" type="number" value="5000" id="BMP_IDX_CASE_NUM">
    BMP_IDX_CASE_NUM = forms.IntegerField()
    BMP_SIMULATION_DAY = forms.IntegerField()


class RunModelForm(forms.Form):
    try_ = forms.IntegerField()
