from django.shortcuts import render, redirect, get_object_or_404

from .models import Clan
from .forms import ClanCreateForm
from Tasks.models import ClanTask


def clans_view(request):

    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')
    clans = Clan.objects.all()
    form = ClanCreateForm()

    return render(request, 'clans.html', {
        'clans': clans,
        'form': form
    })


def join_clan(request, clan_id):

    for clan in request.user.clans.all():
        if request.user == clan.owner:
            return redirect('clans')

    clan = get_object_or_404(Clan, id=clan_id)

    # ❗ Удаляем пользователя из всех кланов
    for c in request.user.clans.all():
        c.members.remove(request.user)

    # Добавляем в новый
    clan.members.add(request.user)

    return redirect('clans')


def join_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            clan = Clan.objects.get(code=code)

            # ❗ выходим из старого клана (если есть)
            for c in request.user.clans.all():
                c.members.remove(request.user)

            clan.members.add(request.user)

        except Clan.DoesNotExist:
            pass

    return redirect('clans')


def leave_clan(request, clan_id):
    clan = get_object_or_404(Clan, id=clan_id)

    if clan.owner == request.user:
        return redirect('clans')

    clan.members.remove(request.user)

    return redirect('clans')


def delete_clan(request, clan_id):
    clan = get_object_or_404(Clan, id=clan_id)

    # ❗ Только владелец может удалить
    if clan.owner != request.user:
        return redirect('clans')

    clan.delete()

    return redirect('clans')


def create_clan(request):
    if request.method == 'POST':
        if request.user.clans.exists():
            return redirect('clans')

        form = ClanCreateForm(request.POST)
        if form.is_valid():
            clan = form.save(commit=False)
            clan.owner = request.user
            clan.save()
            clan.members.add(request.user)

            # Создаём 3 базовых задания
            ClanTask.objects.bulk_create([
                ClanTask(
                    clan=clan,
                    title="Первая тренировка в клане",
                    description="Выполни любое упражнение и отметься в журнале",
                    xp_reward=100,
                    status='todo'
                ),
                ClanTask(
                    clan=clan,
                    title="Завершить 3 ежедневных задания",
                    description="Прояви активность 3 дня подряд",
                    xp_reward=150,
                    status='todo'
                ),
                ClanTask(
                    clan=clan,
                    title="Привести друга в клан",
                    description="Пригласи нового участника по коду",
                    xp_reward=200,
                    status='todo'
                ),
            ])

            return redirect('clans')

    return redirect('clans')