import os
import sys
import time
import threading
import urllib.request
import urllib.error
import json
import itertools

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ===== COLORS =====
RED = "\033[91m"
PURPLE = "\033[35m"
BLUE = "\033[94m"
GRAY = "\033[90m"
GREEN = "\033[92m"
ORANGE = "\033[93m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ===== PATHS =====
TOKEN_FILE = "tokens.txt"
PROXY_FILE = "proxies.txt"
PROGRESS_FILE = "progress.txt"
NAMES_FILE = "names4.txt"
THEME_FILE = "theme.txt"

VERSION = "1.0.1"
UPDATE_URL = "https://raw.githubusercontent.com/albatrosshl/sniper-updater/refs/heads/main/version.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/albatrosshl/sniper-updater/refs/heads/main/sniper.py"

# ===== THEME FUNCTIONS =====
def load_theme():
    try:
        with open(THEME_FILE, "r") as f:
            return f.read().strip()
    except:
        return "red"

def save_theme(theme):
    with open(THEME_FILE, "w") as f:
        f.write(theme)

def get_colors():
    theme = load_theme()
    if theme == "red":
        return RED, PURPLE
    elif theme == "blue":
        return BLUE, GRAY
    elif theme == "green":
        return GREEN, GRAY
    elif theme == "orange":
        return ORANGE, WHITE
    else:
        return RED, PURPLE

# ===== CORE FUNCTIONS =====
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    theme = load_theme()
    primary, secondary = get_colors()

    if theme == "red":
        font = r"""
$$$$$$$\   $$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$$\ $$$$$$$\  $$\   $$\  $$$$$$\  $$\   $$\  $$$$$$\  
$$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  _____|$$  __$$\ \$$\ $$  |$$  __$$\ \$$\ $$  |$$  __$$\ 
$$ |  $$ |$$$$$$$$ |\$$$$$$\  $$ /  $$ |\$$$$$$\  $$ |  $$ | \$$$$  / $$ /  $$ | \$$$$  / $$ |  \__|
$$ |  $$ |$$   ____| \____$$\ $$ |  $$ | \____$$\ $$ |  $$ | $$  $$<  $$ |  $$ | $$  $$<  $$ |      
$$ |  $$ |\$$$$$$$\ $$$$$$$  |\$$$$$$$ |$$$$$$$  |$$ |  $$ |$$  /\$$\ $$$$$$$  |$$  /\$$\ $$ |      
\__|  \__| \_______|\_______/  \____$$ |\_______/ \__|  \__|\__/  \__|$$  ____/ \__/  \__|\__|      
                                    $$ |                              $$ |                          
                                    $$ |                              $$ |                          
                                    \__|                              \__|                         
"""
    elif theme == "blue":
        font = r"""
____  ___  _________ __________  _  ______  _  _______
  / __ \/ _ \/ ___/ __ `/ ___/ __ \| |/_/ __ \| |/_/ ___/
 / / / /  __(__  ) /_/ (__  ) / / />  </ /_/ />  </ /    
/_/ /_/\___/____/\__, /____/_/ /_/_/|_/ .___/_/|_/_/     
                   /_/               /_/
"""
    elif theme == "green":
        font = r"""
 ____   ____   ____________ ______ ____ ___  ____________  __________ 
 /    \_/ __ \ /  ___/ ____//  ___//    \\  \/  /\____ \  \/  /\_  __ \
|   |  \  ___/ \___ < <_|  |\___ \|   |  \>    < |  |_> >    <  |  | \/
|___|  /\___  >____  >__   /____  >___|  /__/\_ \|   __/__/\_ \ |__|   
     \/     \/     \/   |__|    \/     \/      \/|__|        \/
"""
    else:  # orange
        font = r"""
.-. .-..----. .----. .----.  .----..-. .-..-.  .-..----..-.  .-..----. 
|  `| || {_  { {__  /  {}  \{ {__  |  `| | \ \/ / | {}  }\ \/ / | {}  }
| |\  || {__ .-._} }\      /.-._} }| |\  | / /\ \ | .--' / /\ \ | .-. \
`-' `-'`----'`----'  `-----``----' `-' `-'`-'  `-'`-'   `-'  `-'`-' `-'
"""

    print(primary + BOLD + font + RESET)
    print(primary + "  ─────────────────────────────────────────────────────────" + RESET)
    print(primary + "   Discord Username Sniper  |  NESQSNXPR" + RESET)
    print(primary + "  ─────────────────────────────────────────────────────────" + RESET)
    print("")
    print(primary + "  Current Mode: " + secondary + "4L" + RESET)
    print("")
    print(secondary + "  [1]" + primary + "  ▶  Start Sniper")
    print(secondary + "  [2]" + primary + "  ℹ   View Status")
    print(secondary + "  [3]" + primary + "  🗑   Clear captured.txt")
    print(secondary + "  [4]" + primary + "  ✖   Exit")
    print(secondary + "  [5]" + primary + "  💰  Donate")
    print(secondary + "  [6]" + primary + "  🎨  Theme Selector")
    print("")
    print(primary + "  ─────────────────────────────────────────────────────────" + RESET)
    print("")

# ===== UPDATE FUNCTIONS =====
def check_for_updates():
    try:
        with urllib.request.urlopen(UPDATE_URL, timeout=5) as response:
            latest_version = response.read().decode("utf-8").strip()
            if latest_version != VERSION:
                print(RED + f"  [!] New version available: {latest_version}" + RESET)
                print(RED + f"  [!] Your version: {VERSION}" + RESET)
                choice = input(RED + "  Download update? (y/n): " + WHITE)
                if choice.lower() == "y":
                    download_update()
            else:
                print(RED + "  [✓] You are running the latest version." + RESET)
    except Exception as e:
        print(RED + f"  [!] Could not check for updates: {e}" + RESET)

def download_update():
    try:
        with urllib.request.urlopen(SCRIPT_URL, timeout=10) as response:
            new_code = response.read().decode("utf-8")
            with open("sniper_new.py", "w", encoding="utf-8") as f:
                f.write(new_code)
        print(RED + "  [✓] Update downloaded as sniper_new.py" + RESET)
        print(RED + "  [✓] Please close this script and run sniper_new.py" + RESET)
        os._exit(0)
    except Exception as e:
        print(RED + f"  [!] Update failed: {e}" + RESET)

# ===== FILE FUNCTIONS =====
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_progress(index):
    try:
        with open(PROGRESS_FILE, "w") as f:
            f.write(str(index))
    except:
        pass

# ===== MENU FUNCTIONS =====
def status():
    banner()
    tokens = load_file(TOKEN_FILE)
    proxies = load_file(PROXY_FILE)
    names = load_file(NAMES_FILE)
    progress = load_progress()
    print(f"  {RED}[+] Tokens:{WHITE} {len(tokens)}")
    print(f"  {RED}[+] Proxies:{WHITE} {len(proxies)}")
    print(f"  {RED}[+] Names:{WHITE} {len(names)}")
    print(f"  {RED}[+] Progress:{WHITE} {progress}")
    print("")
    input(RED + "  Press Enter to return..." + WHITE)

def clear_captured():
    try:
        os.remove("captured.txt")
        print(RED + "  [+] captured.txt cleared" + RESET)
    except FileNotFoundError:
        print(RED + "  [!] No captured.txt found" + RESET)
    time.sleep(1)

def donate():
    banner()
    print(RED + "  ─────────────────────────────────────────────────────────" + RESET)
    print(WHITE + "  💰 Support the developer:" + RESET)
    print("")
    print(f"  {RED}BTC:{WHITE}  bc1qhftyqlaajz4memzmtsmawx0pfu35p94dvervzk")
    print(f"  {RED}LTC:{WHITE}  ltc1qskzjt0q8zyupmcgqng3a02p77zkcjfk0kwy4xh")
    print(f"  {RED}SOL:{WHITE}  CJRYVsSKoc2BEpSvXvdzzGQLtB5JggvPUQPZ9ZyAaizu")
    print(f"  {RED}XMR:{WHITE}  82a5Q5gcZsKan2Tnj2sUPyPGw6mSYWViSTYCuj7qWimB2a5BFBZ52emQFDCkQ6YfpF7XGYHANd4Kq9CusKijYiiTJ41YitL")
    print("")
    print(RED + "  ─────────────────────────────────────────────────────────" + RESET)
    input(RED + "  Press Enter to return..." + WHITE)

def theme_selector():
    banner()
    primary, secondary = get_colors()
    print(primary + "  ─────────────────────────────────────────────────────────" + RESET)
    print(secondary + "  🎨 Select a theme:" + RESET)
    print("")
    print(primary + "  [1]" + secondary + "  Red / Purple (default)")
    print(primary + "  [2]" + secondary + "  Blue / Gray")
    print(primary + "  [3]" + secondary + "  Green / Black")
    print(primary + "  [4]" + secondary + "  Orange / White")
    print("")
    choice = input(primary + "  └─► " + WHITE)
    themes = ["red", "blue", "green", "orange"]
    if choice in ["1", "2", "3", "4"]:
        save_theme(themes[int(choice)-1])
        print(primary + f"  [✓] Theme switched to {themes[int(choice)-1]}" + RESET)
        time.sleep(1)
    else:
        print(primary + "  [!] Invalid choice" + RESET)
        time.sleep(1)

# ===== SNIPER =====
def start_sniper():
    try:
        banner()
        tokens = load_file(TOKEN_FILE)
        proxies = load_file(PROXY_FILE)
        names = load_file(NAMES_FILE)

        if not tokens:
            print(RED + "  [!] No tokens found in tokens.txt" + RESET)
            input(RED + "  Press Enter to return..." + WHITE)
            return

        if not proxies:
            print(RED + "  [!] No proxies found in proxies.txt" + RESET)
            input(RED + "  Press Enter to return..." + WHITE)
            return

        if not names:
            print(RED + "  [!] No names4.txt found" + RESET)
            input(RED + "  Press Enter to return..." + WHITE)
            return

        MAIN_TOKEN = tokens[0]
        TOTAL = len(names)
        FOUND = None
        LOCK = threading.Lock()
        CHECKED = load_progress()
        BLOCK_SIZE = 100

        if CHECKED >= TOTAL:
            CHECKED = 0
            save_progress(0)

        print(RED + "  [✓] Starting sniper..." + RESET)
        print(f"  {RED}[+] Tokens:{WHITE} {len(tokens)}")
        print(f"  {RED}[+] Proxies:{WHITE} {len(proxies)}")
        print(f"  {RED}[+] Names:{WHITE} {TOTAL}")
        print(f"  {RED}[+] Resuming from:{WHITE} {CHECKED} names already checked")
        print("")

        def try_name(name):
            nonlocal FOUND, CHECKED
            if FOUND:
                return

            for proxy in proxies:
                if not proxy:
                    continue
                try:
                    url = "https://discord.com/api/v9/users/@me"
                    data = json.dumps({"username": name}).encode("utf-8")
                    headers = {
                        "Authorization": MAIN_TOKEN,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")

                    if proxy:
                        proxy_handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
                        opener = urllib.request.build_opener(proxy_handler)
                        urllib.request.install_opener(opener)

                    with urllib.request.urlopen(req, timeout=2) as response:
                        if response.status == 200:
                            with LOCK:
                                if not FOUND:
                                    FOUND = name
                                    print(f"\n{RED}  [🔥] FOUND: {name} — attempting to claim...{RESET}")
                                    with open("captured.txt", "w") as f:
                                        f.write(name)
                                    if os.path.exists(PROGRESS_FILE):
                                        os.remove(PROGRESS_FILE)
                                    print(f"{RED}  [✅] CAPTURED: {name}{RESET}")
                                    os._exit(0)
                            return

                except urllib.error.HTTPError as e:
                    if e.code == 400:
                        with LOCK:
                            CHECKED += 1
                            if CHECKED % BLOCK_SIZE == 0:
                                print(f"  {RED}[✔] BLOCK {CHECKED // BLOCK_SIZE} COMPLETE — Last: {name}{RESET}")
                                save_progress(CHECKED)
                        return
                    elif e.code == 429:
                        continue
                except Exception:
                    continue

        def worker(chunk):
            for name in chunk:
                if FOUND:
                    return
                try_name(name)

        THREADS = 50
        remaining_names = names[CHECKED:]
        chunk_size = max(1, len(remaining_names) // THREADS)
        chunks = [remaining_names[i:i + chunk_size] for i in range(0, len(remaining_names), chunk_size)]
        threads = []

        for chunk in chunks:
            t = threading.Thread(target=worker, args=(chunk,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        if not FOUND:
            print(f"\n{RED}  [!] No available 4L username found.{RESET}")
            if os.path.exists(PROGRESS_FILE):
                os.remove(PROGRESS_FILE)
        input(RED + "  Press Enter to return..." + WHITE)

    except Exception as e:
        print(RED + f"  [ERROR] {e}" + RESET)
        import traceback
        traceback.print_exc()
        input(RED + "  Press Enter to exit..." + WHITE)

# ===== MAIN LOOP =====
while True:
    banner()
    # check_for_updates()   # uncomment to enable auto-updater
    choice = input(PURPLE + "  └─► " + WHITE)
    if choice == "1":
        start_sniper()
    elif choice == "2":
        status()
    elif choice == "3":
        clear_captured()
    elif choice == "4":
        clear()
        print(RED + "  Goodbye." + RESET)
        break
    elif choice == "5":
        donate()
    elif choice == "6":
        theme_selector()
        continue
    else:
        print(RED + "  [!] Invalid option" + RESET)
        time.sleep(1)

input("Press Enter to exit...")
