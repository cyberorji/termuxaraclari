# ============================================================
# CYBER - OLTALAMA ARACLARI v2.0.0
# Oltalama araçları listesi
# 1- TikTok Oltalama
# ============================================================

import os
import sys
import time

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
    print(f"{R.MO}{R.KA}              OLTALAMA ARACLARI{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}\n")

def oltalama_menu():
    while True:
        banner()
        print(f"{R.M}{R.KA}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                  OLTALAMA ARAÇLARI MENÜSÜ                    ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║                                                              ║")
        print(f"║   {R.Y}[1]{R.M}  TIKTOK OLTALAMA                                    ║")
        print(f"║                                                              ║")
        print(f"║   {R.K}[0]{R.M}  GERİ                                                ║")
        print(f"║                                                              ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{R.SF}\n")

        sec = input(f"{R.C}Seçim > {R.SF}").strip()

        if sec == "0":
            return
        elif sec == "1":
            try:
                from ttoltalma import tiktok_oltalama_baslat
                tiktok_oltalama_baslat()
            except ImportError:
                print(f"{R.K}HATA: 'ttoltalma.py' dosyası bulunamadı!{R.SF}")
                time.sleep(2)
            except Exception as e:
                print(f"{R.K}Hata: {e}{R.SF}")
                time.sleep(2)
        else:
            print(f"{R.K}Geçersiz seçim!{R.SF}")
            time.sleep(1)