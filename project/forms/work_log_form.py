from django import forms
from project.models import WorkLog, Salary
from django.utils.translation import gettext_lazy as _
class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ["is_leave", 'paystatus']

        # widgets = {
        #     "time_in": forms.TimeInput(attrs={"type": "time", "class": "border rounded p-2 form-control"}),
        #     "time_out": forms.TimeInput(attrs={"type": "time", "class": "border rounded p-2 form-control"}),
        #     "is_leave": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        #     "task_description": forms.Textarea(attrs={"rows": 3, "class": "border rounded p-2 form-control"}),
        #     "performance_amount": forms.NumberInput(attrs={"class": "border rounded p-2 form-control"}),
        # }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['worklog', 'amount']
        labels = {"amount": _('Amount')}
        widgets ={
            "amount": forms.NumberInput(attrs={"class": "border rounded p-2 form-control"}),
        }
