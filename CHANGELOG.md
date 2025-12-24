# Changelog - COMET System

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

## [2025-12-24] - Sessão de Desenvolvimento

### COMET Bridge Vision v1.0

#### Adicionado
- Sistema de visão computacional completo
- Integração com Ollama/LLaVA para análise de imagens
- Suporte a múltiplos provedores (Ollama, Gemini, Claude, GPT-4o)
- Captura de tela automática usando mss
- API REST para integração externa
- Histórico de análises

#### Otimizado
- **Timeout aumentado de 120s para 300s** - Permite processamento de imagens grandes
- **Redimensionamento automático de imagens** - Imagens maiores que 1920px são redimensionadas
- Método `_resize_image` implementado na classe OllamaVision

#### Performance
| Métrica | Antes | Depois |
|---------|-------|--------|
| Timeout | 120s | 300s |
| Imagem 8800x1350 | Timeout | ~2-3 min |
| Redimensionamento | Não | Sim (max 1920px) |

### Sistema Completo

#### Status dos Serviços
- ✅ COMET Bridge (5000) - Online
- ✅ Obsidian Agent (5001) - v5.0 Online
- ✅ Hub Central (5002) - v1.1 Online (16 triggers)
- ✅ COMET Vision (5003) - v1.0 Online
- ✅ Frontend (5173) - Online
- ✅ ngrok - Online

#### Repositórios GitHub
- [comet-bridge-vision](https://github.com/Rudson-Oliveira/comet-bridge-vision) - Criado e publicado
- [comet-system](https://github.com/Rudson-Oliveira/comet-system) - Sistema principal

---

## [2025-12-23] - Desenvolvimento Anterior

### Hub Central v1.1
- 16 gatilhos configurados
- Scheduler de tarefas
- Conectores: obsidian, google_drive, onedrive, mysql

### Obsidian Agent v5.0
- IntelligentAgent com lógica de decisão
- 26 plugins registrados
- 38 comandos diretos
- Chat integrado no Obsidian

---

## Arquitetura de Portas

| Porta | Serviço | Versão |
|-------|---------|--------|
| 5000 | COMET Bridge | v1.0 |
| 5001 | Obsidian Agent | v5.0 |
| 5002 | Hub Central | v1.1 |
| 5003 | COMET Vision | v1.0 |
| 5173 | Frontend | - |
| 11434 | Ollama | - |
| 27124 | Obsidian API | - |

---

## Próximos Passos

- [ ] Integrar COMET Vision com Obsidian (criar notas com análises)
- [ ] Adicionar comandos de visão no chat do Obsidian
- [ ] Configurar triggers automáticos para análise de tela
- [ ] Implementar cache de análises
- [ ] Adicionar suporte a múltiplos monitores seletivos
