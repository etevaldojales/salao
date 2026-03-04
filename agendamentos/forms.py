from django import forms
from .models import Agendamento, Cliente, Servico, Profissional

class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'profissional', 'data_hora', 'status']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone']

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco', 'duracao']

class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'especialidade']
