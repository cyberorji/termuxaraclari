# ============================================================
# CYBER - MODUL_IP v3.0.0
# IP sorgu + DNS kayıtları (A, AAAA, MX, NS, TXT, CNAME)
# ============================================================

import os, json, time, datetime, socket, urllib.request
from pathlib import Path

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

APILER = [
    "http://ip-api.com/json/{}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query",
    "https://ipwho.is/{}",
    "https://ipinfo.io/{}/json",
]

def temizle():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    temizle()
    print(f"""{R.C}{R.KA}
╔══════════════════════════════════════════════════════════════╗
║                      CYBER : IP SORGU                        ║
║           [ Konum • ISP • DNS • Proxy • Hosting ]           ║
╚══════════════════════════════════════════════════════════════╝
{R.SF}""")

def http_get(url: str, zaman: int = 10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CYBER/3.0"})
        with urllib.request.urlopen(req, timeout=zaman) as y:
            return json.loads(y.read().decode("utf-8"))
    except Exception as e:
        return {"hata": str(e)}

def ip_sorgula(ip: str) -> dict:
    for api in APILER:
        v = http_get(api.format(ip))
        if v and "hata" not in v:
            return v
        time.sleep(0.3)
    return {"hata": "Tüm API'ler başarısız"}

def dns_kayitlari(domain: str) -> dict:
    sonuc = {}
    try:
        sonuc["A"] = socket.gethostbyname_ex(domain)[2]
    except Exception:
        sonuc["A"] = []
    try:
        sonuc["AAAA"] = [x[4][0] for x in socket.getaddrinfo(domain, None, socket.AF_INET6)]
    except Exception:
        sonuc["AAAA"] = []
    # NS, MX, TXT, CNAME için ücretsiz DNS-over-HTTPS (Google)
    for tip in ["NS", "MX", "TXT", "CNAME", "SOA"]:
        try:
            url = f"https://dns.google/resolve?name={domain}&type={tip}"
            v = http_get(url)
            if v and v.get("Answer"):
                sonuc[tip] = [a.get("data") for a in v["Answer"]]
            else:
                sonuc[tip] = []
        except Exception:
            sonuc[tip] = []
    return sonuc

def kaydet(k: str, veri: dict):
    klasor = Path("kayitlar")
    klasor.mkdir(exist_ok=True)
    d = klasor / f"ip_{k.replace('.', '_')}_{int(time.time())}.json"
    with open(d, "w", encoding="utf-8") as f:
        json.dump({"hedef": k, "tarih": datetime.datetime.now().isoformat(), "veri": veri},
                  f, ensure_ascii=False, indent=2)
    return d

def yazdir(veri: dict):
    if "hata" in veri:
        print(f"{R.K}Hata: {veri['hata']}{R.SF}")
        return
    for k, v in veri.items():
        print(f"{R.C}{k:15}{R.SF} : {R.Y}{v}{R.SF}")

def ip_sorgu_menu():
    banner()
    ip = input(f"{R.C}IP veya domain (boş = kendi IP) > {R.SF}").strip()
    if not ip:
        ip = http_get("https://api.ipify.org?format=json").get("ip", "")
    if not ip:
        print(f"{R.K}IP alınamadı.{R.SF}")
        return
    print(f"{R.S}Sorgulanıyor: {ip}{R.SF}\n")
    veri = ip_sorgula(ip)
    print(f"{R.Y}{'-'*52}{R.SF}")
    print(f"{R.MO}{R.KA}[ IP BİLGİSİ ]{R.SF}")
    yazdir(veri)
    # Domain ise DNS kayıtları
    if not ip.replace(".", "").isdigit():
        print(f"\n{R.MO}{R.KA}[ DNS KAYITLARI ]{R.SF}")
        dns = dns_kayitlari(ip)
        for k, v in dns.items():
            print(f"{R.C}{k:8}{R.SF} : {R.Y}{v}{R.SF}")
        veri["dns"] = dns
    print(f"{R.Y}{'-'*52}{R.SF}")
    d = kaydet(ip, veri)
    print(f"{R.S}Kayıt: {R.Y}{d}{R.SF}")