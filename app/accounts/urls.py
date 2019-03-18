from django.urls import path

from app import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
