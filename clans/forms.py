from django import forms
from .models import Clan

class ClanCreateForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['name']
