from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import LoginForm
from .models import Usuario
from .forms import FormularioCadastroUsuario


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['password']
            try:
                # Busca o usuário pelo email
                usuario = Usuario.objects.get(email=email)

                # Valida a senha
                if usuario.check_password(senha):
                    login(request, usuario)  # Autentica o usuário
                    # Redireciona para a página principal
                    return redirect('main')
                else:
                    messages.error(request, 'Senha incorreta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
        else:
            messages.error(request, 'Erro na validação dos campos.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def criar_conta(request):
    if request.method == 'POST':
        formulario = FormularioCadastroUsuario(request.POST, request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "Conta criada com sucesso!")
            return redirect('login')  # Redireciona para a página de login
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        formulario = FormularioCadastroUsuario()

    return render(request, 'core/create.html', {'formulario': formulario})


def main(request):
    return render(request, 'core/main.html')


def connections(request):
    return render(request, 'core/connections.html')


def chat(request):
    return render(request, 'core/chat.html')


def profile(request):
    return render(request, 'core/profile.html')


def settings(request):
    return render(request, 'core/settings.html')


def profile_edit(request):
    return render(request, 'core/profile_edit.html')


def profile_editor(request):
    return render(request, 'core/profile_editor.html')
