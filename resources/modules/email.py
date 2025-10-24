"""Módulo para envio de emails com notificações de erro.

Este módulo fornece funcionalidade para envio de emails automáticos
incluindo anexos de logs para notificação de falhas em processos RPA.
"""

import logging
import os
import smtplib
import socket
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import List, Optional


class EmailNotifier:
    """Notificador de emails para processos RPA.

    Envia emails de notificação com anexos de log quando ocorrem falhas
    em processos automatizados.

    Attributes:
        robot_name: Nome do robô/processo RPA.
        worker_ip: IP da máquina que está executando o processo.
        log_path: Caminho do arquivo de log.
        smtp_server: Servidor SMTP para envio de emails.
        smtp_port: Porta do servidor SMTP.

    Example:
        >>> notifier = EmailNotifier(
        ...     robot_name="ProcessadorNFe",
        ...     log_path="/var/logs/app/2024-01-15.log"
        ... )
        >>> notifier.send_failure_notification()
    """

    def __init__(
        self,
        robot_name: str,
        log_path: Optional[str] = None,
        smtp_server: Optional[str] = None,
        smtp_port: int = 465
    ) -> None:
        """Inicializa o notificador de emails.

        Args:
            robot_name: Nome do robô/processo RPA.
            log_path: Caminho do arquivo de log. Se None, usa padrão baseado em robot_name.
            smtp_server: Servidor SMTP. Se None, usa variável de ambiente EMAIL_SMTP_SERVER.
            smtp_port: Porta SMTP (padrão: 465 para SSL).

        Raises:
            ValueError: Se configurações obrigatórias estiverem ausentes.
        """
        self.robot_name = str(robot_name).strip()
        if not self.robot_name:
            raise ValueError("O nome do robô não pode ser vazio")

        # Configurações do email (variáveis de ambiente ou valores padrão)
        self._sender_email = os.getenv("EMAIL_SENDER", "")
        self._sender_password = os.getenv("EMAIL_PASSWORD", "")
        self._failure_recipient = os.getenv("EMAIL_FAILURE_RECIPIENT", "")
        self.smtp_server = smtp_server or os.getenv("EMAIL_SMTP_SERVER", "smtp.hostinger.com")
        self.smtp_port = smtp_port

        # Validação das credenciais
        if not all([self._sender_email, self._sender_password, self._failure_recipient]):
            logging.warning(
                "Credenciais de email não configuradas. "
                "Configure as variáveis de ambiente: EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_FAILURE_RECIPIENT"
            )

        # Informações do sistema
        try:
            self.worker_ip = socket.gethostbyname(socket.gethostname())
        except socket.error:
            self.worker_ip = "IP desconhecido"
            logging.warning("Não foi possível obter o IP da máquina")

        # Configuração do caminho do log
        if log_path:
            self.log_path = Path(log_path)
        else:
            # Caminho padrão (crossplatform)
            base_dir = Path.home() / "RPA" / self.robot_name / "logs"
            current_date = datetime.now().strftime("%d-%m-%Y")
            self.log_path = base_dir / f"{current_date}.log"

        self.current_date = datetime.today().strftime("%d/%m/%Y")

    def _create_failure_message(self) -> EmailMessage:
        """Cria mensagem de email de falha.

        Returns:
            EmailMessage configurada com assunto e corpo.
        """
        msg = EmailMessage()
        msg["Subject"] = f"{self.worker_ip}:{self.robot_name.upper()} (Apresentou Erro)"
        msg["From"] = self._sender_email
        msg["To"] = self._failure_recipient

        corpo_email = f"""Olá,

O processo RPA '{self.robot_name}' apresentou erro durante a execução.

Detalhes:
- Data/Hora: {self.current_date} {datetime.now().strftime("%H:%M:%S")}
- Máquina: {self.worker_ip}
- Processo: {self.robot_name}

Segue o arquivo de log em anexo para análise.

Atenciosamente,
Sistema Automatizado de Monitoramento
"""
        msg.set_content(corpo_email)
        return msg

    def _attach_log_file(self, msg: EmailMessage) -> None:
        """Anexa arquivo de log à mensagem de email.

        Args:
            msg: Mensagem de email onde o log será anexado.

        Raises:
            FileNotFoundError: Se o arquivo de log não existir.
            OSError: Se houver erro ao ler o arquivo.
        """
        if not self.log_path.exists():
            raise FileNotFoundError(f"Arquivo de log não encontrado: {self.log_path}")

        try:
            with open(self.log_path, "r", encoding="utf-8") as log_file:
                log_content = log_file.read()
                msg.add_attachment(
                    log_content,
                    filename=f"{self.robot_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                )
                logging.info(f"Log anexado: {self.log_path}")
        except OSError as e:
            raise OSError(f"Erro ao ler arquivo de log '{self.log_path}': {e}") from e

    def send_failure_notification(self, attach_log: bool = True) -> None:
        """Envia email de notificação de falha.

        Args:
            attach_log: Se True, anexa o arquivo de log ao email.

        Raises:
            ValueError: Se as credenciais não estiverem configuradas.
            smtplib.SMTPException: Se houver erro ao enviar o email.
            FileNotFoundError: Se attach_log=True e o arquivo não existir.
        """
        if not all([self._sender_email, self._sender_password, self._failure_recipient]):
            raise ValueError(
                "Credenciais de email não configuradas. "
                "Configure as variáveis de ambiente: EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_FAILURE_RECIPIENT"
            )

        try:
            msg = self._create_failure_message()

            if attach_log:
                self._attach_log_file(msg)

            # Envia o email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self._sender_email, self._sender_password)
                smtp.send_message(msg)

            logging.info(f"Email de falha enviado com sucesso para {self._failure_recipient}")

        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"Erro de autenticação SMTP: {e}")
            raise
        except smtplib.SMTPException as e:
            logging.error(f"Erro ao enviar email: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado ao enviar email: {e}")
            raise

    def send_custom_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> None:
        """Envia email customizado.

        Args:
            recipient: Email do destinatário.
            subject: Assunto do email.
            body: Corpo do email.
            attachments: Lista de caminhos de arquivos para anexar.

        Raises:
            ValueError: Se as credenciais não estiverem configuradas.
            smtplib.SMTPException: Se houver erro ao enviar o email.
        """
        if not all([self._sender_email, self._sender_password]):
            raise ValueError("Credenciais de email não configuradas")

        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self._sender_email
            msg["To"] = recipient
            msg.set_content(body)

            # Anexa arquivos se fornecidos
            if attachments:
                for file_path in attachments:
                    path = Path(file_path)
                    if path.exists():
                        with open(path, "rb") as f:
                            msg.add_attachment(
                                f.read(),
                                maintype="application",
                                subtype="octet-stream",
                                filename=path.name
                            )

            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self._sender_email, self._sender_password)
                smtp.send_message(msg)

            logging.info(f"Email enviado com sucesso para {recipient}")

        except smtplib.SMTPException as e:
            logging.error(f"Erro ao enviar email customizado: {e}")
            raise

    def __repr__(self) -> str:
        """Representação em string do objeto EmailNotifier."""
        return f"EmailNotifier(robot_name='{self.robot_name}', log_path='{self.log_path}')"


# Mantém compatibilidade com código legado
class Email(EmailNotifier):
    """Classe de compatibilidade com código legado.

    Deprecated: Use EmailNotifier diretamente.
    """

    def __init__(self, robo: str = "RPA_Process", **kwargs) -> None:
        """Inicializa Email (compatibilidade legado).

        Args:
            robo: Nome do robô.
            **kwargs: Argumentos adicionais passados para EmailNotifier.
        """
        super().__init__(robot_name=robo, **kwargs)
        logging.warning("A classe 'Email' está deprecated. Use 'EmailNotifier' diretamente.")

    def send_email_fail(self) -> None:
        """Envia email de falha (compatibilidade legado).

        Deprecated: Use send_failure_notification().
        """
        try:
            self.send_failure_notification(attach_log=True)
        except Exception as e:
            logging.error(f"Erro ao enviar email de falha: {e}")
            # Não propaga a exceção para manter compatibilidade com código legado
            pass
