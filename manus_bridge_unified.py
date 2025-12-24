#!/usr/bin/env python3
import subprocess
import json
import urllib.request
import urllib.error
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os

PORT = 5000
OBSIDIAN_PORT = 27124
OBSIDIAN_API_KEY = "475ba2e794a2f8312e05dbe801debaf55f232ee98aafd68c7b0b44de19d628fd"
OBSIDIAN_BASE_URL = f"https://127.0.0.1:{OBSIDIAN_PORT}"
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

def obsidian_request(method, endpoint, data=None, content_type="application/json"):
    url = f"{OBSIDIAN_BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {OBSIDIAN_API_KEY}", "Content-Type": content_type}
    if data and isinstance(data, dict): data = json.dumps(data).encode("utf-8")
    elif data and isinstance(data, str): data = data.encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as response:
            result = response.read().decode("utf-8")
            try: return {"success": True, "data": json.loads(result)}
            except: return {"success": True, "data": result}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        return {"success": False, "error": error_body, "status": e.code}
    except Exception as e: return {"success": False, "error": str(e)}

def execute_powershell(command, timeout=60):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=timeout)
        return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}
    except subprocess.TimeoutExpired: return {"success": False, "error": "Timeout"}
    except Exception as e: return {"success": False, "error": str(e)}

class UnifiedBridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): print(f"[{datetime.now().strftime("%H:%M:%S")}] {args[0]}")
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def get_body(self):
        cl = int(self.headers.get("Content-Length", 0))
        if cl > 0:
            body = self.rfile.read(cl).decode("utf-8")
            try: return json.loads(body)
            except: return body
        return {}
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ["/", "/health"]:
            obs = obsidian_request("GET", "/")
            self.send_json({"status": "online", "service": "MANUS-COMET-OBSIDIAN Bridge", "obsidian": "online" if obs.get("success") else "offline"})
        elif path == "/obsidian/vault" or path == "/obsidian/vault/":
            self.send_json(obsidian_request("GET", "/vault/"))
        elif path.startswith("/obsidian/vault/"):
            self.send_json(obsidian_request("GET", f"/vault/{path.replace("/obsidian/vault/", "")}"))
        else: self.send_json({"error": "Not found"}, 404)
    def do_POST(self):
        path = self.path.split("?")[0]
        body = self.get_body()
        if path in ["/exec", "/powershell"]:
            cmd = body.get("command", "") if isinstance(body, dict) else ""
            if not cmd: self.send_json({"error": "No command"}, 400); return
            print(f"\n[EXEC] {cmd[:80]}...")
            self.send_json(execute_powershell(cmd))
        elif path.startswith("/obsidian/vault/"):
            note = path.replace("/obsidian/vault/", "")
            content = body.get("content", "") if isinstance(body, dict) else body
            self.send_json(obsidian_request("PUT", f"/vault/{note}", content, "text/markdown"))
        elif path == "/obsidian/search":
            q = body.get("query", "") if isinstance(body, dict) else ""
            self.send_json(obsidian_request("POST", "/search/simple/", {"query": q}))
        else: self.send_json({"error": "Not found"}, 404)
    def do_PUT(self): self.do_POST()

if __name__ == "__main__":
    print("="*50)
    print("  MANUS-COMET-OBSIDIAN BRIDGE v1.0")
    print("="*50)
    print(f"Servidor: http://localhost:{PORT}")
    print("Endpoints: /exec, /obsidian/vault/, /obsidian/search")
    print("-"*50)
    obs = obsidian_request("GET", "/")
    print(f"Obsidian: {"OK" if obs.get("success") else "OFFLINE"}")
    HTTPServer(("0.0.0.0", PORT), UnifiedBridgeHandler).serve_forever()
