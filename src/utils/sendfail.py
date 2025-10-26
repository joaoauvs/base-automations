import logging
import os
import socket

import requests

from src.config.settings import ExecutionMode


@staticmethod
def send_fail_message(bot, mode, message=None):
    """Envia uma mensagem de erro para o fluxo do Power Automate.

    Args:
        url (str): URL do fluxo do Power Automate.
        bot (str): Nome do bot.
        message (str): Mensagem de erro.
    """

    if message is None:
        message = "Falha durante o processamento."

    if mode is not ExecutionMode.PRODUCTION.value:
        logging.info(f"Modo: {mode}, Bot: {bot}, Mensagem: {message}")
        return True

    # Dados do dispositivo
    nome_usuario = os.getlogin()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Dados a serem enviados
    payload = {
        "bot": bot,
        "error_message": message,
        "device_info": {
            "user": nome_usuario,
            "hostname": hostname,
            "ip_address": ip_address,
        },
    }
    # Envio do payload para o Power Automate
    try:
        response = requests.post(
            url="https://527c349fb787e6d7b0dcfe0dab4775.e8.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/37da68adb9e248c184f7e205555b5d2b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9E_ooioiioiouioiuoioioouio",
            json=payload,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response.status_code == 200
