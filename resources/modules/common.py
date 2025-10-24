"""Módulo com utilitários comuns e decoradores para automação.

Este módulo fornece decoradores e funções utilitárias para medição de tempo,
retry de operações e leitura de mensagens do stdin.
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, TypeVar, Union

# Type variables para type hints genéricos
F = TypeVar('F', bound=Callable[..., Any])


def get_message() -> Dict[str, Any]:
    """Recupera mensagem do stdin e converte em dicionário.

    Returns:
        Dict[str, Any]: Mensagem convertida em dicionário.

    Raises:
        json.JSONDecodeError: Se a entrada não for um JSON válido.
        ValueError: Se houver erro ao ler a entrada.
    """
    try:
        input_data = sys.stdin.read()
        return json.loads(input_data)
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar JSON da entrada: {e}")
        raise
    except Exception as e:
        logging.error(f"Erro ao ler mensagem: {e}")
        raise ValueError(f"Erro ao processar entrada: {e}") from e


def time_execution(func: F) -> F:
    """Decorador que mede e registra o tempo de execução de uma função.

    Suporta tanto funções síncronas quanto assíncronas. Registra o horário de
    início, fim e duração total da execução.

    Args:
        func: Função a ser decorada (síncrona ou assíncrona).

    Returns:
        Função decorada com medição de tempo.

    Example:
        >>> @time_execution
        ... def my_function():
        ...     # código aqui
        ...     pass
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = datetime.now()
        logging.info(f"Execução iniciada às: {start_time.strftime('%H:%M:%S')}")

        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Exceção ocorreu durante execução: {type(e).__name__}: {e}")
            raise
        finally:
            end_time = datetime.now()
            elapsed_time = end_time - start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            logging.info(f"Execução finalizada às: {end_time.strftime('%H:%M:%S')}")
            logging.info(
                f"Tempo de execução: {int(hours):02}h {int(minutes):02}m {int(seconds):02}s"
            )

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = datetime.now()
        logging.info(f"Execução iniciada às: {start_time.strftime('%H:%M:%S')}")

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Exceção ocorreu durante execução: {type(e).__name__}: {e}")
            raise
        finally:
            end_time = datetime.now()
            elapsed_time = end_time - start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            logging.info(f"Execução finalizada às: {end_time.strftime('%H:%M:%S')}")
            logging.info(
                f"Tempo de execução: {int(hours):02}h {int(minutes):02}m {int(seconds):02}s"
            )

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper  # type: ignore


def attempts(max_attempts: int = 3, waiting_time: Union[int, float] = 1) -> Callable[[F], F]:
    """Decorador que tenta executar uma função múltiplas vezes antes de falhar.

    Suporta tanto funções síncronas quanto assíncronas. Aguarda um tempo
    configurável entre tentativas.

    Args:
        max_attempts: Número máximo de tentativas (padrão: 3).
        waiting_time: Tempo de espera em segundos entre tentativas (padrão: 1).

    Returns:
        Decorador configurado com as tentativas especificadas.

    Raises:
        Exception: Após esgotar todas as tentativas.

    Example:
        >>> @attempts(max_attempts=5, waiting_time=2)
        ... def unstable_function():
        ...     # código que pode falhar
        ...     pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.warning(
                        f"Tentativa {attempt}/{max_attempts} falhou. "
                        f"Erro: {type(e).__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        await asyncio.sleep(waiting_time)

            error_msg = (
                f"Não foi possível executar após {max_attempts} tentativas. "
                f"Último erro: {type(last_exception).__name__}: {last_exception}"
            )
            logging.error(error_msg)
            raise Exception(error_msg) from last_exception

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.warning(
                        f"Tentativa {attempt}/{max_attempts} falhou. "
                        f"Erro: {type(e).__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(waiting_time)

            error_msg = (
                f"Não foi possível executar após {max_attempts} tentativas. "
                f"Último erro: {type(last_exception).__name__}: {last_exception}"
            )
            logging.error(error_msg)
            raise Exception(error_msg) from last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper  # type: ignore

    return decorator
