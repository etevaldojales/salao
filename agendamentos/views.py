from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Agendamento, Cliente, Servico, Profissional
from .forms import AgendamentoForm, ClienteForm, ServicoForm, ProfissionalForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django import forms


@login_required
def index(request):
    agendamentos = Agendamento.objects.select_related(
        'cliente', 'servico', 'profissional'
    ).all().order_by('-data_hora')

    return render(request, 'index.html', {'agendamentos': agendamentos})


@login_required
def add_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AgendamentoForm()

    return render(request, 'add_agendamentos.html', {'form': form})


@login_required
def edit_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, 'edit_agendamentos.html', {'form': form})


@login_required
def relatorios(request):
    return render(request, 'relatorios.html')


def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None


@login_required
def dados_relatorio(request):
    """Basic report - completed appointments by day"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO')
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    total = agendamentos.count()

    por_dia = (
        agendamentos
        .annotate(dia=TruncDay('data_hora'))
        .values('dia')
        .annotate(total=Count('id'))
        .order_by('dia')
    )

    return JsonResponse({
        'total': total,
        'por_dia': {
            str(item['dia'].date()): item['total']
            for item in por_dia
        }
    })


@login_required
def dados_relatorio_faturamento(request):
    """Revenue report by day/month"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    periodo = request.GET.get('periodo', 'dia')  # 'dia' or 'mes'
    
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    total_faturamento = agendamentos.aggregate(
        total=Sum('servico__preco')
    )['total'] or 0
    
    if periodo == 'mes':
        por_periodo = (
            agendamentos
            .annotate(periodo=TruncMonth('data_hora'))
            .values('periodo')
            .annotate(total=Sum('servico__preco'))
            .annotate(quantidade=Count('id'))
            .order_by('periodo')
        )
        dados = {
            str(item['periodo'].date()): {
                'total': float(item['total'] or 0),
                'quantidade': item['quantidade']
            }
            for item in por_periodo
        }
    else:
        por_periodo = (
            agendamentos
            .annotate(periodo=TruncDay('data_hora'))
            .values('periodo')
            .annotate(total=Sum('servico__preco'))
            .annotate(quantidade=Count('id'))
            .order_by('periodo')
        )
        dados = {
            str(item['periodo'].date()): {
                'total': float(item['total'] or 0),
                'quantidade': item['quantidade']
            }
            for item in por_periodo
        }

    return JsonResponse({
        'total_faturamento': float(total_faturamento),
        'por_periodo': dados
    })


@login_required
def dados_relatorio_servicos(request):
    """Most popular services report"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    por_servico = (
        agendamentos
        .values('servico__nome', 'servico__preco')
        .annotate(
            quantidade=Count('id'),
            total_faturado=Sum('servico__preco')
        )
        .order_by('-quantidade')
    )

    return JsonResponse({
        'servicos': [
            {
                'nome': item['servico__nome'],
                'preco': float(item['servico__preco']),
                'quantidade': item['quantidade'],
                'total_faturado': float(item['total_faturado'] or 0)
            }
            for item in por_servico
        ]
    })


@login_required
def dados_relatorio_profissionais(request):
    """Professionals performance report"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('profissional', 'servico')
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    por_profissional = (
        agendamentos
        .values('profissional__nome', 'profissional__especialidade')
        .annotate(
            quantidade=Count('id'),
            total_faturado=Sum('servico__preco')
        )
        .order_by('-quantidade')
    )

    return JsonResponse({
        'profissionais': [
            {
                'nome': item['profissional__nome'],
                'especialidade': item['profissional__especialidade'],
                'quantidade': item['quantidade'],
                'total_faturado': float(item['total_faturado'] or 0)
            }
            for item in por_profissional
        ]
    })


@login_required
def dados_relatorio_status(request):
    """Appointments by status report"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    agendamentos = Agendamento.objects.all()
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    por_status = (
        agendamentos
        .values('status')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return JsonResponse({
        'status': [
            {
                'status': item['status'],
                'total': item['total']
            }
            for item in por_status
        ],
        'total_geral': agendamentos.count()
    })


@login_required
def dados_relatorio_clientes(request):
    """Top clients report"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('cliente', 'servico')
    
    if data_inicio:
        data_inicio_dt = parse_date(data_inicio)
        if data_inicio_dt:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_dt)
    
    if data_fim:
        data_fim_dt = parse_date(data_fim)
        if data_fim_dt:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_dt)
    
    por_cliente = (
        agendamentos
        .values('cliente__nome', 'cliente__telefone')
        .annotate(
            quantidade=Count('id'),
            total_gasto=Sum('servico__preco')
        )
        .order_by('-total_gasto')[:10]  # Top 10 clients
    )

    return JsonResponse({
        'clientes': [
            {
                'nome': item['cliente__nome'],
                'telefone': item['cliente__telefone'],
                'quantidade': item['quantidade'],
                'total_gasto': float(item['total_gasto'] or 0)
            }
            for item in por_cliente
        ]
    })


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})


@user_passes_test(is_admin)
def edit_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    class EditUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'is_staff']

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = EditUserForm(instance=usuario)

    return render(request, 'edit_usuarios.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form, 'cliente': cliente})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})

@login_required
def servico_list(request):
    servicos = Servico.objects.all()
    return render(request, 'servico_list.html', {'servicos': servicos})

@login_required
def servico_create(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servico_list')
    else:
        form = ServicoForm()
    return render(request, 'servico_form.html', {'form': form})

@login_required
def servico_update(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('servico_list')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'servico_form.html', {'form': form, 'servico': servico})

@login_required
def servico_delete(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        return redirect('servico_list')
    return render(request, 'servico_confirm_delete.html', {'servico': servico})

# Profissional CRUD
@login_required
def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'profissional_list.html', {'profissionais': profissionais})

@login_required
def profissional_create(request):
    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profissional_list')
    else:
        form = ProfissionalForm()
    return render(request, 'profissional_form.html', {'form': form})

@login_required
def profissional_update(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    if request.method == 'POST':
        form = ProfissionalForm(request.POST, instance=profissional)
        if form.is_valid():
            form.save()
            return redirect('profissional_list')
    else:
        form = ProfissionalForm(instance=profissional)
    return render(request, 'profissional_form.html', {'form': form, 'profissional': profissional})

@login_required
def profissional_delete(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    if request.method == 'POST':
        profissional.delete()
        return redirect('profissional_list')
    return render(request, 'profissional_confirm_delete.html', {'profissional': profissional})
