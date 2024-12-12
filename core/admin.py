from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario


class UsuarioAdmin(BaseUserAdmin):
    # Campos a serem exibidos na listagem de usuários no painel admin
    list_display = ('email', 'nome_completo',
                    'tipo_conta', 'is_active', 'is_staff')
    list_filter = ('tipo_conta', 'is_staff', 'is_active')

    # Configuração dos campos no formulário de edição do admin
    fieldsets = (
        (None, {'fields': ('email', 'nome_completo', 'senha')}),
        ('Informações Pessoais', {
         'fields': ('tipo_conta', 'nicho', 'descricao', 'foto_perfil')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Configuração dos campos no formulário de criação do admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'senha1', 'senha2', 'tipo_conta', 'nicho', 'descricao', 'foto_perfil', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Campos utilizados para busca
    search_fields = ('email', 'nome_completo')
    ordering = ('email',)
    # Removemos os campos 'groups' e 'user_permissions'
    filter_horizontal = ()


# Registra o modelo Usuario no admin
admin.site.register(Usuario, UsuarioAdmin)
