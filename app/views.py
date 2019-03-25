from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from app.forms import *
from app.models import *

from datetime import datetime


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
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


def receita(request):
    assert isinstance(request, HttpRequest)

    return render(request, 'receita.html')


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


def adicionarReceita(request):
    if request.method == 'POST':
        formReceitaset = AdicionarReceitaSet(request.POST)
        if formReceitaset.is_valid():
            for formReceita in formReceitaset:
                nome = formReceita.cleaned_data.get('nome')
                print(nome)
                descricao = formReceita.cleaned_data.get('descricao')
                preparacao = formReceita.cleaned_data.get('preparacao')
                tipo = formReceita.cleaned_data.get('tipo')
                dificuldade = formReceita.cleaned_data.get('dificuldade')
                tempo = formReceita.cleaned_data.get('tempo')
                dose = formReceita.cleaned_data.get('dose')
                nomeIngr = formReceita.cleaned_data.get('nomeIngr')
                print(nomeIngr)
                r = Receita(nome=nome, descricao=descricao, preparacao=preparacao, tipo=tipo, tempo=tempo, dificuldade=dificuldade, dose=dose, utilizador='', imagem='', data=datetime.now().strftime('%Y-%m-%d'))
                #r.save()
                #idReceita = r.id
            return HttpResponse('ERROR')
        else:
            return HttpResponse('ERROR: author can\'t be added')
    else:
        formReceitaset = AdicionarReceitaSet()
    return render(request, 'criarReceita.html', {'formset': formReceitaset})


'''def adicionarIngredientesReceita(request):
    if request.method == 'POST':
        formset = AdicionarIngredientesSet(request.POST)
        if formset.is_valid():
            for form in formset:
                nome = form.cleaned_data.get('nome')
                quantidade = form.cleaned_data.get('quantidade')
            return HttpResponse()
        else:
            return HttpResponse('ERROR: author be added')
    else:
        formset = AdicionarIngredientesSet()
    return render(request, 'adicionarIngrediente.html', {'formset': formset})'''
