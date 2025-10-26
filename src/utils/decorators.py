"""
Módulo de Decorators Utilitários

Este módulo contém decoradores reutilizáveis para:
- Medição de tempo de execução
- Tentativas automáticas com controle de falha
- Envio de status da execução com webhook
- Execução de funções síncronas ou assíncronas

Autor: João Alves da Silva Neto
Data: 2024-01-01
Versão: 1.0.0
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import holidays
import pandas as pd
import requests

from src.config.settings import Settings
from src.utils.databricks import Databricks
from src.utils.sendfail import send_fail_message

# -------------------------------------------------------------------------
# Função utilitária para execução dinâmica
# -------------------------------------------------------------------------


def execute_function(func: Callable, *args, **kwargs):
    """
    Executa dinamicamente uma função, seja ela síncrona ou assíncrona.

    Args:
        func (Callable): Função a ser executada.
        *args: Argumentos posicionais para a função.
        **kwargs: Argumentos nomeados para a função.

    Returns:
        Resultado da função executada ou uma task assíncrona.
    """
    if asyncio.iscoroutinefunction(func):
        return asyncio.create_task(func(*args, **kwargs))
    return func(*args, **kwargs)


# -------------------------------------------------------------------------
# Decorador Unificado: tempo, tentativas, status
# -------------------------------------------------------------------------


def smart_task(mode_getter: Callable[[Any], Any], log_message: str = "Erro inesperado", max_attempts: int = 1, waiting_time: int = 1):
    """
    Decorador unificado que aplica:
    - Tentativas automáticas (retry)
    - Medição de tempo de execução
    - Envio de status da execução via webhook
    - Log de falhas com controle de exceções

    Args:
        mode_getter (Callable): Função que retorna o modo de execução do processo.
        log_message (str): Mensagem padrão de log para erros.
        max_attempts (int): Número máximo de tentativas antes de falhar.
        waiting_time (int): Tempo de espera entre tentativas, em segundos.

    Returns:
        Callable: Função decorada com lógica de monitoramento.
    """

    def decorator(func: Callable):

        @wraps(func)
        async def wrapper_async(self, *args, **kwargs):
            start_time = datetime.now()
            fail = True
            exception_to_raise = None
            result = None

            logging.info(f"🕐 Início da execução: {start_time.strftime('%H:%M:%S')}")

            for attempt in range(1, max_attempts + 1):
                try:
                    result = await func(self, *args, **kwargs)
                    fail = False
                    break
                except Exception as e:
                    logging.error(f"Tentativa {attempt}/{max_attempts} | {type(e).__name__}: {e}")
                    if attempt < max_attempts:
                        await asyncio.sleep(waiting_time)
                    else:
                        exception_to_raise = e
                        break

            if exception_to_raise:
                logging.error(f"[EXCEÇÃO SUPRIMIDA] {type(exception_to_raise).__name__}: {exception_to_raise}")
                send_fail_message(bot=Settings.PROJECT_NAME, mode=mode_getter(self).value, message=f"{log_message} | {type(exception_to_raise).__name__}: {exception_to_raise}")

            _send_status(self, mode_getter, fail)
            _log_duration(start_time, datetime.now())

            return result

        @wraps(func)
        def wrapper_sync(self, *args, **kwargs):
            start_time = datetime.now()
            fail = True
            exception_to_raise = None
            result = None

            logging.info(f"🕐 Início da execução: {start_time.strftime('%H:%M:%S')}")

            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(self, *args, **kwargs)
                    fail = False
                    break
                except Exception as e:
                    logging.error(f"Tentativa {attempt}/{max_attempts} | {type(e).__name__}: {e}")
                    if attempt < max_attempts:
                        time.sleep(waiting_time)
                    else:
                        exception_to_raise = e
                        break

            if exception_to_raise:
                logging.error(f"[EXCEÇÃO SUPRIMIDA] {type(exception_to_raise).__name__}: {exception_to_raise}")
                send_fail_message(bot=Settings.PROJECT_NAME, mode=mode_getter(self).value, message=f"{log_message} | {type(exception_to_raise).__name__}: {exception_to_raise}")

            _send_status(self, mode_getter, fail)
            _log_duration(start_time, datetime.now())

            return result

        return wrapper_async if asyncio.iscoroutinefunction(func) else wrapper_sync

    return decorator


# -------------------------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------------------------


def _log_duration(start: datetime, end: datetime):
    """
    Loga a duração total da execução com base nos timestamps de início e fim.

    Args:
        start (datetime): Horário de início.
        end (datetime): Horário de fim.
    """
    duration = end - start
    h, rem = divmod(duration.total_seconds(), 3600)
    m, s = divmod(rem, 60)
    logging.info(f"🕑 Execution completed at: {end.strftime('%H:%M:%S')}")
    logging.info(f"🕞 Runtime: {int(h):02} horas, {int(m):02} minutos e {int(s):02} segundos.")


def _send_status(self, mode_getter, fail: bool):
    """
    Constrói e envia o status da execução para um webhook definido nas configurações.

    Args:
        self: Instância da classe que contém os atributos `totalCount` e `successCount`.
        mode_getter (Callable): Função que retorna o modo atual de execução.
        fail (bool): Indica se a execução falhou.
    """
    total = getattr(self, "totalCount", 0)
    success = getattr(self, "successCount", 0)

    status = {
        "processName": Settings.PROJECT_NAME,
        "dateTime": datetime.now().isoformat(),
        "mode": mode_getter(self).value if hasattr(mode_getter(self), "value") else str(mode_getter(self)),
        "parameters": {
            "totalCount": total,
            "successCount": success,
        },
        "fail": total < success or fail,
    }

    logging.info("[STATUS DE EXECUÇÃO]")
    logging.info(json.dumps(status, indent=2, ensure_ascii=False))

    try:
        response = requests.post(Settings.WEBHOOK_EXECUTION_STATUS, json=status)

        # Parte Provisória
        df = pd.DataFrame(
            [
                {
                    "data_execucao": datetime.fromisoformat(status["dateTime"]),
                    "projeto": status["processName"],
                    "falha": status["fail"],
                    "tipo_execucao": status["mode"],
                    "quant_total": status["parameters"]["totalCount"],
                    "quant_sucesso": status["parameters"]["successCount"],
                }
            ]
        )

        dbricks = Databricks()
        dbricks.open_connection()
        dbricks.insert_data("sandbox.gi_planejamento.fato_saving", df, batch_size=1000)
        dbricks.optimize_table("sandbox.gi_planejamento.fato_saving")
        dbricks.close_connection()

        response.raise_for_status()
        logging.info(f"[WEBHOOK ENVIADO] Código: {response.status_code}")
    except Exception as e:
        logging.warning(f"[ERRO AO ENVIAR WEBHOOK]: {e}")


def time_execution(func):
    """
    Decorador para medir o tempo de execução de uma função.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.info(f"🕐 Execution started at: {start_time.strftime('%H:%M:%S')}")

        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            raise
        finally:
            end_time = datetime.now()
            elapsed_time = end_time - start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            logging.info(f"🕑 Execution completed at: {end_time.strftime('%H:%M:%S')}")
            logging.info(f"🕞 Runtime: {int(hours):02} horas, {int(minutes):02} minutos e {int(seconds):02} segundos.")

    return wrapper


def attempts(max_attempts=3, waiting_time=1):
    """Decorador que tenta executar uma função várias vezes antes de falhar."""

    def decorator(func):
        @wraps(func)
        async def wrapper_async(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.info(f"Attempt {attempt} of {max_attempts} failed. Error: {e}")
                    attempt += 1
                    await asyncio.sleep(waiting_time)
            raise Exception(f"Not possible to execute after {max_attempts} attempts.")

        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.info(f"Attempt {attempt} of {max_attempts} failed. Error: {e}")
                    attempt += 1
                    time.sleep(waiting_time)
            raise Exception(f"Not possible to execute after {max_attempts} attempts.")

        return wrapper_async if asyncio.iscoroutinefunction(func) else wrapper_sync

    return decorator


def run_on_business_day(_func=None, *, business_day=1, country="BR", state="GO", today=None, debug=False):
    """Decorador para executar a função apenas em um determinado dia útil do mês."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Optional[Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Optional[Any]:
            if debug:
                logging.info("Debug mode activated: function executed regardless of business day.")
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            holiday_list = holidays.country_holidays(country, subdiv=state)
            current_day = today or datetime.now().date()
            day_counter = datetime(current_day.year, current_day.month, 1).date()
            business_days_counted = 0

            while business_days_counted < business_day:
                if day_counter.weekday() < 5 and day_counter not in holiday_list:
                    business_days_counted += 1
                if business_days_counted < business_day:
                    day_counter += timedelta(days=1)

            if current_day == day_counter:
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            else:
                logging.info(f"Today ({current_day}) is not the {business_day} business day of the month. Execution cancelled.")
                return None

        return wrapper if asyncio.iscoroutinefunction(func) else func

    return decorator if _func is None else decorator(_func)
