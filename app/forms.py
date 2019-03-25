from django import forms
from django.forms import formset_factory


class AdicionarReceita(forms.Form):
    TYPES = [
        ('carne', 'Carne'),
        ('peixe', 'Peixe'),
        ('sopa', 'Sopa'),
        ('sobremesas', 'Sobremesa')
    ]

    CHOICES = [
        ('muitoFacil', 'Muito Fácil'),
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
        ('muitoDificil', 'Muito Difícil')
    ]
    nome = forms.CharField(label="Nome:", max_length=70)
    descricao = forms.CharField(label="Descrição:", max_length=500, widget=forms.Textarea)
    tipo = forms.ChoiceField(label="Tipo:", choices=TYPES, widget=forms.RadioSelect)
    preparacao = forms.CharField(label="Passos de preparação:", max_length=3000, widget=forms.Textarea)
    tempo = forms.IntegerField(min_value=0, label="Tempo estimado (min.):", widget=forms.NumberInput)
    dificuldade = forms.ChoiceField(label="Dificuldade:", choices=CHOICES, widget=forms.RadioSelect)
    dose = forms.FloatField(min_value=0, label="Dose:",  widget=forms.NumberInput)
    nomeIngr = forms.CharField(label='Nome do ingrediente:', widget=forms.TextInput)
    quantidadeIngr = forms.FloatField(label='Quantidade:', widget=forms.NumberInput(attrs={'step': '0.5'}))


class AdicionarIngredientes(forms.Form):
    nome = forms.CharField(label='Nome do ingrediente:', widget=forms.TextInput)
    quantidade = forms.FloatField(label='Quantidade:', widget=forms.NumberInput(attrs={'step': '0.5'}))


AdicionarReceitaSet = formset_factory(AdicionarReceita, extra=1)
