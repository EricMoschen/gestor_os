from django.test import TestCase

from src.abertura_os.services.abertura_os_service import AberturaOSService
from src.cadastro.models import CentroCusto


class AberturaOSServiceTests(TestCase):
    def test_deve_rejeitar_tag_pai_como_centro_custo(self):
        pai = CentroCusto.objects.create(cod_centro=1, descricao="Tag Pai")

        with self.assertRaisesRegex(
            ValueError,
            r"Selecione uma subtag de .+ válida\.",
        ):
            AberturaOSService._obter_centro_custo(pai.pk)

    def test_deve_aceitar_subtag_como_centro_custo(self):
        pai = CentroCusto.objects.create(cod_centro=10, descricao="Tag Pai")
        filho = CentroCusto.objects.create(
            cod_centro=11,
            descricao="Tag Filha",
            tag_pai=pai,
        )

        centro = AberturaOSService._obter_centro_custo(filho.pk)

        self.assertEqual(centro.pk, filho.pk)
