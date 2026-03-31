from django import forms
from django.forms import inlineformset_factory

from src.abertura_os.models import AberturaOS, FinalizacaoOS, PecaAplicada
from src.cadastro.models import Cliente


class AberturaOSForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        required=False,
        empty_label="Selecione um cliente"
    )

    class Meta:
        model = AberturaOS
        fields = (
            "descricao_os",
            "cliente",
            "motivo_intervencao",
            "ssm",
        )

        widgets = {
            "descricao_os": forms.Textarea(attrs={"rows": 2}),
        }

    # -------------------------------------------------
    # Inicialização profissional
    # -------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Queryset carregado corretamente
        self.fields["cliente"].queryset = (
            Cliente.objects
            .filter(ativo=True)
            .order_by("nome")
        )

        # Padronização visual automática
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

    # -------------------------------------------------
    # Validação campo SSM
    # -------------------------------------------------
    def clean_ssm(self):
        ssm = self.cleaned_data.get("ssm")

        if not ssm:
            raise forms.ValidationError("SSM é obrigatório.")

        if len(ssm) < 3:
            raise forms.ValidationError("SSM inválido.")

        return ssm

    # -------------------------------------------------
    # Validação global
    # -------------------------------------------------

    def clean(self):
        cleaned_data = super().clean()

        cliente = cleaned_data.get("cliente")
        motivo = cleaned_data.get("motivo_intervencao")

        if motivo and motivo.codigo == "SEM_CLIENTE" and cliente:
            raise forms.ValidationError(
                "Este motivo não permite vincular cliente."
            )

        return cleaned_data





class FinalizacaoOSForm(forms.ModelForm):
    class Meta:
        model = FinalizacaoOS
        fields = (
            "descricao_tecnica_avaria",
            "descricao_intervencao",
            "descricao_sintoma",
            "causa",
            "data_hora_inicio",
            "data_hora_fim",
            "observacoes",
        )
        widgets = {
            "descricao_tecnica_avaria": forms.Textarea(attrs={"rows": 2, "class": "input-field", "required": True}),
            "descricao_intervencao": forms.Textarea(attrs={"rows": 2, "class": "input-field", "required": True}),
            "descricao_sintoma": forms.Textarea(attrs={"rows": 2, "class": "input-field", "required": True}),
            "causa": forms.Textarea(attrs={"rows": 2, "class": "input-field", "required": True}),
            "data_hora_inicio": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "input-field", "required": True}),
            "data_hora_fim": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "input-field", "required": True}),
            "observacoes": forms.Textarea(attrs={"rows": 2, "class": "input-field"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_hora_inicio"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["data_hora_fim"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get("data_hora_inicio")
        fim = cleaned_data.get("data_hora_fim")

        if inicio and fim and fim < inicio:
            self.add_error("data_hora_fim", "A data/hora de fim deve ser maior ou igual ao início.")

        return cleaned_data


class PecaAplicadaForm(forms.ModelForm):
    class Meta:
        model = PecaAplicada
        fields = ("quantidade", "descricao")
        widgets = {
            "quantidade": forms.NumberInput(attrs={"class": "input-field", "min": 1}),
            "descricao": forms.TextInput(attrs={"class": "input-field", "maxlength": 255}),
        }


PecaAplicadaFormSet = inlineformset_factory(
    FinalizacaoOS,
    PecaAplicada,
    form=PecaAplicadaForm,
    extra=1,
    can_delete=True,
)