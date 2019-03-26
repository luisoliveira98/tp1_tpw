from django import forms

class AddReceita(forms.Form):
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
    dose = forms.FloatField(min_value=0, label="Dose:", widget=forms.NumberInput)
    #imagem = forms.ImageField(label='Imagem')

    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n')

        super(AddReceita, self).__init__(*args, **kwargs)
        for i in range(n):
            self.fields['x' + i.__str__()] = forms.CharField(label='Nome do ingrediente:', max_length=100)
            self.fields['y' + i.__str__()] = forms.IntegerField(label='Quantidade:', widget=forms.NumberInput(attrs={'step': '0.5'}))

    def nome_ingredientes(self):
        for nome, value in self.cleaned_data.items():
            if nome.startswith('x'):
                yield (self.fields['nome'].label, value)

    def quat_ingredientes(self):
        for nome, value in self.cleaned_data.items():
            if nome.startswith('y'):
                yield (self.fields['nome'].label, value)


class Numero_ingredientes(forms.Form):
    numero = forms.IntegerField(label='Número de ingredientes da receita:', widget=forms.NumberInput)
