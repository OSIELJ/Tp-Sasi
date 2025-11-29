"""
Views para o app core.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import logging
from .models import Imovel, Cliente, LoginAttempt, Auditoria
from .forms import ClienteForm, ImovelForm
from .utils import validar_cpf, get_client_ip, limpar_cpf

# Configurar logger de segurança
logger = logging.getLogger('security')


def home(request):
    """Página inicial pública."""
    return render(request, 'core/home.html')


def dashboard(request):
    """Dashboard do cliente (rota sensível - HTTPS)."""
    if 'cliente_id' not in request.session:
        messages.error(request, 'Você precisa estar logado para acessar o dashboard.')
        return redirect('login')
    
    try:
        cliente_id = request.session.get('cliente_id')
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        request.session.flush()
        return redirect('login')
    
    # Estatísticas
    total_imoveis = Imovel.objects.count()
    imoveis_ativos = Imovel.objects.filter(ativo=True).count()
    total_clientes = Cliente.objects.count()
    
    # Imóveis recentes
    imoveis_recentes = Imovel.objects.filter(ativo=True).order_by('-data_cadastro')[:5]
    
    # Clientes recentes
    clientes_recentes = Cliente.objects.all().order_by('-data_cadastro')[:5]
    
    context = {
        'cliente': cliente,
        'total_imoveis': total_imoveis,
        'imoveis_ativos': imoveis_ativos,
        'total_clientes': total_clientes,
        'imoveis_recentes': imoveis_recentes,
        'clientes_recentes': clientes_recentes,
    }
    
    return render(request, 'core/dashboard.html', context)


def lista_imoveis(request):
    """Listagem pública de imóveis."""
    imoveis = Imovel.objects.filter(ativo=True).order_by('-data_cadastro')
    context = {
        'imoveis': imoveis
    }
    return render(request, 'core/imoveis_list.html', context)


def contato(request):
    """Página de contato pública."""
    return render(request, 'core/contato.html')


def login_view(request):
    """View de login (rota sensível - HTTPS) com proteção contra força bruta."""
    MAX_TENTATIVAS = 5  # Máximo de tentativas antes de bloquear
    TEMPO_BLOQUEIO = 30  # Minutos de bloqueio após exceder tentativas
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')
        
        # Remove formatação do CPF
        cpf_limpo = limpar_cpf(cpf)
        
        if not cpf_limpo:
            messages.error(request, 'CPF inválido.')
            LoginAttempt.objects.create(
                cpf='',
                ip_address=ip_address,
                user_agent=user_agent,
                sucesso=False,
                motivo_falha='CPF vazio ou inválido'
            )
            logger.warning(f'Tentativa de login com CPF vazio - IP: {ip_address}')
            return render(request, 'core/login.html')
        
        # Verifica se a conta está bloqueada
        try:
            cliente = Cliente.objects.get(cpf=cpf_limpo)
            
            # Verifica se a conta está bloqueada
            if cliente.bloqueado:
                # Verifica se já passou o tempo de bloqueio
                if cliente.ultima_tentativa_login:
                    tempo_bloqueio = timezone.now() - cliente.ultima_tentativa_login
                    if tempo_bloqueio.total_seconds() < (TEMPO_BLOQUEIO * 60):
                        minutos_restantes = int((TEMPO_BLOQUEIO * 60 - tempo_bloqueio.total_seconds()) / 60) + 1
                        messages.error(request, f'Conta temporariamente bloqueada. Tente novamente em {minutos_restantes} minuto(s).')
                        LoginAttempt.objects.create(
                            cpf=cpf_limpo,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            sucesso=False,
                            motivo_falha='Conta bloqueada'
                        )
                        logger.warning(f'Tentativa de login em conta bloqueada - CPF: {cpf_limpo} - IP: {ip_address}')
                        return render(request, 'core/login.html')
                    else:
                        # Desbloqueia a conta após o tempo de bloqueio
                        cliente.bloqueado = False
                        cliente.tentativas_login_falhas = 0
                        cliente.save()
                else:
                    messages.error(request, 'Conta bloqueada. Entre em contato com o suporte.')
                    return render(request, 'core/login.html')
            
            # Verifica tentativas recentes do mesmo IP
            tentativas_recentes = LoginAttempt.objects.filter(
                ip_address=ip_address,
                sucesso=False,
                timestamp__gte=timezone.now() - timedelta(minutes=15)
            ).count()
            
            if tentativas_recentes >= MAX_TENTATIVAS:
                messages.error(request, 'Muitas tentativas de login falhas. Tente novamente em 15 minutos.')
                LoginAttempt.objects.create(
                    cpf=cpf_limpo,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    sucesso=False,
                    motivo_falha='Muitas tentativas do IP'
                )
                logger.warning(f'Muitas tentativas de login do IP: {ip_address}')
                return render(request, 'core/login.html')
                
        except Cliente.DoesNotExist:
            pass
        
        # Tenta autenticar
        cliente = authenticate(request, cpf=cpf_limpo, password=password)
        
        if cliente is not None:
            # Login bem-sucedido
            # Reset contador de tentativas
            cliente.tentativas_login_falhas = 0
            cliente.ultima_tentativa_login = None
            cliente.save()
            
            # Registra tentativa de login bem-sucedida
            LoginAttempt.objects.create(
                cpf=cpf_limpo,
                ip_address=ip_address,
                user_agent=user_agent,
                sucesso=True
            )
            
            # Registra auditoria
            Auditoria.objects.create(
                tipo_acao='login',
                usuario=cliente.nome,
                cpf_usuario=cliente.cpf,
                ip_address=ip_address,
                descricao=f'Login realizado com sucesso'
            )
            
            # Armazena o ID do cliente na sessão
            request.session['cliente_id'] = cliente.id
            request.session['cliente_nome'] = cliente.nome
            request.session['cliente_cpf'] = cliente.cpf
            request.session.set_expiry(86400)  # Sessão expira em 24 horas
            
            logger.info(f'Login bem-sucedido - CPF: {cpf_limpo} - IP: {ip_address}')
            messages.success(request, f'Bem-vindo, {cliente.nome}!')
            return redirect('home')
        else:
            # Login falhou
            motivo = 'CPF ou senha inválidos'
            
            # Incrementa contador de tentativas falhas
            try:
                cliente = Cliente.objects.get(cpf=cpf_limpo)
                cliente.tentativas_login_falhas += 1
                cliente.ultima_tentativa_login = timezone.now()
                
                # Bloqueia conta após MAX_TENTATIVAS tentativas
                if cliente.tentativas_login_falhas >= MAX_TENTATIVAS:
                    cliente.bloqueado = True
                    motivo = 'Conta bloqueada após múltiplas tentativas falhas'
                    logger.warning(f'Conta bloqueada após {MAX_TENTATIVAS} tentativas - CPF: {cpf_limpo}')
                
                cliente.save()
            except Cliente.DoesNotExist:
                pass
            
            # Registra tentativa de login falha
            LoginAttempt.objects.create(
                cpf=cpf_limpo,
                ip_address=ip_address,
                user_agent=user_agent,
                sucesso=False,
                motivo_falha=motivo
            )
            
            logger.warning(f'Tentativa de login falha - CPF: {cpf_limpo} - IP: {ip_address}')
            
            if motivo.startswith('Conta bloqueada'):
                messages.error(request, f'Conta bloqueada após {MAX_TENTATIVAS} tentativas falhas. Tente novamente em {TEMPO_BLOQUEIO} minutos.')
            else:
                messages.error(request, 'CPF ou senha inválidos.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """View de logout (rota sensível - HTTPS)."""
    cliente_cpf = request.session.get('cliente_cpf')
    cliente_nome = request.session.get('cliente_nome')
    ip_address = get_client_ip(request)
    
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
        del request.session['cliente_nome']
        del request.session['cliente_cpf']
    logout(request)
    
    # Registra auditoria de logout
    if cliente_cpf:
        Auditoria.objects.create(
            tipo_acao='logout',
            usuario=cliente_nome,
            cpf_usuario=cliente_cpf,
            ip_address=ip_address,
            descricao='Logout realizado'
        )
        logger.info(f'Logout - CPF: {cliente_cpf} - IP: {ip_address}')
    
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')


class CadastroClienteView(CreateView):
    """View para cadastro de cliente (rota sensível - HTTPS) com auditoria."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/cadastro_cliente.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Obtém IP e informações do usuário
        ip_address = get_client_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Identifica quem está cadastrando
        cadastrado_por = 'Sistema'
        if 'cliente_id' in self.request.session:
            try:
                cliente_logado = Cliente.objects.get(id=self.request.session.get('cliente_id'))
                cadastrado_por = f"Cliente: {cliente_logado.nome} ({cliente_logado.cpf})"
            except Cliente.DoesNotExist:
                pass
        elif self.request.user.is_authenticated:
            cadastrado_por = f"Admin: {self.request.user.username}"
        
        # Salva o cliente
        cliente = form.save(commit=False)
        cliente.cadastrado_por = cadastrado_por
        cliente.ip_cadastro = ip_address
        cliente.save()
        
        # Registra auditoria
        Auditoria.objects.create(
            tipo_acao='cadastro_cliente',
            usuario=cadastrado_por,
            cpf_usuario=cliente.cpf,
            ip_address=ip_address,
            descricao=f'Cadastro de novo cliente: {cliente.nome}',
            dados_novos={
                'nome': cliente.nome,
                'email': cliente.email,
                'telefone': cliente.telefone,
                'cpf': cliente.cpf,
            }
        )
        
        logger.info(f'Novo cliente cadastrado - CPF: {cliente.cpf} - Por: {cadastrado_por} - IP: {ip_address}')
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)


class CadastroImovelView(CreateView):
    """View para cadastro de imóvel (rota sensível - HTTPS)."""
    model = Imovel
    form_class = ImovelForm
    template_name = 'core/cadastro_imovel.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Imóvel cadastrado com sucesso!')
        return super().form_valid(form)

