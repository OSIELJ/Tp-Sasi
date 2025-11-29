"""
Sistema de backup automatizado para o banco de dados.
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from django.conf import settings
import logging

logger = logging.getLogger('backup')


def fazer_backup():
    """
    Realiza backup do banco de dados SQLite.
    Retorna o caminho do arquivo de backup criado.
    """
    try:
        # Cria diretório de backups se não existir
        backup_dir = Path(settings.BASE_DIR) / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Caminho do banco de dados
        db_path = Path(settings.DATABASES['default']['NAME'])
        
        if not db_path.exists():
            logger.error(f'Banco de dados não encontrado: {db_path}')
            return None
        
        # Nome do arquivo de backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'db_backup_{timestamp}.sqlite3'
        backup_path = backup_dir / backup_filename
        
        # Copia o banco de dados
        shutil.copy2(db_path, backup_path)
        
        # Comprime o backup (opcional, mas recomendado)
        # Por enquanto, apenas copia
        
        logger.info(f'Backup criado com sucesso: {backup_path}')
        
        # Remove backups antigos (mantém apenas os últimos 30 dias)
        limpar_backups_antigos(backup_dir, dias_retencao=30)
        
        return str(backup_path)
    except Exception as e:
        logger.error(f'Erro ao criar backup: {str(e)}')
        return None


def limpar_backups_antigos(backup_dir, dias_retencao=30):
    """
    Remove backups mais antigos que o período de retenção.
    """
    try:
        agora = datetime.now()
        arquivos_removidos = 0
        
        for arquivo in backup_dir.glob('db_backup_*.sqlite3'):
            # Extrai timestamp do nome do arquivo
            try:
                timestamp_str = arquivo.stem.replace('db_backup_', '')
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                
                # Verifica se é mais antigo que o período de retenção
                if (agora - timestamp).days > dias_retencao:
                    arquivo.unlink()
                    arquivos_removidos += 1
                    logger.info(f'Backup antigo removido: {arquivo.name}')
            except (ValueError, AttributeError):
                # Se não conseguir extrair timestamp, mantém o arquivo
                pass
        
        if arquivos_removidos > 0:
            logger.info(f'{arquivos_removidos} backup(s) antigo(s) removido(s)')
            
    except Exception as e:
        logger.error(f'Erro ao limpar backups antigos: {str(e)}')


def restaurar_backup(caminho_backup):
    """
    Restaura um backup do banco de dados.
    """
    try:
        backup_path = Path(caminho_backup)
        if not backup_path.exists():
            logger.error(f'Arquivo de backup não encontrado: {caminho_backup}')
            return False
        
        # Caminho do banco de dados atual
        db_path = Path(settings.DATABASES['default']['NAME'])
        
        # Faz backup do banco atual antes de restaurar
        if db_path.exists():
            backup_antes_restauracao = Path(settings.BASE_DIR) / 'backups' / f'pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sqlite3'
            shutil.copy2(db_path, backup_antes_restauracao)
            logger.info(f'Backup de segurança criado antes da restauração: {backup_antes_restauracao}')
        
        # Restaura o backup
        shutil.copy2(backup_path, db_path)
        
        logger.info(f'Backup restaurado com sucesso de: {caminho_backup}')
        return True
        
    except Exception as e:
        logger.error(f'Erro ao restaurar backup: {str(e)}')
        return False


