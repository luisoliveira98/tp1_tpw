from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from datetime import datetime
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
    assert isinstance(request, HttpRequest)

    receita = Receita.objects.get(id=id)
    listIngredientes = Ingredientes.objects.filter(receita=receita)
    preparacaoPassos = re.split(re.compile('[0-9]\. '), receita.preparacao)

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
        'likeclass': likeclass
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
    tags = Tags.objects.all()
    if request.method == 'POST':
        print(request.POST)
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
        'tags': tags
    }
    return render(request, 'testForm.html', tparams)


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






