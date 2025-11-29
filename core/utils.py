"""
Utilitários de segurança para o app core.
"""
import re
from datetime import datetime, timedelta
from django.utils import timezone


def validar_cpf(cpf):
    """
    Valida CPF verificando os dígitos verificadores.
    Retorna True se o CPF é válido, False caso contrário.
    """
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPFs inválidos conhecidos)
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        return False
    
    return True


def get_client_ip(request):
    """Obtém o endereço IP do cliente a partir da requisição."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def limpar_cpf(cpf):
    """Remove formatação do CPF, deixando apenas números."""
    return ''.join(filter(str.isdigit, cpf)) if cpf else ''


