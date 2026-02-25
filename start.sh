#### File 2: start.sh
```bash
#!/bin/bash

echo -e "\033[1;32mXiaomi HyperOS Unlock + Alarm 🛎 - Launching...\033[0m"

# Install deps quietly
pkg install tmux python termux-api sox -y >/dev/null 2>&1
pip install requests ntplib pytz urllib3 icmplib colorama >/dev/null 2>&1

tmux new-session -d -s unlock_alarm
tmux split-window -h -t unlock_alarm
tmux split-window -v -t unlock_alarm:0.0
tmux split-window -v -t unlock_alarm:0.1

tmux send-keys -t unlock_alarm:0.0 "python unlock.py 1" C-m
tmux send-keys -t unlock_alarm:0.1 "python unlock.py 2" C-m
tmux send-keys -t unlock_alarm:0.2 "python unlock.py 3" C-m
tmux send-keys -t unlock_alarm:0.3 "python unlock.py 4" C-m

tmux attach -t unlock_alarm
