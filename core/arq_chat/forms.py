from django import forms
from .models import Usuario


class FormularioCadastroUsuario(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, min_length=6)

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
    email = forms.EmailField(label='Email', max_length=255, required=True)
    senha = forms.CharField(
        label='Senha', widget=forms.PasswordInput, required=True)
