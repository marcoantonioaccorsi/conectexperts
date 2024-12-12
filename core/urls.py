from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login_usuario, name='login'),
    path('login/', views.login_usuario, name='login'),
    path('criar/', views.criar_conta, name='criar_conta'),
    path("excluir-conta/", views.excluir_conta, name="excluir_conta"),
    path('main/', views.main, name='main'),
    path('register-swipe/', views.register_swipe, name='register_swipe'),
    path('connections/', views.connections, name='connections'),
    path('chat/', views.chat, name='chat'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.configuracoes_usuario, name='configuracoes_usuario'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('profile-editor/', views.profile_editor, name='profile_editor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
