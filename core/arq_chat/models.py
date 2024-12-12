from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class GerenciadorUsuario(BaseUserManager):
    def criar_usuario(self, email, senha=None, **campos_extras):
        if not email:
            raise ValueError("O campo Email é obrigatório")
        email = self.normalize_email(email)
        usuario = self.model(email=email, **campos_extras)
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario

    def criar_superusuario(self, email, senha=None, **campos_extras):
        campos_extras.setdefault('is_staff', True)
        campos_extras.setdefault('is_superuser', True)
        return self.criar_usuario(email, senha, **campos_extras)


class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=255)
    tipo_conta = models.CharField(max_length=20, choices=[(
        'especialista', 'Especialista'), ('coprodutor', 'Coprodutor')])
    nicho = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = GerenciadorUsuario()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    def __str__(self):
        return self.email
