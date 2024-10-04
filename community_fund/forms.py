from django import forms
from .models import User, Transaction,Deduction

class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['category', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }
class TransactionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="नाम चुनें")

    class Meta:
        model = Transaction
        fields = ['user', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }
class UserReportForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(),label="नाम चुनें", required=False)
    start_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day")), required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day")), required=False)
