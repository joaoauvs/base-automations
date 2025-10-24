# Refatoração dos Módulos Python - Base Automations

## Resumo

Este documento descreve as melhorias aplicadas aos módulos do projeto base-automations, seguindo as boas práticas do Python e princípios de Programação Orientada a Objetos (POO).

## Objetivos da Refatoração

1. **Aplicar Type Hints completos** em todos os módulos
2. **Padronizar Docstrings** no estilo Google
3. **Melhorar tratamento de exceções** (remover bare excepts)
4. **Implementar uso de variáveis de ambiente** para credenciais
5. **Aplicar princípios SOLID**
6. **Seguir PEP 8** rigorosamente
7. **Adicionar constantes e Enums** onde apropriado
8. **Corrigir bugs** identificados

## Mudanças por Módulo

### 1. common.py
**Melhorias aplicadas:**
- ✅ Type hints completos com TypeVar para genericidade
- ✅ Docstrings detalhadas estilo Google com exemplos
- ✅ Melhor error handling com exceções específicas
- ✅ Mensagens de log mais informativas
- ✅ Tratamento de exceção anterior (exception chaining)

**Novos recursos:**
- Captura da última exceção em decoradores de retry
- Mensagens de erro mais descritivas

### 2. log.py
**Melhorias aplicadas:**
- ✅ Renomeado para `LogManager` (classe mais descritiva)
- ✅ Uso de `pathlib.Path` ao invés de concatenação de strings
- ✅ Remoção de handlers duplicados
- ✅ Type hints completos
- ✅ Novos métodos: `delete_old_logs()`, `get_log_size()`
- ✅ Parâmetros configuráveis (level, file_mode, encoding)
- ✅ `__repr__` para melhor debugging

**Compatibilidade:**
- Mantido alias `Log = LogManager` para código legado

### 3. email.py
**Melhorias aplicadas:**
- ✅ Renomeado para `EmailNotifier` (mais descritivo)
- ✅ **Uso de variáveis de ambiente** para credenciais:
  - `EMAIL_SENDER`
  - `EMAIL_PASSWORD`
  - `EMAIL_FAILURE_RECIPIENT`
  - `EMAIL_SMTP_SERVER`
- ✅ Caminhos crossplatform usando `pathlib.Path`
- ✅ Tratamento de exceções específicas (SMTPAuthenticationError, SMTPException)
- ✅ Novo método `send_custom_email()` para emails personalizados
- ✅ Context manager para conexão SMTP
- ✅ Validação de credenciais antes do envio

**Compatibilidade:**
- Mantida classe `Email` herdando de `EmailNotifier`
- Método `send_email_fail()` deprecated mas funcional

### 4. validate.py
**Melhorias aplicadas:**
- ✅ Renomeado para `Validator`
- ✅ Implementação completa de validação de CNPJ e CPF
- ✅ Novos validadores:
  - `validate_cpf()` - Valida e formata CPF
  - `validate_email()` - Valida email com regex
  - `validate_phone()` - Valida e formata telefone brasileiro
- ✅ Método `is_valid_date_range()` com formato configurável
- ✅ `validate_dictionary()` com campos obrigatórios específicos
- ✅ Type hints completos
- ✅ Raises explícitos em docstrings

**Compatibilidade:**
- Classe `Validate` mantida para compatibilidade
- Métodos privados `_generate_first_digit()` e `_generate_second_digit()` mantidos

### 5. convert.py
**Melhorias aplicadas:**
- ✅ Renomeado para `DateConverter`
- ✅ **Constantes para meses** (MONTHS_FULL, MONTHS_ABBREV_MAP)
- ✅ Nomes de métodos mais descritivos:
  - `to_first_day_of_month()`
  - `to_last_day_of_month()`
  - `to_year_and_month_name()`
  - `expand_month_name()`
- ✅ Novos métodos utilitários:
  - `get_month_name()` - Retorna nome do mês por número
  - `get_month_number()` - Retorna número do mês por abreviação
- ✅ Error handling robusto com mensagens claras
- ✅ Formato de entrada configurável

**Compatibilidade:**
- Classe `Conversions` mantida como alias

### 6. captcha.py
**Melhorias aplicadas:**
- ✅ Renomeado para `CaptchaSolver`
- ✅ **Uso de variável de ambiente** `TWOCAPTCHA_API_KEY`
- ✅ Tratamento de exceções específicas:
  - `ApiException`
  - `NetworkException`
  - `TimeoutException`
- ✅ Novos métodos:
  - `solve_image_from_url()` (renomeado e melhorado)
  - `solve_image_from_file()` (com validação de arquivo)
  - `solve_recaptcha_v3()` (suporte a reCAPTCHA v3)
  - `get_balance()` (consulta saldo da conta)
- ✅ Logging detalhado
- ✅ Mascaramento de API key em __repr__
- ✅ Validação de arquivo antes de processar

**Compatibilidade:**
- Classe `Captcha` mantida com comportamento legado
- Permite inicialização sem API key (com warning)

### 7. excelstyler.py
**Melhorias aplicadas:**
- ✅ Renomeado para `ExcelFormatter`
- ✅ **Remoção de bare except** - substituído por tratamento específico
- ✅ Type hints usando `Worksheet` do openpyxl
- ✅ Parâmetros configuráveis (min_width, max_width, border_style)
- ✅ Novo método `apply_header_style()` para formatar cabeçalhos
- ✅ Método `center_text_in_cells()` unificado com parâmetro opcional exclude_columns
- ✅ Logging de erros apropriado

**Compatibilidade:**
- Classe `ExcelStyler` mantida
- Método `center_text_in_cells_except()` deprecated

### 8. main.py
**Bugs corrigidos:**
- ✅ Adicionado `__init__()` à classe Bot com atributo `cnpj`
- ✅ Removido uso incorreto de `asyncio.run()` em função síncrona
- ✅ Adicionada inicialização do `LogManager`
- ✅ Tratamento adequado do navegador no finally
- ✅ Verificação de `self.navegador` antes de chamar `.quit()`
- ✅ Melhor estrutura com função `main()` separada

**Melhorias:**
- ✅ Type hints completos
- ✅ Docstrings adequadas
- ✅ Separação de responsabilidades
- ✅ Error handling robusto

## Novos Arquivos

### .env.example
Arquivo de exemplo com todas as variáveis de ambiente necessárias:
- Configurações de email (SMTP, credenciais)
- API keys (2Captcha)
- Configurações do sistema
- Diretórios padrão
- Configurações opcionais

## Princípios Aplicados

### SOLID
- **S**ingle Responsibility: Cada classe tem uma responsabilidade única
- **O**pen/Closed: Classes abertas para extensão, fechadas para modificação
- **L**iskov Substitution: Classes legadas podem substituir novas classes
- **I**nterface Segregation: Métodos específicos e bem definidos
- **D**ependency Inversion: Uso de injeção de dependências (ex: api_key via parâmetro ou env)

### PEP 8
- Nomenclatura adequada (snake_case para funções, PascalCase para classes)
- Imports organizados
- Linhas com máximo 88-100 caracteres
- Docstrings formatadas corretamente

### Type Safety
- Type hints em todos os métodos e funções
- Uso de `Optional`, `Union`, `List`, `Dict`, `Tuple`
- TypeVar para genericidade em decoradores

### Error Handling
- Exceções específicas ao invés de bare except
- Exception chaining com `from e`
- Logging apropriado de erros
- Mensagens descritivas

## Compatibilidade com Código Legado

Todas as refatorações mantêm **compatibilidade total** com código existente através de:

1. **Classes Alias**: Classes antigas herdam das novas
   ```python
   class Email(EmailNotifier):  # Mantém compatibilidade
       ...
   ```

2. **Métodos Deprecated**: Métodos antigos redirecionam para novos
   ```python
   def send_email_fail(self):
       return self.send_failure_notification()
   ```

3. **Comportamento Preservado**: Mesmo sem configuração, o código não quebra
   - Credenciais opcionais com warnings
   - Valores padrão sensatos
   - Tratamento gracioso de erros

## Como Migrar para Novas Classes

### Exemplo: Email
```python
# Código antigo (ainda funciona)
from resources.modules.email import Email
notifier = Email("MeuRobo")
notifier.send_email_fail()

# Código novo (recomendado)
from resources.modules.email import EmailNotifier
notifier = EmailNotifier(robot_name="MeuRobo", log_path="/path/to/log")
notifier.send_failure_notification()
```

### Exemplo: Validação
```python
# Código antigo (ainda funciona)
from resources.modules.validate import Validate
cnpj = Validate.validate_cnpj("12345678000190")

# Código novo (recomendado)
from resources.modules.validate import Validator
cnpj = Validator.validate_cnpj("12345678000190")
cpf = Validator.validate_cpf("12345678909")  # Novo método!
```

## Configuração Necessária

### 1. Criar arquivo .env
```bash
cp .env.example .env
```

### 2. Preencher variáveis de ambiente
Edite `.env` com suas credenciais reais:
```env
EMAIL_SENDER=seu_email@exemplo.com
EMAIL_PASSWORD=sua_senha
EMAIL_FAILURE_RECIPIENT=destinatario@exemplo.com
TWOCAPTCHA_API_KEY=sua_chave_aqui
```

### 3. Instalar dependências (se necessário)
```bash
pip install -r requirements.txt
```

## Benefícios das Mudanças

1. **Segurança**: Credenciais não estão mais hardcoded
2. **Manutenibilidade**: Código mais legível e documentado
3. **Type Safety**: Menos erros em tempo de execução
4. **Extensibilidade**: Mais fácil adicionar novos recursos
5. **Testabilidade**: Código mais testável com dependências injetáveis
6. **Profissionalismo**: Código segue padrões da indústria

## Próximos Passos Recomendados

1. ✅ Migrar código existente para usar novas classes
2. ✅ Adicionar testes unitários
3. ✅ Implementar CI/CD
4. ✅ Adicionar type checking com mypy
5. ✅ Implementar linting com pylint/flake8
6. ✅ Adicionar pre-commit hooks

## Conclusão

Esta refatoração moderniza o código base seguindo as melhores práticas do Python, mantendo 100% de compatibilidade com código legado. O código está mais seguro, mais fácil de manter e pronto para crescer.
