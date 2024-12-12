from django import forms
from .models import Usuario


class FormularioCadastroUsuario(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite um email válido',
            'maxlength': 320,
        }),
        label='Endereço de Email',
        required=True
    )

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        }),
        min_length=2
    )

    nome_completo = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo',
        })

    )

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'email', 'senha',
                  'tipo_conta', 'nicho', 'descricao', 'foto_perfil']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['senha'])
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Endereço de Email',
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class ConfiguracoesUsuarioForm(forms.ModelForm):
    nova_senha = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Nova Senha"
    )

    class Meta:
        model = Usuario
        fields = [
            'nome_completo',
            'email',
            'foto_perfil',
            'tipo_conta',
            'nicho',
            'descricao'
        ]

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # Verifica se uma nova senha foi fornecida
        nova_senha = self.cleaned_data.get('nova_senha')
        if nova_senha:
            usuario.set_password(nova_senha)

        # Verifica se uma nova imagem foi enviada
        nova_foto_perfil = self.cleaned_data.get('foto_perfil')
        if nova_foto_perfil:
            usuario.foto_perfil = nova_foto_perfil

        nova_foto_perfil = forms.ImageField(
            required=False,
            widget=forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            label="Foto de Perfil"
        )

        if commit:
            usuario.save()
        return usuario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona placeholders e estilização para os campos
        self.fields['nome_completo'].widget.attrs.update({
            'placeholder': 'Digite seu nome completo'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Digite seu email'
        })
        self.fields['nova_senha'].widget.attrs.update({
            'placeholder': 'Digite uma nova senha (opcional)'
        })
        self.fields['foto_perfil'].widget.attrs.update({
            'accept': 'image/*'
        })
        self.fields['tipo_conta'].widget.attrs.update({
            'placeholder': 'Selecione o tipo de conta'
        })
        self.fields['nicho'].widget.attrs.update({
            'placeholder': 'Informe seu nicho profissional'
        })
        self.fields['descricao'].widget.attrs.update({
            'placeholder': 'Escreva uma breve descrição sobre você'
        })
