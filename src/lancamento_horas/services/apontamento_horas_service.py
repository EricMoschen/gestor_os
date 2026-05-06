from datetime import datetime, time, timedelta
from django.utils import timezone
from ..models.apontamento_horas import ApontamentoHoras
from ..utils.feriados import eh_feriado_ou_domingo, eh_sabado

class ApontamentoHorasService:

    TOLERANCIA_APONTAMENTO = timedelta(minutes=5)

    @staticmethod
    def _duracao_em_horas(inicio, fim):
        if fim <= inicio:
            return 0
        return(fim - inicio).total_seconds() / 3600

    @staticmethod
    def _normalizar_datahora(datahora):
        """Normaliza detetime para evitar erros entre naive/aware"""
        if not datahora:
            return datahora
        if timezone.is_naive(datahora):
            if timezone.is_aware(timezone.now()):
                return timezone.make_aware(datahora,timezone.get_current_timezone())
            return datahora
        return timezone.localtime(datahora)
    
    @staticmethod
    def _ajustar_para_referencia(datahora, referencia):
        """Mantém naive/aware alinhado com a referência para evitar erros de comparação"""
        if timezone.is_aware(referencia) and timezone.is_naive(datahora):
            return timezone.make_aware(datahora)
        if timezone.is_naive(referencia) and timezone.is_aware(datahora):
            return timezone.make_naive(datahora)
        return datahora

    @staticmethod
    def _arredondar_horas(valor):
        return round(valor, 10)

    @staticmethod
    def _apontamento_cobre_pausa(inicio, fim, inicio_pausa, fim_pausa):
        return inicio <= inicio_pausa and fim > fim_pausa

    @staticmethod
    def _esta_dentro_da_tolerancia(datahora, limite):
        return abs(datahora - limite) <= ApontamentoHorasService.TOLERANCIA_APONTAMENTO

    @staticmethod
    def _limites_intervalos_no_dia(colaborador, data_referencia, referencia_timezone):
        inicios = []
        fins = []

        for inicio_turno, fim_turno in ApontamentoHorasService._obter_intervalos_normais_no_dia(
            colaborador,
            data_referencia,
            referencia_timezone,
        ):
            if inicio_turno.date() == data_referencia:
                inicios.append(inicio_turno)
            if fim_turno.date() == data_referencia:
                fins.append(fim_turno)

        return inicios, fins

    @staticmethod
    def _ajustar_inicio_por_tolerancia(colaborador, inicio):
        if ApontamentoHorasService.classificar_tipo_dia(inicio.date()) != "Dia Normal":
            return inicio

        inicios_turno, _ = ApontamentoHorasService._limites_intervalos_no_dia(
            colaborador,
            inicio.date(),
            inicio,
        )

        for limite in inicios_turno:
            if ApontamentoHorasService._esta_dentro_da_tolerancia(inicio, limite):
                return limite

        return inicio

    @staticmethod
    def _ajustar_fim_por_tolerancia(colaborador, fim):
        if ApontamentoHorasService.classificar_tipo_dia(fim.date()) != "Dia Normal":
            return fim

        _, fins_turno = ApontamentoHorasService._limites_intervalos_no_dia(
            colaborador,
            fim.date(),
            fim,
        )

        for limite in fins_turno:
            if ApontamentoHorasService._esta_dentro_da_tolerancia(fim, limite):
                return limite

        return fim

    @staticmethod
    def _aplicar_tolerancia_apontamento(colaborador, inicio, fim):
        inicio_ajustado = ApontamentoHorasService._ajustar_inicio_por_tolerancia(colaborador, inicio)
        fim_ajustado = ApontamentoHorasService._ajustar_fim_por_tolerancia(colaborador, fim)
        return inicio_ajustado, fim_ajustado

    @staticmethod
    def _turno_cruza_meia_noite(colaborador):
        return any(
            entrada and saida and entrada > saida
            for entrada, saida in ApontamentoHorasService.obter_intervalos_turno(colaborador)
        )

    @staticmethod
    def obter_intervalos_turno(colaborador):
        turno = colaborador.turno

        if turno == "A":
            return [(time(7, 0), time(11, 0)), (time(12, 0), time(16, 48))]
        elif turno == "B":
            return [(time(16, 48), time(19, 0)), (time(20, 0), time(2, 0))]
        elif turno == "HC":
            return [(time(8, 0), time(12, 0)), (time(13, 0), time(17, 48))]
        elif turno == "OUTROS":
            return [
                (colaborador.hr_entrada_am, colaborador.hr_saida_am),
                (colaborador.hr_entrada_pm, colaborador.hr_saida_pm),
            ]
        return []

    @staticmethod
    def classificar_tipo_dia(data):
        if eh_feriado_ou_domingo(data):
            return "Dom/Feriado"
        elif eh_sabado(data):
            return "Sábado"
        return "Dia Normal"

    @staticmethod
    def calcular_horas(apontamento: ApontamentoHoras):
        if not apontamento.data_fim:
            return 0, 0, 0

        inicio = ApontamentoHorasService._normalizar_datahora(apontamento.data_inicio)
        fim = ApontamentoHorasService._normalizar_datahora(apontamento.data_fim)
        inicio, fim = ApontamentoHorasService._aplicar_tolerancia_apontamento(
            apontamento.colaborador,
            inicio,
            fim,
        )
        if fim <= inicio:
            return 0, 0, 0

        horas_normais, horas_50, horas_100 = 0, 0, 0
        cursor = inicio

        while cursor < fim:
            inicio_dia = datetime.combine(cursor.date(), time.min)
            fim_dia = inicio_dia + timedelta(days=1)

            inicio_dia = ApontamentoHorasService._ajustar_para_referencia(inicio_dia, inicio)
            fim_dia = ApontamentoHorasService._ajustar_para_referencia(fim_dia, inicio)

            bloco_inicio = cursor
            bloco_fim = min(fim, fim_dia)

            tipo_dia = ApontamentoHorasService.classificar_tipo_dia(bloco_inicio.date())
            horas_bloco = ApontamentoHorasService._duracao_em_horas(bloco_inicio, bloco_fim)

            if tipo_dia == "Dom/Feriado":
                horas_100 += horas_bloco
            elif tipo_dia == "Sábado":
                horas_50_bloco, horas_100_bloco = ApontamentoHorasService._classificar_horas_sabado(
                    apontamento.colaborador,
                    bloco_inicio,
                    bloco_fim,
                    inicio,
                )
                horas_50 += horas_50_bloco
                horas_100 += horas_100_bloco
            else:
                horas_normais_no_bloco = 0
                for ini_turno, fim_turno in ApontamentoHorasService._obter_intervalos_normais_no_dia(
                    apontamento.colaborador,
                    bloco_inicio.date(),
                    inicio,
                ):
                    inter_inicio = max(bloco_inicio, ini_turno)
                    inter_fim = min(bloco_fim, fim_turno)
                    horas_normais_no_bloco += ApontamentoHorasService._duracao_em_horas(inter_inicio, inter_fim)

                horas_pausadas_no_bloco = 0
                for ini_pausa, fim_pausa in ApontamentoHorasService._obter_intervalos_pausa_no_dia(
                    apontamento.colaborador,
                    bloco_inicio.date(),
                    inicio,
                ):
                    inter_inicio = max(bloco_inicio, ini_pausa)
                    inter_fim = min(bloco_fim, fim_pausa)
                    horas_pausa = ApontamentoHorasService._duracao_em_horas(inter_inicio, inter_fim)
                    if horas_pausa <= 0:
                        continue

                    if ApontamentoHorasService._deve_contar_pausa_como_normal(
                        apontamento.colaborador,
                        inicio,
                        fim,
                        bloco_fim,
                        ini_pausa,
                        fim_pausa,
                    ):
                        horas_normais_no_bloco += horas_pausa
                    elif ApontamentoHorasService._apontamento_cobre_pausa(inicio, fim, ini_pausa, fim_pausa):
                        horas_pausadas_no_bloco += horas_pausa

                horas_normais += max(horas_normais_no_bloco, 0)
                horas_50 += max(horas_bloco - horas_normais_no_bloco - horas_pausadas_no_bloco, 0)

            cursor = bloco_fim

        return (
            ApontamentoHorasService._arredondar_horas(horas_normais),
            ApontamentoHorasService._arredondar_horas(horas_50),
            ApontamentoHorasService._arredondar_horas(horas_100),
        )
    

    @staticmethod
    def _deve_contar_pausa_como_normal(
        colaborador,
        inicio_apontamento,
        fim_apontamento,
        fim_bloco,
        inicio_pausa,
        fim_pausa,
    ):
        proximo_dia = fim_bloco.date()
        return (
            ApontamentoHorasService._turno_cruza_meia_noite(colaborador)
            and fim_bloco < fim_apontamento
            and ApontamentoHorasService.classificar_tipo_dia(proximo_dia) == "Sábado"
            and ApontamentoHorasService._apontamento_cobre_pausa(
                inicio_apontamento,
                fim_apontamento,
                inicio_pausa,
                fim_pausa,
            )
        )

    @staticmethod
    def _classificar_horas_sabado(colaborador, bloco_inicio, bloco_fim, inicio_apontamento):
        horas_bloco = ApontamentoHorasService._duracao_em_horas(bloco_inicio, bloco_fim)
        if horas_bloco <= 0:
            return 0, 0

        if (
            ApontamentoHorasService._turno_cruza_meia_noite(colaborador)
            and bloco_inicio.date() > inicio_apontamento.date()
            and ApontamentoHorasService.classificar_tipo_dia(inicio_apontamento.date()) == "Dia Normal"
        ):
            horas_50 = min(horas_bloco, 1)
            return horas_50, max(horas_bloco - horas_50, 0)

        return horas_bloco, 0
    

    @staticmethod
    def _obter_intervalos_normais_no_dia(colaborador, data_referencia, referencia_timezone):
        intervalos_normais = []

        for entrada, saida in ApontamentoHorasService.obter_intervalos_turno(colaborador):
            if not entrada or not saida:
                continue

            if entrada < saida:
                ini = datetime.combine(data_referencia, entrada)
                fim = datetime.combine(data_referencia, saida)
                intervalos_normais.append((
                    ApontamentoHorasService._ajustar_para_referencia(ini, referencia_timezone),
                    ApontamentoHorasService._ajustar_para_referencia(fim, referencia_timezone),
                ))
                continue

            inicio_continuacao =  datetime.combine(data_referencia, time.min)
            fim_continuacao = datetime.combine(data_referencia, saida)
            inicio_turno = datetime.combine(data_referencia, entrada)
            fim_turno = datetime.combine( data_referencia + timedelta(days=1), time.min)

            intervalos_normais.append((
                ApontamentoHorasService._ajustar_para_referencia(inicio_continuacao, referencia_timezone),
                ApontamentoHorasService._ajustar_para_referencia(fim_continuacao, referencia_timezone),
            ))

            intervalos_normais.append((
                ApontamentoHorasService._ajustar_para_referencia(inicio_turno, referencia_timezone),
                ApontamentoHorasService._ajustar_para_referencia(fim_turno, referencia_timezone),
            ))

        return intervalos_normais
    
    @staticmethod
    def _obter_intervalos_pausa_no_dia(colaborador, data_referencia, referencia_timezone):
        
        intervalos_pausa = []
        intervalos_turno = ApontamentoHorasService.obter_intervalos_turno(colaborador)

        for indice in range(len(intervalos_turno) - 1):
            _, saida_atual = intervalos_turno[indice]
            entrada_proximo, _ = intervalos_turno[indice + 1]

            if not saida_atual or not entrada_proximo:
                continue

            inicio_pausa = datetime.combine(data_referencia, saida_atual)
            fim_pausa = datetime.combine(data_referencia, entrada_proximo)

            if fim_pausa <= inicio_pausa:
                fim_pausa += timedelta(days=1)

            intervalos_pausa.append((
                ApontamentoHorasService._ajustar_para_referencia(inicio_pausa, referencia_timezone),
                ApontamentoHorasService._ajustar_para_referencia(fim_pausa, referencia_timezone),
            ))

        return intervalos_pausa
    
    @staticmethod
    def _calcular_fim_turno_para_inicio(inicio, turno_inicio, turno_fim):
        if not turno_inicio or not turno_fim:
            return None
        
        if turno_inicio <= turno_fim:
            fim = datetime.combine(inicio.date(), turno_fim)
        else:
            #turno cruza maia-noite (ex.: 16:48 -> 02:00)
            if inicio.time() <= turno_fim:
                fim = datetime.combine(inicio.date(), turno_fim)
            else:
                fim = datetime.combine(inicio.date() + timedelta(days=1), turno_fim)

        return ApontamentoHorasService._ajustar_para_referencia(fim, inicio)
  
    @staticmethod
    def encerrar_aberto(cls, colaborador, referencia_agora=None):
        aberto = cls.objects.filter(
            colaborador=colaborador,
            data_fim__isnull=True
        ).order_by('-data_inicio').first()

        if not aberto:
            raise ValueError("Nenhum apontamento aberto encontrado.")

        inicio = ApontamentoHorasService._normalizar_datahora(aberto.data_inicio)
        agora = referencia_agora or timezone.now()

        turno_inicio = colaborador.horario_inicio_turno()
        turno_fim = colaborador.horario_fim_turno()

        if inicio.date() < agora.date():
            fim_turno = ApontamentoHorasService._calcular_fim_turno_para_inicio(inicio, turno_inicio, turno_fim)
            if not fim_turno or fim_turno <= inicio:
                raise ValueError("Não foi possivel encerra automaticamente no fim do turno. Solicite ao seu Supervisor para efetuar o encerramento manual.")

            aberto.data_fim = fim_turno
            aberto.save(update_fields=["data_fim"])
            return aberto
        
        # encerra com horário atual
        aberto.data_fim = agora
        aberto.save(update_fields=["data_fim"])

        return aberto