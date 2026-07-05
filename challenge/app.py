from flask import Flask, request, jsonify, make_response
import secrets, base64

app = Flask(__name__)

FLAG = "CTF{d4rk_truths_4r3_h1dd3n_1n_pl41n_s1ght}"
sessions = {}
tokens   = {}

b64_hint = base64.b64encode(b"X-Bootstrap: enable").decode()
b64_hint2 = base64.b64encode(b"/robots.txt").decode()

HTML_PAGE = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>NEXUS // Terminal Interface v3.7.1</title>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap" rel="stylesheet"/>
<script>
tailwind.config={{theme:{{extend:{{colors:{{terminal:'#0B0C10',terminal2:'#121212',matrix:'#1F2833',lime:'#00FF66',orange:'#FF7700',warnred:'#ff3b3b'}},fontFamily:{{mono:['"JetBrains Mono"','monospace']}}}}}}}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{color-scheme:dark}}
body{{font-family:'JetBrains Mono',monospace;background:#0B0C10;min-height:100vh;display:flex;align-items:center;justify-content:center}}
.grid-bg{{background-image:linear-gradient(rgba(0,255,102,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,102,0.04) 1px,transparent 1px);background-size:42px 42px}}
.scanlines::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;background:repeating-linear-gradient(to bottom,rgba(0,0,0,0) 0,rgba(0,0,0,0) 2px,rgba(0,0,0,0.06) 3px,rgba(0,0,0,0) 4px)}}
.glow-lime{{box-shadow:0 0 12px rgba(0,255,102,0.35),inset 0 0 6px rgba(0,255,102,0.08)}}
.glow-orange{{box-shadow:0 0 12px rgba(255,119,0,0.35),inset 0 0 6px rgba(255,119,0,0.08)}}
.glow-text{{text-shadow:0 0 8px rgba(0,255,102,0.55),0 0 22px rgba(0,255,102,0.25)}}
.glow-hover{{transition:box-shadow .2s ease,border-color .2s ease}}
.glow-hover:hover{{box-shadow:0 0 18px rgba(0,255,102,0.45)}}
::-webkit-scrollbar{{width:6px}}
::-webkit-scrollbar-track{{background:#0B0C10}}
::-webkit-scrollbar-thumb{{background:#1F2833;border:1px solid #00FF6633}}
::-webkit-scrollbar-thumb:hover{{background:#00FF66}}
.pulse-dot{{animation:pulse-dot 1.5s ease-in-out infinite}}
@keyframes pulse-dot{{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}
.crt{{animation:crt-flicker 8s infinite}}
@keyframes crt-flicker{{0%{{opacity:1}}50%{{opacity:0.98}}}}
.terminal-box{{background:linear-gradient(135deg,#0B0C10 0%,#111 100%)}}
.log-line{{animation:fadeIn .5s ease both;border-left:2px solid #00FF66;padding-left:12px;margin-bottom:8px}}
@keyframes fadeIn{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:translateX(0)}}}}
</style>
</head>
<body class="grid-bg scanlines">
<div class="relative w-full max-w-4xl mx-4 crt">
  <div class="absolute -top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-lime/5 rounded-full blur-3xl pointer-events-none"></div>

  <div class="terminal-box border border-matrix rounded-lg overflow-hidden glow-lime">
    <div class="flex items-center gap-2 px-4 py-3 border-b border-matrix bg-matrix/40">
      <span class="w-3 h-3 rounded-full bg-warnred/80"></span>
      <span class="w-3 h-3 rounded-full bg-yellow-500/80"></span>
      <span class="w-3 h-3 rounded-full bg-lime/80"></span>
      <span class="ml-3 text-xs text-gray-400">agent@nexus: ~/recon/logs</span>
    </div>

    <div class="p-6 sm:p-10">
      <div class="flex items-center gap-2 mb-6">
        <span class="text-lime text-sm font-bold">$</span>
        <span class="text-white text-sm font-bold">cat /var/log/bootstrap.log</span>
        <span class="w-2 h-5 bg-lime pulse-dot"></span>
      </div>

      <div class="log-line text-xs text-lime/80" style="animation-delay:0.1s">[2026-07-04 14:00:00] NEXUS::bootstrap iniciando secuencia de arranque...</div>
      <div class="log-line text-xs text-lime/80" style="animation-delay:0.3s">[2026-07-04 14:00:01] NEXUS::kernel Cargando módulos del sistema...</div>
      <div class="log-line text-xs text-lime/80" style="animation-delay:0.5s">[2026-07-04 14:00:02] NEXUS::network Interfaz de red activa en 0.0.0.0:9090</div>
      <div class="log-line text-xs text-lime/80" style="animation-delay:0.7s">[2026-07-04 14:00:03] NEXUS::fs Detectada estructura de directorios oculta</div>
      <div class="log-line text-xs text-gray-400" style="animation-delay:0.9s">[2026-07-04 14:00:04] NEXUS::hint El acceso a ciertos paths requiere autenticación de múltiples factores</div>
      <div class="log-line text-xs text-orange/80" style="animation-delay:1.1s">[2026-07-04 14:00:05] NEXUS::warning Endpoints sensibles detectados: /init, /portal, /flag</div>
      <div class="log-line text-xs text-gray-400" style="animation-delay:1.3s">[2026-07-04 14:00:06] NEXUS::hint Revisa el mapa del sitio antes de continuar</div>
      <div class="log-line text-xs text-gray-500" style="animation-delay:1.5s">[2026-07-04 14:00:07] NEXUS::debug Coded message follows...</div>
      <div class="log-line text-xs text-gray-500" style="animation-delay:1.7s">[2026-07-04 14:00:08] NEXUS::debug {b64_hint}</div>

      <div class="mt-8 border border-matrix rounded-md bg-terminal/80 p-5 sm:p-7">
        <div class="text-[10px] uppercase tracking-[0.3em] text-orange mb-4">// BRIEFING</div>
        <p class="text-xs text-gray-300 leading-relaxed">
          Has sido desplegado en un sistema NEXUS versión 3.7.1. El objetivo es obtener la flag de acceso.
          El sistema tiene <span class="text-orange font-bold">múltiples capas de seguridad</span>.
          Deberás descubrir los endpoints ocultos, autenticarte en cada etapa y escalar privilegios hasta
          alcanzar el recurso protegido.
        </p>
        <p class="text-xs text-gray-300 mt-3">
          <span class="text-lime">Pista:</span> No todo se ve a simple vista. A veces los mensajes
          vienen <span class="text-orange">codificados</span>.
        </p>
      </div>
    </div>
  </div>
</div>

<div class="fixed bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4 sm:gap-6">
  <a href="https://v-sandbox.vultaethel.com" target="_blank"><img src="https://v-sandbox.vultaethel.com/assets/images/logo/logo-transparent.png" alt="V-SANDBOX" class="h-6 sm:h-7 w-auto opacity-60 hover:opacity-100 transition"/></a>
  <a href="https://vultaethel.com" target="_blank"><img src="https://v-sandbox.vultaethel.com/assets/images/sponsors/logovultaethelsponsor.png" alt="VULTAETHEL" class="h-5 sm:h-6 w-auto opacity-60 hover:opacity-100 transition"/></a>
  <span class="text-[9px] text-gray-600 tracking-[0.3em]">NEXUS // FLASH EASY</span>
</div>

<div class="fixed bottom-16 left-1/2 -translate-x-1/2 w-full max-w-md px-4">
  <div class="terminal-box border border-matrix rounded-lg overflow-hidden">
    <div class="flex items-center gap-2 px-3 py-2 border-b border-matrix bg-matrix/40">
      <span class="w-2 h-2 rounded-full bg-warnred/80"></span>
      <span class="w-2 h-2 rounded-full bg-yellow-500/80"></span>
      <span class="w-2 h-2 rounded-full bg-lime/80"></span>
      <span class="ml-2 text-[10px] text-gray-400">flag_validator</span>
    </div>
    <div class="p-3">
      <form id="submitForm" class="flex gap-2" autocomplete="off">
        <div class="flex items-center flex-1 border border-matrix focus-within:border-lime bg-terminal rounded-sm px-2 transition">
          <span class="text-lime text-xs mr-1 select-none">$</span>
          <input id="flagInput" type="text" placeholder="CTF{...}"
                 class="flex-1 bg-transparent py-2 text-xs text-white placeholder-gray-600 focus:outline-none font-mono"/>
        </div>
        <button type="submit"
                class="text-[11px] font-bold text-terminal bg-orange px-3 py-2 rounded-sm hover:brightness-110 transition whitespace-nowrap">
          VALIDAR
        </button>
      </form>
      <div id="submitResult" class="mt-2 text-[10px] hidden"></div>
    </div>
  </div>
</div>

<script>
document.getElementById('submitForm').addEventListener('submit', async function(e) {{
  e.preventDefault();
  const input = document.getElementById('flagInput');
  const result = document.getElementById('submitResult');
  const val = input.value.trim();
  if (!val) {{ result.className = 'mt-2 text-[10px] text-gray-400'; result.textContent = '[*] Ingresa una flag.'; result.classList.remove('hidden'); return; }}
  try {{
    const resp = await fetch('/submit', {{ method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{flag:val}}) }});
    const data = await resp.json();
    if (data.status === 'correct') {{
      result.className = 'mt-2 text-[10px] text-lime font-bold';
      result.textContent = '[+] ' + data.message;
    }} else {{
      result.className = 'mt-2 text-[10px] text-warnred font-bold';
      result.textContent = '[-] ' + data.message;
    }}
  }} catch(e) {{
    result.className = 'mt-2 text-[10px] text-warnred';
    result.textContent = '[!] Error de conexión.';
  }}
  result.classList.remove('hidden');
}});
</script>
</body>
</html>"""

@app.route('/')
def index():
    return make_response(HTML_PAGE)

@app.route('/robots.txt')
def robots():
    return make_response("User-agent: *\nDisallow: /init\nDisallow: /portal\nDisallow: /flag\n", 200, {'Content-Type': 'text/plain'})

@app.route('/init', methods=['GET', 'POST'])
def init_endpoint():
    if request.method == 'GET':
        return jsonify({"error": "METHOD_NOT_ALLOWED", "allowed": ["POST"], "hint": "init requires bootstrap token"}), 405
    if request.headers.get('X-Bootstrap') != 'enable':
        return jsonify({"error": "FORBIDDEN", "message": "Missing or invalid bootstrap token"}), 403
    session_id = secrets.token_hex(16)
    sessions[session_id] = True
    return jsonify({"status": "SESSION_CREATED", "session_id": session_id, "next": "/portal"})

@app.route('/portal', methods=['POST'])
def portal():
    data = request.get_json(force=True, silent=True)
    if not data or 'session_id' not in data:
        return jsonify({"error": "BAD_REQUEST", "message": "session_id required in JSON body"}), 400
    if data['session_id'] not in sessions:
        return jsonify({"error": "FORBIDDEN", "message": "Invalid or expired session_id"}), 403
    auth_token = secrets.token_hex(32)
    tokens[auth_token] = True
    return jsonify({"status": "AUTH_GRANTED", "auth_token": auth_token, "next": "/flag"})

@app.route('/flag')
def flag():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({"error": "UNAUTHORIZED", "message": "Bearer token required in Authorization header"}), 401
    token = auth[7:]
    if token not in tokens:
        return jsonify({"error": "FORBIDDEN", "message": "Invalid or expired token"}), 403
    return jsonify({"status": "ACCESS_GRANTED", "flag": FLAG})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(force=True, silent=True) or request.form
    flag = data.get('flag', '')
    if flag == FLAG:
        return jsonify({"status": "correct", "message": "ACCESS GRANTED // Flag verificada correctamente. Has completado el reto NEXUS."})
    return jsonify({"status": "incorrect", "message": "ACCESS DENIED // Flag inválida. Sigue analizando el sistema."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
