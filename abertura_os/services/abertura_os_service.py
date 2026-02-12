from cadastro.models import CentroCusto
from ..models import AberturaOS


class AberturaOSService:

    @staticmethod
    def criar_os(form, centro_id):
        """
        Cria uma nova Ordem de Serviço a partir do formulário.
        """
        os_obj = form.save(commit=False)
        os_obj.situacao = AberturaOS.Status.ABERTA  # Status padrão

        if not centro_id:
            raise ValueError("Selecione um centro de custo válido.")

        try:
            os_obj.centro_custo = CentroCusto.objects.get(pk=centro_id)
        except CentroCusto.DoesNotExist:
            raise ValueError("Centro de custo inválido.")

        os_obj.save()  # Aqui o número da OS será gerado automaticamente pelo model
        return os_obj

    @staticmethod
    def listar_ordens():
        """
        Retorna todas as OS ordenadas pela data de abertura.
        """
        return AberturaOS.objects.all().order_by("-data_abertura")

    @staticmethod
    def finalizar_os(os: AberturaOS):
        """
        Finaliza uma OS existente.
        """
        os.situacao = AberturaOS.Status.FINALIZADA
        os.save()
        return os
