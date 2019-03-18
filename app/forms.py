from django import forms


class AdicionarReceita(forms.Form):
    nome = forms.CharField(label="Nome:", max_length=70)
    descricao = forms.CharField(label="Descrição:", max_length=500, widget=forms.Textarea)
    preparacao =