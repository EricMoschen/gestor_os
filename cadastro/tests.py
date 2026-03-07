from cadastro.models import CentroCusto
from cadastro.services.centro_custo_service import atualizar_centro_custo

class CentroCustoServiceTest(TestCase):

    def test_deve_atualizar_codigo_e_reapontar_subcentros(self):
        pai = CentroCusto.objects.create(cod_centro=10, descicao="Pai")
        filho = CentroCusto.objects.create(cod_centro=11, descricao="Filho", centro_pai=pai)

        centro_atualizado = atualizar_centro_custo(
            pai,
            cod_centro=100,
            descricao="Pai Atualizado",
            centro_pai=None,
        )

        self.assertFalse(CentroCusto.objects.filter(cod_centro=10).exists())
        self.assertTrue(CentroCusto.objects.filter(cod_centro=100).exists())
        self.assertEqual(centro_atualizado.descricao, "Pai Atualizado")

        filho.refresh_from_db()
        self.assertEqual(filho.centro_pai_id, 100)

    def test_deve_permitir_alterar_centro_pai_para_qualquer_nivel(self):

        raiz = CentroCusto.objects.create(cod_centro=1, descricao="Raiz")
        intermediario = CentroCusto.objects.create(cod_centro=2, descricao="Intermediário", centro_pai=raiz)
        folha = CentroCusto.objects.create(cod_centro=3, descricao="Folha", centro_pai=intermediario)

        atualizar_centro_custo(
            folha,
            cod_centro=3,
            descricao="Folha",
            centro_pai=raiz,
        )

        folha.refresh_from_db()
        self.assertEqual(folha.centro_pai_id, raiz.cod_centro)