from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

# Форма регистрации на основе UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@kingdom.com'})
    )
    # Поле выбора класса (используем выборы из модели Profile)
    character_class = forms.ChoiceField(
        choices=Profile.CharacterClass.choices,
        label='Класс',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs['placeholder'] = 'Железный паладин'
        self.fields['password1'].widget.attrs['placeholder'] = '●●●●●●●●'
        self.fields['password2'].widget.attrs['placeholder'] = '●●●●●●●●'
        # Убираем form-control у select для класса, так как используем form-select
        self.fields['character_class'].widget.attrs.pop('class', None)
        self.fields['character_class'].widget.attrs['class'] = 'form-select'

    def save(self, commit=True):
        user = super().save(commit=True)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.character_class = self.cleaned_data['character_class']
        profile.save()
        return user


# Форма входа
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'you@kingdom.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '●●●●●●●●'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем автофокус с поля username (опционально)
        self.fields['username'].widget.attrs.pop('autofocus', None)


class ProfileSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = [
            'display_name', 'character_class', 'home_location', 'main_goal', 'bio',
            'favorite_dungeon',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap классы
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Сохраняем связанного пользователя
            user = profile.user
            user.email = self.cleaned_data['email']
            if self.cleaned_data.get('display_name'):
                # display_name хранится в профиле, но также можно сохранять в username или в отдельное поле
                # Допустим, у нас есть поле display_name в модели Profile
                profile.display_name = self.cleaned_data['display_name']
                profile.save()
            user.save()
        return profile



class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }