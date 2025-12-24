@echo off
REM ============================================
REM   INICIALIZADOR UNIFICADO - SISTEMA IA
REM   Criado por Manus para Rudson-Oliveira
REM   Data: 24-12-2025 (COM HUB CENTRAL)
REM ============================================
REM ORDEM DE INICIALIZACAO:
REM 1. Obsidian (precisa abrir primeiro)
REM 2. ngrok (com dominio estatico)
REM 3. COMET Bridge (espera Obsidian)
REM 4. Obsidian Agent (espera COMET)
REM 5. Hub Central (coordenador)
REM 6. Frontend (interface)
REM ============================================

echo ============================================
echo   INICIANDO SISTEMA DE IA...
echo ============================================

REM === PASSO 1: OBSIDIAN ===
echo [1/6] Abrindo Obsidian...
start "" "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
echo Aguardando Obsidian carregar (15 segundos)...
timeout /t 15 /nobreak >nul

REM === PASSO 2: NGROK COM DOMINIO ESTATICO ===
echo [2/6] Iniciando ngrok com dominio fixo...
start "ngrok" cmd /c "ngrok http 5000 --url=charmless-maureen-subadministratively.ngrok-free.dev"
timeout /t 5 /nobreak >nul

REM === PASSO 3: COMET BRIDGE ===
echo [3/6] Iniciando COMET Bridge...
start "COMET Bridge" cmd /c "cd /d C:\Users\rudpa\COMET && python manus_bridge_unified.py"
echo Aguardando COMET iniciar (10 segundos)...
timeout /t 10 /nobreak >nul

REM === PASSO 4: OBSIDIAN AGENT ===
echo [4/6] Iniciando Obsidian Agent...
start "Obsidian Agent" cmd /c "cd /d C:\Users\rudpa\obsidian-agente\agent && python agent.py"
timeout /t 5 /nobreak >nul

REM === PASSO 5: HUB CENTRAL ===
echo [5/6] Iniciando Hub Central...
start "Hub Central" cmd /c "cd /d C:\Users\rudpa\hub_central && python hub_server.py"
timeout /t 3 /nobreak >nul

REM === PASSO 6: FRONTEND ===
echo [6/6] Iniciando Frontend...
start "Frontend" cmd /c "cd /d C:\Users\rudpa\obsidian-agente\frontend && npm run dev"

echo ============================================
echo   SISTEMA INICIADO COM SUCESSO!
echo   URL FIXA: charmless-maureen-subadministratively.ngrok-free.dev
echo   Hub Central: http://localhost:5002
echo   Frontend: http://localhost:5173
echo ============================================
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul

