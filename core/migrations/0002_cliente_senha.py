# Generated manually

from django.db import migrations, models
from django.contrib.auth.hashers import make_password


def set_default_passwords(apps, schema_editor):
    """Define senhas padrão para clientes existentes."""
    Cliente = apps.get_model('core', 'Cliente')
    # Define uma senha padrão temporária para clientes existentes
    # Os clientes precisarão redefinir a senha
    default_password = make_password('temp123456')
    for cliente in Cliente.objects.all():
        if not cliente.senha:
            cliente.senha = default_password
            cliente.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='senha',
            field=models.CharField(max_length=128, null=True, blank=True, verbose_name='Senha'),
        ),
        migrations.RunPython(set_default_passwords),
        migrations.AlterField(
            model_name='cliente',
            name='senha',
            field=models.CharField(max_length=128, verbose_name='Senha'),
        ),
    ]

