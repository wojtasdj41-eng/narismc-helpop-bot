# NariseMC Helpop Bot 🤖

Bot Discord integrujący serwer Minecraft z systemem weryfikacji rang poprzez LuckPerms.

## Funkcjonalności

✅ **Helpop na Discord** - Wiadomości `/helpop` trafiają na Discord z avatarem gracza  
✅ **Weryfikacja rang** - Automatyczne przydzielanie ról na podstawie rang MC  
✅ **Synchronizacja** - Automatyczna aktualizacja rang co 5 minut  
✅ **Auto-kick** - Gracze bez rangi są automatycznie wyrzuceni  

## Wymagania

- Python 3.10+
- discord.py 2.3.2+
- Serwer Minecraft 1.21.1 z Skriptem
- LuckPerms na serwerze MC

## Instalacja

### 1. Klonowanie repo
```bash
git clone https://github.com/wojtasdj41-eng/narismc-helpop-bot.git
cd narismc-helpop-bot
```

### 2. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 3. Konfiguracja

Utwórz plik `.env`:
```env
DISCORD_TOKEN=your_bot_token_here
```

### 4. Skrypt Skript

Umieść plik `helpop.sk` w folderze `plugins/Skript/scripts/` na serwerze MC.

Przeładuj Skript:
```
/sk reload helpop
```

## Konfiguracja Webhook'a

Discord Webhook URL już je skonfigurowany w kodzie.

## Uruchomienie

```bash
python bot.py
```

## Komendy

| Komenda | Opis |
|---------|------|
| `/helpop <wiadomość>` | Wysłanie helpop'a na Discord |
| `!verify` | Ręczna weryfikacja rang (Admin) |
| `!check_rank <gracz>` | Sprawdzenie rangi gracza |

## Mapowanie rang

| Minecraft | Discord |
|-----------|----------|
| Owner | Zarząd + Technik/Developer |
| HeadAdmin | HeadAdmin |
| Admin | Administrator |
| Mod/Helper | Moderator + Helper |

## Autor

**wojtasdj41-eng**

## Licencja

MIT License