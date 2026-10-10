# ============================================================
# CYBER - MODUL_WEB v2.0.0
# Web Analiz: sadece aktif açıkları gösterir, bulunmayanları göstermez.
# Admin panelleri, açık dosyalar, dizin listeleme, portlar, IP, DNS
# ============================================================

import os
import sys
import time
import socket
import ssl
import json
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

# ---------- ADMIN PANEL YOLLARI ----------
ADMIN_PANELLER = [
    "/admin", "/admin/", "/admin.php", "/admin.html", "/admin/login",
    "/administrator", "/administrator/", "/administrator/index.php",
    "/wp-admin", "/wp-admin/", "/wp-login.php", "/wp-login", "/wp-admin/admin.php",
    "/panel", "/panel/", "/panel/login", "/cpanel", "/cpanel/",
    "/plesk", "/plesk/", "/webmin", "/webmin/", "/phpmyadmin",
    "/phpmyadmin/", "/pma", "/pma/", "/adminer", "/adminer.php",
    "/login", "/login.php", "/login.html", "/signin", "/signin/",
    "/dashboard", "/dashboard/", "/manage", "/manage/", "/manager",
    "/manager/", "/console", "/console/", "/system", "/system/",
    "/control", "/control/", "/backend", "/backend/", "/secure",
    "/secure/", "/user", "/user/", "/users", "/users/",
    "/account", "/account/", "/profile", "/profile/",
    "/moderator", "/moderator/", "/staff", "/staff/",
    "/root", "/root/", "/superuser", "/superuser/",
    "/auth", "/auth/", "/oauth", "/oauth/", "/sso", "/sso/",
    "/cms", "/cms/", "/adminpanel", "/adminpanel/",
]

# ---------- AÇIK DOSYA YOLLARI ----------
ACIK_DOSYALAR = [
    "/.env", "/.env.bak", "/.env.local", "/.env.production",
    "/.git/config", "/.git/HEAD", "/.gitignore",
    "/.svn/entries", "/.htaccess", "/.htpasswd", "/.DS_Store",
    "/web.config", "/config.php", "/configuration.php",
    "/wp-config.php", "/wp-config.php.bak", "/wp-config.txt",
    "/config.json", "/config.yml", "/config.yaml", "/config.xml",
    "/settings.py", "/local_settings.py", "/database.yml",
    "/backup.sql", "/backup.zip", "/backup.tar.gz", "/dump.sql",
    "/db.sql", "/database.sql", "/data.sql",
    "/server-status", "/server-info", "/phpinfo.php", "/info.php",
    "/test.php", "/robots.txt", "/sitemap.xml",
    "/.well-known/security.txt", "/readme.html", "/readme.md",
    "/LICENSE", "/CHANGELOG.md", "/composer.json", "/package.json",
    "/Dockerfile", "/docker-compose.yml", "/.dockerignore",
    "/api/", "/api/v1/", "/api/v2/", "/graphql", "/graphiql",
    "/swagger.json", "/openapi.json", "/api-docs",
    "/console/", "/jmx-console/", "/web-console/",
    "/actuator", "/actuator/health", "/actuator/env",
    "/metrics", "/health", "/status", "/debug", "/trace",
    "/storage/", "/uploads/", "/files/", "/backup/", "/backups/",
    "/old/", "/temp/", "/tmp/", "/cache/", "/logs/",
    "/error.log", "/access.log", "/debug.log",
    "/.bash_history", "/.ssh/id_rsa", "/.aws/credentials",
    "/.kube/config", "/.npmrc", "/.pypirc",
    "/cgi-bin/", "/cgi-bin/test.cgi", "/cgi-bin/printenv",
    "/shell.php", "/cmd.php", "/webshell.php", "/xmlrpc.php",
    "/wp-json/", "/wp-json/wp/v2/users",
    "/www.zip", "/www.tar.gz", "/site.zip", "/site.tar.gz",
    "/.index.php.swp", "/index.php.bak", "/index.html.bak",
]

# ---------- DİZİN LİSTELEME YOLLARI ----------
DIZIN_LISTELEME = [
    "/", "/..", "/../", "/./", "/%2e%2e/", "/%2e/",
    "/backup/", "/backups/", "/bak/", "/old/", "/new/",
    "/temp/", "/tmp/", "/files/", "/uploads/", "/images/",
    "/img/", "/css/", "/js/", "/assets/", "/static/",
    "/media/", "/video/", "/audio/", "/download/", "/downloads/",
    "/docs/", "/doc/", "/data/", "/db/", "/log/", "/logs/",
    "/private/", "/secret/", "/hidden/", "/internal/",
    "/.git/", "/.svn/", "/.hg/", "/.bzr/", "/CVS/",
]

# ---------- PORTLAR ----------
PORTLAR = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    993, 995, 1433, 1521, 1723, 3306, 3389, 5432, 5900, 6379,
    8080, 8443, 8888, 9000, 9090, 9200, 9300, 27017
]

# ---------- ALT ALAN ADLARI ----------
ALT_ALANLAR = [
    "www", "mail", "ftp", "webmail", "smtp", "pop", "imap", "admin",
    "administrator", "api", "dev", "test", "staging", "beta", "demo",
    "blog", "shop", "store", "portal", "cpanel", "whm", "ns1", "ns2",
    "dns", "dns1", "dns2", "vpn", "remote", "secure", "ssl", "cdn",
    "static", "assets", "img", "images", "media", "video", "files",
    "docs", "doc", "help", "support", "forum", "community", "wiki",
    "git", "gitlab", "github", "jenkins", "ci", "build", "deploy",
    "db", "database", "sql", "mysql", "postgres", "mongo", "redis",
    "monitor", "metrics", "status", "health", "log", "logs", "elk",
    "kibana", "grafana", "prometheus", "nagios", "zabbix",
    "old", "new", "backup", "bak", "temp", "tmp", "private", "internal",
    "intranet", "extranet", "partner", "client", "customer", "user",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

def temizle():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    temizle()
    print(f"""{R.C}{R.KA}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
{R.SF}""")
    print(f"{R.MO}{R.KA}              WEB ANALIZ ARACI{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}\n")

def ssl_ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c

def normalize(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url.rstrip("/")

def http_istek(url: str, zaman: int = 8):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": "*/*",
            "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
            "Connection": "close",
        })
        with urllib.request.urlopen(req, timeout=zaman, context=ssl_ctx()) as y:
            return y.status, dict(y.headers), y.read(8192)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers) if e.headers else {}, b""
    except Exception:
        return None, {}, b""

def yol_tara(taban: str, yol: str):
    url = taban + yol
    kod, basliklar, icerik = http_istek(url)
    if kod and kod < 400:
        boyut = len(icerik)
        tip = basliklar.get("Content-Type", "")
        sunucu = basliklar.get("Server", "")
        return (yol, kod, boyut, tip, sunucu)
    return None

# ==================== AKTİF TARAMALAR ====================
def admin_panel_tara(taban: str):
    print(f"{R.MO}{R.KA}[ ADMIN PANEL TARAMASI ]{R.SF}")
    print(f"{R.S}{len(ADMIN_PANELLER)} yol taranıyor...{R.SF}\n")
    bulunanlar = []
    with ThreadPoolExecutor(max_workers=32) as ex:
        gorevler = {ex.submit(yol_tara, taban, y): y for y in ADMIN_PANELLER}
        for g in as_completed(gorevler):
            try:
                s = g.result()
                if s:
                    yol, kod, boyut, tip, sunucu = s
                    bulunanlar.append(s)
                    print(f"{R.Y}[PANEL]{R.SF} {R.C}{yol}{R.SF} | {R.Y}{kod}{R.SF} | {boyut}B | {tip} | {sunucu}")
            except Exception:
                pass
    if not bulunanlar:
        print(f"{R.K}Admin panel bulunamadı.{R.SF}")
    else:
        print(f"\n{R.Y}Toplam: {len(bulunanlar)} panel{R.SF}")
    return bulunanlar

def acik_dosya_tara(taban: str):
    print(f"\n{R.MO}{R.KA}[ AÇIK DOSYA TARAMASI ]{R.SF}")
    print(f"{R.S}{len(ACIK_DOSYALAR)} yol taranıyor...{R.SF}\n")
    bulunanlar = []
    with ThreadPoolExecutor(max_workers=32) as ex:
        gorevler = {ex.submit(yol_tara, taban, y): y for y in ACIK_DOSYALAR}
        for g in as_completed(gorevler):
            try:
                s = g.result()
                if s:
                    yol, kod, boyut, tip, sunucu = s
                    bulunanlar.append(s)
                    print(f"{R.Y}[DOSYA]{R.SF} {R.C}{yol}{R.SF} | {R.Y}{kod}{R.SF} | {boyut}B | {tip}")
            except Exception:
                pass
    if not bulunanlar:
        print(f"{R.K}Açık dosya bulunamadı.{R.SF}")
    else:
        print(f"\n{R.Y}Toplam: {len(bulunanlar)} dosya{R.SF}")
    return bulunanlar

def dizin_listeleme_tara(taban: str):
    print(f"\n{R.MO}{R.KA}[ DİZİN LİSTELEME TARAMASI ]{R.SF}")
    print(f"{R.S}{len(DIZIN_LISTELEME)} yol taranıyor...{R.SF}\n")
    bulunanlar = []
    with ThreadPoolExecutor(max_workers=32) as ex:
        gorevler = {ex.submit(yol_tara, taban, y): y for y in DIZIN_LISTELEME}
        for g in as_completed(gorevler):
            try:
                s = g.result()
                if s:
                    yol, kod, boyut, tip, sunucu = s
                    bulunanlar.append(s)
                    print(f"{R.Y}[INDEX]{R.SF} {R.C}{yol}{R.SF} | {R.Y}{kod}{R.SF} | {boyut}B | {tip}")
            except Exception:
                pass
    if not bulunanlar:
        print(f"{R.K}Dizin listeleme bulunamadı.{R.SF}")
    else:
        print(f"\n{R.Y}Toplam: {len(bulunanlar)} dizin{R.SF}")
    return bulunanlar

def port_tara(host: str):
    print(f"\n{R.MO}{R.KA}[ PORT TARAMASI ]{R.SF}")
    print(f"{R.S}{len(PORTLAR)} port taranıyor...{R.SF}\n")
    aciklar = []
    for p in PORTLAR:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            if s.connect_ex((host, p)) == 0:
                aciklar.append(p)
                print(f"{R.Y}[PORT]{R.SF} {R.C}{p}{R.SF} açık")
        except Exception:
            pass
        s.close()
    if not aciklar:
        print(f"{R.K}Açık port bulunamadı.{R.SF}")
    else:
        print(f"\n{R.Y}Toplam: {len(aciklar)} port{R.SF}")
    return aciklar

def alt_alan_tara(domain: str):
    print(f"\n{R.MO}{R.KA}[ ALT ALAN ADI TARAMASI ]{R.SF}")
    print(f"{R.S}{len(ALT_ALANLAR)} alt alan deneniyor...{R.SF}\n")
    bulunanlar = []
    def dene(alt):
        tam = f"{alt}.{domain}"
        try:
            ip = socket.gethostbyname(tam)
            return (tam, ip)
        except Exception:
            return None
    with ThreadPoolExecutor(max_workers=32) as ex:
        gorevler = {ex.submit(dene, a): a for a in ALT_ALANLAR}
        for g in as_completed(gorevler):
            try:
                s = g.result()
                if s:
                    bulunanlar.append(s)
                    print(f"{R.Y}[SUB]{R.SF} {R.C}{s[0]}{R.SF} -> {R.Y}{s[1]}{R.SF}")
            except Exception:
                pass
    if not bulunanlar:
        print(f"{R.K}Alt alan bulunamadı.{R.SF}")
    else:
        print(f"\n{R.Y}Toplam: {len(bulunanlar)} alt alan{R.SF}")
    return bulunanlar

def dns_tara(domain: str):
    print(f"\n{R.MO}{R.KA}[ DNS KAYITLARI ]{R.SF}")
    sonuc = {}
    try:
        sonuc["A"] = socket.gethostbyname_ex(domain)[2]
    except Exception:
        sonuc["A"] = []
    try:
        sonuc["AAAA"] = [x[4][0] for x in socket.getaddrinfo(domain, None, socket.AF_INET6)]
    except Exception:
        sonuc["AAAA"] = []
    for tip in ["NS", "MX", "TXT", "CNAME", "SOA"]:
        try:
            url = f"https://dns.google/resolve?name={domain}&type={tip}"
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=8, context=ssl_ctx()) as y:
                v = json.loads(y.read().decode())
            sonuc[tip] = [a.get("data") for a in v.get("Answer", [])]
        except Exception:
            sonuc[tip] = []
    for k, v in sonuc.items():
        if v:
            print(f"{R.C}{k:6}{R.SF} : {R.Y}{v}{R.SF}")
    return sonuc

def header_tara(taban: str):
    print(f"\n{R.MO}{R.KA}[ HTTP BAŞLIKLARI ]{R.SF}")
    kod, basliklar, _ = http_istek(taban)
    if kod:
        print(f"{R.C}Durum:{R.SF} {R.Y}{kod}{R.SF}")
        for k, v in basliklar.items():
            print(f"{R.C}{k:22}{R.SF} : {R.Y}{v}{R.SF}")
    else:
        print(f"{R.K}Bağlantı kurulamadı.{R.SF}")
    return basliklar

def whois_tara(domain: str):
    print(f"\n{R.MO}{R.KA}[ WHOIS ]{R.SF}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(6)
        s.connect(("whois.iana.org", 43))
        s.send((domain + "\r\n").encode())
        v = b""
        while True:
            p = s.recv(4096)
            if not p:
                break
            v += p
        s.close()
        print(v.decode("utf-8", errors="ignore")[:1500])
    except Exception as e:
        print(f"{R.K}Whois hata: {e}{R.SF}")

# ==================== ANA MENÜ ====================
def web_analiz_menu():
    banner()
    hedef = input(f"{R.C}Hedef URL veya domain > {R.SF}").strip()
    if not hedef:
        print(f"{R.K}Boş olamaz.{R.SF}")
        return
    taban = normalize(hedef)
    domain = urllib.parse.urlparse(taban).netloc or taban
    print(f"{R.S}Hedef: {R.Y}{taban}{R.SF}")
    print(f"{R.S}Domain: {R.Y}{domain}{R.SF}\n")

    print(f"{R.Y}[1]{R.SF} Tam tarama (tümü)")
    print(f"{R.Y}[2]{R.SF} Sadece admin panelleri")
    print(f"{R.Y}[3]{R.SF} Sadece açık dosyalar")
    print(f"{R.Y}[4]{R.SF} Sadece dizin listeleme")
    print(f"{R.Y}[5]{R.SF} Sadece port taraması")
    print(f"{R.Y}[6]{R.SF} Sadece alt alan adları")
    print(f"{R.Y}[7]{R.SF} Sadece DNS + Whois + Header")
    sec = input(f"{R.C}Seçim (1) > {R.SF}").strip() or "1"

    rapor = {"hedef": taban, "domain": domain, "tarih": time.strftime("%Y-%m-%d %H:%M:%S")}

    if sec in ("1", "7"):
        header_tara(taban)
        rapor["dns"] = dns_tara(domain)
        whois_tara(domain)
    if sec in ("1", "2"):
        rapor["admin"] = admin_panel_tara(taban)
    if sec in ("1", "3"):
        rapor["dosya"] = acik_dosya_tara(taban)
    if sec in ("1", "4"):
        rapor["dizin"] = dizin_listeleme_tara(taban)
    if sec in ("1", "5"):
        rapor["port"] = port_tara(domain)
    if sec in ("1", "6"):
        rapor["sub"] = alt_alan_tara(domain)

    klasor = Path("kayitlar")
    klasor.mkdir(exist_ok=True)
    dosya = klasor / f"web_{domain.replace('.', '_')}_{int(time.time())}.json"
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n{R.S}Rapor kaydedildi: {R.Y}{dosya}{R.SF}")