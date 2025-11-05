# Guia de Configuração do Azure Key Vault

Este documento explica como configurar e utilizar o Azure Key Vault para gerenciar credenciais de forma segura no projeto Base Automations.

## 📋 Índice

1. [Por que usar Azure Key Vault?](#por-que-usar-azure-key-vault)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração do Azure Key Vault](#configuração-do-azure-key-vault)
4. [Autenticação](#autenticação)
5. [Configuração do Projeto](#configuração-do-projeto)
6. [Nomes dos Segredos](#nomes-dos-segredos)
7. [Uso no Código](#uso-no-código)
8. [Troubleshooting](#troubleshooting)

## 🔐 Por que usar Azure Key Vault?

O Azure Key Vault oferece:

- **Segurança**: Credenciais são armazenadas de forma criptografada no Azure
- **Controle de Acesso**: Permissões granulares via Azure RBAC
- **Auditoria**: Logs de todas as operações de acesso aos segredos
- **Rotação**: Facilita a rotação de credenciais sem alterar código
- **Centralização**: Único local para gerenciar todas as credenciais

## 📦 Pré-requisitos

1. **Conta Azure** com permissões para criar Key Vault
2. **Azure CLI** instalado (opcional, mas recomendado)
3. **Dependências Python** instaladas:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Configuração do Azure Key Vault

### 1. Criar o Key Vault

Via Azure Portal:
1. Acesse o [Portal Azure](https://portal.azure.com)
2. Navegue para "Key vaults" → "Create"
3. Preencha os dados:
   - **Subscription**: Sua assinatura Azure
   - **Resource group**: Crie ou selecione um grupo
   - **Key vault name**: Nome único (ex: `base-automations-kv`)
   - **Region**: Escolha a região mais próxima
   - **Pricing tier**: Standard (suficiente para a maioria dos casos)

Via Azure CLI:
```bash
# Login no Azure
az login

# Criar grupo de recursos (se não existir)
az group create --name rpa-resources --location brazilsouth

# Criar Key Vault
az keyvault create \
  --name base-automations-kv \
  --resource-group rpa-resources \
  --location brazilsouth
```

### 2. Adicionar os Segredos

Via Azure Portal:
1. Acesse seu Key Vault
2. Navegue para "Secrets" → "Generate/Import"
3. Adicione cada segredo com seu valor

Via Azure CLI:
```bash
# Adicionar segredos
az keyvault secret set --vault-name base-automations-kv --name EMAIL-SENDER --value "seu_email@exemplo.com"
az keyvault secret set --vault-name base-automations-kv --name EMAIL-PASSWORD --value "sua_senha"
az keyvault secret set --vault-name base-automations-kv --name EMAIL-FAILURE-RECIPIENT --value "destinatario@exemplo.com"
az keyvault secret set --vault-name base-automations-kv --name EMAIL-SMTP-SERVER --value "smtp.hostinger.com"
az keyvault secret set --vault-name base-automations-kv --name TWOCAPTCHA-API-KEY --value "sua_chave_2captcha"
az keyvault secret set --vault-name base-automations-kv --name DATABRICKS-HOST --value "sua_url_databricks"
az keyvault secret set --vault-name base-automations-kv --name DATABRICKS-HTTP-PATH --value "seu_http_path"
az keyvault secret set --vault-name base-automations-kv --name DATABRICKS-ACCESS-TOKEN --value "seu_token"
az keyvault secret set --vault-name base-automations-kv --name WEBHOOK-EXECUTION-STATUS --value "sua_webhook_url"
```

## 🔑 Autenticação

O projeto suporta múltiplos métodos de autenticação via `DefaultAzureCredential`:

### Opção 1: Managed Identity (Recomendado para Produção)

Se o bot estiver rodando em uma Azure VM, App Service, ou Container Instance:

1. Habilite Managed Identity no recurso Azure
2. Conceda permissões ao Key Vault:
   ```bash
   # Obter o principal ID da Managed Identity
   PRINCIPAL_ID=$(az vm identity show --name sua-vm --resource-group seu-rg --query principalId -o tsv)

   # Conceder acesso ao Key Vault
   az keyvault set-policy \
     --name base-automations-kv \
     --object-id $PRINCIPAL_ID \
     --secret-permissions get list
   ```
3. Configure apenas a URL no `.env`:
   ```bash
   USE_AZURE_KEYVAULT=true
   AZURE_KEYVAULT_URL=https://base-automations-kv.vault.azure.net/
   ```

### Opção 2: Service Principal (Para ambientes locais/desenvolvimento)

1. Criar Service Principal:
   ```bash
   az ad sp create-for-rbac --name base-automations-sp
   ```

   Isso retornará:
   ```json
   {
     "appId": "xxxx-xxxx-xxxx-xxxx",
     "password": "xxxx-xxxx-xxxx-xxxx",
     "tenant": "xxxx-xxxx-xxxx-xxxx"
   }
   ```

2. Conceder acesso ao Key Vault:
   ```bash
   az keyvault set-policy \
     --name base-automations-kv \
     --spn <appId> \
     --secret-permissions get list
   ```

3. Configure o `.env`:
   ```bash
   USE_AZURE_KEYVAULT=true
   AZURE_KEYVAULT_URL=https://base-automations-kv.vault.azure.net/
   AZURE_CLIENT_ID=<appId>
   AZURE_TENANT_ID=<tenant>
   AZURE_CLIENT_SECRET=<password>
   ```

### Opção 3: Azure CLI (Para desenvolvimento local)

1. Faça login no Azure CLI:
   ```bash
   az login
   ```

2. Conceda acesso ao seu usuário:
   ```bash
   USER_ID=$(az ad signed-in-user show --query id -o tsv)
   az keyvault set-policy \
     --name base-automations-kv \
     --object-id $USER_ID \
     --secret-permissions get list
   ```

3. Configure o `.env`:
   ```bash
   USE_AZURE_KEYVAULT=true
   AZURE_KEYVAULT_URL=https://base-automations-kv.vault.azure.net/
   ```

## ⚙️ Configuração do Projeto

1. **Copie o arquivo `.env.example` para `.env`:**
   ```bash
   cp .env.example .env
   ```

2. **Edite o arquivo `.env`:**
   ```bash
   # Habilitar Key Vault
   USE_AZURE_KEYVAULT=true

   # URL do seu Key Vault
   AZURE_KEYVAULT_URL=https://seu-keyvault.vault.azure.net/

   # Se usar Service Principal, adicione também:
   AZURE_CLIENT_ID=seu_client_id
   AZURE_TENANT_ID=seu_tenant_id
   AZURE_CLIENT_SECRET=seu_client_secret
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 📝 Nomes dos Segredos

Os segredos no Key Vault devem seguir esta convenção (usar **hyphens**, não underscores):

| Variável de Ambiente | Nome no Key Vault | Descrição |
|---------------------|-------------------|-----------|
| `EMAIL_SENDER` | `EMAIL-SENDER` | Email remetente |
| `EMAIL_PASSWORD` | `EMAIL-PASSWORD` | Senha do email |
| `EMAIL_FAILURE_RECIPIENT` | `EMAIL-FAILURE-RECIPIENT` | Email para notificações de falha |
| `EMAIL_SMTP_SERVER` | `EMAIL-SMTP-SERVER` | Servidor SMTP |
| `TWOCAPTCHA_API_KEY` | `TWOCAPTCHA-API-KEY` | Chave API do 2Captcha |
| `DATABRICKS_HOST` | `DATABRICKS-HOST` | URL do Databricks |
| `DATABRICKS_HTTP_PATH` | `DATABRICKS-HTTP-PATH` | HTTP Path do Databricks |
| `DATABRICKS_ACCESS_TOKEN` | `DATABRICKS-ACCESS-TOKEN` | Token de acesso Databricks |
| `WEBHOOK_EXECUTION_STATUS` | `WEBHOOK-EXECUTION-STATUS` | URL do webhook |

## 💻 Uso no Código

### Importação Automática

O sistema importa credenciais automaticamente ao inicializar:

```python
# As credenciais são carregadas automaticamente ao importar Settings
from src.modules.email import EmailNotifier
from src.modules.captcha import CaptchaSolver

# Os módulos já usam o Key Vault automaticamente
email = EmailNotifier(robot_name="MeuBot")
captcha = CaptchaSolver()
```

### Uso Direto do KeyVaultClient

Para casos específicos, você pode usar o cliente diretamente:

```python
from src.config.keyvault import get_keyvault_client

# Obter cliente
client = get_keyvault_client()

# Buscar um segredo específico
api_key = client.get_secret("MINHA-API-KEY")

# Buscar múltiplos segredos
secrets = client.get_all_secrets([
    "EMAIL-SENDER",
    "EMAIL-PASSWORD"
])

# Buscar com fallback para variável de ambiente
value = client.get_secret_with_fallback(
    "NOVA-CREDENCIAL",
    env_var_name="NOVA_CREDENCIAL",
    default="valor_padrao"
)
```

### Usando a Função Helper

```python
from src.config.settings import get_config_value

# Busca primeiro no Key Vault, depois no .env
email = get_config_value("EMAIL_SENDER", "EMAIL-SENDER")

# Com valor padrão
timeout = get_config_value("TIMEOUT", default="30")
```

## 🔧 Troubleshooting

### Erro: "URL do Azure Key Vault não fornecida"

**Problema**: A variável `AZURE_KEYVAULT_URL` não está configurada.

**Solução**: Adicione no `.env`:
```bash
AZURE_KEYVAULT_URL=https://seu-keyvault.vault.azure.net/
```

### Erro: "Authentication failed" ou "Unauthorized"

**Problema**: Sem permissões no Key Vault.

**Solução**:
```bash
# Para Service Principal
az keyvault set-policy --name seu-keyvault --spn <appId> --secret-permissions get list

# Para Managed Identity
az keyvault set-policy --name seu-keyvault --object-id <principal-id> --secret-permissions get list

# Para usuário (desenvolvimento)
az keyvault set-policy --name seu-keyvault --upn seu-email@exemplo.com --secret-permissions get list
```

### Erro: "Secret not found"

**Problema**: Segredo não existe no Key Vault ou nome incorreto.

**Solução**:
1. Verifique se o segredo existe:
   ```bash
   az keyvault secret list --vault-name seu-keyvault
   ```
2. Verifique o nome (deve usar hyphens, não underscores)
3. Adicione o segredo se não existir:
   ```bash
   az keyvault secret set --vault-name seu-keyvault --name NOME-SEGREDO --value "valor"
   ```

### Modo de Fallback

Se o Key Vault não estiver configurado ou houver erro, o sistema automaticamente usa o `.env` como fallback:

```bash
# Desabilitar Key Vault temporariamente
USE_AZURE_KEYVAULT=false
```

Isso é útil para:
- Desenvolvimento local sem acesso ao Azure
- Troubleshooting de problemas
- Ambientes de teste

## 🎯 Melhores Práticas

1. **Produção**: Use Managed Identity sempre que possível
2. **Desenvolvimento**: Use Azure CLI authentication ou Service Principal
3. **Segredos**: Nunca commite credenciais no código ou `.env`
4. **Permissões**: Conceda apenas as permissões mínimas necessárias (get, list)
5. **Auditoria**: Habilite logs de diagnóstico no Key Vault
6. **Rotação**: Estabeleça política de rotação regular de credenciais
7. **Backup**: Configure backup automático do Key Vault

## 📚 Recursos Adicionais

- [Documentação Azure Key Vault](https://docs.microsoft.com/azure/key-vault/)
- [DefaultAzureCredential](https://docs.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)
- [Melhores Práticas Key Vault](https://docs.microsoft.com/azure/key-vault/general/best-practices)

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique a seção [Troubleshooting](#troubleshooting)
2. Revise os logs da aplicação
3. Abra uma issue no repositório do projeto
