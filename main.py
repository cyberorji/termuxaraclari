# ============================================================
# CYBER - ANA MENÜ v7.0.0# 4 seçenekli: IP Sorgu, DOS Saldırısı, Web Analiz, SMS Bomber
# ============================================================

import os
import sys
import time
import platform
import datetime

from modul_ip import ip_sorgu_menu
from modul_ddos import ddos_menu
from modul_web import web_analiz_menu
from smsbomber import smsbomber_menu

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

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
    print(f"{R.MO}{R.KA}              CYBER TOOL v7.0.0{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}")
    print(f"{R.S}  Sistem : {R.Y}{platform.system()} {platform.release()}{R.SF}")
    print(f"{R.S}  Python : {R.Y}{platform.python_version()}{R.SF}")
    print(f"{R.S}  Tarih  : {R.Y}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{R.SF}")
    print()

def menu():
    print(f"""{R.M}{R.KA}
╔══════════════════════════════════════════════════════════════════════╗
║                          CYBER ANA MENÜ                              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   {R.Y}[1]{R.M}  IP SORGU          → Konum, ISP, DNS, cihaz, proxy      ║
║   {R.Y}[2]{R.M}  DOS SALDIRISI     → 600 thread, GET/POST/HEAD, süreli  ║
║   {R.Y}[3]{R.M}  WEB ANALIZ        → index, admin, DNS, açık dosyalar   ║
║   {R.Y}[4]{R.M}  SMS BOMBER        → Normal / Turbo, 90+ Türk servisi   ║
║                                                                      ║
║   {R.K}[0]{R.M}  ÇIKIŞ                                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{R.SF}""")

def main():
    while True:
        banner()
        menu()
        secim = input(f"{R.C}Seçim > {R.SF}").strip()
        if secim == "1":
            ip_sorgu_menu()
        elif secim == "2":
            ddos_menu()
        elif secim == "3":
            web_analiz_menu()
        elif secim == "4":
            smsbomber_menu()
        elif secim == "0":
            print(f"{R.K}Çıkılıyor...{R.SF}")
            sys.exit(0)
        else:
            print(f"{R.K}Geçersiz seçim!{R.SF}")
            time.sleep(1)
        input(f"\n{R.S}Devam etmek için ENTER...{R.SF}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R.K}Kapatıldı.{R.SF}")
        sys.exit(0)