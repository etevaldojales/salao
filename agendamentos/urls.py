from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.add_agendamento, name='add_agendamento'),
    path('editar/<int:pk>/', views.edit_agendamento, name='edit_agendamento'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/dados/', views.dados_relatorio, name='dados_relatorio'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/editar/<int:pk>/', views.edit_usuario, name='edit_usuario'),
    path('register/', views.register, name='register'),
]