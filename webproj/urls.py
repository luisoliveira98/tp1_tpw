"""
webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from app.models import *

from app import views


urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('receita/<int:id>/', views.receita, name='receita'),
    path('criarReceita/', views.criar_receita, name='criarReceita'),
    path('tipoReceita/<str:tipo>/', views.receita_tipo, name='tipoReceita'),
    path('receitaTag/<str:tag>/', views.receita_tag, name='receitaTag'),
    path('pesquisa', views.pesquisa, name='pesquisa'),
    path('apagarReceita/<int:id>', views.apagar_receita, name='apagarReceita'),
    path('comentario/<int:id>', views.comentar_receita, name='comentario'),
    path('updateReceita/<int:id>', views.update_receita, name='updateReceita'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
