from datetime import datetime
from types import SimpleNamespace

from django.test import SimpleTestCase

from zoneinfo import ZoneInfo

from django.test import override_settings

from lancamento_horas.views.ajuste_horas import _gerar_competencias

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
@@ -75,26 +81,44 @@ class ApontamentoHorasServiceTestes(SimpleTestCase):
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

class _FakeQueryset:
    def __init__(self, datas):
        self._datas = datas

    def values_list(self, *_args, **_kwargs):
        return self._datas


class CompetenciaAjusteHorasTestes(SimpleTestCase):
    @override_settings(USE_TZ=True, TIME_ZONE="America/Sao_Paulo")
    def test_gerar_competencias_respeita_data_local_em_datetime_timezone_aware(self):
        datas = [datetime(2026, 3, 21, 2, 30, tzinfo=ZoneInfo("UTC"))]

        competencias = _gerar_competencias(_FakeQueryset(datas))

        self.assertEqual(competencias[0]["valor"], "2026-03")
