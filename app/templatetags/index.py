from django import template
register = template.Library()

@register.filter
def quantidade(List, i):
    return List[int(i)].ingredienteQuant

@register.filter
def nome(List, i):
    return List[int(i)].ingredienteName


@register.filter
def unidade(List, i):
    return List[int(i)].unidade