from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.add_agendamento, name='add_agendamento'),
    path('editar/<int:pk>/', views.edit_agendamento, name='edit_agendamento'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/dados/', views.dados_relatorio, name='dados_relatorio'),
    path('relatorios/faturamento/', views.dados_relatorio_faturamento, name='dados_relatorio_faturamento'),
    path('relatorios/servicos/', views.dados_relatorio_servicos, name='dados_relatorio_servicos'),
    path('relatorios/profissionais/', views.dados_relatorio_profissionais, name='dados_relatorio_profissionais'),
    path('relatorios/status/', views.dados_relatorio_status, name='dados_relatorio_status'),
    path('relatorios/clientes/', views.dados_relatorio_clientes, name='dados_relatorio_clientes'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/editar/<int:pk>/', views.edit_usuario, name='edit_usuario'),
    path('register/', views.register, name='register'),

    # Cliente CRUD
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.cliente_update, name='cliente_update'),
    path('clientes/excluir/<int:pk>/', views.cliente_delete, name='cliente_delete'),

    # Servico CRUD
    path('servicos/', views.servico_list, name='servico_list'),
    path('servicos/novo/', views.servico_create, name='servico_create'),
    path('servicos/editar/<int:pk>/', views.servico_update, name='servico_update'),
    path('servicos/excluir/<int:pk>/', views.servico_delete, name='servico_delete'),

    # Profissional CRUD
    path('profissionais/', views.profissional_list, name='profissional_list'),
    path('profissionais/novo/', views.profissional_create, name='profissional_create'),
    path('profissionais/editar/<int:pk>/', views.profissional_update, name='profissional_update'),
    path('profissionais/excluir/<int:pk>/', views.profissional_delete, name='profissional_delete'),
]
