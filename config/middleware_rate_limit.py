"""
Middleware para rate limiting básico (proteção contra bots e ataques).
"""
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger('security')


class RateLimitMiddleware:
    """
    Middleware que limita o número de requisições por IP.
    """
    # Limites por tipo de rota
    LIMITS = {
        'login': {'requests': 10, 'window': 300},  # 10 requisições em 5 minutos
        'cadastro': {'requests': 5, 'window': 3600},  # 5 requisições em 1 hora
        'recuperar_senha': {'requests': 3, 'window': 3600},  # 3 requisições em 1 hora
    }
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Identifica o tipo de rota
        route_type = self._identify_route(request.path)
        
        if route_type and route_type in self.LIMITS:
            ip_address = self._get_client_ip(request)
            limit_config = self.LIMITS[route_type]
            
            # Verifica rate limit
            if self._is_rate_limited(ip_address, route_type, limit_config):
                logger.warning(f'Rate limit excedido - IP: {ip_address} - Rota: {request.path}')
                return HttpResponseForbidden(
                    'Muitas requisições. Por favor, aguarde alguns minutos antes de tentar novamente.'
                )
        
        response = self.get_response(request)
        return response
    
    def _identify_route(self, path):
        """Identifica o tipo de rota baseado no caminho."""
        if '/login' in path:
            return 'login'
        elif '/cadastro' in path:
            return 'cadastro'
        elif '/recuperar-senha' in path:
            return 'recuperar_senha'
        return None
    
    def _get_client_ip(self, request):
        """Obtém o endereço IP do cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _is_rate_limited(self, ip_address, route_type, limit_config):
        """Verifica se o IP excedeu o limite de requisições."""
        cache_key = f'rate_limit_{route_type}_{ip_address}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= limit_config['requests']:
            return True
        
        # Incrementa contador
        cache.set(cache_key, request_count + 1, limit_config['window'])
        return False


