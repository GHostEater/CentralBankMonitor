from django import forms
from models import Bank, SpecialTrans
import datetime


class BankOfficerForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()
    email = forms.EmailField()
    bank = forms.ModelChoiceField(queryset=Bank.objects.all())


class SpecialTransRequestForm(forms.ModelForm):
    class Meta:
        model = SpecialTrans
        labels = {
            'trans_type': 'Transaction Type'
        }
        fields = [
            'type',
            'trans_type',
            'amount',
            'detail',
        ]


class SpecialTransProcessForm(forms.Form):
    status_choices = (
        (1, 'Approved'),
        (2, 'Declined'),
    )
    status = forms.ChoiceField(choices=status_choices)
    reason = forms.Textarea()


class ReportForm(forms.Form):
    type_choices = (
        (1, 'Month Report'),
        (2, 'Year Report'),
    )
    months_choices = []
    for i in range(1, 13):
        months_choices.append((datetime.date(2017, i, 1).strftime('%m'), datetime.date(2017, i, 1).strftime('%B')))

    year_choices = []
    min_year = int(datetime.MINYEAR)
    max_year = int(datetime.date(2017, 01, 01).strftime('%Y'))
    for year in range(max_year, min_year, -1):
        year_choices.append((datetime.date(year, 01, 01).strftime('%Y'), datetime.date(year, 01, 01).strftime('%Y')))

    type = forms.ChoiceField(choices=type_choices)
    month = forms.ChoiceField(choices=months_choices)
    year = forms.ChoiceField(choices=year_choices)
