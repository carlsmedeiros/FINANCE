from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants


def home(request):
    return render(request, 'home.html')

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = 0
    for conta in contas:
        total_contas = total_contas + conta.valor
    return render(request, 'gerenciar.html',{'contas': contas, 'total_contas': float(total_contas),'categorias':categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os dados!')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone,
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Criado com sucesso!')
    return redirect('/perfil/gerenciar')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    conta = Categoria(
        categoria=nome,
        essencial=essencial,
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Criado com sucesso!')
    return redirect('/perfil/gerenciar')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar')