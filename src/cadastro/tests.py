from django.test import TestCase

from src.cadastro.forms import CentroCustoForm
from src.cadastro.models import CentroCusto
from src.cadastro.services.centro_custo_service import atualizar_centro_custo, criar_centro_custo


class CentroCustoServiceTests(TestCase):
    def test_deve_gerar_cod_centro_quando_nao_informado(self):
        CentroCusto.objects.create(cod_centro=1, descricao="Existente")

        centro = criar_centro_custo(descricao="Novo")

        self.assertEqual(centro.cod_centro, 2)

    def test_deve_atualizar_tag_pai(self):
        raiz = CentroCusto.objects.create(cod_centro=1, descricao="Raiz", cod_tag=100)
        folha = CentroCusto.objects.create(cod_centro=2, descricao="Folha", cod_tag=101)

        atualizar_centro_custo(folha, tag_pai=raiz, descricao="Folha")

        folha.refresh_from_db()
        self.assertEqual(folha.tag_pai_id, raiz.pk)


class CentroCustoFormTests(TestCase):
    def test_deve_exigir_codigos_para_tag_filha(self):
        pai = CentroCusto.objects.create(cod_centro=10, descricao="Pai")

        form = CentroCustoForm(
            data={
                "descricao": "Filho",
                "tag_pai": pai.pk,
                "cod_tag": "",
                "cod_do_ativo": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cod_tag", form.errors)
        self.assertIn("cod_do_ativo", form.errors)