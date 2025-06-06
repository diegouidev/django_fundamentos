from django.shortcuts import render
from .models import Cliente
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from datetime import datetime
from .forms import ClienteForm
from .entidades import cliente
from .services import cliente_service

# Create your views here.

def listar_clientes(request):
    clientes = cliente_service.listar_clientes()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})

def inserir_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sexo = form.cleaned_data['sexo']
            data_nascimento = form.cleaned_data['data_nascimento']
            email = form.cleaned_data['email']
            profissao = form.cleaned_data['profissao']
            cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)

            cliente_service.cadastrar_cliente(cliente_novo)
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form})

def listar_cliente_id(request, id):
    cliente = cliente_service.listar_cliente_id(id)
    return render(request, 'clientes/lista_cliente.html', {'cliente': cliente})

def editar_cliente(request, id):
    cliente_antigo = cliente_service.listar_cliente_id(id)
    form = ClienteForm(request.POST or None, instance=cliente_antigo)
    if form.is_valid():
        nome = form.cleaned_data['nome']
        sexo = form.cleaned_data['sexo']
        data_nascimento = form.cleaned_data['data_nascimento']
        email = form.cleaned_data['email']
        profissao = form.cleaned_data['profissao']
        cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)
        
        cliente_service.editar_cliente(cliente_antigo, cliente_novo)
        return redirect('listar_clientes')
    return render(request, 'clientes/form_cliente.html', {'form': form})

def remover_cliente(request, id):
    cliente = cliente_service.listar_cliente_id(id)
    if request.method == 'POST':
        cliente_service.remover_cliente(cliente)
        return redirect('listar_clientes')
    return render(request, 'clientes/confirma_exclusao.html', {'cliente': cliente})



def gerar_relatorio_clientes_pdf(request):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    clientes = Cliente.objects.all()

    html_string = render_to_string('clientes/relatorio_clientes.html', {
        'clientes': clientes,
        'data': data_atual,
    })

    # Gera o PDF em memória
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_clientes.pdf"'
    return response
