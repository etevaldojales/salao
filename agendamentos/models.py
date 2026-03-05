from django.db import models
from django_softdelete.models import SoftDeleteModel

class Cliente(SoftDeleteModel, models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Servico(SoftDeleteModel, models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    #duracao = models.DurationField()

    def __str__(self):
        return self.nome


class Profissional(SoftDeleteModel, models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Agendamento(SoftDeleteModel, models.Model):

    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'data_hora']),
        ]

    def __str__(self):
        return f"{self.cliente} - {self.servico}"