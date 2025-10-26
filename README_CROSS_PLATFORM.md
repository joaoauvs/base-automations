# 🤖 Base Automations - RPA Framework

Framework completo para automações RPA compatível com **Windows** e **Linux**.

## 🌍 Compatibilidade de Sistemas

### ✅ Sistemas Suportados

- **Windows 10/11**
- **Linux** (Ubuntu 20.04+, CentOS 8+, Debian 11+)
- **macOS** (compatibilidade básica)

### 🔧 Requisitos de Sistema

#### Todos os Sistemas

- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonagem do repositório)

#### Linux Específico

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv wget curl unzip

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip python3-venv wget curl unzip
```

#### Windows Específico

- **PowerShell 5.0+** (geralmente já incluído)
- **Visual C++ Redistributable** (para algumas dependências)

## 🚀 Instalação Rápida

### 1. Clone o Repositório

```bash
git clone https://github.com/joaoauvs/base-automations.git
cd base-automations
```

### 2. Execute o Setup Automatizado

```bash
# Todos os sistemas
python setup.py
```

O script de setup irá:

- ✅ Verificar compatibilidade do sistema
- 📁 Criar diretórios necessários
- 📦 Instalar dependências
- ⚙️ Configurar arquivo .env

### 3. Configure suas Credenciais

Edite o arquivo `.env` com suas credenciais:

```bash
# Windows
notepad .env

# Linux
nano .env
```

## 📁 Estrutura do Projeto

```
base-automations/
├── 📄 main.py              # Script principal para automações gerais
├── 🌐 mainweb.py           # Script especializado em automações web
├── ⚙️ setup.py             # Script de configuração automatizada
├── 📋 requirements.txt     # Dependências do projeto
├── 🔧 .env.example         # Exemplo de configurações
├── 📂 src/
│   ├── 📁 config/          # Configurações do sistema
│   ├── 📁 core/            # Funcionalidades centrais
│   ├── 📁 modules/         # Módulos de automação
│   │   ├── 📁 web/         # Drivers e configurações web
│   │   ├── 📄 email.py     # Envio de emails
│   │   ├── 📄 log.py       # Sistema de logging
│   │   └── 📄 ...
│   └── 📁 utils/           # Utilitários e helpers
├── 📂 logs/                # Arquivos de log (criado automaticamente)
├── 📂 downloads/           # Downloads automáticos
└── 📂 backups/             # Backups de dados
```

## 🎯 Uso Básico

### Automação Geral

```bash
python main.py
```

### Automação Web Específica

```bash
python mainweb.py
```

### Executar com Configurações Personalizadas

```python
from src.modules.log import LogManager
from main import Bot

# Configurar logging personalizado
LogManager(path="meus_logs")

# Criar bot com CNPJ específico
bot = Bot(cnpj="12.345.678/0001-90", robot_name="MeuRobot")
bot.main()
```

## 🛠️ Configurações Específicas por Sistema

### Windows

```python
# main.py - Exemplo Windows
from src.modules.web.webdriver import Browser, WebDriver

navegador = WebDriver.get_navegador(
    Browser.CHROME,  # ou Browser.EDGE
    headless=False
)
```

### Linux

```python
# main.py - Exemplo Linux
from src.modules.web.webdriver import Browser, WebDriver

navegador = WebDriver.get_navegador(
    Browser.CHROME,
    headless=True  # Recomendado para servidores sem GUI
)
```

## 🔧 Funcionalidades Multi-Plataforma

### Sistema de Logging Inteligente

```python
from src.modules.log import LogManager

# Usa caminhos compatíveis automaticamente
log_manager = LogManager()  # Linux: logs/, Windows: logs\
```

### Detecção Automática de Sistema

```python
from src.utils.platform_utils import PlatformUtils

if PlatformUtils.is_windows():
    print("Executando no Windows")
elif PlatformUtils.is_linux():
    print("Executando no Linux")

# Obter informações do sistema
info = PlatformUtils.get_environment_info()
print(f"Sistema: {info['system']}")
```

### Argumentos de Navegador Otimizados

O sistema automaticamente aplica argumentos específicos por plataforma:

**Linux**: `--no-sandbox`, `--disable-gpu`, `--no-zygote`
**Windows**: Configurações otimizadas para desktop
**Ambos**: Argumentos anti-detecção e performance

## 📧 Configuração de Email

Configurações compatíveis com provedores populares:

```env
# .env
EMAIL_SMTP_SERVER=smtp.gmail.com        # Gmail
EMAIL_SMTP_SERVER=smtp.outlook.com      # Outlook
EMAIL_SMTP_SERVER=smtp.hostinger.com    # Hostinger
EMAIL_SENDER=seu_email@exemplo.com
EMAIL_PASSWORD=sua_senha_ou_token_app
```

## 🐛 Troubleshooting

### Linux: Erro de Permissão

```bash
# Dar permissão de execução
chmod +x setup.py
python setup.py
```

### Linux: Chrome não encontrado

```bash
# Ubuntu/Debian
sudo apt install google-chrome-stable

# CentOS/RHEL/Fedora
sudo dnf install google-chrome-stable
```

### Windows: Erro de PowerShell

Execute o PowerShell como Administrador:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema com Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 🔒 Segurança

### Variáveis de Ambiente

- ✅ Use arquivos `.env` para credenciais
- ❌ Nunca commite credenciais no código
- 🔐 Use tokens de aplicação quando disponível

### Arquivos Sensíveis

O `.gitignore` já está configurado para excluir:

- `.env` (credenciais)
- `logs/` (logs podem conter dados sensíveis)
- `downloads/` (arquivos baixados)
- `__pycache__/` (cache Python)

## 📊 Monitoramento

### Logs Estruturados

```python
import logging

logging.info("Processo iniciado")
logging.warning("Atenção: dados inconsistentes")
logging.error("Erro ao processar arquivo")
```

### Notificações por Email

```python
from src.modules.email import Email

email = Email(robo="MeuRobot")
email.send_email_fail()  # Notifica falhas
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit: `git commit -m 'Adiciona nova feature'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 📧 Email: suporte@exemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/joaoauvs/base-automations/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/joaoauvs/base-automations/wiki)

---

**Desenvolvido com ❤️ para automações RPA multiplataforma**
