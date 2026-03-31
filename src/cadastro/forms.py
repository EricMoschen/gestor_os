from django import forms
from .models import CentroCusto, Intervencao, Colaborador


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['descricao', 'cod_tag', 'tag_pai', 'cod_do_ativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tag_pai"].queryset = CentroCusto.objects.filter(tag_pai__isnull=True)

        if self.instance and self.instance.pk:
            self.fields["tag_pai"].queryset = self.fields["tag_pai"].queryset.exclude(pk=self.instance.pk)

        self.fields["descricao"].label = "Descrição"
        self.fields["cod_tag"].label = "Código Tag"
        self.fields["tag_pai"].label = "Tag Pai"
        self.fields["cod_do_ativo"].label = "Código do Ativo"
        self.fields["tag_pai"].required = False
        self.fields["cod_tag"].required = False
        self.fields["cod_do_ativo"].required = False

    def clean(self):
        cleaned_data = super().clean()
        tag_pai = cleaned_data.get("tag_pai")
        descricao = cleaned_data.get("descricao")
        cod_tag = cleaned_data.get("cod_tag")
        cod_do_ativo = cleaned_data.get("cod_do_ativo")

        if not descricao:
            self.add_error("descricao", "A descrição é obrigatória.")

        # Nó filho: obrigatoriamente deve ter pai, descrição, cod_tag e cod_do_ativo.
        # Nó raiz (sem pai): descrição obrigatória e códigos opcionais.
        if tag_pai:
            if not cod_tag:
                self.add_error("cod_tag", "Código Tag é obrigatório para tags filhas.")
            if not cod_do_ativo:
                self.add_error("cod_do_ativo", "Código do Ativo é obrigatório para tags filhas.")

        return cleaned_data



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
           "matricula",
            "nome",
            "funcao",
            "turno",
            "ativo",
            "hr_entrada_am",
            "hr_saida_am",
            "hr_entrada_pm",
            "hr_saida_pm",
        ]
        widgets = {
            "matricula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 1234"}),
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo do colaborador"}),
            "funcao": forms.Select(attrs={"class": "form-control"}),
            "turno": forms.Select(attrs={"class": "form-select", "id": "id_turno"}),
            "ativo": forms.Select(choices=[(True, "Ativo"), (False, "Desligado")], attrs={"class": "form-select"}),
            "hr_entrada_am": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "hr_saida_am": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "hr_entrada_pm": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "hr_saida_pm": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        turno = cleaned_data.get("turno")

        if turno == "OUTROS":
            required_fields = ["hr_entrada_am", "hr_saida_am", "hr_entrada_pm", "hr_saida_pm"]

            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "Campo obrigatório para o turno OUTROS.")
        return cleaned_data
    