from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Agendamento
from .forms import AgendamentoForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
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

    return render(request, 'add_agendamento.html', {'form': form})


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

    return render(request, 'edit_agendamento.html', {'form': form})


@login_required
def relatorios(request):
    return render(request, 'relatorios.html')


@login_required
def dados_relatorio(request):
    agendamentos = Agendamento.objects.filter(status='CONCLUIDO')

    total = agendamentos.count()

    por_dia = (
        agendamentos
        .annotate(dia=TruncDay('data_hora'))
        .values('dia')
        .annotate(total=Count('id'))
    )

    return JsonResponse({
        'total': total,
        'por_dia': {
            str(item['dia'].date()): item['total']
            for item in por_dia
        }
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

    return render(request, 'edit_usuario.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})