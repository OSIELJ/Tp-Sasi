"""
URLs para o app core.
"""
from django.urls import path
from . import views
from . import views_seguranca

# URLs públicas (HTTP:8080)
urlpatterns_publicas = [
    path('', views.home, name='home'),
    path('imoveis/', views.lista_imoveis, name='lista_imoveis'),
    path('contato/', views.contato, name='contato'),
]

# URLs sensíveis (HTTPS:8443)
urlpatterns_seguras = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastroCliente/', views.CadastroClienteView.as_view(), name='cadastro_cliente'),
    path('cadastroImovel/', views.CadastroImovelView.as_view(), name='cadastro_imovel'),
    path('recuperar-senha/', views_seguranca.recuperar_senha, name='recuperar_senha'),
    path('redefinir-senha/<int:cliente_id>/', views_seguranca.redefinir_senha, name='redefinir_senha'),
]

# Combina todas as URLs
urlpatterns = urlpatterns_publicas + urlpatterns_seguras

