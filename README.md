<div align="center">
  <h1>🔥 Xiaomi HyperOS Unlock Automator + Alarm Bell 🛎</h1>
  <p><strong>Termux-only tool na may tunog pag na-grant na ang bootloader permission!</strong></p>
  <p>4 parallel slots • Auto midnight trigger • Super colorful logs</p>

  <img src="https://img.shields.io/badge/Termux-Android-green?style=for-the-badge&logo=android&logoColor=white" />
  <img src="https://img.shields.io/badge/Alarm%20on%20Success-red?style=for-the-badge&logo=bell" />
  <img src="https://img.shields.io/badge/Python%20%2B%20tmux-blue?style=for-the-badge" />
</div>

### Features ✨
✅ 4 split-screen windows (tmux) para mas mataas chance sa quota  
✅ Auto sync sa Beijing time + live countdown bar  
✅ 2 tokens lang kailangan (reuse sa odd/even slots)  
✅ **Alarm pag success**: Vibration + notification + voice "Success!" + loud siren beep  
✅ Colored real-time logs + status icons (READY / WAITING / SUCCESS)

### One-Command Install (copy-paste lang sa Termux)
```bash
pkg update -y && pkg install git tmux python termux-api sox -y && \
pip install requests ntplib pytz urllib3 icmplib colorama && \
git clone https://github.com/MrHyperOS/xiaomi-hyperos-unlock-alarm.git && \
cd xiaomi-hyperos-unlock-alarm && \
bash start.sh
