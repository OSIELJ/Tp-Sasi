"""
Script para backup automatizado do banco de dados.
Pode ser executado via cron job ou agendador de tarefas.
"""
import os
import sys
import django

# Configura o Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.backup import fazer_backup

if __name__ == '__main__':
    print('Iniciando backup automatizado...')
    backup_path = fazer_backup()
    
    if backup_path:
        print(f'✓ Backup criado com sucesso: {backup_path}')
        sys.exit(0)
    else:
        print('✗ Erro ao criar backup')
        sys.exit(1)


