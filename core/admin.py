"""
Admin configuration for core app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Cliente, Imovel


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf_formatado', 'telefone', 'data_cadastro_formatada', 'acoes']
    search_fields = ['nome', 'email', 'cpf', 'telefone']
    list_filter = ['data_cadastro']
    readonly_fields = ['data_cadastro', 'cpf_formatado_display']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone', 'cpf')
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes', 'data_cadastro')
        }),
    )
    
    def cpf_formatado(self, obj):
        """Retorna CPF formatado."""
        cpf = obj.cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    cpf_formatado.short_description = 'CPF'
    
    def cpf_formatado_display(self, obj):
        """CPF formatado para exibição."""
        if obj.cpf:
            cpf = obj.cpf
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
        return "-"
    cpf_formatado_display.short_description = 'CPF'
    
    def data_cadastro_formatada(self, obj):
        """Retorna data formatada."""
        return obj.data_cadastro.strftime('%d/%m/%Y %H:%M')
    data_cadastro_formatada.short_description = 'Data de Cadastro'
    data_cadastro_formatada.admin_order_field = 'data_cadastro'
    
    def acoes(self, obj):
        """Botões de ação."""
        return format_html(
            '<a class="button" href="{}" style="background-color: #3498db; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Ver</a>',
            reverse('admin:core_cliente_change', args=[obj.pk])
        )
    acoes.short_description = 'Ações'


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_badge', 'preco_formatado', 'endereco', 'status_badge', 'data_cadastro_formatada', 'acoes']
    search_fields = ['titulo', 'endereco', 'descricao']
    list_filter = ['tipo', 'ativo', 'data_cadastro']
    readonly_fields = ['data_cadastro', 'preco_formatado_display']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'tipo', 'preco')
        }),
        ('Localização', {
            'fields': ('endereco',)
        }),
        ('Descrição', {
            'fields': ('descricao',)
        }),
        ('Status', {
            'fields': ('ativo', 'data_cadastro')
        }),
    )
    list_per_page = 25
    ordering = ['-data_cadastro']
    
    def tipo_badge(self, obj):
        """Retorna tipo com badge colorido."""
        if obj.tipo == 'venda':
            return format_html('<span style="background-color: #3498db; color: white; padding: 3px 10px; border-radius: 3px;">Venda</span>')
        else:
            return format_html('<span style="background-color: #27ae60; color: white; padding: 3px 10px; border-radius: 3px;">Aluguel</span>')
    tipo_badge.short_description = 'Tipo'
    
    def preco_formatado(self, obj):
        """Retorna preço formatado."""
        return f"R$ {obj.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    preco_formatado.short_description = 'Preço'
    preco_formatado.admin_order_field = 'preco'
    
    def preco_formatado_display(self, obj):
        """Preço formatado para exibição."""
        if obj.preco:
            return f"R$ {obj.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "-"
    preco_formatado_display.short_description = 'Preço'
    
    def status_badge(self, obj):
        """Retorna status com badge colorido."""
        if obj.ativo:
            return format_html('<span style="background-color: #27ae60; color: white; padding: 3px 10px; border-radius: 3px;">Ativo</span>')
        else:
            return format_html('<span style="background-color: #95a5a6; color: white; padding: 3px 10px; border-radius: 3px;">Inativo</span>')
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'ativo'
    
    def data_cadastro_formatada(self, obj):
        """Retorna data formatada."""
        return obj.data_cadastro.strftime('%d/%m/%Y %H:%M')
    data_cadastro_formatada.short_description = 'Data de Cadastro'
    data_cadastro_formatada.admin_order_field = 'data_cadastro'
    
    def acoes(self, obj):
        """Botões de ação."""
        return format_html(
            '<a class="button" href="{}" style="background-color: #3498db; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Ver</a>',
            reverse('admin:core_imovel_change', args=[obj.pk])
        )
    acoes.short_description = 'Ações'


# Customização do Admin Site
admin.site.site_header = "Imóvel Prime - Administração"
admin.site.site_title = "Imóvel Prime Admin"
admin.site.index_title = "Painel de Controle"

