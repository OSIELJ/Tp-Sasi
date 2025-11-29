"""
Views relacionadas à segurança: recuperação de senha, etc.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import secrets
import logging
from datetime import datetime
from .models import Cliente, Auditoria
from .utils import get_client_ip, limpar_cpf, validar_cpf

DEBUG = settings.DEBUG

logger = logging.getLogger('security')


def recuperar_senha(request):
    """View para solicitar recuperação de senha."""
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        
        cpf_limpo = limpar_cpf(cpf)
        
        if not cpf_limpo or not validar_cpf(cpf_limpo):
            messages.error(request, 'CPF inválido.')
            return render(request, 'core/recuperar_senha.html')
        
        try:
            cliente = Cliente.objects.get(cpf=cpf_limpo, email=email)
            
            # Gera token de recuperação
            token = secrets.token_urlsafe(32)
            
            # Armazena token na sessão (em produção, usar banco de dados ou cache)
            request.session[f'recuperacao_token_{cliente.id}'] = token
            request.session[f'recuperacao_timestamp_{cliente.id}'] = timezone.now().isoformat()
            request.session.set_expiry(3600)  # Token válido por 1 hora
            
            # Em produção, enviar e-mail com link de recuperação
            # Por enquanto, apenas mostra o token (não recomendado para produção)
            if DEBUG:
                messages.info(request, f'Token de recuperação (apenas para desenvolvimento): {token}')
                messages.warning(request, 'Em produção, este token seria enviado por e-mail.')
            
            # Registra auditoria
            Auditoria.objects.create(
                tipo_acao='alteracao_dados',
                usuario=cliente.nome,
                cpf_usuario=cliente.cpf,
                ip_address=get_client_ip(request),
                descricao='Solicitação de recuperação de senha'
            )
            
            logger.info(f'Solicitação de recuperação de senha - CPF: {cpf_limpo} - IP: {get_client_ip(request)}')
            
            return redirect('redefinir_senha', cliente_id=cliente.id)
            
        except Cliente.DoesNotExist:
            # Por segurança, não revela se o CPF ou e-mail existe
            messages.error(request, 'Se o CPF e e-mail estiverem corretos, você receberá instruções.')
            logger.warning(f'Tentativa de recuperação de senha com CPF/e-mail inválido - IP: {get_client_ip(request)}')
    
    return render(request, 'core/recuperar_senha.html')


def redefinir_senha(request, cliente_id):
    """View para redefinir senha com token."""
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        
        # Verifica se há token válido na sessão
        token = request.session.get(f'recuperacao_token_{cliente.id}')
        timestamp_str = request.session.get(f'recuperacao_timestamp_{cliente.id}')
        
        if not token or not timestamp_str:
            messages.error(request, 'Token de recuperação inválido ou expirado.')
            return redirect('recuperar_senha')
        
        # Verifica se o token não expirou (1 hora)
        timestamp = timezone.datetime.fromisoformat(timestamp_str)
        if (timezone.now() - timestamp).total_seconds() > 3600:
            messages.error(request, 'Token de recuperação expirado. Solicite novamente.')
            del request.session[f'recuperacao_token_{cliente.id}']
            del request.session[f'recuperacao_timestamp_{cliente.id}']
            return redirect('recuperar_senha')
        
        if request.method == 'POST':
            token_inserido = request.POST.get('token')
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')
            
            # Verifica token
            if token_inserido != token:
                messages.error(request, 'Token inválido.')
                return render(request, 'core/redefinir_senha.html', {'cliente': cliente})
            
            # Valida senhas
            if not nova_senha or len(nova_senha) < 6:
                messages.error(request, 'A senha deve ter no mínimo 6 caracteres.')
                return render(request, 'core/redefinir_senha.html', {'cliente': cliente})
            
            if nova_senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem.')
                return render(request, 'core/redefinir_senha.html', {'cliente': cliente})
            
            # Atualiza senha
            cliente.senha = make_password(nova_senha)
            cliente.tentativas_login_falhas = 0  # Reset contador
            cliente.bloqueado = False  # Desbloqueia conta se estiver bloqueada
            cliente.save()
            
            # Remove token da sessão
            del request.session[f'recuperacao_token_{cliente.id}']
            del request.session[f'recuperacao_timestamp_{cliente.id}']
            
            # Registra auditoria
            Auditoria.objects.create(
                tipo_acao='alteracao_dados',
                usuario=cliente.nome,
                cpf_usuario=cliente.cpf,
                ip_address=get_client_ip(request),
                descricao='Senha redefinida via recuperação'
            )
            
            logger.info(f'Senha redefinida com sucesso - CPF: {cliente.cpf} - IP: {get_client_ip(request)}')
            messages.success(request, 'Senha redefinida com sucesso! Você já pode fazer login.')
            return redirect('login')
        
        return render(request, 'core/redefinir_senha.html', {'cliente': cliente})
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('recuperar_senha')

