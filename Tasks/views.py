from django.shortcuts import render, redirect, get_object_or_404
from .models import ClanTask, ClanTaskCompletion
from .forms import ClanTaskForm
from clans.models import Clan
from Profiles.models import Profile


def start_task(request, task_id):
    task = get_object_or_404(ClanTask, id=task_id)

    if request.user not in task.participants.all():
        task.participants.add(request.user)

    task.status = 'doing'
    task.save()

    return redirect('quests')


def complete_task(request, task_id):
    task = get_object_or_404(ClanTask, id=task_id)

    if request.user not in task.participants.all():
        return redirect('quests')

    if task.status == 'done':
        return redirect('quests')

    task.status = 'done'
    task.save()

    ClanTaskCompletion.objects.create(
        task=task,
        completed_by=request.user
    )

    # ✅ XP только участникам
    for user in task.participants.all():
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.experience += task.xp_reward
        profile.completed_tasks += 1
        profile.save()

    return redirect('quests')


def clan_tasks(request):

    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')

    clan = Clan.objects.filter(members=request.user).first()

    if not clan:
        return render(request, 'no_clan.html')

    tasks_todo = clan.tasks.filter(status='todo')
    tasks_doing = clan.tasks.filter(status='doing')
    tasks_done = clan.tasks.filter(status='done')

    return render(request, 'quests.html', {
        'clan': clan,
        'tasks_todo': tasks_todo,
        'tasks_doing': tasks_doing,
        'tasks_done': tasks_done,
    })


def create_task(request):
    clan = Clan.objects.filter(members=request.user).first()

    if not clan:
        return redirect('quests')

    if request.method == 'POST':
        form = ClanTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.clan = clan
            task.save()
            return redirect('quests')
    else:
        form = ClanTaskForm()

    return render(request, 'create_task.html', {'form': form})


