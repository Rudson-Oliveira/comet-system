# COMET - Cognitive Operational Management & Execution Technology

Sistema integrado de automação e inteligência artificial para Windows, conectando Obsidian, Ollama e múltiplos serviços.

## 🎯 Visão Geral

O COMET é um ecossistema completo que integra:
- **Obsidian** como base de conhecimento
- **Ollama/LLaVA** para IA local
- **N8n** para automações
- **Múltiplos agentes** para diferentes tarefas

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         COMET ECOSYSTEM                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Obsidian   │  │    Ollama    │  │     N8n      │              │
│  │   (Vault)    │  │   (LLaVA)    │  │  (Workflows) │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                      │
│         └────────────┬────┴──────────────────┘                      │
│                      │                                              │
│  ┌───────────────────┴───────────────────────────────────────────┐ │
│  │                      SERVIÇOS COMET                            │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │ │
│  │  │  COMET Bridge   │  │ Obsidian Agent  │  │  Hub Central   │ │ │
│  │  │   Porta 5000    │  │   Porta 5001    │  │  Porta 5002    │ │ │
│  │  │  (Automação)    │  │  (IA + Chat)    │  │  (Triggers)    │ │ │
│  │  └─────────────────┘  └─────────────────┘  └────────────────┘ │ │
│  │                                                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                     │ │
│  │  │  COMET Vision   │  │    Frontend     │                     │ │
│  │  │   Porta 5003    │  │   Porta 5173    │                     │ │
│  │  │  (Análise Tela) │  │   (Interface)   │                     │ │
│  │  └─────────────────┘  └─────────────────┘                     │ │
│  │                                                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                         ngrok                                  │ │
│  │         Acesso Externo: charmless-maureen-...ngrok-free.dev   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 📦 Componentes

### Serviços Principais

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **COMET Bridge** | 5000 | Ponte de automação Windows/PowerShell |
| **Obsidian Agent** | 5001 | Agente inteligente v5.0 com chat |
| **Hub Central** | 5002 | Gerenciador de triggers e automações |
| **COMET Vision** | 5003 | Análise de tela com LLaVA |
| **Frontend** | 5173 | Interface web (Vite + React) |

### Arquivos do Sistema

| Arquivo | Descrição |
|---------|-----------|
| `comet_bridge.py` | Servidor HTTP para execução de comandos |
| `manus_bridge_unified.py` | Bridge unificado Manus-COMET-Obsidian |
| `obsidian_plugin_registry.py` | Registro de plugins do Obsidian |
| `Iniciar_Sistema_IA.bat` | Script de inicialização completa |
| `INICIAR_TUDO.ps1` | PowerShell para iniciar todos os serviços |
| `RESTAURAR_SISTEMA.ps1` | Script de restauração do sistema |

## 🚀 Instalação

### Pré-requisitos

- Windows 10/11
- Python 3.10+
- Node.js 18+
- Ollama com LLaVA
- Obsidian
- ngrok (para acesso externo)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/Rudson-Oliveira/comet-system.git
cd comet-system
```

2. Instale as dependências Python:
```bash
pip install flask requests mss pillow
```

3. Configure o Ollama:
```bash
ollama pull llava
ollama pull llama3.2
```

4. Inicie o sistema:
```bash
# Windows
Iniciar_Sistema_IA.bat

# Ou PowerShell
.\INICIAR_TUDO.ps1
```

## 📡 Endpoints da API

### COMET Bridge (5000)
```http
GET /health
POST /exec {"command": "powershell command"}
POST /powershell {"command": "powershell command"}
```

### Obsidian Agent (5001)
```http
GET /health
POST /chat {"message": "sua pergunta"}
POST /create-note {"title": "titulo", "content": "conteudo"}
```

### Hub Central (5002)
```http
GET /health
GET /triggers
POST /trigger/{name}
```

### COMET Vision (5003)
```http
GET /health
GET /history
POST /capture-and-analyze {"prompt": "descreva a tela", "provider": "ollama"}
```

## 🔧 Configuração

### SYSTEM_CONTEXT.json
Contém o contexto do sistema e configurações globais.

### plugin_registry.json
Registro de plugins do Obsidian com comandos disponíveis.

## 📊 Evolução do Sistema

### v1.0 - Base
- COMET Bridge básico
- Integração Obsidian

### v1.1 - Hub Central
- Gerenciador de triggers
- 16 gatilhos configurados
- Automações agendadas

### v5.0 - Obsidian Agent
- Agente inteligente com chat
- 26 plugins, 38 comandos
- Lógica de decisão avançada

### v1.0 - COMET Vision
- Análise de tela com LLaVA
- Timeout otimizado (300s)
- Redimensionamento automático de imagens

## 🔗 Repositórios Relacionados

- [COMET Bridge Vision](https://github.com/Rudson-Oliveira/comet-bridge-vision) - Sistema de visão computacional

## 📝 Licença

MIT License

## 🤝 Contribuição

Parte do ecossistema COMET - Cognitive Operational Management & Execution Technology

---

**Desenvolvido com 🧠 por Manus AI**

*Última atualização: 24/12/2025*

---

## 🆕 Agente PicaPau (v1.1.0)

O COMET Bridge Vision agora inclui o **Agente PicaPau**, um executor de comandos visuais:

- **Comandos em linguagem natural**: "PicaPau abra o Google e pesquise por clima"
- **Automação com Playwright**: Navegação, cliques, digitação
- **Validação visual com LLaVA**: Confirma sucesso das ações
- **Credenciais seguras**: Criptografia Fernet (AES-128)

Veja o repositório [comet-bridge-vision](https://github.com/Rudson-Oliveira/comet-bridge-vision) para mais detalhes.
