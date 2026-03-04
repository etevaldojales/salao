from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'profissional', 'data_hora', 'status']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }