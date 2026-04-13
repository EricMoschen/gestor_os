from src.cadastro.models import CentroCusto
from ..models import AberturaOS


class AberturaOSService:

    @staticmethod
    def _obter_centro_custo(centro_id):
        if not centro_id:
            raise ValueError("Selecione um ativo válido.")
        
        try:
            centro_custo = CentroCusto.objects.get(pk=centro_id)
        except CentroCusto.DoesNotExist as exc:
            raise ValueError("ativo inválido.") from exc
        if centro_custo.tag_pai_id is None:
            raise ValueError("Selecione uma subtag de ativo válida.")

        return centro_custo

    @staticmethod
    def criar_os(form, centro_id):
        """
        Cria uma nova Ordem de Serviço a partir do formulário.
        """
        os_obj = form.save(commit=False)
        os_obj.situacao = AberturaOS.Status.ABERTA  # Status padrão

        os_obj.centro_custo = AberturaOSService._obter_centro_custo(centro_id)

        os_obj.save()  # Aqui o número da OS será gerado automaticamente pelo model
        return os_obj

    @staticmethod
    def atualizar_os(form, centro_id):
        os_obj = form.save(commit=False)
        os_obj.centro_custo = AberturaOSService._obter_centro_custo(centro_id)
        os_obj.save()
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
