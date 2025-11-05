# Base Automations

Sistema base para automações RPA (Robotic Process Automation) em Python, com foco em boas práticas, type safety e código limpo.

## 📋 Descrição

Este projeto fornece uma base sólida e reutilizável para desenvolvimento de automações RPA, incluindo:

- **Módulos de automação web** com Selenium e Undetected ChromeDriver
- **Sistema de logging** configurável e robusto
- **Utilitários para manipulação de arquivos** Excel, CSV e gerenciamento de downloads
- **Sistema de notificação por email** para monitoramento de execução
- **Validadores** de CPF, CNPJ, email e telefone
- **Resolução de captchas** integrada com 2Captcha
- **Decoradores úteis** para retry, medição de tempo e tratamento de erros
- **Integração com Azure Key Vault** para gerenciamento seguro de credenciais
- **Integração com Databricks** para operações de dados

## 🚀 Principais Características

- ✅ **Type hints completos** em todos os módulos
- ✅ **Docstrings padronizadas** no estilo Google
- ✅ **Tratamento robusto de exceções** sem bare excepts
- ✅ **Azure Key Vault** para gerenciamento seguro de credenciais (com fallback para .env)
- ✅ **Variáveis de ambiente** para credenciais sensíveis
- ✅ **Princípios SOLID** aplicados
- ✅ **Compatibilidade com código legado** através de classes alias
- ✅ **PEP 8 compliant**

## 📦 Estrutura do Projeto

```
base-automations/
├── src/
│   ├── modules/          # Módulos principais
│   │   ├── web/         # Automação web (Selenium)
│   │   │   ├── webdriver.py      # Gerenciamento de drivers
│   │   │   └── driveroptions.py  # Configurações de drivers
│   │   ├── base.py      # Classes base para automações
│   │   ├── captcha.py   # Resolução de captchas
│   │   ├── common.py    # Decoradores e utilitários comuns
│   │   ├── convert.py   # Conversão de datas
│   │   ├── email.py     # Notificações por email
│   │   ├── excelstyler.py # Formatação de Excel
│   │   ├── file.py      # Manipulação de arquivos
│   │   ├── log.py       # Sistema de logging
│   │   └── validate.py  # Validadores
│   ├── config/          # Configurações
│   │   ├── keyvault.py  # Integração com Azure Key Vault
│   │   └── settings.py  # Configurações gerais
│   ├── core/            # Funcionalidades core
│   │   └── log.py       # Sistema de logging core
│   └── utils/           # Utilitários diversos
│       ├── databricks.py    # Integração com Databricks
│       ├── decorators.py    # Decoradores úteis
│       ├── platform_utils.py # Utilitários de plataforma
│       └── sendfail.py      # Notificações de falha
├── main.py              # Script principal de exemplo
├── mainweb.py           # Exemplo de automação web
├── .env.example         # Exemplo de variáveis de ambiente
├── requirements.txt     # Dependências do projeto
├── REFACTORING.md       # Documentação detalhada da refatoração
└── README.md            # Este arquivo
```

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/joaoauvs/base-automations.git
cd base-automations
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### Principais dependências:

- **Automação Web:** selenium, undetected-chromedriver, webdriver-manager
- **Manipulação de Dados:** pandas, openpyxl, xlsxwriter
- **Azure:** azure-keyvault-secrets, azure-identity
- **Databricks:** databricks-sql-connector
- **Captcha:** 2captcha-python
- **Configuração:** python-dotenv
- **Logging:** loguru
- **Desenvolvimento:** pytest, black, flake8, mypy

## ⚙️ Configuração

Este projeto suporta duas formas de gerenciar credenciais:

### Opção 1: Azure Key Vault (Recomendado para Produção) 🔐

O Azure Key Vault fornece armazenamento seguro e gerenciamento centralizado de credenciais.

#### 1.1. Configure o Key Vault

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
# Habilitar Azure Key Vault
USE_AZURE_KEYVAULT=true

# URL do seu Key Vault
AZURE_KEYVAULT_URL=https://seu-keyvault.vault.azure.net/

# Credenciais do Service Principal (se não usar Managed Identity)
AZURE_CLIENT_ID=seu_client_id
AZURE_TENANT_ID=seu_tenant_id
AZURE_CLIENT_SECRET=seu_client_secret
```

#### 1.2. Configure os segredos no Key Vault

Os segredos devem ter os seguintes nomes (use hyphens):
- `EMAIL-SENDER`
- `EMAIL-PASSWORD`
- `EMAIL-FAILURE-RECIPIENT`
- `EMAIL-SMTP-SERVER`
- `TWOCAPTCHA-API-KEY`
- `DATABRICKS-HOST`
- `DATABRICKS-HTTP-PATH`
- `DATABRICKS-ACCESS-TOKEN`

### Opção 2: Variáveis de Ambiente (.env)

Para desenvolvimento local ou quando Key Vault não está disponível:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Desabilitar Azure Key Vault
USE_AZURE_KEYVAULT=false

# Configurações de Email
EMAIL_SMTP_SERVER=smtp.hostinger.com
EMAIL_SENDER=seu_email@exemplo.com
EMAIL_PASSWORD=sua_senha_aqui
EMAIL_FAILURE_RECIPIENT=destinatario@exemplo.com

# 2Captcha API Key
TWOCAPTCHA_API_KEY=sua_chave_2captcha_aqui

# Outras configurações
ROBOT_NAME=ProcessadorRPA
ENVIRONMENT=development
LOG_LEVEL=INFO
```

> ⚠️ **IMPORTANTE:** Nunca commite o arquivo `.env` com credenciais reais!

## 🎯 Uso Básico

### Exemplo 1: Bot RPA Simples

```python
from src.modules.common import attempts, time_execution
from src.modules.log import LogManager
from src.modules.web.webdriver import Browser, WebDriver

# Configurar logging
log_manager = LogManager(path="./logs/")

# Criar navegador
navegador = WebDriver.get_navegador(
    Browser.UNDETECTED_CHROME,
    headless=False
)

try:
    # Sua automação aqui
    navegador.get("https://exemplo.com")
    # ... suas operações ...
finally:
    navegador.quit()
```

### Exemplo 2: Usando Decoradores

```python
from src.modules.common import attempts, time_execution

@time_execution
@attempts(max_attempts=3, waiting_time=2)
def minha_funcao():
    # Função será executada com retry automático
    # e medição de tempo de execução
    pass
```

### Exemplo 3: Validação de Documentos

```python
from src.modules.validate import Validator

# Validar CNPJ
cnpj_valido = Validator.validate_cnpj("12.345.678/0001-90")

# Validar CPF
cpf_valido = Validator.validate_cpf("123.456.789-09")

# Validar Email
email_valido = Validator.validate_email("usuario@exemplo.com")
```

### Exemplo 4: Manipulação de Arquivos

```python
from src.modules.file import File

# Aguardar download
File.wait_for_download("./downloads", timeout=30)

# Ler arquivo Excel
df = File.read_excel("./data/arquivo.xlsx")

# Mover arquivos por extensão
File.move_files_by_extension("./downloads", "./processados", ".pdf")
```

## 📧 Sistema de Notificações

```python
from src.modules.email import EmailNotifier

# Criar notificador
notifier = EmailNotifier(
    robot_name="MeuRobo",
    log_path="./logs/robot.log"
)

# Enviar notificação de falha
try:
    # ... seu código ...
    pass
except Exception as e:
    notifier.send_failure_notification()
```

## 🔍 Resolução de Captchas

```python
from src.modules.captcha import CaptchaSolver

# Criar solver (usa TWOCAPTCHA_API_KEY do .env)
solver = CaptchaSolver()

# Resolver captcha de imagem
solution = solver.solve_image_from_url("https://exemplo.com/captcha.png")

# Resolver reCAPTCHA v2
recaptcha_solution = solver.solve_recaptcha_v2(
    "site_key_aqui",
    "https://exemplo.com"
)
```

## 🔐 Azure Key Vault

### Uso Básico

```python
from src.config.keyvault import KeyVaultClient, get_keyvault_client

# Opção 1: Usar singleton (recomendado)
client = get_keyvault_client()

# Buscar um segredo
email_password = client.get_secret("EMAIL-PASSWORD")

# Buscar múltiplos segredos
secrets = client.get_all_secrets([
    "EMAIL-SENDER",
    "EMAIL-PASSWORD",
    "TWOCAPTCHA-API-KEY"
])

# Opção 2: Criar cliente diretamente
client = KeyVaultClient("https://seu-keyvault.vault.azure.net/")
password = client.get_secret("EMAIL-PASSWORD")
```

### Fallback Automático

O KeyVault suporta fallback automático para variáveis de ambiente:

```python
from src.config.keyvault import get_keyvault_client

client = get_keyvault_client()

# Tenta Key Vault primeiro, depois EMAIL_SENDER do .env
email = client.get_secret_with_fallback("EMAIL-SENDER", "EMAIL_SENDER")
```

### Autenticação

O KeyVaultClient suporta múltiplos métodos de autenticação (em ordem de prioridade):

1. **Managed Identity** (recomendado para Azure VMs/Functions/App Services)
2. **Service Principal** (via variáveis de ambiente AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
3. **Azure CLI** (se autenticado via `az login`)
4. **Visual Studio Code** (se autenticado)
5. **Azure PowerShell** (se autenticado)

## 📊 Integração com Databricks

O projeto inclui utilitários para integração com Databricks:

```python
from src.utils.databricks import DatabricksClient

# Criar cliente (usa credenciais do .env ou Key Vault)
client = DatabricksClient(
    host=os.getenv("DATABRICKS_HOST"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_ACCESS_TOKEN")
)

# Executar query
result = client.execute_query("SELECT * FROM my_table LIMIT 10")

# Trabalhar com os resultados
for row in result:
    print(row)
```

## 📚 Documentação Adicional

Para informações detalhadas sobre a refatoração e melhorias aplicadas, consulte:

- [REFACTORING.md](REFACTORING.md) - Documentação completa das mudanças e melhorias

## 🛠️ Desenvolvimento

### Executando o projeto

```bash
python main.py
```

### Estrutura de um Bot

1. Inicialize o `LogManager`
2. Crie seu bot herdando de uma classe base ou criando do zero
3. Use os decoradores `@time_execution` e `@attempts` conforme necessário
4. Implemente tratamento de erros adequado
5. Envie notificações em caso de falha

## 🔐 Segurança

- ✅ **Azure Key Vault** para gerenciamento seguro de credenciais em produção
- ✅ **Fallback automático** para variáveis de ambiente durante desenvolvimento
- ✅ **Múltiplos métodos de autenticação** (Managed Identity, Service Principal, Azure CLI)
- ✅ **Cache de segredos** para reduzir chamadas ao Key Vault
- ✅ Credenciais armazenadas em variáveis de ambiente como fallback
- ✅ Arquivo `.env` incluído no `.gitignore`
- ✅ Exemplo `.env.example` fornecido sem dados sensíveis
- ✅ Logs de API keys são mascarados
- ✅ Suporte a diferentes ambientes (development, staging, production)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código

- Siga PEP 8
- Adicione type hints em todas as funções
- Documente usando docstrings no estilo Google
- Evite bare excepts
- Use variáveis de ambiente para credenciais

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

**João Vitor**

- GitHub: [@joaoauvs](https://github.com/joaoauvs)

## 🙏 Agradecimentos

- Selenium WebDriver
- Undetected ChromeDriver
- 2Captcha
- Microsoft Azure (Key Vault e Identity)
- Databricks
- Comunidade Python

## 📝 Changelog

### Versão 2.0.0 (Atual)
- ✨ Adicionada integração com Azure Key Vault para gerenciamento seguro de credenciais
- ✨ Implementado sistema de fallback automático (Key Vault → .env)
- ✨ Adicionada integração com Databricks
- ✨ Melhorias na estrutura de configuração com módulo `config/`
- ✨ Adicionados utilitários de plataforma (Windows/Linux)
- ✨ Documentação completa atualizada
- 🔒 Segurança aprimorada com suporte a Managed Identity
- 📦 Dependências atualizadas no requirements.txt

### Versão 1.0.0
- 🎉 Release inicial com refatoração completa
- ✅ Type hints e docstrings padronizadas
- ✅ Módulos de automação web, email, captcha, validação
- ✅ Sistema de logging robusto
- ✅ Suporte a variáveis de ambiente

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação](REFACTORING.md)
2. Abra uma [issue](https://github.com/joaoauvs/base-automations/issues)
3. Consulte os exemplos no código

---

Desenvolvido com ❤️ para a comunidade RPA
