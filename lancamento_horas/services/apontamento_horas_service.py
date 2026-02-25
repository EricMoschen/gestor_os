from datetime import datetime, time, timedelta
from django.utils import timezone
from ..models.apontamento_horas import ApontamentoHoras
from ..utils.feriados import eh_feriado_ou_domingo, eh_sabado

class ApontamentoHorasService:

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
        total_horas = (fim - inicio).total_seconds() / 3600
        tipo_dia = ApontamentoHorasService.classificar_tipo_dia(inicio.date())

        horas_normais, horas_50, horas_100 = 0, 0, 0

        if tipo_dia == "Dom/Feriado":
            horas_100 = total_horas
        elif tipo_dia == "Sábado":
            horas_50 = total_horas
        else:  # Dia normal
            for entrada, saida in ApontamentoHorasService.obter_intervalos_turno(apontamento.colaborador):
                if not entrada or not saida:
                    continue

                ini_turno = datetime.combine(inicio.date(), entrada)
                fim_turno = datetime.combine(inicio.date(), saida)

                # Turno passa da meia-noite
                if saida < entrada:
                    fim_turno += timedelta(days=1)

                ini_turno = ApontamentoHorasService._ajustar_para_referencia(ini_turno, inicio)
                fim_turno = ApontamentoHorasService._ajustar_para_referencia(fim_turno, inicio)

                inter_inicio = max(inicio, ini_turno)
                inter_fim = min(fim, fim_turno)

                if inter_inicio < inter_fim:
                    horas_normais += (inter_fim - inter_inicio).total_seconds() / 3600

            horas_50 = max(total_horas - horas_normais, 0)

        return horas_normais, horas_50, horas_100

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
