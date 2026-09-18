from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Profiles.forms import LoginForm, RegistrationForm
from Profiles.models import Profile



def home(request):
    login_form = LoginForm()
    registration_form = RegistrationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'Вы успешно вошли!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка входа. Проверьте имя пользователя и пароль.')

        elif 'register_submit' in request.POST:
            registration_form = RegistrationForm(request.POST)

            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка регистрации. Проверьте введённые данные.')

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
    }
    return render(request, 'index.html', context)



def rating_view(request):
    # Получаем топ‑5 профилей по убыванию опыта
    top_profiles = Profile.objects.select_related('user').order_by('-experience')[:5]

    if request.user.is_authenticated:
        user_profile = request.user.profile

        # Подсчёт реального места пользователя
        user_rank = Profile.objects.filter(
            experience__gt=user_profile.experience
        ).count() + 1
    else:
        user_rank = None

    return render(request, 'rating.html', {'rating': top_profiles, 'user_rank': user_rank})