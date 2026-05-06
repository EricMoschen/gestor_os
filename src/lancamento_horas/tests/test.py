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

    class MatrizCenariosCalculoHorasTestes(_ApontamentoFactoryMixin, SimpleTestCase):
        DATA_NORMAL = (2026, 1, 5)

        def _dt(self, hora, minuto=0):
            return datetime(*self.DATA_NORMAL, hora, minuto)

        def test_matriz_de_cenarios_extraida_da_planilha(self):
            # Jornada HC usada como base da matriz:
            # Hij=08:00, Hia=12:00, Hfa=13:00, Hfj=17:48 e tol=10 minutos.
            # C5 usa Hfi na planilha; o teste considera Hfj.
            # C11 possui condição Hi > Hf + tol na planilha, incompatível com a fórmula;
            # o teste usa Hi após o almoço e Hf após o fim da jornada.
            cenarios = {
                "C1": ((6, 0), (7, 30), 0, 1.5, 0),
                "C2": ((7, 30), (15, 0), 6, 0.5, 0),
                "C3": ((7, 30), (18, 30), 8.8, 1.2, 0),
                "C4": ((8, 5), (17, 55), 8.8, 0, 0),
                "C5": ((8, 0), (15, 0), 6, 0, 0),
                "C6": ((9, 0), (17, 55), 7.8, 0, 0),
                "C7": ((9, 0), (15, 0), 5, 0, 0),
                "C8": ((9, 0), (11, 0), 2, 0, 0),
                "C9": ((14, 0), (17, 55), 3.8, 0, 0),
                "C10": ((14, 0), (16, 0), 2, 0, 0),
                "C11": ((14, 0), (18, 30), 3.8, 0.7, 0),
                "C12": ((9, 0), (12, 5), 3, 0, 0),
                "C13": ((12, 55), (17, 55), 4.8, 0, 0),
                "C14": ((8, 0), (12, 30), 4, 0, 0),
                "C15": ((7, 30), (17, 55), 8.8, 0.5, 0),
                "C16": ((12, 55), (18, 30), 4.8, 0.7, 0),
                "C17": ((9, 0), (18, 30), 7.8, 0.7, 0),
                "C18": ((8, 5), (18, 30), 8.8, 0.7, 0),
                "C21": ((7, 55), (10, 0), 2, 0, 0),
                "C22": ((9, 0), (12, 30), 3, 0, 0),
                "C23": ((12, 30), (17, 55), 4.8, 0, 0),
                "C24": ((12, 30), (18, 30), 4.8, 0.7, 0),
                "C25": ((7, 30), (10, 0), 2, 0.5, 0),
            }

            for codigo, (inicio_hora, fim_hora, normais_esperadas, extra50_esperada, extra100_esperada) in cenarios.items():
                with self.subTest(cenario=codigo):
                    apontamento = self._apontamento(
                        self._dt(*inicio_hora),
                        self._dt(*fim_hora),
                        turno="HC",
                    )

                    normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

                    self.assertAlmostEqual(normais, normais_esperadas, places=2)
                    self.assertAlmostEqual(extra50, extra50_esperada, places=2)
                    self.assertAlmostEqual(extra100, extra100_esperada, places=2)

        def test_tolerancia_tambem_considera_saida_antecipada_dentro_do_limite(self):
            apontamento = self._apontamento(
                self._dt(8, 0),
                self._dt(17, 40),
                turno="HC",
            )

            normais, extra50, extra100 = ApontamentoHorasService.calcular_horas(apontamento)

            self.assertAlmostEqual(normais, 8.8, places=2)
            self.assertEqual(extra50, 0)
            self.assertEqual(extra100, 0)


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