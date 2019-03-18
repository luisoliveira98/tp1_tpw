from django.db import models


class Receita(models.Model):
    nome = models.CharField(max_length=70)
    descricao = models.CharField(max_length=500)
    preparacao = models.CharField(max_length=3000)
    tempo = models.IntegerField()
    dificuldade = models.CharField(max_length=10)
    dose = models.IntegerField()
    imagem = models.CharField(max_length=50)
    data = models.DateField()
    utilizador = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Ingredientes(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingredienteName = models.CharField(max_length=100)
    ingredienteQuant = models.FloatField()

    def __str__(self):
        return self.ingredienteName + self.ingredienteQuant


class Tags(models.Model):
    nome = models.CharField(max_length=50)
    receitas = models.ManyToManyField(Receita)

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=200)
    data = models.DateTimeField()
    utilizador = models.CharField(max_length=100)

    def __str__(self):
        return self.comentario
