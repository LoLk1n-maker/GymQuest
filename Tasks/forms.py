from django import forms
from .models import ClanTask
from django.core.exceptions import ValidationError


class ClanTaskForm(forms.ModelForm):
    class Meta:
        model = ClanTask
        fields = ['title', 'description', 'xp_reward', 'deadline']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 1000}),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_xp_reward(self):
        xp = self.cleaned_data.get('xp_reward')

        if xp is None:
            raise ValidationError("Укажите награду за задание")

        if xp <= 0:
            raise ValidationError("Награда за задание не может быть отрицательной или нулевой")

        if xp > 1000:
            raise ValidationError("Максимальная награда — 1000 XP")

        return xp
