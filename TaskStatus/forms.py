from django import forms
from django.core import validators
import re

class NameForm(forms.Form):
    reg = re.compile('^[a-z]+$')
    task_name = forms.CharField(label='Insert Taskname', 
                                max_length=100, 
                                validators=[validators.RegexValidator(regex=reg, message='Invalid taskname')])

