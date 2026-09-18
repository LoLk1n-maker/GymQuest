from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', profile, name='profile'),
    path('update/', update_profile, name='update_profile'),
    path('avatar/', update_avatar, name='update_avatar'),
    path('<str:username>/', public_profile_view, name='public_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)