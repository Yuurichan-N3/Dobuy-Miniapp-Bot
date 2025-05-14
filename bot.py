import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

# Inisialisasi colorama
init()

# Banner
BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════╗
║       🌟 DOBUY BOT - Point Sync Automation   ║
║   Automate point synchronization for Dobuy!  ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Membaca initData dari data.txt
def read_init_data():
    try:
        with open('data.txt', 'r') as file:
            init_data = file.read().strip()
        return init_data
    except FileNotFoundError:
        print(f"{Fore.RED}File data.txt tidak ditemukan!{Style.RESET_ALL}")
        exit(1)

# Mendapatkan timestamp
def get_current_timestamp():
    return int(datetime.now().timestamp() * 1000)

# Header
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://dobuy.onecoinbuy.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://dobuy.onecoinbuy.com/clicker?tgWebAppStartParam=kentId6509376374",
    "sec-ch-ua": '"Microsoft Edge";v="136", "Microsoft Edge WebView2";v="136", "Not.A/Brand";v="99", "Chromium";v="136"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}

# URL
sync_url = "https://dobuy.onecoinbuy.com/api/sync"
user_url = "https://dobuy.onecoinbuy.com/api/user"

print(BANNER)

# Membaca query
init_data = read_init_data()

# Payload
user_payload = {
    "telegramInitData": init_data,
    "referrerTelegramId": "6004380466"
}

try:
    user_response = requests.post(user_url, headers=headers, json=user_payload)
    if user_response.status_code == 200:
        user_data = user_response.json()
        print(f"{Fore.YELLOW}User data loaded: Points : {user_data['points']}, Energy : {user_data['energy']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}User data failed to load: Status {user_response.status_code}{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Error saat mengirim request ke /api/user: {e}{Style.RESET_ALL}")

# Payload
sync_payload = {
    "initData": init_data,
    "unsynchronizedPoints": 2.4,
    "currentEnergy": 500,
    "syncTimestamp": 0
}

# Melacak energi
current_energy = 500

# Kirim request hanya status 200
while True:
    # Update timestamp dan energi di payload
    sync_payload["syncTimestamp"] = get_current_timestamp()
    sync_payload["currentEnergy"] = current_energy

    # Cek jika energi tidak cukup untuk 2.4 poin
    if current_energy < 2.4:
        print(f"{Fore.RED}Energi tidak cukup (kurang dari 2.4), menghentikan loop.{Style.RESET_ALL}")
        break

    try:
        # Kirim request
        sync_response = requests.post(sync_url, headers=headers, json=sync_payload)
        
        # Cek status response
        if sync_response.status_code == 200:
            response_data = sync_response.json()
            updated_points = response_data.get("updatedPoints", "N/A")
            updated_energy = response_data.get("updatedEnergy", current_energy - 2.4)
            print(f"{Fore.GREEN}Sync successful: Points : {updated_points}, Energy : {updated_energy}{Style.RESET_ALL}")
            current_energy = updated_energy
        else:
            error_message = sync_response.json().get("error", "Unknown error")
            print(f"{Fore.RED}Sync failed: {error_message}{Style.RESET_ALL}")
            print(f"{Fore.RED}Status code bukan 200 ({sync_response.status_code}), menghentikan loop.{Style.RESET_ALL}")
            break

        # Tunggu 2 detik
        time.sleep(2)

    except Exception as e:
        print(f"{Fore.RED}Error saat mengirim request ke /api/sync: {e}{Style.RESET_ALL}")
        break

print(f"{Fore.CYAN}Script selesai.{Style.RESET_ALL}")
