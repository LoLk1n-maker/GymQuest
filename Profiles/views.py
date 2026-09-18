from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProfileSettingsForm, AvatarForm
from .models import Profile
from clans.models import Clan
from django.contrib.auth.models import User
from Tasks.models import ClanTaskCompletion


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')
    profile, _ = Profile.objects.get_or_create(user=request.user)
    clan = Clan.objects.filter(members=request.user).first()

    # Последние выполненные задания
    completed_tasks = ClanTaskCompletion.objects.filter(
        completed_by=request.user
    ).select_related('task').order_by('-completed_at')[:10]

    # === Добавляем прогрессбар ===
    current_progress = profile.experience % 100  # от 0 до 99

    context = {
        'clan': clan,
        'profile': profile,
        'settings_form': ProfileSettingsForm(instance=profile, initial={'email': request.user.email}),
        'avatar_form': AvatarForm(instance=profile),
        'completed_tasks': completed_tasks,
        'current_progress': current_progress,
    }
    return render(request, 'profile.html', context)


def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')  # или на страницу с сообщением
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=profile, initial={'email': request.user.email})
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки профиля обновлены.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return redirect('profile')


def update_avatar(request):
    if not request.user.is_authenticated:
        return redirect('home')
    profile = request.user.profile
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар успешно обновлён.')
        else:
            messages.error(request, 'Ошибка при загрузке аватара.')
        return redirect('profile')
    else:
        form = AvatarForm(instance=profile)
        return render(request, 'avatar_upload.html', {'form': form})


def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    clan = Clan.objects.filter(members=user).first()

    completed_tasks = ClanTaskCompletion.objects.filter(
        completed_by=user
    ).select_related('task')[:10]

    context = {
        'profile': profile,
        'clan': clan,
        'completed_tasks': completed_tasks,
        'is_own_profile': request.user == user,
    }
    return render(request, 'public_profile.html', context)

