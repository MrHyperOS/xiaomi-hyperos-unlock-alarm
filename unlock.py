import requests, time, sys, ntplib, pytz, os
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

slot = int(sys.argv[1]) if len(sys.argv) > 1 else 1

print(f"{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════╗")
print(f"║   SLOT {slot} - HYPEROS UNLOCKER   ║")
print(f"╚════════════════════════════════╝{Style.RESET_ALL}")

# Token
with open('token.txt', 'r') as f:
    tokens = [line.strip() for line in f if line.strip()]
token = tokens[0] if slot % 2 == 1 else tokens[1] if len(tokens) > 1 else tokens[0]

print(f"{Fore.YELLOW}Token: {token[:10]}...{Style.RESET_ALL}")

# Time
beijing_tz = pytz.timezone('Asia/Shanghai')
now = datetime.now(beijing_tz)
midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
seconds_left = (midnight - now).total_seconds()

print(f"{Fore.MAGENTA}Waiting for 00:00 Beijing...{Style.RESET_ALL}")

# Live Countdown
while seconds_left > 0:
    h = int(seconds_left // 3600)
    m = int((seconds_left % 3600) // 60)
    s = int(seconds_left % 60)
    print(f"\r{Fore.BLUE}{h:02d}:{m:02d}:{s:02d} remaining...{Style.RESET_ALL}", end="", flush=True)
    time.sleep(1)
    seconds_left -= 1

print(f"\n{Fore.GREEN}{Style.BRIGHT}🚀 MIDNIGHT NA! BRUTE FORCE START! 🚀{Style.RESET_ALL}")

url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
headers = {"Cookie": f"new_bbs_serviceToken={token}", "Content-Type": "application/json"}

for attempt in range(1, 101):
    try:
        r = requests.post(url, headers=headers, json={"is_retry": True}, timeout=6)
        print(f"{Fore.BLUE}[Attempt {attempt}] {r.text}{Style.RESET_ALL}")
        if '"code":0' in r.text:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ SUCCESS SA SLOT {slot}! 🎉{Style.RESET_ALL}")
            os.system(f'termux-notification --title "SUCCESS SLOT {slot}" --content "Permission granted na!" --vibrate 1500 --sound')
            os.system(f'termux-tts-speak "Slot {slot} success! Permission granted na!"')
            os.system('play -q -n synth 4 sin 400-1200 fade h 0 4 1 &')
            break
    except:
        pass
    time.sleep(0.35)
