import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from functools import wraps


def get_message():
    """Recupera a mensagem do input e a converte em um dicionário.

    Returns:
        dict: Mensagem convertida em dicionário.
    """
    return json.loads(sys.stdin.read())


def time_execution(func):
    """Decorador que mede o tempo de execução de uma função.

    Args:
        func (callable): A função para medir o tempo de execução.

    Returns:
        callable: A função wrapper que adiciona a medição do tempo.
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
    """Decorador que tenta executar uma função várias vezes antes de falhar.

    Args:
        max_attempts (int): Número máximo de tentativas.
        waiting_time (int): Tempo de espera entre tentativas.

    Returns:
        callable: A função wrapper que adiciona a tentativa de repetição.
    """

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
