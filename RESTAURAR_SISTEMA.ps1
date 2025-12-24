# ============================================
# MANUS-COMET-OBSIDIAN - Restauracao Completa
# Restaura todo o sistema a partir do GitHub
# ============================================

param(
    [switch]$Force,
    [switch]$SkipBackup
)

$ErrorActionPreference = "Stop"

# Configuracoes
$GITHUB_REPO = "https://github.com/Rudson-Oliveira/obsidian-agente.git"
$COMET_DIR = "$env:USERPROFILE\COMET"
$AGENT_DIR = "$env:USERPROFILE\obsidian-agente"
$BACKUP_DIR = "$env:USERPROFILE\COMET_BACKUP"

function Write-Status($msg, $color = "White") {
    Write-Host $msg -ForegroundColor $color
}

function Write-Section($title) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  $title" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

Write-Section "MANUS-COMET-OBSIDIAN - RESTAURACAO"

Write-Host "Este script vai:" -ForegroundColor Yellow
Write-Host "  1. Fazer backup da configuracao atual" -ForegroundColor White
Write-Host "  2. Baixar a versao mais recente do GitHub" -ForegroundColor White
Write-Host "  3. Restaurar o COMET Bridge" -ForegroundColor White
Write-Host "  4. Restaurar o Obsidian Agent" -ForegroundColor White
Write-Host "  5. Configurar inicializacao automatica" -ForegroundColor White
Write-Host ""

if (-not $Force) {
    $confirm = Read-Host "Deseja continuar? (S/N)"
    if ($confirm -ne "S" -and $confirm -ne "s") {
        Write-Status "Operacao cancelada." "Yellow"
        exit 0
    }
}

# ==================== PASSO 1: Parar servicos ====================
Write-Section "1. Parando servicos..."

# Parar processos Python relacionados
Get-Process -Name python -ErrorAction SilentlyContinue | ForEach-Object {
    $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    if ($cmdLine -like "*comet*" -or $cmdLine -like "*agent*" -or $cmdLine -like "*obsidian*") {
        Write-Status "  Parando processo: $($_.Id)" "Yellow"
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}

# Parar ngrok
Get-Process -Name ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Status "  Servicos parados!" "Green"

# ==================== PASSO 2: Backup ====================
if (-not $SkipBackup) {
    Write-Section "2. Fazendo backup..."
    
    $backupTimestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $backupPath = "$BACKUP_DIR\backup_$backupTimestamp"
    
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
    
    # Backup COMET
    if (Test-Path $COMET_DIR) {
        Copy-Item -Path $COMET_DIR -Destination "$backupPath\COMET" -Recurse -ErrorAction SilentlyContinue
        Write-Status "  COMET backup: OK" "Green"
    }
    
    # Backup Agent config
    if (Test-Path "$AGENT_DIR\agent\config.json") {
        Copy-Item -Path "$AGENT_DIR\agent\config.json" -Destination "$backupPath\agent_config.json" -ErrorAction SilentlyContinue
        Write-Status "  Agent config backup: OK" "Green"
    }
    
    Write-Status "  Backup salvo em: $backupPath" "Cyan"
} else {
    Write-Status "  Backup pulado (--SkipBackup)" "Yellow"
}

# ==================== PASSO 3: Baixar do GitHub ====================
Write-Section "3. Baixando do GitHub..."

# Verificar se git esta instalado
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Status "[ERRO] Git nao encontrado. Instale o Git primeiro." "Red"
    exit 1
}

# Remover pasta antiga do agent
if (Test-Path $AGENT_DIR) {
    Remove-Item -Path $AGENT_DIR -Recurse -Force -ErrorAction SilentlyContinue
}

# Clonar repositorio
Write-Status "  Clonando repositorio..." "White"
git clone $GITHUB_REPO $AGENT_DIR 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Status "  Repositorio clonado com sucesso!" "Green"
} else {
    Write-Status "[ERRO] Falha ao clonar repositorio" "Red"
    exit 1
}

# ==================== PASSO 4: Restaurar COMET Bridge ====================
Write-Section "4. Configurando COMET Bridge..."

# Criar pasta COMET se nao existir
if (-not (Test-Path $COMET_DIR)) {
    New-Item -ItemType Directory -Path $COMET_DIR -Force | Out-Null
}

# Copiar comet_bridge.py do repositorio se existir
if (Test-Path "$AGENT_DIR\comet_bridge.py") {
    Copy-Item -Path "$AGENT_DIR\comet_bridge.py" -Destination "$COMET_DIR\comet_bridge.py" -Force
    Write-Status "  comet_bridge.py restaurado!" "Green"
} else {
    # Criar comet_bridge.py basico
    $cometBridgeCode = @'
#!/usr/bin/env python3
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 5000

class CometBridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[COMET] {args[0]}")
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self.send_json({"status": "online", "service": "COMET Bridge"})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(body) if body else {}
        except:
            self.send_json({"error": "JSON invalido"}, 400)
            return
        
        if self.path == '/exec':
            command = data.get('command', '')
            if not command:
                self.send_json({"error": "Comando nao fornecido"}, 400)
                return
            print(f"\n[EXEC] {command}")
            try:
                result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True, timeout=60)
                self.send_json({"success": result.returncode == 0, "output": result.stdout, "error": result.stderr})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
        else:
            self.send_json({"error": "Endpoint nao encontrado"}, 404)

print("=" * 50)
print("  COMET BRIDGE - Servidor HTTP")
print("=" * 50)
print(f"Servidor em http://localhost:{PORT}")
print("POST /exec - Executar PowerShell")
print("-" * 50)
HTTPServer(('0.0.0.0', PORT), CometBridgeHandler).serve_forever()
'@
    $cometBridgeCode | Out-File -FilePath "$COMET_DIR\comet_bridge.py" -Encoding UTF8
    Write-Status "  comet_bridge.py criado!" "Green"
}

# ==================== PASSO 5: Instalar dependencias ====================
Write-Section "5. Instalando dependencias..."

# Instalar dependencias do agent
if (Test-Path "$AGENT_DIR\requirements.txt") {
    pip install -r "$AGENT_DIR\requirements.txt" --quiet 2>&1 | Out-Null
    Write-Status "  Dependencias instaladas!" "Green"
} else {
    pip install flask flask-cors --quiet 2>&1 | Out-Null
    Write-Status "  Dependencias basicas instaladas!" "Green"
}

# ==================== PASSO 6: Configurar Startup ====================
Write-Section "6. Configurando inicializacao automatica..."

$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"

# Criar atalho para INICIAR_TUDO.ps1
$shortcutPath = "$startupPath\MANUS-COMET-Startup.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$COMET_DIR\INICIAR_TUDO.ps1`""
$shortcut.WorkingDirectory = $COMET_DIR
$shortcut.Description = "MANUS-COMET-OBSIDIAN Auto Startup"
$shortcut.Save()

Write-Status "  Atalho de startup criado!" "Green"

# Copiar scripts para COMET_DIR
if (Test-Path "$AGENT_DIR\scripts\INICIAR_TUDO.ps1") {
    Copy-Item -Path "$AGENT_DIR\scripts\INICIAR_TUDO.ps1" -Destination "$COMET_DIR\INICIAR_TUDO.ps1" -Force
}
if (Test-Path "$AGENT_DIR\scripts\RESTAURAR_SISTEMA.ps1") {
    Copy-Item -Path "$AGENT_DIR\scripts\RESTAURAR_SISTEMA.ps1" -Destination "$COMET_DIR\RESTAURAR_SISTEMA.ps1" -Force
}

# ==================== RESUMO ====================
Write-Section "RESTAURACAO COMPLETA!"

Write-Host "O sistema foi restaurado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "Estrutura restaurada:" -ForegroundColor Cyan
Write-Host "  $COMET_DIR" -ForegroundColor White
Write-Host "    - comet_bridge.py" -ForegroundColor Gray
Write-Host "    - INICIAR_TUDO.ps1" -ForegroundColor Gray
Write-Host "    - RESTAURAR_SISTEMA.ps1" -ForegroundColor Gray
Write-Host "  $AGENT_DIR" -ForegroundColor White
Write-Host "    - agent/" -ForegroundColor Gray
Write-Host "    - frontend/" -ForegroundColor Gray
Write-Host ""
Write-Host "Para iniciar os servicos:" -ForegroundColor Yellow
Write-Host "  .\INICIAR_TUDO.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Ou reinicie o computador (iniciara automaticamente)" -ForegroundColor Yellow
Write-Host ""

# Perguntar se quer iniciar agora
$startNow = Read-Host "Deseja iniciar os servicos agora? (S/N)"
if ($startNow -eq "S" -or $startNow -eq "s") {
    & "$COMET_DIR\INICIAR_TUDO.ps1"
}
