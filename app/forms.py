from django import forms


class AdicionarReceita(forms.Form):
    nome = forms.CharField(label="Nome:", max_length=70)
    descricao = forms.CharField(label="Descrição:", max_length=500, widget=forms.Textarea)
    preparacao = forms.CharField(label="Passos de preparação:", max_length=3000, widget=forms.Textarea)
    tempo = forms.IntegerField(label="Tempo estimado:", widget=forms.NumberInput)
    CHOICES = [
        ('muitoFacil', 'Muito Fácil'),
        ('facil', 'Fácil')
    ]
    dificuldade = forms.ChoiceField(label="Dificuldade:", choices=CHOICES, widget=forms.RadioSelect)
    dose = forms.IntegerField(label="Dose:",  widget=forms.NumberInput)
