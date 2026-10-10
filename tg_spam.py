# ============================================================
# CYBER - TG SPAM v1.0.0
# Telegram spam aracı - giriş + hedef + mesaj + gönderim
# ============================================================

import os
import sys
import time
import asyncio
import threading

try:
    from telethon import TelegramClient
    from telethon.errors import (
        SessionPasswordNeededError, PhoneCodeInvalidError,
        FloodWaitError, UsernameNotOccupiedError, UsernameInvalidError,
        ChannelPrivateError, UserBannedInChannelError, ChatWriteForbiddenError
    )
except ImportError:
    print("\n[!] HATA: 'telethon' kütüphanesi bulunamadı.")
    print("[!] Termux'ta kurmak için: pip install telethon")
    sys.exit(1)

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

# ==================== GLOBAL ====================
client = None
loop = None

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
    print(f"{R.MO}{R.KA}              SPAM ARACI{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}\n")

# ==================== GİRİŞ ====================
async def _giris(api_id, api_hash, tel):
    global client
    oturum = f"cyber_{tel.replace('+', '').replace(' ', '')}"
    client = TelegramClient(oturum, int(api_id), api_hash)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"{R.Y}[+] Oturum hazır: {me.first_name} (@{me.username or me.id}){R.SF}")
        return True

    print(f"{R.S}Kod gönderiliyor: {R.Y}{tel}{R.SF}")
    try:
        await client.send_code_request(tel)
    except FloodWaitError as e:
        print(f"{R.K}Flood bekle: {e.seconds} sn{R.SF}")
        return False
    except Exception as e:
        print(f"{R.K}Kod hatası: {e}{R.SF}")
        return False

    kod = input(f"{R.C}Telegram kodu > {R.SF}").strip()
    try:
        await client.sign_in(tel, kod)
    except SessionPasswordNeededError:
        sifre = input(f"{R.C}İki adımlı şifre > {R.SF}").strip()
        try:
            await client.sign_in(password=sifre)
        except Exception as e:
            print(f"{R.K}Şifre hatası: {e}{R.SF}")
            return False
    except PhoneCodeInvalidError:
        print(f"{R.K}Geçersiz kod!{R.SF}")
        return False
    except Exception as e:
        print(f"{R.K}Giriş hatası: {e}{R.SF}")
        return False

    me = await client.get_me()
    print(f"{R.Y}[+] Hesaba girildi: {me.first_name} (@{me.username or me.id}){R.SF}")
    return True

def giris_yap(api_id, api_hash, tel):
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_giris(api_id, api_hash, tel))
    except Exception as e:
        print(f"{R.K}Giriş hatası: {e}{R.SF}")
        return False

# ==================== HEDEF ÇÖZÜMLE ====================
async def _hedef_coz(hedef):
    hedef = hedef.strip()
    if hedef.startswith("https://t.me/"):
        hedef = "@" + hedef.replace("https://t.me/", "").split("/")[0]
    elif hedef.startswith("t.me/"):
        hedef = "@" + hedef.replace("t.me/", "").split("/")[0]
    elif not hedef.startswith("@") and not hedef.lstrip("-").isdigit():
        hedef = "@" + hedef
    try:
        return await client.get_entity(hedef)
    except Exception:
        return None

def hedef_coz(hedef):
    global loop
    try:
        return loop.run_until_complete(_hedef_coz(hedef))
    except Exception:
        return None

# ==================== MESAJ GÖNDER ====================
async def _tek_mesaj(entity, mesaj):
    try:
        await client.send_message(entity, mesaj)
        return True, None
    except FloodWaitError as e:
        return False, f"FloodWait:{e.seconds}"
    except ChatWriteForbiddenError:
        return False, "Yazma izni yok"
    except UserBannedInChannelError:
        return False, "Banlısın"
    except ChannelPrivateError:
        return False, "Kanal özel"
    except Exception as e:
        return False, str(e)[:40]

def gonderici(entity, mesaj, adet, aralik, kilit, ist):
    while not ist["dur"].is_set():
        with kilit:
            if ist["giden"] >= adet:
                ist["dur"].set()
                return
        try:
            basarili, hata = loop.run_until_complete(_tek_mesaj(entity, mesaj))
            with kilit:
                if basarili:
                    ist["giden"] += 1
                else:
                    ist["gitmeyen"] += 1
                    if hata and hata.startswith("FloodWait:"):
                        bekle = int(hata.split(":")[1])
                        time.sleep(min(bekle, 10))
        except Exception:
            with kilit:
                ist["gitmeyen"] += 1
        if aralik > 0:
            time.sleep(aralik)

def mesaj_gonder(entity, mesaj, adet, aralik):
    global loop
    kilit = threading.Lock()
    ist = {"giden": 0, "gitmeyen": 0, "dur": threading.Event(), "bas": time.time()}
    thread_sayisi = 10 if aralik == 0 else 1

    def istatistik():
        while not ist["dur"].is_set():
            time.sleep(0.5)
            with kilit:
                gecen = time.time() - ist["bas"]
                hiz = ist["giden"] / gecen if gecen > 0 else 0
                sys.stdout.write(
                    f"\r{R.Y}GİDEN:{R.SF} {ist['giden']:>6}  "
                    f"{R.K}GİTMEYEN:{R.SF} {ist['gitmeyen']:>6}  "
                    f"{R.S}HEDEF:{R.SF} {adet:>6}  "
                    f"{R.MO}HIZ:{R.SF} {hiz:>6.1f}/s   "
                )
                sys.stdout.flush()

    thread_listesi = []
    for _ in range(thread_sayisi):
        t = threading.Thread(target=gonderici, args=(entity, mesaj, adet, aralik, kilit, ist), daemon=True)
        t.start()
        thread_listesi.append(t)

    ist_t = threading.Thread(target=istatistik, daemon=True)
    ist_t.start()

    try:
        for t in thread_listesi:
            t.join()
    except KeyboardInterrupt:
        ist["dur"].set()
        print(f"\n{R.S}Kullanıcı durdurdu.{R.SF}")

    ist["dur"].set()
    ist_t.join(timeout=1)
    print()
    with kilit:
        gecen = time.time() - ist["bas"]
        with open("tg_rapor.txt", "w", encoding="utf-8") as f:
            f.write(f"Mesaj: {mesaj}\nGiden: {ist['giden']}\nGitmeyen: {ist['gitmeyen']}\nSüre: {gecen:.1f} sn\n")
        print(f"\n{R.Y}{'='*56}{R.SF}")
        print(f"{R.Y}              SPAM RAPORU{R.SF}")
        print(f"{R.Y}{'='*56}{R.SF}")
        print(f"{R.C}Giden      : {R.SF}{ist['giden']}")
        print(f"{R.C}Gitmeyen   : {R.SF}{ist['gitmeyen']}")
        print(f"{R.C}Süre       : {R.SF}{gecen:.1f} sn")
        print(f"{R.S}Rapor: {R.Y}tg_rapor.txt{R.SF}")

# ==================== SPAM BAŞLAT ====================
def spam_baslat():
    global client, loop
    banner()

    # Giriş
    print(f"{R.MO}{R.KA}[ TELEGRAM GİRİŞ ]{R.SF}")
    print(f"{R.S}API ID ve Hash: my.telegram.org adresinden al.{R.SF}\n")

    api_id = input(f"{R.C}API ID > {R.SF}").strip()
    if not api_id.isdigit():
        print(f"{R.K}Geçersiz API ID.{R.SF}")
        input(f"{R.S}ENTER...{R.SF}")
        return
    api_hash = input(f"{R.C}API Hash > {R.SF}").strip()
    if len(api_hash) != 32:
        print(f"{R.K}API Hash 32 karakter olmalı.{R.SF}")
        input(f"{R.S}ENTER...{R.SF}")
        return
    tel = input(f"{R.C}Telefon (+905551234567) > {R.SF}").strip()
    if not tel.startswith("+"):
        tel = "+" + tel

    if not giris_yap(api_id, api_hash, tel):
        print(f"{R.K}Giriş başarısız.{R.SF}")
        input(f"{R.S}ENTER...{R.SF}")
        return

    # Hedef menüsü
    while True:
        temizle()
        banner()
        print(f"{R.MO}{R.KA}[ HEDEF SEÇİMİ ]{R.SF}\n")
        print(f"{R.Y}[1]{R.SF} Grup")
        print(f"{R.Y}[2]{R.SF} Kanal")
        print(f"{R.Y}[3]{R.SF} Bot")
        print(f"{R.Y}[4]{R.SF} Kişi")
        print(f"{R.K}[0]{R.SF} Geri\n")
        sec = input(f"{R.C}Seçim > {R.SF}").strip()

        if sec == "0":
            return
        if sec not in ("1", "2", "3", "4"):
            print(f"{R.K}Geçersiz seçim.{R.SF}")
            time.sleep(1)
            continue

        tur = {"1": "grup", "2": "kanal", "3": "bot", "4": "kişi"}[sec]
        hedef = input(f"{R.C}Hedef link veya kullanıcı adı > {R.SF}").strip()
        if not hedef:
            print(f"{R.K}Boş olamaz.{R.SF}")
            time.sleep(1)
            continue

        print(f"{R.S}Hedef çözümleniyor...{R.SF}")
        entity = hedef_coz(hedef)
        if entity is None:
            print(f"{R.K}Hedef bulunamadı!{R.SF}")
            time.sleep(2)
            continue

        isim = getattr(entity, "title", None) or getattr(entity, "first_name", None) or getattr(entity, "username", "?")
        print(f"{R.Y}[+] Hedef bulundu: {isim}{R.SF}")

        mesaj = input(f"{R.C}Gönderilecek mesaj > {R.SF}")
        if not mesaj:
            print(f"{R.K}Mesaj boş olamaz.{R.SF}")
            time.sleep(1)
            continue

        adet_s = input(f"{R.C}Kaç defa gönderilsin > {R.SF}").strip()
        if not adet_s.isdigit() or int(adet_s) < 1:
            print(f"{R.K}Geçersiz sayı.{R.SF}")
            time.sleep(1)
            continue
        adet = int(adet_s)

        print(f"{R.S}0 = son hız (10 thread), yoksa saniye cinsinden aralık.{R.SF}")
        aralik_s = input(f"{R.C}Kaç saniyede bir > {R.SF}").strip()
        aralik = float(aralik_s) if aralik_s.replace(".", "").isdigit() else 0

        print(f"\n{R.S}Hedef : {R.Y}{isim}{R.SF}")
        print(f"{R.S}Adet  : {R.Y}{adet}{R.SF}")
        print(f"{R.S}Aralık: {R.Y}{aralik} sn{R.SF}")
        onay = input(f"{R.C}Başlat? (e/h) > {R.SF}").strip().lower()
        if onay != "e":
            continue

        try:
            mesaj_gonder(entity, mesaj, adet, aralik)
        except KeyboardInterrupt:
            print(f"\n{R.S}Durduruldu.{R.SF}")
        except Exception as e:
            print(f"{R.K}Hata: {e}{R.SF}")

        input(f"\n{R.S}ENTER...{R.SF}")

if __name__ == "__main__":
    spam_baslat()