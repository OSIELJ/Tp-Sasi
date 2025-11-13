"""
Middleware para redirecionar rotas sensíveis para HTTPS.
"""
from django.http import HttpResponsePermanentRedirect


class ForceHTTPSSelective:
    """
    Middleware que redireciona apenas rotas sensíveis para HTTPS:8443
    se forem acessadas via HTTP.
    """
    
    # Rotas sensíveis que devem ser acessadas apenas via HTTPS
    SENSITIVE_PATHS = [
        '/login',
        '/cadastroCliente',
        '/cadastroImovel',
        '/admin',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verifica se a rota é sensível e se não está usando HTTPS
        if not request.is_secure():
            for sensitive_path in self.SENSITIVE_PATHS:
                if request.path.startswith(sensitive_path):
                    # Redireciona para HTTPS na porta 8443
                    host = request.get_host().split(':')[0]  # Remove porta atual
                    redirect_url = f"https://{host}:8443{request.get_full_path()}"
                    return HttpResponsePermanentRedirect(redirect_url)
        
        response = self.get_response(request)
        return response

