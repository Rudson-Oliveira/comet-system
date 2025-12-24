# ============================================
# MANUS-COMET-OBSIDIAN - Inicializacao Completa
# Inicia todos os servicos automaticamente
# ============================================

$ErrorActionPreference = "SilentlyContinue"

# Cores para output
function Write-Status($msg, $color = "White") {
    Write-Host $msg -ForegroundColor $color
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MANUS-COMET-OBSIDIAN" -ForegroundColor Cyan
Write-Host "  Inicializacao Automatica v1.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Definir caminhos
$COMET_DIR = "$env:USERPROFILE\COMET"
$AGENT_DIR = "$env:USERPROFILE\obsidian-agente\agent"
$LOG_DIR = "$env:USERPROFILE\COMET\logs"

# Criar pasta de logs se nao existir
if (-not (Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
}

$LOG_FILE = "$LOG_DIR\startup_$(Get-Date -Format 'yyyy-MM-dd').log"

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $msg" | Out-File -FilePath $LOG_FILE -Append
    Write-Status $msg
}

# ==================== PASSO 1: Verificar dependencias ====================
Log "[1/4] Verificando dependencias..."

# Verificar Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Log "[ERRO] Python nao encontrado!" "Red"
    pause
    exit 1
}
Log "  Python: $pythonVersion" "Green"

# Verificar ngrok
$ngrokVersion = ngrok version 2>&1
if ($LASTEXITCODE -ne 0) {
    Log "[AVISO] ngrok nao encontrado. Instale com: winget install ngrok.ngrok" "Yellow"
} else {
    Log "  ngrok: $ngrokVersion" "Green"
}

# ==================== PASSO 2: Iniciar COMET Bridge ====================
Log "[2/4] Iniciando COMET Bridge..."

# Verificar se ja esta rodando
$cometProcess = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($cometProcess) {
    Log "  COMET Bridge ja esta rodando na porta 5000" "Yellow"
} else {
    # Iniciar COMET Bridge
    if (Test-Path "$COMET_DIR\comet_bridge.py") {
        Start-Process powershell -ArgumentList "-NoExit -Command cd '$COMET_DIR'; python comet_bridge.py" -WindowStyle Minimized
        Start-Sleep -Seconds 3
        Log "  COMET Bridge iniciado!" "Green"
    } else {
        Log "[ERRO] comet_bridge.py nao encontrado em $COMET_DIR" "Red"
    }
}

# ==================== PASSO 3: Iniciar Obsidian Agent ====================
Log "[3/4] Iniciando Obsidian Agent..."

# Verificar se ja esta rodando
$agentProcess = Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue
if ($agentProcess) {
    Log "  Obsidian Agent ja esta rodando na porta 5001" "Yellow"
} else {
    # Iniciar Obsidian Agent
    if (Test-Path "$AGENT_DIR\agent.py") {
        Start-Process powershell -ArgumentList "-NoExit -Command cd '$AGENT_DIR'; python agent.py" -WindowStyle Minimized
        Start-Sleep -Seconds 3
        Log "  Obsidian Agent iniciado!" "Green"
    } else {
        Log "[ERRO] agent.py nao encontrado em $AGENT_DIR" "Red"
    }
}

# ==================== PASSO 4: Iniciar ngrok ====================
Log "[4/4] Iniciando ngrok..."

# Verificar se ngrok ja esta rodando
$ngrokProcess = Get-Process -Name ngrok -ErrorAction SilentlyContinue
if ($ngrokProcess) {
    Log "  ngrok ja esta rodando" "Yellow"
} else {
    # Iniciar ngrok
    $ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue
    if ($ngrokPath) {
        Start-Process powershell -ArgumentList "-NoExit -Command ngrok http 5000" -WindowStyle Minimized
        Start-Sleep -Seconds 5
        Log "  ngrok iniciado!" "Green"
    } else {
        Log "[AVISO] ngrok nao encontrado. Execute manualmente: ngrok http 5000" "Yellow"
    }
}

# ==================== RESUMO ====================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INICIALIZACAO COMPLETA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Servicos:" -ForegroundColor Cyan
Write-Host "  COMET Bridge:    http://localhost:5000" -ForegroundColor White
Write-Host "  Obsidian Agent:  http://localhost:5001" -ForegroundColor White
Write-Host "  ngrok Dashboard: http://127.0.0.1:4040" -ForegroundColor White
Write-Host ""
Write-Host "Para ver a URL publica do ngrok:" -ForegroundColor Yellow
Write-Host "  Abra: http://127.0.0.1:4040" -ForegroundColor Yellow
Write-Host ""
Write-Host "Log salvo em: $LOG_FILE" -ForegroundColor Gray
Write-Host ""

Log "Inicializacao completa!"
