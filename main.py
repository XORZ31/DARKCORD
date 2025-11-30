#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RELAX OLUCANNNN
# ÇALMAOC
# L9GA
# XORN
# /KELES
# KATIRINISKMM
# TÜM ANTİKEMALİSTLERİN AMK
# Sana hiç sahip olmadım ama unutamadım da… 
#ELİN OGLU MUTLU ETSİN SENİ BER211

import json
# XORN
# /KELES
import os
# XORN
# /KELES
import re
# XORN
# /KELES
import sys
# XORN
# /KELES
import time
# XORN
# /KELES
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

try:
    import requests
except ImportError:
    print("requests modülü yüklü değil. Kurmak için:\n\n    pip install requests\n")
    sys.exit(1)
# XORN
# /KELES

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data_files"
HISTORY_PATH = BASE_DIR / "history"
EXPORT_PATH = BASE_DIR / "exports"
# XORN
# /KELES
for p in [HISTORY_PATH, EXPORT_PATH]:
    p.mkdir(exist_ok=True)
# XORN
# /KELES

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
GREY = "\033[90m"
# XORN
# /KELES
# https://l9ga.com.tr
DEFAULT_ANIM_SPEED = 0.02
# XORN
# /KELES
# https://l9ga.com.tr

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
# XORN
# /KELES
# https://l9ga.com.tr

def slow_print(text: str, delay: float = None, end: str = "\n"):
    if delay is None:
        delay = DEFAULT_ANIM_SPEED
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

# XORN
# /KELES
# https://l9ga.com.tr
def progress_bar(label: str = "Progress", duration: float = 1.0, steps: int = 25):
    for i in range(steps + 1):
        filled = "█" * i
        empty = " " * (steps - i)
        percent = int((i / steps) * 100)
        sys.stdout.write(f"\r{label}: [{filled}{empty}] {percent:3d}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

# XORN
# /KELES
# https://l9ga.com.tr
def print_header(title: str):
    width = 70
    print(GREY + "-" * width + RESET)
    print(BOLD + title.center(width) + RESET)
    print(GREY + "-" * width + RESET)


def print_kv(key: str, value, indent: int = 2):
    space = " " * indent
    print(f"{space}{CYAN}{key}{RESET}: {value}")

# XORN
# /KELES
# https://l9ga.com.tr
class DarkcordConfig:
    def __init__(self, path: Path):
        self.path = path
        self.data = {
            "animation_speed": DEFAULT_ANIM_SPEED,
            "stealth": False,
            "use_findcord": True,
            "findcord_api_key": ""
        }
        self.load()

    def load(self):
        if self.path.exists():
            try:
                self.data.update(json.loads(self.path.read_text(encoding="utf-8")))
            except Exception:
                pass
# XORN
# /KELES
# https://l9ga.com.tr
    def save(self):
        try:
            self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"{RED}[Config Hatası]{RESET} {e}")

    @property
    def animation_speed(self) -> float:
        return float(self.data.get("animation_speed", DEFAULT_ANIM_SPEED))

    @animation_speed.setter
    def animation_speed(self, value: float):
        self.data["animation_speed"] = value

    @property
    def stealth(self) -> bool:
        return bool(self.data.get("stealth", False))

    @stealth.setter
    def stealth(self, value: bool):
        self.data["stealth"] = bool(value)

    @property
    def use_findcord(self) -> bool:
        return bool(self.data.get("use_findcord", True))

    @use_findcord.setter
    def use_findcord(self, value: bool):
        self.data["use_findcord"] = bool(value)

    @property
    def api_key(self) -> str:
        return self.data.get("findcord_api_key", "")

    @api_key.setter
    def api_key(self, value: str):
        self.data["findcord_api_key"] = value


class LocalDataStore:
    def __init__(self, base: Path):
        self.base = base
        self.data_files = {
            "main": base / "data.txt",
            "extra": base / "dcıdsorgudata.txt",
            "iddata": base / "ID DATA.txt",
            "ip_map": base / "discord_data.txt",
            "forged": base / "pdh50i.txt",
        }
        self.json_main = {"users": []}
        self.json_extra = {"users": []}
        self.json_iddata = {"users": []}
        self.ip_map = {}
        self.forged = []
        self.username_index = {}

    def check_files(self):
        print_header("LOKAL DOSYA KONTROLÜ")
        for name, path in self.data_files.items():
            if path.exists():
                print(f"{GREEN}[OK]{RESET} {path}")
            else:
                print(f"{RED}[YOK]{RESET} {path}")

    def _load_json(self, path: Path) -> dict:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"{RED}[JSON HATA]{RESET} {path}: {e}")
            return {"users": []}
# XORN
# /KELES
# https://l9ga.com.tr
    def _load_ip_map(self, path: Path) -> dict:
        result = {}
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if ":" in line:
                    uid, ip = line.split(":", 1)
                    result[uid.strip()] = ip.strip()
        except Exception as e:
            print(f"{RED}[IP MAP HATA]{RESET} {path}: {e}")
        return result

    def _load_forged(self, path: Path) -> list:
        try:
            text = path.read_text(encoding="utf-8")
            m = re.search(r"\[(.*)", text, re.DOTALL)
            if not m:
                return []
            fragment = m.group(0)
            last_brace = fragment.rfind("}")
            if last_brace == -1:
                return []
            fixed = fragment[: last_brace + 1] + "]"
            return json.loads(fixed)
        except Exception as e:
            print(f"{RED}[FORGED HATA]{RESET} {path}: {e}")
            return []

    def load_all(self):
        print_header("LOKAL VERİ YÜKLENİYOR")
        self.json_main = self._load_json(self.data_files["main"])
        self.json_extra = self._load_json(self.data_files["extra"])
        self.json_iddata = self._load_json(self.data_files["iddata"])
        self.ip_map = self._load_ip_map(self.data_files["ip_map"])
        self.forged = self._load_forged(self.data_files["forged"])

        self.username_index = {}
        for j in [self.json_main, self.json_extra, self.json_iddata]:
            for u in j.get("users", []):
                uname = str(u.get("username", "")).lower()
                uid = str(u.get("id"))
                self.username_index[uname] = uid

        print(f"{GREEN}[OK]{RESET} Lokal veriler yüklendi.")
        print(f"{GREY}Users main: {len(self.json_main.get('users', []))}, "
              f"extra: {len(self.json_extra.get('users', []))}, "
              f"iddata: {len(self.json_iddata.get('users', []))}{RESET}")

    def find_user_by_id(self, user_id: str) -> dict | None:
        for j in [self.json_main, self.json_extra, self.json_iddata]:
            for u in j.get("users", []):
                if str(u.get("id")) == str(user_id):
                    return u
        return None

    def get_ip_for_id(self, user_id: str) -> str | None:
        return self.ip_map.get(str(user_id))

    def get_forged_hits(self, user_id: str) -> list:
        hits = []
        for row in self.forged:
            if str(row.get("username")) == str(user_id):
                hits.append(row)
        return hits

    def find_id_by_username(self, username: str) -> str | None:
        return self.username_index.get(username.lower())


class FindCordClient:
    BASE_URL = "https://app.findcord.com/api"

    def __init__(self, api_key: str, enabled: bool = True):
        self.api_key = api_key
        self.enabled = enabled

    def fetch_user_raw(self, user_id: str) -> dict:
        if not self.enabled:
            return {"error": "FindCord devre dışı."}
        if not self.api_key:
            return {"error": "API key yok (Ayarlar → API Key menüsünden ekleyin)."}

        url = f"{self.BASE_URL}/user/{user_id}"
        headers = {"Authorization": self.api_key}
        try:
            r = requests.get(url, headers=headers, timeout=6)
            data = r.json()
            return data
        except Exception as e:
            return {"error": f"FindCord istek hatası: {e}"}

    def extract_user(self, raw: dict) -> dict | None:
        if not isinstance(raw, dict):
            return None
        if raw.get("success") is False:
            return None
        return raw.get("user") or raw.get("data") or None

# XORN
# /KELES
# https://l9ga.com.tr
class HistoryManager:
    def __init__(self, history_dir: Path):
        self.dir = history_dir

    def _history_file_for_id(self, user_id: str) -> Path:
        safe = re.sub(r"[^0-9]", "_", str(user_id))
        return self.dir / f"{safe}.json"

    def save_entry(self, user_id: str, payload: dict):
        path = self._history_file_for_id(user_id)
        entry = {
            "user_id": str(user_id),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        try:
            path.write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"{RED}[History Hata]{RESET} {e}")

    def list_entries(self) -> list[Path]:
        return sorted(self.dir.glob("*.json"))

    def load_entry(self, path: Path) -> dict | None:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None


DISCORD_EPOCH = 1420070400000


def decode_snowflake(user_id: int | str) -> dict | None:
    try:
        val = int(user_id)
    except ValueError:
        return None

    timestamp_ms = (val >> 22) + DISCORD_EPOCH
    ts = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)

    worker_id = (val & 0x3E0000) >> 17
    process_id = (val & 0x1F000) >> 12
    increment = (val & 0xFFF)

    now = datetime.now(timezone.utc)
    age = now - ts

    return {
        "timestamp": ts.isoformat(),
        "age_days": age.days,
        "age_human": f"{age.days} gün {age.seconds // 3600} saat",
        "worker_id": worker_id,
        "process_id": process_id,
        "increment": increment,
    }


class RiskAnalyzer:
    def compute_score(self, user_id: str, local_user: dict | None,
                      ip_data: str | None, forged_hits: list,
                      snowflake_info: dict | None) -> dict:
        score = 0
        reasons = []

        if snowflake_info:
            if snowflake_info.get("age_days", 0) < 30:
                score += 30
                reasons.append("Hesap 30 günden genç")

        if forged_hits:
            score += 40
            reasons.append(f"Forged kayıtlarında {len(forged_hits)} adet hit")

        if ip_data:
            score += 10
            reasons.append("Ek IP verisi mevcut")

        if not local_user:
            score += 10
            reasons.append("Lokal user kaydı yok (sadece harici)")

        if score == 0:
            score = 5
            reasons.append("Belirgin risk bulunamadı (baz skor)")

        if score >= 70:
            level = "YÜKSEK"
            color = RED
        elif score >= 40:
            level = "ORTA"
            color = YELLOW
        else:
            level = "DÜŞÜK"
            color = GREEN

        return {
            "score": score,
            "level": level,
            "color": color,
            "reasons": reasons,
        }


class ReportExporter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def export_json(self, user_id: str, data: dict) -> Path:
        safe = re.sub(r"[^0-9]", "_", str(user_id))
        path = self.base_dir / f"{safe}.json"
        try:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            return path
        except Exception as e:
            print(f"{RED}[JSON Export Hatası]{RESET} {e}")
            return path

    def export_html(self, user_id: str, data: dict) -> Path:
        safe = re.sub(r"[^0-9]", "_", str(user_id))
        path = self.base_dir / f"{safe}.html"

        html = dedent(f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="utf-8" />
            <title>Darkcord Analyzer Report - {user_id}</title>
            <style>
                body {{
                    background-color: #050608;
                    color: #e0ffe0;
                    font-family: Consolas, monospace;
                    padding: 20px;
                }}
                h1, h2 {{
                    color: #7CFC00;
                }}
                .section {{
                    border: 1px solid #333;
                    padding: 10px;
                    margin-bottom: 15px;
                    background: #0b0f16;
                }}
            </style>
        </head>
        <body>
            <h1>Darkcord Analyzer - Rapor</h1>
            <h2>Kullanıcı ID: {user_id}</h2>
        """)

        def render_section(title, content_dict):
            nonlocal html
            html += f'<div class="section"><h2>{title}</h2><pre>'
            html += json.dumps(content_dict, indent=2, ensure_ascii=False)
            html += '</pre></div>'

        for section_name, payload in data.items():
            render_section(section_name, payload)

        html += "</body></html>"

        try:
            path.write_text(html, encoding="utf-8")
        except Exception as e:
            print(f"{RED}[HTML Export Hatası]{RESET} {e}")

        return path


def bulk_scan_ids(ids_file: Path, local_store: LocalDataStore,
                  fc_client: FindCordClient, history: HistoryManager,
                  risk_analyzer: RiskAnalyzer):
    if not ids_file.exists():
        print(f"{RED}[Bulk] Dosya yok:{RESET} {ids_file}")
        return

    lines = [l.strip() for l in ids_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    print_header(f"BULK SCAN ({len(lines)} ID)")

    for idx, user_id in enumerate(lines, start=1):
        print(f"{YELLOW}[{idx}/{len(lines)}]{RESET} ID: {user_id}")

        local_user = local_store.find_user_by_id(user_id)
        ip_data = local_store.get_ip_for_id(user_id)
        forged_hits = local_store.get_forged_hits(user_id)
        snow = decode_snowflake(user_id)
        fc_raw = fc_client.fetch_user_raw(user_id)
        fc_user = fc_client.extract_user(fc_raw)
        risk = risk_analyzer.compute_score(user_id, local_user, ip_data, forged_hits, snow)

        payload = {
            "local_user": local_user,
            "ip_data": ip_data,
            "forged_hits": forged_hits,
            "snowflake": snow,
            "findcord_raw": fc_raw,
            "findcord_user": fc_user,
            "risk": risk,
        }
        history.save_entry(user_id, payload)
        print(f"  -> Risk Score: {risk['score']} ({risk['level']})")
        time.sleep(0.05)


def analyze_single_id(user_id: str, local_store: LocalDataStore,
                      fc_client: FindCordClient, history: HistoryManager,
                      risk_analyzer: RiskAnalyzer, exporter: ReportExporter,
                      config: DarkcordConfig):
    clear_screen()
    print_header(f"DARKCORD ANALYZER - ID ANALİZ ({user_id})")

    print(f"{GREEN}[LOCAL LOOKUP]{RESET}")
    local_user = local_store.find_user_by_id(user_id)
    ip_data = local_store.get_ip_for_id(user_id)
    forged_hits = local_store.get_forged_hits(user_id)
    snow = decode_snowflake(user_id)
    time.sleep(0.2)

    print(f"\n{GREEN}[FINDCORD LOOKUP]{RESET}")
    if config.use_findcord:
        fc_raw = fc_client.fetch_user_raw(user_id)
        fc_user = fc_client.extract_user(fc_raw)
    else:
        fc_raw = {"error": "FindCord devre dışı (config)."}
        fc_user = None
    time.sleep(0.2)

    risk = risk_analyzer.compute_score(user_id, local_user, ip_data, forged_hits, snow)

    print_header("ÖZET")
    print_kv("Risk Skoru", f"{risk['score']} ({risk['level']})")
    print("  Nedenler:")
    for r in risk["reasons"]:
        print(f"    - {r}")

    print_header("LOKAL PROFİL")
    if local_user:
        for k, v in local_user.items():
            print_kv(k, v)
    else:
        print("  (Lokal user yok)")

    print_header("LOKAL IP BİLGİLERİ")
    print_kv("Ek IP", ip_data if ip_data else "(yok)")

    print_header("FORGED KAYITLARI")
    if forged_hits:
        for row in forged_hits:
            print("  -", row)
    else:
        print("  (hiç yok)")

    print_header("SNOWFLAKE ANALİZ")
    if snow:
        for k, v in snow.items():
            print_kv(k, v)
    else:
        print("  (Geçersiz snowflake)")

    print_header("FINDCORD PROFİL")
    if fc_user:
        for k, v in fc_user.items():
            print_kv(k, v)
    else:
        print("  (FindCord user verisi yok veya hata)")
        if isinstance(fc_raw, dict) and "error" in fc_raw:
            print_kv("Hata", fc_raw["error"])

    combined_payload = {
        "local_user": local_user,
        "ip_data": ip_data,
        "forged_hits": forged_hits,
        "snowflake": snow,
        "findcord_raw": fc_raw,
        "findcord_user": fc_user,
        "risk": risk,
    }
    if not config.stealth:
        history.save_entry(user_id, combined_payload)

    print_header("EXPORT")
    print("1) JSON olarak kaydet")
    print("2) HTML rapor üret")
    print("3) Hiçbiri (geri dön)")
    choice = input("Seçim: ").strip()
    if choice == "1":
        path = exporter.export_json(user_id, combined_payload)
        print(f"{GREEN}[OK]{RESET} JSON kaydedildi: {path}")
    elif choice == "2":
        path = exporter.export_html(user_id, combined_payload)
        print(f"{GREEN}[OK]{RESET} HTML rapor kaydedildi: {path}")

    input("\nDevam etmek için ENTER...")


def history_menu(history: HistoryManager):
    clear_screen()
    print_header("GEÇMİŞ SORGULAR")

    entries = history.list_entries()
    if not entries:
        print("(Henüz sorgu yok)")
        input("\nGeri dönmek için ENTER...")
        return

    for i, p in enumerate(entries, start=1):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            ts = data.get("timestamp", "?")
            uid = data.get("user_id", "?")
        except Exception:
            ts = "?"
            uid = "?"
        print(f"[{i}] ID={uid}  |  TS={ts}")

    choice = input("\nDetay görmek için numara gir (ENTER geri): ").strip()
    if not choice.isdigit():
        return
    idx = int(choice)
    if not (1 <= idx <= len(entries)):
        return

    entry_path = entries[idx - 1]
    entry = history.load_entry(entry_path)
    clear_screen()
    print_header(f"HISTORY DETAIL - {entry_path.name}")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    input("\nGeri dönmek için ENTER...")


def settings_menu(config: DarkcordConfig):
    global DEFAULT_ANIM_SPEED
    while True:
        clear_screen()
        print_header("AYARLAR")
        print_kv("Animasyon Hızı", config.animation_speed)
        print_kv("Stealth Mod", "Açık" if config.stealth else "Kapalı")
        print_kv("FindCord Kullanımı", "Açık" if config.use_findcord else "Kapalı")
        print_kv("API Key", "(ayarlı)" if config.api_key else "(yok)")
        print("\n1) Animasyon hızını değiştir")
        print("2) Stealth mod aç/kapat")
        print("3) FindCord API aç/kapat")
        print("4) API Key değiştir")
        print("5) API Key sil")
        print("0) Geri dön")
        choice = input("Seçim: ").strip()
        if choice == "0":
            config.save()
            return
        elif choice == "1":
            val = input("Yeni hız (örn 0.01 hızlı / 0.1 yavaş): ").strip()
            try:
                f = float(val)
                config.animation_speed = f
                DEFAULT_ANIM_SPEED = f
            except ValueError:
                pass
        elif choice == "2":
            config.stealth = not config.stealth
        elif choice == "3":
            config.use_findcord = not config.use_findcord
        elif choice == "4":
            new_key = input("Yeni API Key: ").strip()
            if new_key:
                config.api_key = new_key
                config.save()
                print(GREEN + "API Key güncellendi!" + RESET)
                time.sleep(1)
        elif choice == "5":
            confirm = input("API Key'i silmek istiyor musun? (e/h): ").strip().lower()
            if confirm == "e":
                config.api_key = ""
                config.save()
                print(RED + "API Key silindi!" + RESET)
                time.sleep(1)


def main_menu():
    config = DarkcordConfig(BASE_DIR / "darkcord_config.json")
    global DEFAULT_ANIM_SPEED
    DEFAULT_ANIM_SPEED = config.animation_speed

    if not config.api_key:
        clear_screen()
        print_header("FINDCORD API KEY GEREKLİ")
        print("Bu işlem yalnızca 1 kere yapılacak.")
        key = input("\nFINDCORD API KEY giriniz (boş geçmek için ENTER): ").strip()
        if key:
            config.api_key = key
            config.save()
            print("\n[OK] API key kaydedildi!")
            time.sleep(1)
# XORN
# /KELES
# https://l9ga.com.tr
    local_store = LocalDataStore(DATA_PATH)
    local_store.check_files()
    local_store.load_all()

    fc_client = FindCordClient(config.api_key, enabled=config.use_findcord)
    history = HistoryManager(HISTORY_PATH)
    risk_analyzer = RiskAnalyzer()
    exporter = ReportExporter(EXPORT_PATH)

    while True:
        clear_screen()
        print_header("DARKCORD ANALYZER V4 - ULTIMATE")
        print("1) Tek ID analizi")
        print("2) Username → ID bul ve analiz et")
        print("3) Snowflake (ID) analiz aracı")
        print("4) Geçmiş sorguları görüntüle")
        print("5) Bulk scan (dosyadan ID listesi)")
        print("6) Ayarlar")
        print("0) Çıkış")
        choice = input("\nSeçim: ").strip()
# XORN
# /KELES
# https://l9ga.com.tr
        if choice == "0":
            print("Çıkılıyor...")
            break
        elif choice == "1":
            uid = input("ID gir: ").strip()
            if uid:
                analyze_single_id(uid, local_store, fc_client, history, risk_analyzer, exporter, config)
        elif choice == "2":
            uname = input("Username gir: ").strip()
            if not uname:
                continue
            uid = local_store.find_id_by_username(uname)
            if not uid:
                print(f"{RED}Bu username lokal veride yok.{RESET}")
                input("ENTER ile geri dön...")
            else:
                analyze_single_id(uid, local_store, fc_client, history, risk_analyzer, exporter, config)
        elif choice == "3":
            uid = input("Snowflake (ID) gir: ").strip()
            info = decode_snowflake(uid)
            clear_screen()
            print_header("SNOWFLAKE ANALİZ SONUCU")
            if not info:
                print("Geçersiz sayı.")
            else:
                for k, v in info.items():
                    print_kv(k, v)
            input("\nGeri dönmek için ENTER...")
        elif choice == "4":
            history_menu(history)
        elif choice == "5":
            path_str = input("ID listesi dosya yolu (örn: ids.txt): ").strip()
            if not path_str:
                continue
            ids_file = Path(path_str)
            bulk_scan_ids(ids_file, local_store, fc_client, history, risk_analyzer)
            input("\nBulk scan bitti. ENTER ile geri dön...")
        elif choice == "6":
            settings_menu(config)
# XORN
# /KELES
# https://l9ga.com.tr

if __name__ == "__main__":
    main_menu()
# XORN
# /KELES
# https://l9ga.com.tr# XORN
# /KELES
# https://l9ga.com.tr# XORN
# /KELES
# https://l9ga.com.tr# XORN
# /KELES
# https://l9ga.com.tr# XORN
# /KELES
# https://l9ga.com.tr
