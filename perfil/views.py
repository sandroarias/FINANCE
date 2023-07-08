from django.shortcuts import render, redirect
from .models import Conta, Categoria
from contas.models import ContaPaga, ContaPagar
from extrato.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financieiro
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required(login_url='auth/logar')
def home(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')

    saldo_mensal = total_entradas - total_saidas



    contas = Conta.objects.all()

    total_conta = calcula_total(contas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financieiro()


    contas_filtro = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas_filtro.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas_filtro.filter(dia_pagamento__lte=DIA_ATUAL + 5).filter(
        dia_pagamento__gt=DIA_ATUAL).exclude(id__in=contas_pagas)

    context = {
        'contas': contas,
        'total_conta': total_conta,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
        'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'saldo_mensal': saldo_mensal

    }
    return render(request, 'home.html', context)

@login_required(login_url='auth/logar')
def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_conta = calcula_total(contas, 'valor')

    context = {
        'contas': contas,
        'total_conta': total_conta,
        'categorias': categorias,
    }
    return render(request, 'gerenciar.html', context)


@login_required(login_url='auth/logar')
def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')


@login_required(login_url='auth/logar')
def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')

@login_required(login_url='auth/logar')
def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = Categoria(
        categoria=nome,
        essencial=essencial,
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

@login_required(login_url='auth/logar')
def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('/perfil/gerenciar/')

@login_required(login_url='auth/logar')
def dashboard(request):
    dados = {}

    categorias = Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            total = total + v.valor
        dados[categoria.categoria] = total
    return  render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})