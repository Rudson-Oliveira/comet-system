#!/usr/bin/env python3
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 5000

class CometBridgeHandler(BaseHTTPRequestHandler ):
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
print(f"Servidor em http://localhost:{PORT}" )
print("POST /exec - Executar PowerShell")
print("-" * 50)
HTTPServer(('0.0.0.0', PORT), CometBridgeHandler).serve_forever()
