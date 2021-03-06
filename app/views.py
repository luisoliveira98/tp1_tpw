from typing import List, Any

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import re
from app.forms import *
from app.models import *

from datetime import datetime


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    listaReceitas = Receita.objects.order_by("-classificacao")[0:6]

    tparams = {
        'listaReceitas': listaReceitas,
    }
    return render(request, 'index.html', tparams)


def receita(request, id):
    print(id)
    assert isinstance(request, HttpRequest)
    receita = Receita.objects.get(id=id)
    tags = [tag for tag in Tags.objects.all() if receita in tag.receitas.all()]
    listIngredientes = Ingredientes.objects.filter(receita=receita)
    preparacaoPassos = re.split(re.compile('[0-9]\. '), receita.preparacao)
    comentarios = Comentario.objects.filter(receita=receita)
    saved = ReceitasGuardadas.objects.filter(receita=receita, utilizador=request.user)
    liked = ReceitasGostadas.objects.filter(receita=receita, utilizador=request.user)

    if not saved:
        booksave = "far fa-bookmark"
    else:
        booksave = "fas fa-bookmark"

    if not liked:
        likeclass = "far fa-heart"
    else:
        likeclass = "fas fa-heart"

    if request.method == 'POST':
        if 'save' in request.POST:
            if saved:
                ReceitasGuardadas.objects.get(receita=receita, utilizador=request.user).delete()
                booksave = "far fa-bookmark"
            else:
                new = ReceitasGuardadas(receita=receita, utilizador=request.user)
                new.save()
                booksave = "fas fa-bookmark"
        if 'like' in request.POST:
            if liked:
                ReceitasGostadas.objects.get(receita=receita, utilizador=request.user).delete()
                receita.classificacao -= 1
                receita.save()
                likeclass = "far fa-heart"
            else:
                newLike = ReceitasGostadas(receita=receita, utilizador=request.user)
                newLike.save()
                receita.classificacao += 1
                receita.save()
                likeclass = "fas fa-heart"


    tparams = {
        'id':receita.id,
        'nome': receita.nome,
        'descricao': receita.descricao,
        'imagem': '/media/'+str(receita.imagem),
        'duracao': receita.tempo,
        'dificuldade': receita.dificuldade,
        'dose': receita.dose,
        'listIngredientes': listIngredientes,
        'preparacao': preparacaoPassos[1:],
        'booksaveclass': booksave,
        'likeclass': likeclass,
        'comentarios': comentarios,
        'tags': tags
    }

    return render(request, 'receita.html', tparams)


def signup(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()

            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            messages.success(request, 'Account created successfully')
            return redirect('home')

    else:
        f = UserCreationForm()

    return render(request, 'signup.html', {'form': f})


def criar_receita(request):
    assert isinstance(request, HttpRequest)
    tags = Tags.objects.all()
    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        passos = request.POST['passos']
        tipo = request.POST['tipoReceita']
        dificuldade = request.POST['dificuldade']
        tempo = request.POST['tempo']
        dose = request.POST['dose']
        imagem = request.FILES['imagem']
        receita = Receita(nome=nome, descricao=descricao, dificuldade=dificuldade, preparacao=passos, tipo=tipo, tempo=tempo, dose=dose, imagem=imagem, data=datetime.now().strftime('%Y-%m-%d'), utilizador=request.user, classificacao=0)
        receita.save()
        lst_ingredientes = []
        lst_quantidades = []
        lst_unidades = []
        for key in request.POST:
            if key.startswith('ing-'):
                lst_ingredientes.append(request.POST[key])
            elif key.startswith('qt-'):
                lst_quantidades.append(request.POST[key])
            elif key.startswith('un-'):
                lst_unidades.append(request.POST[key])

        for i in range(len(lst_quantidades)):
            ing = Ingredientes(receita=receita, ingredienteName=lst_ingredientes[i],
                               ingredienteQuant=lst_quantidades[i], unidade=lst_unidades[i])
            ing.save()

        for tag in request.POST.getlist('tags', []):
            t = Tags.objects.get(nome=tag)
            t.receitas.add(receita)

        return redirect('home')

    tparams = {
        'tipos': ['Sopa', 'Carne', 'Peixe', 'Acompanhamento', 'Vegetariano', 'Sobremesa', 'Massas', 'Entrada'],
        'dificuldade': ['Muito Fácil', 'Fácil', 'Médio', 'Difícil', 'Muito Difícil'],
        'unidades': ['unidade', 'mL', 'L', 'g', 'kg', 'chávena', 'c. sopa', 'c. chá', 'c. café', 'qb'],
        'tags': tags[::-1]
    }

    return render(request, 'adicionarReceita.html', tparams)


def perfil(request):
    assert isinstance(request, HttpRequest)

    minhasReceitas = Receita.objects.filter(utilizador=request.user)
    receitasGuardadas = ReceitasGuardadas.objects.filter(utilizador=request.user)

    print(minhasReceitas)
    print(receitasGuardadas)

    tparams = {
        'infominhasreceitas': minhasReceitas,
        'inforeceitasguardadas': receitasGuardadas
    }

    return render(request, 'perfil.html', tparams)


def receita_tipo(request, tipo : str):
    print(tipo)
    receitas = Receita.objects.filter(tipo=tipo)
    print(receitas)

    tparams = {
        'tipo': tipo,
        'listaReceitas': receitas
    }
    return render(request, 'receitasTipo.html', tparams)

def pesquisa(request):
    query=''
    lst_tags = []
    tags = Tags.objects.all()
    if request.method=='POST':
        if 'query' in request.POST:
            query = request.POST['query']
            queryResult = Receita.objects.filter(nome__contains=query)
        if 'tags' in request.POST and len(request.POST.getlist('tags', []))>1:
            lst_tags = request.POST.getlist('tags', [])
            temp_receitas = []
            for t in lst_tags:
                if t=='':
                    continue
                tag = Tags.objects.get(nome=t)
                tag_receitas = tag.receitas.all()
                for r in queryResult:
                    if r in tag_receitas:
                        temp_receitas.append(r)

            queryResult = temp_receitas

    tparams = {
        'query': query,
        'queryResult': queryResult,
        'tags': tags,
        'lst_tags': lst_tags
    }
    return render(request, 'resultadosPesquisa.html', tparams)

def apagar_receita(request, id):
    receita = Receita.objects.get(id=id)
    receita.delete()
    return redirect('perfil')


def comentar_receita(request, id):
    if request.method == 'POST':
        comentario = request.POST['comentario']
        receita = Receita.objects.get(id=id)
        c = Comentario(receita=receita, data=datetime.now().strftime('%Y-%m-%d'), utilizador=request.user, comentario=comentario)
        c.save()
        return redirect('receita', id)


def update_receita(request, id):
    receita = Receita.objects.get(id=id)
    tags = Tags.objects.all()
    tags_receita = Tags.objects.filter(receitas=receita)
    ingredientes_receita = Ingredientes.objects.filter(receita=receita)
    print(request.POST)

    if request.method == 'POST':
        print('aqui')
        receita.nome = request.POST['nome']
        receita.descricao = request.POST['descricao']
        receita.preparacao = request.POST['passos']
        receita.tipo = request.POST['tipoReceita']
        receita.tempo = request.POST['tempo']
        receita.dificuldade = request.POST['dificuldade']
        receita.dose = request.POST['dose']
        receita.save()

        for ingrediente in ingredientes_receita:
            ingrediente.delete()
        for tag in tags_receita:
            tag.receitas.remove(receita)

        lst_ingredientes = []
        lst_quantidades = []
        lst_unidades = []
        for key in request.POST:
            if key.startswith('ing-'):
                lst_ingredientes.append(request.POST[key])
            elif key.startswith('qt-'):
                lst_quantidades.append(request.POST[key])
            elif key.startswith('un-'):
                lst_unidades.append(request.POST[key])

        for i in range(len(lst_quantidades)):
            ing = Ingredientes(receita=receita, ingredienteName=lst_ingredientes[i],
                               ingredienteQuant=lst_quantidades[i], unidade=lst_unidades[i])
            ing.save()

        for tag in request.POST.getlist('tags', []):
            t = Tags.objects.get(nome=tag)
            t.receitas.add(receita)

        return redirect('perfil')

    tparams = {
        'receita': receita,
        'tipos': ['Sopa', 'Carne', 'Peixe', 'Acompanhamentos', 'Vegetariano', 'Sobremesa'],
        'dificuldade': ['Muito Fácil', 'Fácil', 'Médio', 'Difícil', 'Muito Difícil'],
        'unidades': ['unidade', 'mL', 'L', 'g', 'kg', 'chávena', 'c. sopa', 'c. chá', 'c. café', 'qb'],
        'tags': tags[::-1],
        'tags_receita': tags_receita,
        'ingredientes_receita': ingredientes_receita,
        'range_ingredientes': range(len(ingredientes_receita)),
        'n_ingredientes': len(ingredientes_receita)-1
    }
    return render(request, 'updateReceita.html', tparams)


def receita_tag(request, tag):
    print(tag)
    tag = Tags.objects.get(nome=tag)
    receitas = tag.receitas.all()
    tparams = {
        'tag': tag,
        'receitas':receitas
    }
    return render(request, 'receitasTags.html', tparams)


