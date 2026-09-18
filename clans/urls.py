
from django.urls import path

from . import views

urlpatterns = [
    path('clans/', views.clans_view, name='clans'),
    path('clans/create/', views.create_clan, name='create_clan'),
    path('clans/join/<int:clan_id>/', views.join_clan, name='join_clan'),
    path('clans/leave/<int:clan_id>/', views.leave_clan, name='leave_clan'),
    path('clans/join-code/', views.join_by_code, name='join_by_code'),
    path('clans/delete/<int:clan_id>/', views.delete_clan, name='delete_clan'),
]