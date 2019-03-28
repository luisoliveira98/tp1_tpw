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

    listaReceitas = Receita.objects.all()

    tparams = {
        'listaReceitas': listaReceitas,
    }
    return render(request, 'index.html', tparams)


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'contact.html', tparams)


def about(request):
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'about.html', tparams)


def receita(request, id):
    assert isinstance(request, HttpRequest)

    receita = Receita.objects.get(id=id)
    listIngredientes = Ingredientes.objects.filter(receita=receita)
    preparacaoPassos = re.split(re.compile('[0-9]\. '), receita.preparacao)

    saved = ReceitasGuardadas.objects.filter(receita=receita)

    if not saved:
        booksave = "far fa-bookmark"
    else:
        booksave = "fas fa-bookmark"

    if request.method == 'POST':
        if saved:
            print("entrei if")
            ReceitasGuardadas.objects.get(receita=receita).delete()
            booksave = "far fa-bookmark"
        else:
            print("entrei else")
            new = ReceitasGuardadas(receita=receita, utilizador=request.user)
            new.save()
            booksave = "fas fa-bookmark"

    tparams = {
        'nome': receita.nome,
        'descricao': receita.descricao,
        'imagem': '/media/'+str(receita.imagem),
        'duracao': receita.tempo,
        'dificuldade': receita.dificuldade,
        'dose': receita.dose,
        'listIngredientes': listIngredientes,
        'preparacao': preparacaoPassos[1:],
        'booksaveclass': booksave,
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


'''def criar_receita(request, numero):
    print(numero)
    if request.method == 'POST':
        print('aqui!')
        form = AddReceita(request.POST, request.FILES,  n=numero)
        print(form.is_valid())
        if form.is_valid():
            print('aqui')
            nome = form.cleaned_data.get('nome')
            descricao = form.cleaned_data.get('descricao')
            passos = form.cleaned_data.get('preparacao')
            tipo = form.cleaned_data.get('tipo')
            dificuldade = form.cleaned_data.get('dificuldade')
            tempo = form.cleaned_data.get('tempo')
            dose = form.cleaned_data.get('dose')
            imagem = form.cleaned_data.get('imagem')

            receita = Receita(nome=nome, descricao=descricao, dificuldade=dificuldade, preparacao=passos, tipo=tipo, tempo=tempo, dose=dose, imagem=imagem, data=datetime.now().strftime('%Y-%m-%d'), utilizador='luis', classificacao=0)
            receita.save()
            lst_ingredientes = []
            lst_quantidades = []
            for (value, ingrediente) in form.nome_ingredientes():
                lst_ingredientes.append(ingrediente)
            for (value, quantidade) in form.quat_ingredientes():
                lst_quantidades.append(quantidade)

            for i in range(len(lst_quantidades)):
                ing = Ingredientes(receita=receita, ingredienteName=lst_ingredientes[i], ingredienteQuant=lst_quantidades[i])
                ing.save()
            return HttpResponse('Success')
    else:
        form = AddReceita(n=numero)
    return render(request, 'criarReceita.html', {'form': form, 'range': range(numero)})


def numero_ingredientes(request):
    print('aqui')
    if request.method == 'POST':
        form = Numero_ingredientes(request.POST)
        if form.is_valid():
            numero = form.cleaned_data.get('numero')
            return redirect('criarReceita', numero=numero)
    else:
        form = Numero_ingredientes()
    return render(request, 'numeroIngredientes.html', {'form': form})'''

def criar_receita(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        passos = request.POST['passos']
        tipo = request.POST['tipoReceita']
        dificuldade = request.POST['dificuldade']
        tempo = request.POST['tempo']
        dose = request.POST['dose']
        imagem = request.FILES['imagem']
        receita = Receita(nome=nome, descricao=descricao, dificuldade=dificuldade, preparacao=passos, tipo=tipo, tempo=tempo, dose=dose, imagem=imagem, data=datetime.now().strftime('%Y-%m-%d'), utilizador='luis', classificacao=0)
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
        return redirect('home')

    return render(request, 'testForm.html')


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






