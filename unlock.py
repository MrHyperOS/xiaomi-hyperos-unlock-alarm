import requests, time, sys, ntplib, pytz, os
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

slot = int(sys.argv[1]) if len(sys.argv) > 1 else 1

print(f"{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════╗")
print(f"║   SLOT {slot} - HYPEROS UNLOCKER   ║")
print(f"╚════════════════════════════════╝{Style.RESET_ALL}")

# Token reuse
try:
    with open('token.txt', 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]
    token = tokens[0] if slot % 2 == 1 else tokens[1] if len(tokens) > 1 else tokens[0]
    print(f"{Fore.YELLOW}Token: {token[:10]}...{Style.RESET_ALL}")
except:
    print(f"{Fore.RED}Walang token.txt! Gumawa muna.{Style.RESET_ALL}")
    sys.exit(1)

# Time sync
beijing_tz = pytz.timezone('Asia/Shanghai')
now = datetime.now(beijing_tz)

print(f"{Fore.GREEN}Beijing Time: {now.strftime('%H:%M:%S')}{Style.RESET_ALL}")

# Next midnight
midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
seconds_left = (midnight - now).total_seconds()

print(f"{Fore.MAGENTA}Waiting for 00:00 Beijing... ({int(seconds_left // 3600)} hrs {int((seconds_left % 3600) // 60)} mins){Style.RESET_ALL}")

# Live countdown bar
bar_length = 30
while seconds_left > 0:
    h, rem = divmod(seconds_left, 3600)
    m, s = divmod(rem, 60)
    percent = 1 - (seconds_left / (24 * 3600))  # rough daily percent
    filled = int(bar_length * (1 - percent))
    bar = '█' * filled + ' ' * (bar_length - filled)
    print(f"\r{Fore.BLUE}{int(h):02d}:{int(m):02d}:{int(s):02d} [{bar}] {int(percent*100)}%{Style.RESET_ALL}", end="", flush=True)
    time.sleep(1)
    seconds_left -= 1

print(f"\n{Fore.GREEN}{Style.BRIGHT}🚀 00:00 BEIJING NA! BRUTE FORCE START! 🚀{Style.RESET_ALL}")

url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
headers = {"Cookie": f"new_bbs_serviceToken={token}", "Content-Type": "application/json"}

success = False
for attempt in range(1, 101):
    try:
        r = requests.post(url, headers=headers, json={"is_retry": True}, timeout=6)
        print(f"{Fore.BLUE}[Attempt {attempt}] {r.text}{Style.RESET_ALL}")
        if '"code":0' in r.text:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ SUCCESS SA SLOT {slot}! 🎉🎉🎉{Style.RESET_ALL}")
            success = True
            break
        if "quota" in r.text.lower():
            print(f"{Fore.RED}Quota limit... stop slot {slot}{Style.RESET_ALL}")
            break
    except:
        print(f"{Fore.RED}Request error... retry{Style.RESET_ALL}")
    time.sleep(0.3)

# ALARM if success
if success:
    os.system(f'termux-notification --title "UNLOCK SUCCESS SLOT {slot}" --content "Permission granted na! Check mo na!" --vibrate 1500 500 1500 --sound')
    os.system(f'termux-tts-speak "Slot {slot} success! Unlock permission granted na! Good job!"')
    os.system('play -q -n synth 4 sin 300-1200 fade h 0 4 1 &')  # 4-sec siren beep

print(f"{Fore.CYAN}Slot {slot} tapos na.{Style.RESET_ALL}")
