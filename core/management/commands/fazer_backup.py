"""
Comando Django para fazer backup do banco de dados.
Uso: python manage.py fazer_backup
"""
from django.core.management.base import BaseCommand
from core.backup import fazer_backup


class Command(BaseCommand):
    help = 'Realiza backup do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando backup do banco de dados...')
        backup_path = fazer_backup()
        
        if backup_path:
            self.stdout.write(self.style.SUCCESS(f'Backup criado com sucesso: {backup_path}'))
        else:
            self.stdout.write(self.style.ERROR('Erro ao criar backup. Verifique os logs.'))


