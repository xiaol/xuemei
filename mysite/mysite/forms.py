from django import forms
from django.utils.translation import ugettext_lazy as _


class ToggleForm(forms.Form):
     id = forms.IntegerField(label=_("Id"))
