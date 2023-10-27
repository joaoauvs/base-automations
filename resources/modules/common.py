import logging
from datetime import datetime
from functools import wraps


def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(f"🕐 Execução iniciada às: {start_time.strftime('%H:%M:%S')}")
        logging.info(f"🕐 Execução iniciada às: {start_time.strftime('%H:%M:%S')}")

        result = func(*args, **kwargs)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"🕞 Tempo de execução: {int(hours):02} horas, {int(minutes):02} minutos e {int(seconds):02} segundos.")
        logging.info(f"🕞 Tempo de execução: {int(hours):02} horas, {int(minutes):02} minutos e {int(seconds):02} segundos.")

        return result
    return wrapper