from django.shortcuts import render
from perfil.models import Categoria
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

@login_required(login_url='auth/logar')
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@login_required(login_url='auth/logar')
@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})

@login_required(login_url='auth/logar')
def ver_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_planejamento.html', {'categorias': categorias})