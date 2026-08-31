import os
import sys
import time
import threading
import urllib.request
import urllib.error
import json

# ANSI colors
RED = "\033[91m"
PURPLE = "\033[35m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ===== PATHS =====
TOKEN_FILE = "tokens.txt"
PROXY_FILE = "proxies.txt"
NAME_FILE = "names.txt"
PROGRESS_FILE = "progress.txt"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(RED + BOLD + r"""
 $$$$$$\  $$\              $$$$$$\  $$\   $$\ $$$$$$\ $$$$$$$\  $$$$$$$$\ $$$$$$$\        $$\    $$\    $$\   
$$ ___$$\ $$ |            $$  __$$\ $$$\  $$ |\_$$  _|$$  __$$\ $$  _____|$$  __$$\       $$ |   $$ | $$$$ |  
\_/   $$ |$$ |            $$ /  \__|$$$$\ $$ |  $$ |  $$ |  $$ |$$ |      $$ |  $$ |      $$ |   $$ | \_$$ |  
  $$$$$ / $$ |            \$$$$$$\  $$ $$\$$ |  $$ |  $$$$$$$  |$$$$$\    $$$$$$$  |      \$$\  $$  |   $$ |  
  \___$$\ $$ |             \____$$\ $$ \$$$$ |  $$ |  $$  ____/ $$  __|   $$  __$$<        \$$\$$  /    $$ |  
$$\   $$ |$$ |            $$\   $$ |$$ |\$$$ |  $$ |  $$ |      $$ |      $$ |  $$ |        \$$$  /     $$ |  
\$$$$$$  |$$$$$$$$\       \$$$$$$  |$$ | \$$ |$$$$$$\ $$ |      $$$$$$$$\ $$ |  $$ |         \$  /$$\ $$$$$$\ 
 \______/ \________|       \______/ \__|  \__|\______|\__|      \________|\__|  \__|          \_/ \__|\______|
                                                                                                              
""" + RESET)
    print(RED + "  ─────────────────────────────────────────────────────────" + RESET)
    print(RED + "   Discord 3-Letter Username Sniper  |  Commercial" + RESET)
    print(RED + "  ─────────────────────────────────────────────────────────" + RESET)
    print("")
    print(PURPLE + "  [1]" + RED + "  ▶  Start Sniper")
    print(PURPLE + "  [2]" + RED + "  ℹ   View Status")
    print(PURPLE + "  [3]" + RED + "  🗑   Clear captured.txt")
    print(PURPLE + "  [4]" + RED + "  ✖   Exit")
    print(PURPLE + "  [5]" + RED + "  💰  Donate")
    print("")
    print(RED + "  ─────────────────────────────────────────────────────────" + RESET)
    print("")

def load_file(filename):
    try:
        with open(filename, "r") as f:
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

def status():
    banner()
    tokens = load_file(TOKEN_FILE)
    proxies = load_file(PROXY_FILE)
    names = load_file(NAME_FILE)
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

def start_sniper():
    banner()
    tokens = load_file(TOKEN_FILE)
    proxies = load_file(PROXY_FILE)
    names = load_file(NAME_FILE)

    if not tokens:
        print(RED + "  [!] No tokens found in tokens.txt" + RESET)
        input("  Press Enter to return...")
        return

    if not proxies:
        print(RED + "  [!] No proxies found in proxies.txt" + RESET)
        input("  Press Enter to return...")
        return

    if not names:
        print(RED + "  [!] No names found in names.txt" + RESET)
        input("  Press Enter to return...")
        return

    MAIN_TOKEN = tokens[0]
    TOTAL = len(names)
    FOUND = None
    LOCK = threading.Lock()
    CHECKED = 2600  # <-- hardcoded start
    BLOCK_SIZE = 100

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
        print(f"\n{RED}  [!] No available 3-letter username found.{RESET}")
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
    input("  Press Enter to return...")

# ---- MAIN LOOP ----
while True:
    banner()
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
    else:
        print(RED + "  [!] Invalid option" + RESET)
        time.sleep(1)