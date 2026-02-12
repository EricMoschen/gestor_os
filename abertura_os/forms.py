from django import forms
from abertura_os.models import AberturaOS
from cadastro.models import Cliente


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
            "descricao_os": forms.Textarea(attrs={"rows": 3}),
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

        # Exemplo regra real corporativa
        if motivo and motivo.codigo == "SEM_CLIENTE" and cliente:
            raise forms.ValidationError(
                "Este motivo não permite vincular cliente."
            )

        return cleaned_data
