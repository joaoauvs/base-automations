import logging
from math import ceil
from typing import Optional

import pandas as pd
from databricks import sql

from src.config.settings import DatabricksConfig, Settings


class Databricks:
    """
    Classe para gerenciar conexões e interações com o Databricks usando a biblioteca databricks.sql.
    Permite executar consultas SQL e inserir dados em tabelas do Databricks.

    Atributos:
        host (str): Host do Databricks, fornecido pelo ambiente.
        http_path (str): Caminho HTTP para acessar o SQL Warehouse.
        token (str): Token de acesso para autenticação no Databricks.
        connection: Objeto de conexão com o SQL Warehouse.
        cursor: Objeto cursor para executar comandos SQL.
    """

    def __init__(self, config: Optional[DatabricksConfig] = None):
        """
        Inicializa a classe com as informações do host, caminho HTTP e token de autenticação.

        Args:
            config (DatabricksConfig, opcional): Configuração explícita. Se não for informada,
                usa valores globais definidos em Settings.
        """
        self.config = config or Settings.databricks
        self.host = self.config.host
        self.http_path = self.config.http_path
        self.token = self.config.access_token

        self.connection = None
        self.cursor = None

    def open_connection(self):
        """
        Abre uma conexão com o Databricks SQL Warehouse.

        Cria um objeto de conexão e inicializa o cursor para execução de consultas.
        """
        self.connection = sql.connect(server_hostname=self.host, http_path=self.http_path, access_token=self.token)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """
        Fecha a conexão com o Databricks SQL Warehouse.

        Encerra o cursor e a conexão, garantindo que os recursos sejam liberados.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def run_query(self, query):
        """
        Executa uma consulta SQL no Databricks SQL Warehouse.

        Args:
            query (str): A consulta SQL a ser executada.

        Returns:
            pd.DataFrame: Os resultados da consulta em formato de DataFrame Pandas.
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        data = self.cursor.fetchall()
        return pd.DataFrame(data, columns=columns)

    def insert_data(self, table_name, dataframe, batch_size=10000):
        """
        Insere dados de um DataFrame em uma tabela do Databricks SQL Warehouse em lotes.

        Args:
            table_name (str): O nome da tabela onde os dados serão inseridos.
            dataframe (pd.DataFrame): O DataFrame contendo os dados a serem inseridos.
            batch_size (int): O número de linhas por lote (padrão: 10000).
        """
        # Substituir valores ausentes por None para compatibilidade com SQL
        dataframe = dataframe.replace({pd.NaT: None, pd.NA: None})

        # Converter o DataFrame para uma lista de tuplas
        data_tuples = [tuple(x) for x in dataframe.to_numpy()]

        # Gerar colunas para o comando SQL
        columns = ", ".join(dataframe.columns)

        total_batches = ceil(len(data_tuples) / batch_size)
        for batch_num in range(total_batches):
            # Dividir os dados em lotes
            start = batch_num * batch_size
            end = start + batch_size
            batch = data_tuples[start:end]
            # Montar os valores do lote em um único comando SQL
            values = ",\n".join([f"({', '.join(repr(value) if value is not None else 'NULL' for value in row)})" for row in batch])
            insert_statement = f"""
            INSERT INTO {table_name} ({columns})
            VALUES
            {values}
            """

            # Executar o comando para o lote inteiro
            self.cursor.execute(insert_statement)
            logging.info(f"Batch {batch_num + 1}/{total_batches} inserted successfully.")

    def optimize_table(self, table_name):
        """
        Otimiza uma tabela do Databricks.

        Args:
            table_name (str): Nome da tabela a ser otimizada.
        """
        query = f"OPTIMIZE {table_name}"
        self.cursor.execute(query)
