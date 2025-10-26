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

## 🚀 Principais Características

- ✅ **Type hints completos** em todos os módulos
- ✅ **Docstrings padronizadas** no estilo Google
- ✅ **Tratamento robusto de exceções** sem bare excepts
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
│   │   ├── captcha.py   # Resolução de captchas
│   │   ├── common.py    # Decoradores e utilitários comuns
│   │   ├── convert.py   # Conversão de datas
│   │   ├── email.py     # Notificações por email
│   │   ├── excelstyler.py # Formatação de Excel
│   │   ├── file.py      # Manipulação de arquivos
│   │   ├── log.py       # Sistema de logging
│   │   └── validate.py  # Validadores
│   ├── config/          # Configurações
│   ├── core/            # Funcionalidades core
│   └── utils/           # Utilitários diversos
├── main.py              # Script principal de exemplo
├── .env.example         # Exemplo de variáveis de ambiente
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

> **Nota:** Se o arquivo `requirements.txt` não existir, instale as dependências principais:
> ```bash
> pip install selenium undetected-chromedriver webdriver-manager
> pip install openpyxl pandas numpy
> pip install python-dotenv
> pip install twocaptcha-python
> ```

## ⚙️ Configuração

### 1. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

### 2. Edite o arquivo `.env`

```env
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

- ✅ Credenciais armazenadas em variáveis de ambiente
- ✅ Arquivo `.env` incluído no `.gitignore`
- ✅ Exemplo `.env.example` fornecido sem dados sensíveis
- ✅ Logs de API keys são mascarados

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
- Comunidade Python

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação](REFACTORING.md)
2. Abra uma [issue](https://github.com/joaoauvs/base-automations/issues)
3. Consulte os exemplos no código

---

Desenvolvido com ❤️ para a comunidade RPA
