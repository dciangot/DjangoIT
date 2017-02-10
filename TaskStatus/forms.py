from django import forms
from django.core import validators
import re

class NameForm(forms.Form):
    reg = re.compile('^[0-9]{6}_[0-9]{6}:\S+_crab_\S+$')
    #reg = re.compile('^\S+$')
    task_name = forms.CharField(label='Insert Taskname', 
                                max_length=100, 
                                validators=[validators.RegexValidator(regex=reg, message='Invalid taskname')])

