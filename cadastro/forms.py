from django import forms
from .models import  CentroCusto, Intervencao, Colaborador


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['descricao', 'cod_tag', 'tag_pai', 'cod_do_ativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exibe apenas as Tags "pais" (aqueles que não têm pai)
        self.fields['tag_pai'].queryset = CentroCusto.objects.filter(tag_pai__isnull=True)

        if self.instance and self.instance.pk:
            self.fields['tag_pai'].queryset = self.fields['tag_pai'].queryset.exclude(pk=self.instance.pk)

        self.fields['tag_pai'].label = "Centro de Custo Pai (opcional)"
        self.fields['tag_pai'].required = False




# =====================================================
# Formulário para cadastro de Clientes
# =====================================================

class IntervencaoForm(forms.ModelForm):
    class Meta:
        model = Intervencao
        fields = '__all__'







# =====================================================
# Formulário para cadastro de colaboradores
# =====================================================

class ColaboradorForm(forms.ModelForm):
    def __init__(self, *args, include_status=False, **kwargs):
        super().__init__(*args, **kwargs)

        if not include_status:
            self.fields.pop('ativo', None)
    class Meta:
        model = Colaborador
        fields = [
            'matricula', 'nome', 'funcao', 'turno', 'ativo',
            'hr_entrada_am', 'hr_saida_am',
            'hr_entrada_pm', 'hr_saida_pm'
        ]
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1234'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do colaborador'
            }),
            'funcao': forms.Select(attrs={   
                'class': 'form-control'
            }),
            'turno': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_turno'
            }),
            'ativo': forms.Select(choices=[(True, 'Ativo'), (False, 'Desligado')], attrs={
                'class': 'form-select'
            }),
            'hr_entrada_am': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hr_saida_am': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hr_entrada_pm': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hr_saida_pm': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

    def clean(self):
        cleaned_data = super(). clean()
        turno = cleaned_data.get('turno')
        
         # Se o turno for OUTROS, exige que os horários personalizados sejam preenchidos
        if turno == 'OUTROS':
            required_fields = ['hr_entrada_am', 'hr_saida_am', 'hr_entrada_pm', 'hr_saida_pm']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'Campo obrigatório para o turno OUTROS.')
        return cleaned_data
        