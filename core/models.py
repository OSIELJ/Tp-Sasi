"""
Models para o app core.
"""
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password


class Cliente(models.Model):
    """Modelo para representar um cliente."""
    
    TIPO_CHOICES = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
        ('ambos', 'Ambos'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
            )
        ]
    )
    cpf = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='CPF',
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message="CPF deve conter exatamente 11 dígitos numéricos."
            )
        ]
    )
    senha = models.CharField(max_length=128, verbose_name='Senha')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    
    def set_password(self, raw_password):
        """Define a senha do cliente usando hash."""
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta."""
        return check_password(raw_password, self.senha)
    
    # Métodos necessários para compatibilidade com Django auth
    @property
    def is_authenticated(self):
        """Retorna True se o cliente está autenticado."""
        return True
    
    @property
    def is_anonymous(self):
        """Retorna False pois Cliente não é anônimo."""
        return False
    
    @property
    def is_active(self):
        """Retorna True se o cliente está ativo."""
        return True
    
    @property
    def is_staff(self):
        """Retorna False - clientes não são staff."""
        return False
    
    @property
    def is_superuser(self):
        """Retorna False - clientes não são superusuários."""
        return False
    
    def get_username(self):
        """Retorna o CPF como username."""
        return self.cpf
    
    USERNAME_FIELD = 'cpf'
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Imovel(models.Model):
    """Modelo para representar um imóvel."""
    
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name='Tipo'
    )
    preco = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Preço'
    )
    endereco = models.CharField(max_length=300, verbose_name='Endereço')
    descricao = models.TextField(verbose_name='Descrição')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"

