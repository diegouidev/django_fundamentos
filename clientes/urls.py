from django.urls import path
from .views import *

urlpatterns = [
    path('listar', listar_clientes, name='listar_clientes'),
    path('relatorio-clientes/', gerar_relatorio_clientes_pdf, name='relatorio_clientes_pdf'),
    path('cadastrar/', inserir_clientes, name='cadastrar_clientes'),
    path('listar/<int:id>/', listar_cliente_id, name='listar_cliente_id'),
    path('editar/<int:id>/', editar_cliente, name='editar_cliente'),
    path('remover/<int:id>/', remover_cliente, name='remover_cliente'),
]
