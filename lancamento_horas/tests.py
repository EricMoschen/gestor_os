from datetime import datetime
from types import SimpleNamespace

from django.test import SimpleTestCase

from lancamento_horas.services.apontamento_horas_service import ApontamentoHorasService


class ApontamentoHorasServiceTestes(SimpleTestCase):
    def _apontamento(self, inicio, fim,  turno="A", **horarios):
        colaborador = SimpleNamespace(
            turno = turno,
            hr_entrada_am=horarios.get("hr_entrada_am"),
            hr_saida_am=horarios.get("hr_saida_am"),
            hr_entrada_pm=horarios.get("hr_entrada_pm"),
            hr_saida_pm=horarios.get("hr_saida_pm"),
         )           
        return SimpleNamespace(data_inicio=inicio, data_fim=fim, colaborador=colaborador)

    def test_horas_normais_dentro_turno_sem_contar_almoco(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 5, 10, 0),
            datetime(2026, 1, 5, 13, 0),
            turno="A",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 2)
        self.assertEqual(extra50, 0)
        self.assertEqual(extra100, 0)

    def test_horas_apos_turno_em_dia_util_vira_extra_50(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 6, 16, 0),
            datetime(2026, 1, 6, 18, 0),
            turno="A",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 0.8)
        self.assertEqual(extra50, 1.2)
        self.assertEqual(extra100, 0)
        

    def test_dia_normal_desconciderar_somente_almoco(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 6, 8, 0),
            datetime(2026, 1, 6, 17, 48),
            turno="A",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 8.8)
        self.assertEqual(extra50, 0)
        self.assertEqual(extra100, 0)


    def test_sabado_todo_periodo_e_extra_50(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 10, 7, 0),
            datetime(2026, 1, 10, 9, 30),
            turno="HC",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 0)
        self.assertEqual(extra50, 2.5)
        self.assertEqual(extra100, 0)


    def test_domingo_todo_periodo_e_extra_100(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 11, 7, 0),
            datetime(2026, 1, 11, 9, 0),
            turno="HC",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 0)
        self.assertEqual(extra50, 0)
        self.assertEqual(extra100, 2)


    def test_cruzando_sabado_para_domingo_separa_50_e_100(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 10, 23, 0),
            datetime(2026, 1, 11, 2, 0),
            turno="B",
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 0)
        self.assertEqual(extra50, 1)
        self.assertEqual(extra100, 2)