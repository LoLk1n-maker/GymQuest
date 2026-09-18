from .views import *
from django.urls import path

urlpatterns = [
    path('', clan_tasks, name='quests'),
    path('tasks/<int:task_id>/complete/', complete_task, name='complete_task'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/start/', start_task, name='start_task'),
]