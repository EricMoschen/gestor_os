from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase, override_settings

from src.lancamento_horas.services.apontamento_horas_service import ApontamentoHorasService
from src.lancamento_horas.views.ajuste_horas import _gerar_competencias


class _ApontamentoFactoryMixin:
    def _apontamento(self, inicio, fim, turno="HC", **horarios):
        colaborador = SimpleNamespace(
            turno=turno,
            hr_entrada_am=horarios.get("hr_entrada_am"),
            hr_saida_am=horarios.get("hr_saida_am"),
            hr_entrada_pm=horarios.get("hr_entrada_pm"),
            hr_saida_pm=horarios.get("hr_saida_pm"),
        )
        return SimpleNamespace(data_inicio=inicio, data_fim=fim, colaborador=colaborador)


class ApontamentoHorasServiceTestes(_ApontamentoFactoryMixin, SimpleTestCase):
    def test_dia_normal_desconciderar_somente_almoco(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 5, 8, 0),
            datetime(2026, 1, 5, 17, 48),
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 8.8)
        self.assertEqual(extra50, 0)
        self.assertEqual(extra100, 0)

    def test_horas_fora_turno_em_dia_normal_sao_extra_50(self):
        apontamento = self._apontamento(
            datetime(2026, 1, 5, 7, 0),
            datetime(2026, 1, 5, 8, 0),
        )

        normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

        self.assertEqual(normais, 0)
        self.assertEqual(extra50, 1)
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


class _FakeQueryset:
    def __init__(self, datas):
        self._datas = datas

    def values_list(self, *_args, **_kwargs):
        return self._datas


class CompetenciaAjusteHorasTestes(_ApontamentoFactoryMixin, SimpleTestCase):
    @override_settings(USE_TZ=True, TIME_ZONE="America/Sao_Paulo")
    def test_gerar_competencias_respeita_data_local_em_datetime_timezone_aware(self):
        datas = [datetime(2026, 3, 21, 2, 30, tzinfo=ZoneInfo("UTC"))]

        competencias = _gerar_competencias(_FakeQueryset(datas))

        self.assertEqual(competencias[0]["valor"], "2026-03")

    def test_gerar_competencias_avanca_mes_para_datas_maiores_que_20(self):
        datas = [datetime(2026, 1, 21, 10, 0), datetime(2026, 1, 10, 10, 0)]

        competencias = _gerar_competencias(_FakeQueryset(datas))
        valores = [item["valor"] for item in competencias]

        self.assertIn("2026-01", valores)
        self.assertIn("2026-02", valores)

    def test_gerar_competencias_usa_mes_atual_quando_lista_vazia(self):
        competencias = _gerar_competencias(_FakeQueryset([]))

        self.assertTrue(competencias)
        self.assertRegex(competencias[0]["valor"], r"^\d{4}-\d{2}$")