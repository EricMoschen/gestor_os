from datetime import datetime, time, timedelta
from django.utils import timezone
from ..models.apontamento_horas import ApontamentoHoras
from ..utils.feriados import eh_feriado_ou_domingo, eh_sabado

class ApontamentoHorasService:

    @staticmethod
    def _duracao_em_horas(inicio, fim):
        if fim <= inicio:
            return 0
        return(fim - inicio).total_seconds() / 3600

    @staticmethod
    def _normalizar_datahora(datahora):
        """Retornar datetime no timezone local apenas quando ele for aware."""
        if timezone.is_naive(datahora):
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
                horas_bloco =  ApontamentoHorasService._duracao_em_horas(bloco_inicio, bloco_fim)

                if tipo_dia == "Dom/Feriado":
                    horas_100 += horas_bloco
                elif tipo_dia == "Sábado":
                    horas_50 += horas_bloco
                else:
                    normais_no_bloco = 0
                    for ini_turno, fim_turno  in ApontamentoHorasService._obter_intervalos_normais_no_dia(
                        apontamento.colaborador,
                        bloco_inicio.date(),
                        inicio,
                    ):
                        inter_inicio = max(bloco_inicio, ini_turno)
                        inter_fim = min(bloco_fim, fim_turno)
                        normais_no_bloco += ApontamentoHorasService._duracao_em_horas(inter_inicio, inter_fim)

                    horas_normais += normais_no_bloco
                    horas_50 += max(horas_bloco - normais_no_bloco, 0)

                cursor = bloco_fim

        return horas_normais, horas_50, horas_100
    

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
    def encerrar_aberto(cls, colaborador):
        aberto = cls.objects.filter(
            colaborador=colaborador,
            data_fim__isnull=True
        ).order_by('-data_inicio').first()

        if not aberto:
            raise ValueError("Nenhum apontamento aberto encontrado.")

        inicio = ApontamentoHorasService._normalizar_datahora(aberto.data_inicio)
        tipo_dia = ApontamentoHorasService.classificar_tipo_dia(inicio.date())
        turno_inicio = colaborador.calcular_horario_inicio_turno()
        turno_fim = colaborador.calcular_horario_fim_turno()

        if tipo_dia != "Dia Normal":
            raise ValueError("Apontamento fora do horário normal. Encerramento manual necessário.")

        hora_inicio = inicio.time()
        if turno_inicio <= turno_fim:
            dentro_turno = turno_inicio <= hora_inicio <= turno_fim
            fim_turno_date = inicio.date()
        else:
            dentro_turno = hora_inicio >= turno_inicio or hora_inicio <= turno_fim
            fim_turno_date = inicio.date()
            if hora_inicio <= turno_fim:
                fim_turno_date += timedelta(days=1)

        if not dentro_turno:
            raise ValueError("Apontamento fora do horário normal. Encerramento manual necessário.")

        fim_turno = datetime.combine(fim_turno_date, turno_fim)
        fim_turno = ApontamentoHorasService._ajustar_para_referencia(fim_turno, inicio)
        if fim_turno < inicio:
            raise ValueError("Horário de término do turno inválido para encerramento automático.")

        aberto.data_fim = fim_turno
        aberto.save(update_fields=["data_fim"])

        return aberto
