from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='auth/logar')
def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/perfil/home')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        confirmar_pasword = request.POST.get('confirm-password')

        if not senha == confirmar_pasword:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
            return redirect('/auth/cadastro')
        if len(username.strip()) == 0  or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Nome de usuário e senha não pode ter espaços.')

        if len(senha) < 5:
            messages.add_message(request, constants.ERROR, 'A senha deve de ter pelo menos 5 letras')
            return redirect('/auth/cadastro')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já tem um usuário com esse nome')
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=username, password=senha)
            user.save()
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro do sistema, tente de novo!')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/perfil/home')
        return render(request, 'logar.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/perfil/home')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')



