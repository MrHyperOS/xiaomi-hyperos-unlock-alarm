#!/usr/bin/env python3
# ============================================================
# CF LHAX - BL AUTH BLASTER v2.0 (Beijing Midnight Precise Burst)
# Designed & Enhanced by kennedy • 2026
# Official Channel: https://t.me/Cflhax
# For educational & research use only. Use at your own risk.
# ============================================================

import subprocess
import sys
import os
import time
import json
import hashlib
import random
import linecache
import signal
from datetime import datetime, timezone, timedelta
import ntplib
import pytz
import urllib3
from colorama import init, Fore, Style
from threading import Thread

# Auto-install missing packages
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

for p in ("ntplib", "pytz", "urllib3", "colorama"):
    try:
        __import__(p)
    except ImportError:
        install(p)

# Color setup
init(autoreset=True)
G  = Fore.GREEN
Y  = Fore.YELLOW
R  = Fore.RED
B  = Fore.BLUE
C  = Fore.CYAN
P  = Fore.MAGENTA
GB = Style.BRIGHT + Fore.GREEN
RB = Style.BRIGHT + Fore.RED
WB = Style.BRIGHT + Fore.WHITE
N  = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Graceful Ctrl+C
def signal_handler(sig, frame):
    print(f"\n{RB}[!] Interrupted by user. Clean exit.{N}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ============================================================
# CONFIG (Beijing Time Zone Only)
# ============================================================
SKIP_TIMING       = False           # True = manual time, False = next midnight
MANUAL_FIRE_HOUR  = 19
MANUAL_FIRE_MIN   = 37
MANUAL_FIRE_SEC   = 0
OFFSET_MS         = 120             # Fire X ms BEFORE target
BURST_INTERVAL_MS = 50              # Delay between each shot
BURST_COUNT       = 10              # How many rapid requests

UA = "okhttp/4.12.0"
NTP_SERVERS = ["ntp0.ntp-servers.net", "ntp1.ntp-servers.net", "ntp2.ntp-servers.net", "pool.ntp.org"]

URL_STATUS = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
URL_APPLY  = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"

# ============================================================
# BANNER
# ============================================================
def show_banner():
    clear()
    print(f"{C}╔════════════════════════════════════════════════════╗{N}")
    print(f"{C}║          {P}★ CF LHAX - BL AUTH BLASTER v2.0 ★{C}          ║{N}")
    print(f"{C}║     {WB}Precise Midnight Burst • Xiaomi Global BL{N}      ║{N}")
    print(f"{C}║  {Y}Telegram:{WB} https://t.me/Cflhax                  {C}║{N}")
    print(f"{C}║     {G}2026 • kennedy edition • High-Speed Timing{C}      ║{N}")
    print(f"{C}╚════════════════════════════════════════════════════╝{N}\n")

# ============================================================
# BEIJING TIME & NTP
# ============================================================
def get_beijing_time():
    return datetime.now(timezone.utc).astimezone(pytz.timezone("Asia/Shanghai"))

def show_beijing_time(prefix=""):
    bt = get_beijing_time()
    print(f"{B}{prefix}[BEIJING] {bt.strftime('%H:%M:%S.%f')[:-3]}{N}")

def get_ntp_beijing():
    tz = pytz.timezone("Asia/Shanghai")
    c = ntplib.NTPClient()
    for server in NTP_SERVERS:
        try:
            resp = c.request(server, version=3, timeout=4)
            bt = datetime.fromtimestamp(resp.tx_time, tz=timezone.utc).astimezone(tz)
            print(f"{G}[NTP SYNC] {bt.strftime('%H:%M:%S.%f')[:-3]} via {server}{N}")
            return bt
        except:
            pass
    print(f"{Y}[FALLBACK] Using system time (may have drift){N}")
    return get_beijing_time()

# ============================================================
# SPINNER for waiting (threaded)
# ============================================================
def spinner(stop_event):
    chars = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(f"\r{Y}Waiting... {chars[i % len(chars)]}{N}", end="", flush=True)
        i += 1
        time.sleep(0.15)
    print("\r" + " " * 20 + "\r", end="", flush=True)

# ============================================================
# TIMING LOGIC
# ============================================================
def get_target_time(start_bt):
    if SKIP_TIMING:
        target = start_bt.replace(hour=MANUAL_FIRE_HOUR, minute=MANUAL_FIRE_MIN,
                                  second=MANUAL_FIRE_SEC, microsecond=0)
        print(f"{Y}[MANUAL] Target → {target.strftime('%H:%M:%S Beijing')}{N}")
    else:
        target = (start_bt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        print(f"{Y}[AUTO] Target → Next Midnight {target.strftime('%Y-%m-%d %H:%M:%S Beijing')}{N}")
    return target

def wait_until(target_time, start_bt, start_ts):
    print(f"{C}→ Syncing & waiting for precise trigger...{N}")
    stop_event = type('obj', (object,), {})()
    stop_event.is_set = lambda: False
    spinner_thread = Thread(target=spinner, args=(stop_event,))
    spinner_thread.daemon = True
    spinner_thread.start()

    while True:
        now = start_bt + timedelta(seconds=time.time() - start_ts)
        diff_sec = (target_time - now).total_seconds()
        if diff_sec <= 0:
            break
        time.sleep(min(max(diff_sec - 0.005, 0.0005), 0.3))

    stop_event.is_set = lambda: True
    spinner_thread.join(timeout=0.5)
    print(f"\r{GB}→ TARGET REACHED! Burst sequence starting...{N}\n")

# ============================================================
# HTTP SESSION
# ============================================================
class HttpSession:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=12,
            retries=urllib3.Retry(total=2, backoff_factor=0.3),
            timeout=urllib3.Timeout(connect=3.0, read=6.0)
        )

    def req(self, method, url, headers=None, body=None):
        try:
            hd = headers or {}
            if method.upper() == 'POST':
                body = body or b'{"is_retry":true}'
                hd.update({
                    'Content-Type': 'application/json',
                    'Content-Length': str(len(body)),
                    'User-Agent': UA,
                    'Connection': 'keep-alive',
                    'Accept-Encoding': 'gzip'
                })
            r = self.http.request(method.upper(), url, headers=hd, body=body)
            return r
        except Exception as e:
            print(f"{R}[HTTP ERROR] {e}{N}")
            return None

# ============================================================
# CORE FUNCTIONS
# ============================================================
def generate_device_id():
    seed = f"{random.random()}-{time.time()}-{os.urandom(8)}"
    return hashlib.sha1(seed.encode()).hexdigest().upper()

def check_status(sess, token, dev_id):
    headers = {"Cookie": f"new_bbs_serviceToken={token};versionCode=500411;versionName=5.4.11;deviceId={dev_id};"}
    r = sess.req('GET', URL_STATUS, headers=headers)
    if not r or r.status != 200:
        print(f"{R}Status check failed (HTTP {r.status if r else 'None'}){N}")
        return False
    try:
        data = json.loads(r.data.decode())
        info = data.get("data", {})
        is_pass = info.get("is_pass")
        button = info.get("button_state")
        print(f"{G}[STATUS] ", end="")
        if is_pass == 4 and button == 1:
            print(f"{GB}READY TO FIRE! ✓{N}")
            return True
        elif is_pass == 1:
            print(f"{GB}Already approved / passed!{N}")
            sys.exit(0)
        else:
            print(f"{RB}Not eligible yet{N}")
            sys.exit(1)
    except:
        print(f"{R}Status parse error{N}")
        return False

def send_apply(sess, token, dev_id):
    headers = {"Cookie": f"new_bbs_serviceToken={token};versionCode=500411;versionName=5.4.11;deviceId={dev_id};"}
    r = sess.req('POST', URL_APPLY, headers=headers)
    if not r:
        return None
    try:
        return json.loads(r.data.decode())
    except:
        return None

def process_response(resp, shot_num):
    if not resp or resp.get("code") != 0:
        print(f"{R}API Error: {resp.get('msg', 'Unknown')}{N}")
        return False
    result = resp.get("data", {}).get("apply_result")
    deadline = resp.get("data", {}).get("deadline_format", "N/A")
    now = get_beijing_time().strftime("%H:%M:%S.%f")[:-3]
    if result == 1:
        print(f"{GB}[{shot_num}] @{now} → SUCCESS! APPROVED! 🎉{N}")
        return True
    elif result == 3:
        print(f"{Y}[{shot_num}] @{now} → Quota reached ({deadline}){N}")
    elif result == 4:
        print(f"{RB}[{shot_num}] @{now} → BLOCKED ({deadline}){N}")
    else:
        print(f"{R}[{shot_num}] @{now} → Unknown result: {result}{N}")
    return False

# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    show_banner()
    show_beijing_time("[NOW] ")

    try:
        slot = int(input(f"{G}Enter Slot [1-4]: {N}"))
    except:
        print(f"{R}Invalid input!{N}")
        sys.exit(1)

    token_line = 1 if slot in (1,3) else 2 if slot in (2,4) else 0
    if token_line == 0:
        print(f"{R}Invalid slot! Choose 1-4 only.{N}")
        sys.exit(1)

    clear()
    show_beijing_time("[NOW] ")
    print(f"{GB}Using Token #{token_line}{N}")

    token = linecache.getline("token.txt", token_line).strip()
    if not token:
        print(f"{R}Token #{token_line} not found or empty in token.txt{N}")
        sys.exit(1)

    sess = HttpSession()
    dev_id = generate_device_id()

    print(f"{Y}→ Checking eligibility...{N}")
    if not check_status(sess, token, dev_id):
        print(f"{R}Aborting...{N}")
        return

    start_bt = get_ntp_beijing()
    start_ts = time.time()

    target = get_target_time(start_bt)
    trigger_time = target - timedelta(milliseconds=OFFSET_MS)

    wait_until(trigger_time, start_bt, start_ts)

    clear()
    show_beijing_time("[FIRE] ")
    print(f"{GB}╔═══════════════════════╗{N}")
    print(f"{GB}║  BURST MODE ACTIVATED ║{N}")
    print(f"{GB}╚═══════════════════════╝{N}\n")

    success = False
    for i in range(BURST_COUNT):
        shot_target = target + timedelta(milliseconds=i * BURST_INTERVAL_MS)
        while True:
            now = start_bt + timedelta(seconds=time.time() - start_ts)
            if (shot_target - now).total_seconds() <= 0:
                break
            time.sleep(0.0003)

        now_str = get_beijing_time().strftime("%H:%M:%S.%f")[:-3]
        print(f"{C}[{i+1}/{BURST_COUNT}] ", end="")
        resp = send_apply(sess, token, dev_id)
        print(f"@{now_str} ", end="")
        if process_response(resp, i+1):
            success = True
            break
        time.sleep(0.005)  # tiny delay para hindi ma-rate-limit agad

    print()
    if success:
        print(f"{GB}🎉 SUCCESS! BL Auth Approved on one of the bursts!{N}")
    else:
        print(f"{RB}Burst finished — No approval received.{N}")

    print(f"{Y}[NEXT] Quota resets → 00:00 Beijing tomorrow{N}")
    print(f"\n{P}Join for updates & new tools: https://t.me/Cflhax{N}")

if __name__ == "__main__":
    main()
