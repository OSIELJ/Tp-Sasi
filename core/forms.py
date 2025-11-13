"""
Forms para o app core.
"""
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import Cliente, Imovel


class ClienteForm(forms.ModelForm):
    """Formulário para cadastro de cliente."""
    
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'id': 'cpf',
            'maxlength': '14'
        }),
        label='CPF'
    )
    
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        }),
        label='Senha',
        min_length=6,
        help_text='Mínimo de 6 caracteres'
    )
    
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        }),
        label='Confirmar Senha',
        min_length=6
    )
    
    telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: (38) 99999-9999'
        })
    )
    
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'cpf', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações adicionais (opcional)'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'cpf': 'CPF',
            'observacoes': 'Observações',
        }
    
    def clean_cpf(self):
        """Remove formatação do CPF e valida."""
        cpf = self.cleaned_data.get('cpf')
        # Remove pontos e hífen
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            raise forms.ValidationError("CPF deve conter exatamente 11 dígitos.")
        
        return cpf_limpo
    
    def clean_confirmar_senha(self):
        """Valida se as senhas coincidem."""
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        
        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return confirmar_senha
    
    def save(self, commit=True):
        """Salva o cliente com senha hash."""
        cliente = super(ClienteForm, self).save(commit=False)
        senha = self.cleaned_data.get('senha')
        if senha:
            # Define a senha usando hash
            cliente.senha = make_password(senha)
        if commit:
            cliente.save()
        return cliente


class ImovelForm(forms.ModelForm):
    """Formulário para cadastro de imóvel."""
    
    class Meta:
        model = Imovel
        fields = ['titulo', 'tipo', 'preco', 'endereco', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Casa 3 quartos com piscina'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, número, bairro, cidade'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Descreva o imóvel em detalhes...'
            }),
        }
        labels = {
            'titulo': 'Título',
            'tipo': 'Tipo',
            'preco': 'Preço (R$)',
            'endereco': 'Endereço',
            'descricao': 'Descrição',
        }

