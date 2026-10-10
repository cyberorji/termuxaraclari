# ============================================================
# CYBER - ANA MENÜ v9.0.0
# 6 seçenekli: IP Sorgu, DOS, SMS Bomber, TG Araçları,
#              Web Analiz, Oltalama Araçları
# ============================================================

import os
import sys
import time

from modul_ip import ip_sorgu_menu
from modul_ddos import ddos_menu
from modul_web import web_analiz_menu
from smsbomber import smsbomber_menu
from modul_tg import tg_menu
from oltalama import oltalama_menu

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"
    GIZLE="\033[?25l"; GOSTER="\033[?25h"

def temizle():
    os.system("clear" if os.name != "nt" else "cls")

BANNER_ART = (
    "\n"
    "              \033[38;5;57m...\033[0m\n"
    "             \033[38;5;57m;::::;\033[0m\n"
    "           \033[38;5;57m;::::; :;\033[0m\n"
    "         \033[38;5;57m;:::::;   :;\033[0m\n"
    "        \033[38;5;57m;:::::;     ;.\033[0m\n"
    "       \033[38;5;57m,:::::;       ;\033[0m           \033[38;5;15mOOO\\ \\\033[0m\n"
    "       \033[38;5;57m::::::;       ;\033[0m          \033[38;5;15mOOOOO\\ \\\033[0m\n"
    "       \033[38;5;57m;:::::;       ;\033[0m         \033[38;5;15mOOOOOOOO\033[0m\n"
    "      \033[38;5;57m,;::::::;     ;;\033[0m         \033[38;5;40m/\033[0m \033[38;5;15mOOOOOOO\033[0m\n"
    "    \033[38;5;57m;:::::::::`. ,,,;.\033[0m        \033[38;5;40m/  / \033[38;5;196mDOO\033[0m\033[38;5;15mOOOO\033[0m\n"
    "  \033[38;5;57m.;;:::::::::::::::::;,\033[0m     \033[38;5;40m/  /     \033[38;5;196mDO\033[0m\033[38;5;15mOOO\033[0m\n"
    " \033[38;5;57m,::::::;::::::;;;;::::;,\033[0m   \033[38;5;40m/  /        \033[38;5;196mDO\033[0m\033[38;5;15mOO \033[0m\n"
    "\033[38;5;57m;`::::::`:::::::;;;:::::,\033[0m \033[38;5;10m#\033[0m\033[38;5;40m/  /          \033[38;5;196mDO\033[0m\033[38;5;15mOO\033[0m\n"
    "\033[38;5;57m:`:::::::`;::::::;;::: ;::\033[0m\033[38;5;10m#\033[0m  \033[38;5;40m/            \033[38;5;196mDO\033[0m\033[38;5;15mOO\033[0m\n"
    "\033[38;5;57m::`:::::::`;:::::::: ;::::\033[0m\033[38;5;10m#\033[0m \033[38;5;40m/              \033[38;5;196mDO\033[0m\033[38;5;15mO\033[0m\n"
    "\033[38;5;57m`:`:::::::`;:::::: ;::::::\033[0m\033[38;5;10m#\033[0m\033[38;5;40m/               \033[38;5;196mDO\033[0m\033[38;5;15mO\033[0m\n"
    " \033[38;5;57m:::`:::::::`;; ;:::::::::\033[0m\033[38;5;10m##\033[0m                \033[38;5;196mO\033[0m\033[38;5;15mO\033[0m\n"
    " \033[38;5;57m::::`:::::::`;::::::::;:::\033[0m\033[38;5;10m#\033[0m                \033[38;5;196mO\033[0m\033[38;5;15mO\033[0m\n"
    " \033[38;5;57m`:::::`::::::::::::;``:;::\033[0m\033[38;5;10m#\033[0m                \033[38;5;196mO\n"
    "  \033[38;5;57m`:::::`:::::::::`\033[0m \033[38;5;40m/  / \033[38;5;57m`:\033[0m\033[38;5;10m#\033[0m\n"
    "   \033[38;5;57m::::::`:::::;`\033[0m  \033[38;5;40m/  /   \033[38;5;57m`\033[0m\033[38;5;10m#\033[0m\n"
)

def giris_efekti():
    temizle()
    sys.stdout.write(R.GIZLE)
    sys.stdout.flush()

    satirlar = BANNER_ART.split("\n")

    for i in range(len(satirlar)):
        sys.stdout.write("\033[H")
        for j in range(len(satirlar)):
            if j <= i:
                sys.stdout.write(satirlar[j] + "\n")
            else:
                sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(0.04)

    kurucu = f"\n{R.K}{R.KA}                 Kurucu: CYBER{R.SF}\n"
    for ch in kurucu:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(0.02)

    sys.stdout.write(R.GOSTER)
    sys.stdout.flush()
    time.sleep(0.3)

def banner():
    temizle()
    print(BANNER_ART, end="")
    print(f"{R.K}{R.KA}                 Kurucu: CYBER{R.SF}")
    print()

def menu():
    print(f"""{R.C}{R.KA}╔══════════════════════════════════════════════════════════════════════╗{R.SF}
{R.MO}{R.KA}║                          CYBER ANA MENÜ                              ║{R.SF}
{R.C}{R.KA}╠══════════════════════════════════════════════════════════════════════╣{R.SF}
{R.C}║                                                                      ║{R.SF}
{R.K}║   [1]  IP SORGU          → Konum, ISP, DNS, cihaz, proxy            ║{R.SF}
{R.S}║   [2]  DOS SALDIRISI     → 600 thread, GET/POST/HEAD, süreli        ║{R.SF}
{R.Y}║   [3]  WEB ANALIZ        → index, admin, DNS, açık dosyalar         ║{R.SF}
{R.C}║   [4]  SMS BOMBER        → Normal / Turbo, 90+ Türk servisi         ║{R.SF}
{R.MO}║   [5]  TG ARACLARI       → Telegram mesaj gönderimi                 ║{R.SF}
{R.B}║   [6]  OLTALAMA ARACLARI → Oltalama araçları listesi                ║{R.SF}
{R.C}║                                                                      ║{R.SF}
{R.K}{R.KA}║   [0]  ÇIKIŞ                                                         ║{R.SF}
{R.C}║                                                                      ║{R.SF}
{R.C}{R.KA}╚══════════════════════════════════════════════════════════════════════╝{R.SF}
""")

def main():
    giris_efekti()
    while True:
        banner()
        menu()
        secim = input(f"{R.K}Seçim > {R.SF}").strip()
        if secim == "1":
            ip_sorgu_menu()
        elif secim == "2":
            ddos_menu()
        elif secim == "3":
            web_analiz_menu()
        elif secim == "4":
            smsbomber_menu()
        elif secim == "5":
            tg_menu()
        elif secim == "6":
            oltalama_menu()
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