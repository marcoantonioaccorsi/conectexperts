from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Usuario, Matches
from .forms import FormularioCadastroUsuario
from .forms import ConfiguracoesUsuarioForm
import random
import json


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Tenta autenticar o usuário
            usuario = authenticate(request, username=email, password=senha)

            if usuario:
                # Realiza o login se autenticado
                login(request, usuario)
                messages.success(request, '')
                return redirect('main')
            else:
                # Caso a autenticação falhe, verifica manualmente
                try:
                    usuario = Usuario.objects.get(email=email)
                    if not usuario.check_password(senha):
                        messages.error(request, 'Senha incorreta.')
                    else:
                        messages.error(
                            request, 'Erro ao autenticar o usuário.')
                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuário não encontrado.')
        else:
            messages.error(
                request, 'Erro na validação dos campos. Verifique os dados informados.')
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
            messages.error(request, "Email já está em uso.")
    else:
        formulario = FormularioCadastroUsuario()

    return render(request, 'core/create.html', {'formulario': formulario})


def main(request):
    # Obter os IDs dos usuários que já foram swipados (like ou nope)
    swiped_users = Matches.objects.filter(
        usuario=request.user).values_list('target_usuario', flat=True)

    # Filtrar usuários disponíveis (excluindo quem já foi swipado e o próprio usuário logado)
    usuarios_disponiveis = Usuario.objects.exclude(
        id__in=swiped_users).exclude(id=request.user.id)

    # Embaralhar para exibir de forma randômica
    usuarios_randomizados = list(usuarios_disponiveis)
    random.shuffle(usuarios_randomizados)

    # Retornar até 10 usuários
    return render(request, 'core/main.html', {
        'usuarios': usuarios_randomizados[:20],  # Exibir 10 usuários no máximo
    })


def register_swipe(request):
    if request.method == 'POST':
        try:
            # Obter dados do corpo da requisição
            data = json.loads(request.body)
            target_user_id = data.get('userId')
            action = data.get('action')

            # Validar entrada
            target_usuario = Usuario.objects.get(id=target_user_id)
            match = action == 'like'  # Se a ação for 'like', o match é True

            # Evitar duplicar registros
            existing_match = Matches.objects.filter(
                usuario=request.user,
                target_usuario=target_usuario
            ).first()

            if not existing_match:
                # Criar um novo registro
                Matches.objects.create(
                    usuario=request.user,
                    target_usuario=target_usuario,
                    match=match
                )
                return JsonResponse({'status': 'success', 'message': f'{action.capitalize()} registrado com sucesso'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Interação já registrada'}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=400)


def connections(request):
    return render(request, 'core/connections.html')


def chat(request):
    return render(request, 'core/chat.html')


def profile(request):
    return render(request, 'core/profile.html')


def configuracoes_usuario(request):
    print(request.user)  # Deve exibir o nome do usuário autenticado
    print(request.user.is_authenticated)  # Deve ser True

    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        messages.error(
            request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')

    # Carrega o formulário e atualiza as informações do usuário
    if request.method == 'POST':
        # Incluímos request.FILES para lidar com arquivos enviados no formulário
        form = ConfiguracoesUsuarioForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "As configurações foram atualizadas com sucesso.")
            return redirect('configuracoes_usuario')
        else:
            print(form.errors)
            messages.error(
                request, "Erro ao salvar as configurações. Por favor, corrija os erros abaixo.")
    else:
        form = ConfiguracoesUsuarioForm(instance=request.user)

    # Renderiza o template com o formulário
    return render(request, 'core/settings.html', {'form': form})


def excluir_conta(request):
    if request.method == "POST":
        usuario = request.user
        usuario.delete()  # Exclui o usuário logado
        messages.success(request, "Sua conta foi excluída com sucesso.")
        # Redireciona para a tela de login após excluir
        return redirect("login")
    else:
        messages.error(request, "Método inválido para excluir conta.")
        # Redireciona para as configurações se algo der errado
        return redirect("settings")


def profile_edit(request):
    return render(request, 'core/profile_edit.html')


def profile_editor(request):
    return render(request, 'core/profile_editor.html')
