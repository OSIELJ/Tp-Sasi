"""
Backend de autenticação customizado para Cliente usando CPF.
"""
from django.contrib.auth.backends import BaseBackend
from .models import Cliente


class ClienteBackend(BaseBackend):
    """Backend de autenticação para Cliente usando CPF e senha."""
    
    def authenticate(self, request, cpf=None, password=None, **kwargs):
        """Autentica um cliente usando CPF e senha."""
        if cpf is None or password is None:
            return None
        
        try:
            # CPF já deve estar limpo quando chega aqui
            cliente = Cliente.objects.get(cpf=cpf)
        except Cliente.DoesNotExist:
            return None
        
        # Verifica a senha
        if cliente.check_password(password):
            return cliente
        return None
    
    def get_user(self, user_id):
        """Retorna o cliente pelo ID."""
        try:
            return Cliente.objects.get(pk=user_id)
        except Cliente.DoesNotExist:
            return None

