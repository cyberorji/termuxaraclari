# Turmearaclari - Cyber Tool

Termux için çok amaçlı konsol aracı. IP sorgu, DOS saldırısı, web analiz ve SMS bomber modülleri içerir.

---

## 📋 İçindekiler

- [Ne İşe Yarar](#ne-i̇şe-yarar)
- [Kurulum](#kurulum)
- [Çalıştırma](#çalıştırma)
- [Menü Seçenekleri](#menü-seçenekleri)
- [Modül Detayları](#modül-detayları)
- [Sık Karşılaşılan Hatalar](#sık-karşılaşılan-hatalar)
- [Uyarı](#uyarı)

---

## Ne İşe Yarar

**Turmearaclari**, Termux üzerinden çalışan 4 modüllü bir konsol aracıdır:

| # | Modül | Açıklama |
|---|-------|----------|
| 1 | **IP SORGU** | Hedef IP/domain hakkında konum, ISP, DNS kayıtları, proxy/hosting bilgisi |
| 2 | **DOS SALDIRISI** | 600 thread ile HTTP/HTTPS flood, süre bazlı çalışır |
| 3 | **WEB ANALIZ** | Admin panel, açık dosya, dizin listeleme, port taraması, alt alan adı |
| 4 | **SMS BOMBER** | 90+ Türk servisine SMS gönderir, Normal/Turbo mod |

---

## Kurulum

### 1. Termux'u aç ve güncelle

```bash
pkg update && pkg upgrade -y
```
