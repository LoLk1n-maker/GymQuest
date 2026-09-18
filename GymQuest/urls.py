"""
URL configuration for GymQuest project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import *

DOCS_ROOT = settings.BASE_DIR / 'docs' / 'build' / 'html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('profile/', include('Profiles.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('', include('clans.urls')),
    path('rating/', rating_view, name='rating'),
    path('quests/', include('Tasks.urls')),

    # Документация (Sphinx HTML)
    path('docs/', serve, {'document_root': DOCS_ROOT, 'path': 'index.html'}),
    re_path(r'^docs/(?P<path>.*)$', serve, {'document_root': DOCS_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
