#!/usr/bin/env python3
"""
Obsidian Plugin Registry v1.0
Sistema de auto-descoberta e cadastro automático de plugins do Obsidian
Inclui mapeamento de comandos, integrações e prompts para reconhecimento pelo agente
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Arquivo de registro de plugins
REGISTRY_FILE = Path.home() / "COMET" / "plugin_registry.json"
CONTEXT_FILE = Path.home() / "COMET" / "SYSTEM_CONTEXT.json"


# ==================== DEFINIÇÕES DE PLUGINS ====================

PLUGIN_DEFINITIONS = {
    # ===== PLUGINS NATIVOS =====
    "backlinks": {
        "name": "Backlinks",
        "type": "native",
        "category": "navigation",
        "description": "Mostra links que apontam para a nota atual",
        "commands": ["app:toggle-backlinks"],
        "triggers": ["backlinks", "links de volta", "quem linka", "referências"],
        "integrations": ["dataview", "omnisearch"],
        "prompt_examples": [
            "mostrar backlinks",
            "quem linka para esta nota",
            "ver referências"
        ]
    },
    "canvas": {
        "name": "Canvas",
        "type": "native",
        "category": "visual",
        "description": "Cria quadros visuais para organizar notas e ideias",
        "commands": ["canvas:new-file", "canvas:convert-to-file"],
        "triggers": ["canvas", "quadro", "mapa mental", "diagrama"],
        "integrations": ["excalidraw"],
        "prompt_examples": [
            "criar canvas",
            "novo quadro",
            "abrir canvas"
        ]
    },
    "note-composer": {
        "name": "Compositor de Notas",
        "type": "native",
        "category": "editing",
        "description": "Mescla e divide notas",
        "commands": ["note-composer:merge-file", "note-composer:split-file"],
        "triggers": ["mesclar", "dividir", "juntar notas", "separar nota"],
        "integrations": [],
        "prompt_examples": [
            "mesclar notas",
            "dividir nota",
            "juntar arquivos"
        ]
    },
    "page-preview": {
        "name": "Espiar Página",
        "type": "native",
        "category": "navigation",
        "description": "Mostra preview de links ao passar o mouse",
        "commands": [],
        "triggers": ["preview", "espiar", "visualizar link"],
        "integrations": [],
        "prompt_examples": []
    },
    "templates": {
        "name": "Modelos",
        "type": "native",
        "category": "productivity",
        "description": "Insere templates em notas",
        "commands": ["templates:insert-template"],
        "triggers": ["template", "modelo", "inserir modelo"],
        "integrations": ["templater-obsidian"],
        "prompt_examples": [
            "inserir template",
            "usar modelo",
            "aplicar template"
        ]
    },
    "switcher": {
        "name": "Navegação Rápida",
        "type": "native",
        "category": "navigation",
        "description": "Abre notas rapidamente pelo nome",
        "commands": ["switcher:open"],
        "triggers": ["abrir nota", "ir para", "navegar", "buscar nota"],
        "integrations": ["omnisearch"],
        "prompt_examples": [
            "abrir nota X",
            "ir para nota",
            "navegar para"
        ]
    },
    "daily-notes": {
        "name": "Notas Diárias",
        "type": "native",
        "category": "productivity",
        "description": "Cria e gerencia notas diárias",
        "commands": ["daily-notes:open", "daily-notes:open-prev", "daily-notes:open-next"],
        "triggers": ["nota de hoje", "diário", "daily note", "nota diária", "hoje"],
        "integrations": ["templater-obsidian", "tasks"],
        "prompt_examples": [
            "abrir nota de hoje",
            "criar nota diária",
            "nota de ontem",
            "nota de amanhã"
        ]
    },
    "command-palette": {
        "name": "Paleta de Comandos",
        "type": "native",
        "category": "navigation",
        "description": "Acessa todos os comandos do Obsidian",
        "commands": ["command-palette:open"],
        "triggers": ["comandos", "paleta", "ctrl+p"],
        "integrations": ["cmdr"],
        "prompt_examples": [
            "abrir paleta de comandos",
            "mostrar comandos"
        ]
    },
    "file-recovery": {
        "name": "Recuperação de Arquivos",
        "type": "native",
        "category": "utility",
        "description": "Recupera versões anteriores de notas",
        "commands": ["file-recovery:open"],
        "triggers": ["recuperar", "versão anterior", "histórico", "backup"],
        "integrations": [],
        "prompt_examples": [
            "recuperar nota",
            "ver histórico",
            "versão anterior"
        ]
    },
    "sync": {
        "name": "Sincronização",
        "type": "native",
        "category": "utility",
        "description": "Sincroniza vault entre dispositivos",
        "commands": ["sync:view-version-history"],
        "triggers": ["sincronizar", "sync", "backup nuvem"],
        "integrations": [],
        "prompt_examples": [
            "sincronizar vault",
            "ver histórico de sync"
        ]
    },
    "publish": {
        "name": "Visualizador Web",
        "type": "native",
        "category": "utility",
        "description": "Publica notas na web",
        "commands": [],
        "triggers": ["publicar", "web", "publish"],
        "integrations": [],
        "prompt_examples": [
            "publicar nota"
        ]
    },
    
    # ===== PLUGINS NÃO OFICIAIS =====
    "obsidian-admonition": {
        "name": "Admonition",
        "type": "community",
        "category": "visual",
        "description": "Callouts e blocos de destaque aprimorados",
        "commands": ["obsidian-admonition:insert-admonition"],
        "triggers": ["admonition", "callout", "destaque", "aviso", "nota", "dica"],
        "integrations": [],
        "prompt_examples": [
            "inserir callout",
            "criar admonition",
            "adicionar aviso"
        ]
    },
    "ai-commander": {
        "name": "AI Commander",
        "type": "community",
        "category": "ai",
        "description": "Integração com OpenAI/ChatGPT para transcrição, imagens e texto",
        "commands": [
            "ai-commander:generate-text",
            "ai-commander:generate-image",
            "ai-commander:transcribe-audio"
        ],
        "triggers": ["ai commander", "chatgpt", "gerar texto", "transcrever", "gerar imagem"],
        "integrations": ["obsidian-textgenerator-plugin", "chat-with-bard"],
        "api_required": ["openai"],
        "prompt_examples": [
            "gerar texto com IA",
            "transcrever áudio",
            "criar imagem com IA"
        ]
    },
    "obsidian42-brat": {
        "name": "BRAT",
        "type": "community",
        "category": "utility",
        "description": "Instala plugins beta para testes",
        "commands": ["obsidian42-brat:BRAT-AddBetaPlugin"],
        "triggers": ["brat", "plugin beta", "instalar beta"],
        "integrations": [],
        "prompt_examples": [
            "instalar plugin beta",
            "adicionar plugin via BRAT"
        ]
    },
    "browser-interface": {
        "name": "Browser Interface",
        "type": "community",
        "category": "integration",
        "description": "Salva e reabre abas do navegador no vault",
        "commands": ["browser-interface:save-tabs"],
        "triggers": ["browser", "navegador", "abas", "tabs"],
        "integrations": ["open-gate"],
        "prompt_examples": [
            "salvar abas do navegador",
            "importar tabs"
        ]
    },
    "cmdr": {
        "name": "Commander",
        "type": "community",
        "category": "productivity",
        "description": "Cria macros e adiciona comandos personalizados",
        "commands": ["cmdr:open-commander"],
        "triggers": ["commander", "macro", "comando personalizado", "atalho"],
        "integrations": ["command-palette"],
        "prompt_examples": [
            "criar macro",
            "adicionar comando",
            "configurar atalho"
        ]
    },
    "dataview": {
        "name": "Dataview",
        "type": "community",
        "category": "data",
        "description": "Consultas e visualizações de dados complexas",
        "commands": [],
        "triggers": ["dataview", "consulta", "query", "tabela", "lista dinâmica"],
        "integrations": ["obsidian-tasks-plugin", "templater-obsidian"],
        "query_syntax": ["TABLE", "LIST", "TASK", "FROM", "WHERE", "SORT"],
        "prompt_examples": [
            "criar consulta dataview",
            "listar notas com tag X",
            "mostrar tarefas pendentes"
        ]
    },
    "obsidian-excalidraw-plugin": {
        "name": "Excalidraw",
        "type": "community",
        "category": "visual",
        "description": "Editor de desenhos e diagramas",
        "commands": [
            "obsidian-excalidraw-plugin:excalidraw-new",
            "obsidian-excalidraw-plugin:excalidraw-open"
        ],
        "triggers": ["excalidraw", "desenho", "diagrama", "sketch", "rabisco"],
        "integrations": ["canvas"],
        "prompt_examples": [
            "criar desenho",
            "novo excalidraw",
            "abrir diagrama"
        ]
    },
    "chat-with-bard": {
        "name": "Gemini AI Assistant",
        "type": "community",
        "category": "ai",
        "description": "Integração com Google Gemini",
        "commands": ["chat-with-bard:open-chat"],
        "triggers": ["gemini", "bard", "google ai", "chat gemini"],
        "integrations": ["ai-commander", "obsidian-textgenerator-plugin"],
        "api_required": ["gemini"],
        "prompt_examples": [
            "abrir chat gemini",
            "perguntar ao gemini"
        ]
    },
    "obsidian-local-rest-api": {
        "name": "Local REST API",
        "type": "community",
        "category": "integration",
        "description": "API REST para automação externa do Obsidian",
        "commands": [],
        "triggers": ["api", "rest", "automação", "integração externa"],
        "integrations": ["*"],  # Integra com tudo via API
        "endpoints": [
            "/vault/", "/open/", "/search/", "/commands/", "/periodic/"
        ],
        "prompt_examples": [
            "usar api do obsidian",
            "automação via api"
        ]
    },
    "obsidian-tasks-plugin": {
        "name": "Tasks",
        "type": "community",
        "category": "productivity",
        "description": "Gerenciamento avançado de tarefas com datas e recorrência",
        "commands": [
            "obsidian-tasks-plugin:toggle-done",
            "obsidian-tasks-plugin:create-or-edit-task"
        ],
        "triggers": ["tarefa", "task", "todo", "pendente", "concluir", "prazo"],
        "integrations": ["dataview", "daily-notes", "templater-obsidian"],
        "task_syntax": ["📅", "⏳", "🛫", "✅", "❌", "🔁"],
        "prompt_examples": [
            "criar tarefa",
            "listar tarefas pendentes",
            "marcar como concluída",
            "tarefas de hoje"
        ]
    },
    "obsidian-textgenerator-plugin": {
        "name": "Text Generator",
        "type": "community",
        "category": "ai",
        "description": "Geração de texto com IA",
        "commands": [
            "obsidian-textgenerator-plugin:generate-text",
            "obsidian-textgenerator-plugin:generate-text-with-metadata"
        ],
        "triggers": ["gerar texto", "text generator", "completar", "expandir"],
        "integrations": ["ai-commander", "chat-with-bard"],
        "api_required": ["openai", "gemini"],
        "prompt_examples": [
            "gerar texto",
            "completar parágrafo",
            "expandir ideia"
        ]
    },
    "omnisearch": {
        "name": "Omnisearch",
        "type": "community",
        "category": "search",
        "description": "Busca avançada que funciona",
        "commands": ["omnisearch:show-modal"],
        "triggers": ["buscar", "pesquisar", "encontrar", "search", "omnisearch"],
        "integrations": ["switcher", "backlinks"],
        "prompt_examples": [
            "buscar no vault",
            "pesquisar termo",
            "encontrar nota"
        ]
    },
    "open-gate": {
        "name": "Open Gate",
        "type": "community",
        "category": "integration",
        "description": "Incorpora websites no Obsidian",
        "commands": ["open-gate:open-gate"],
        "triggers": ["open gate", "incorporar site", "embed", "website"],
        "integrations": ["browser-interface"],
        "prompt_examples": [
            "abrir site no obsidian",
            "incorporar página"
        ]
    },
    "pane-relief": {
        "name": "Pane Relief",
        "type": "community",
        "category": "navigation",
        "description": "Navegação avançada entre painéis e abas",
        "commands": [
            "pane-relief:go-prev",
            "pane-relief:go-next",
            "pane-relief:go-1st",
            "pane-relief:go-last"
        ],
        "triggers": ["painel", "aba", "navegar", "próximo", "anterior"],
        "integrations": [],
        "prompt_examples": [
            "ir para próxima aba",
            "voltar painel anterior"
        ]
    },
    "templater-obsidian": {
        "name": "Templater",
        "type": "community",
        "category": "productivity",
        "description": "Templates avançados com JavaScript",
        "commands": [
            "templater-obsidian:insert-templater",
            "templater-obsidian:create-new-note-from-template"
        ],
        "triggers": ["templater", "template avançado", "modelo js", "criar nota template"],
        "integrations": ["templates", "daily-notes", "dataview"],
        "template_syntax": ["<% %>", "tp.file", "tp.date", "tp.system"],
        "prompt_examples": [
            "inserir template",
            "criar nota com template",
            "aplicar templater"
        ]
    }
}


class PluginRegistry:
    """Gerenciador de registro de plugins do Obsidian"""
    
    def __init__(self):
        self.registry = self._load_registry()
        self.context = self._load_context()
        self.vault_path = self.context.get("paths", {}).get("vault", "")
    
    def _load_registry(self) -> Dict:
        """Carrega o registro de plugins do arquivo"""
        if REGISTRY_FILE.exists():
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"plugins": {}, "last_scan": None, "version": "1.0"}
    
    def _load_context(self) -> Dict:
        """Carrega o contexto do sistema"""
        if CONTEXT_FILE.exists():
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_registry(self):
        """Salva o registro de plugins"""
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def scan_plugins(self) -> List[Dict]:
        """Escaneia e registra todos os plugins instalados"""
        plugins_path = Path(self.vault_path) / ".obsidian" / "plugins"
        discovered = []
        
        if not plugins_path.exists():
            return discovered
        
        for plugin_dir in plugins_path.iterdir():
            if plugin_dir.is_dir():
                manifest_path = plugin_dir / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    
                    plugin_id = manifest.get("id", plugin_dir.name)
                    plugin_info = self._build_plugin_info(plugin_id, manifest, plugin_dir)
                    discovered.append(plugin_info)
                    self.registry["plugins"][plugin_id] = plugin_info
        
        # Adicionar plugins nativos
        for plugin_id, definition in PLUGIN_DEFINITIONS.items():
            if definition.get("type") == "native":
                self.registry["plugins"][plugin_id] = {
                    **definition,
                    "id": plugin_id,
                    "enabled": True,
                    "installed": True
                }
        
        self.registry["last_scan"] = datetime.now().isoformat()
        self._save_registry()
        
        return discovered
    
    def _build_plugin_info(self, plugin_id: str, manifest: Dict, plugin_dir: Path) -> Dict:
        """Constrói informações completas do plugin"""
        # Usar definição conhecida se existir
        definition = PLUGIN_DEFINITIONS.get(plugin_id, {})
        
        # Tentar extrair comandos do main.js
        commands = definition.get("commands", [])
        main_js = plugin_dir / "main.js"
        if main_js.exists() and not commands:
            try:
                content = main_js.read_text(encoding="utf-8", errors="ignore")
                # Buscar padrões de addCommand
                cmd_matches = re.findall(r'id:\s*["\']([^"\']+)["\']', content)
                commands = [f"{plugin_id}:{cmd}" for cmd in cmd_matches[:10]]  # Limitar a 10
            except:
                pass
        
        return {
            "id": plugin_id,
            "name": manifest.get("name", plugin_id),
            "version": manifest.get("version", "unknown"),
            "description": manifest.get("description", definition.get("description", "")),
            "author": manifest.get("author", ""),
            "type": "community",
            "category": definition.get("category", "other"),
            "commands": commands,
            "triggers": definition.get("triggers", []),
            "integrations": definition.get("integrations", []),
            "api_required": definition.get("api_required", []),
            "prompt_examples": definition.get("prompt_examples", []),
            "enabled": True,
            "installed": True,
            "registered_at": datetime.now().isoformat()
        }
    
    def get_plugin(self, plugin_id: str) -> Optional[Dict]:
        """Obtém informações de um plugin específico"""
        return self.registry["plugins"].get(plugin_id)
    
    def get_all_plugins(self) -> Dict[str, Dict]:
        """Retorna todos os plugins registrados"""
        return self.registry["plugins"]
    
    def get_plugins_by_category(self, category: str) -> List[Dict]:
        """Retorna plugins de uma categoria específica"""
        return [
            p for p in self.registry["plugins"].values()
            if p.get("category") == category
        ]
    
    def get_ai_plugins(self) -> List[Dict]:
        """Retorna todos os plugins de IA"""
        return self.get_plugins_by_category("ai")
    
    def find_plugin_by_trigger(self, text: str) -> Optional[Dict]:
        """Encontra um plugin baseado em triggers no texto"""
        text_lower = text.lower()
        for plugin in self.registry["plugins"].values():
            for trigger in plugin.get("triggers", []):
                if trigger.lower() in text_lower:
                    return plugin
        return None
    
    def get_command_for_action(self, action: str) -> Optional[str]:
        """Encontra o comando apropriado para uma ação"""
        action_lower = action.lower()
        
        for plugin in self.registry["plugins"].values():
            for trigger in plugin.get("triggers", []):
                if trigger.lower() in action_lower:
                    commands = plugin.get("commands", [])
                    if commands:
                        return commands[0]
        return None
    
    def get_integration_graph(self) -> Dict[str, List[str]]:
        """Retorna o grafo de integrações entre plugins"""
        graph = {}
        for plugin_id, plugin in self.registry["plugins"].items():
            integrations = plugin.get("integrations", [])
            graph[plugin_id] = integrations
        return graph
    
    def generate_prompt_context(self) -> str:
        """Gera contexto de prompts para o agente"""
        context = "=== PLUGINS DO OBSIDIAN DISPONÍVEIS ===\n\n"
        
        categories = {}
        for plugin in self.registry["plugins"].values():
            cat = plugin.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(plugin)
        
        category_names = {
            "ai": "🤖 Plugins de IA",
            "productivity": "📋 Produtividade",
            "navigation": "🧭 Navegação",
            "visual": "🎨 Visual",
            "data": "📊 Dados",
            "search": "🔍 Busca",
            "integration": "🔗 Integração",
            "utility": "🔧 Utilitários",
            "editing": "✏️ Edição",
            "other": "📦 Outros"
        }
        
        for cat, plugins in categories.items():
            context += f"\n{category_names.get(cat, cat.upper())}:\n"
            for plugin in plugins:
                name = plugin.get("name", plugin.get("id"))
                triggers = ", ".join(plugin.get("triggers", [])[:3])
                context += f"  • {name}: {triggers}\n"
        
        return context
    
    def export_for_agent(self) -> Dict:
        """Exporta dados formatados para uso pelo agente"""
        return {
            "plugins": self.registry["plugins"],
            "categories": list(set(p.get("category") for p in self.registry["plugins"].values())),
            "ai_plugins": [p["id"] for p in self.get_ai_plugins()],
            "all_triggers": self._get_all_triggers(),
            "all_commands": self._get_all_commands(),
            "integration_graph": self.get_integration_graph(),
            "prompt_context": self.generate_prompt_context()
        }
    
    def _get_all_triggers(self) -> Dict[str, str]:
        """Retorna mapeamento de todos os triggers para plugin_id"""
        triggers = {}
        for plugin_id, plugin in self.registry["plugins"].items():
            for trigger in plugin.get("triggers", []):
                triggers[trigger.lower()] = plugin_id
        return triggers
    
    def _get_all_commands(self) -> Dict[str, str]:
        """Retorna mapeamento de todos os comandos para plugin_id"""
        commands = {}
        for plugin_id, plugin in self.registry["plugins"].items():
            for cmd in plugin.get("commands", []):
                commands[cmd] = plugin_id
        return commands


# Instância global
plugin_registry = PluginRegistry()


def scan_and_register():
    """Função de conveniência para escanear e registrar plugins"""
    return plugin_registry.scan_plugins()


def get_plugin_for_text(text: str) -> Optional[Dict]:
    """Encontra plugin apropriado para um texto"""
    return plugin_registry.find_plugin_by_trigger(text)


def get_command(action: str) -> Optional[str]:
    """Obtém comando para uma ação"""
    return plugin_registry.get_command_for_action(action)


def get_prompt_context() -> str:
    """Obtém contexto de prompts"""
    return plugin_registry.generate_prompt_context()


if __name__ == "__main__":
    # Teste do sistema
    print("Escaneando plugins...")
    plugins = scan_and_register()
    print(f"Encontrados {len(plugins)} plugins")
    
    print("\nContexto para o agente:")
    print(get_prompt_context())
