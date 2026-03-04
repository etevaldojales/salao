from django.contrib import admin
from .models import Cliente, Servico, Profissional, Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servico', 'profissional', 'data_hora', 'status')
    list_filter = ('status', 'data_hora')
    search_fields = ('cliente__nome', 'profissional__nome')


admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(Profissional)