from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('login/', views.login_usuario, name='login'),
    path('criar/', views.criar_conta, name='criar_conta'),
    path('main/', views.main, name='main'),
    path('connections/', views.connections, name='connections'),
    path('chat/', views.chat, name='chat'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('profile-editor/', views.profile_editor, name='profile_editor'),
]
