from django.contrib import admin
from app.models import *


# Register your models here.
admin.site.register(Receita)
admin.site.register(Ingredientes)
admin.site.register(Tags)
admin.site.register(Comentario)
admin.site.register(ReceitasGuardadas)