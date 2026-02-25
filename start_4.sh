#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# CF LHAX - START 4x BLASTER v2.0
# Parallel Burst • 4 Tokens at Once
# kennedy • 2026 • https://t.me/Cflhax
# ============================================================

clear

# Mga kulay para mas maganda tingnan
R='\033[1;31m'
G='\033[1;32m'
Y='\033[1;33m'
B='\033[1;34m'
P='\033[1;35m'
C='\033[1;36m'
W='\033[1;37m'
N='\033[0m'

# Path ng folder (pwede mo palitan kung iba)
SCRIPT_DIR="$HOME/storage/shared/script/unlock-tool"
SCRIPT_NAME="bl_blaster.py"   # ← Palitan mo kung iba pangalan ng .py mo

# Banner
echo -e "\( {C}╔════════════════════════════════════════════╗ \){N}"
echo -e "${C}║     \( {P}★ CF LHAX - 4x PARALLEL BLASTER ★ \){C}       ║${N}"
echo -e "${C}║  \( {Y}Telegram : \){W} https://t.me/Cflhax            \( {C}║ \){N}"
echo -e "${C}║  \( {G}Mode     : \){W} 4 Tokens Simultaneous Burst    \( {C}║ \){N}"
echo -e "\( {C}╚════════════════════════════════════════════╝ \){N}"
echo -e ""

# Check kung may folder at script
if [ ! -d "$SCRIPT_DIR" ]; then
    echo -e "${R}[ERROR] Folder not found: \( SCRIPT_DIR \){N}"
    echo -e "\( {Y}→ Siguraduhin mong nasa tamang path yan! \){N}"
    exit 1
fi

cd "$SCRIPT_DIR" || {
    echo -e "${R}[CRITICAL] Cannot cd to \( SCRIPT_DIR \){N}"
    exit 1
}

if [ ! -f "$SCRIPT_NAME" ]; then
    echo -e "${R}[ERROR] Python script not found: \( SCRIPT_NAME \){N}"
    echo -e "\( {Y}→ Siguraduhing nasa folder yan at tama ang pangalan. \){N}"
    exit 1
fi

# Check kung installed na ang tmux
if ! command -v tmux &> /dev/null; then
    echo -e "\( {Y}Installing tmux... \){N}"
    pkg install tmux -y
fi

# Kill old session kung meron (para walang conflict)
tmux kill-session -t mibox 2>/dev/null

# Create new tmux session (detached)
echo -e "${G}→ Creating 4-pane tmux session: \( {W}mibox \){N}"
tmux new-session -d -s mibox

# Layout: 4 panes (2x2 grid)
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v

# Optional: equalize pane sizes para pantay-pantay
tmux select-layout even-horizontal
tmux select-layout tiled 2>/dev/null || true

# Run script sa bawat pane + label para madaling makita
echo -e "\( {Y}→ Starting 4 parallel instances... \){N}"

tmux send-keys -t 0 "clear && echo -e '\( {P}=== TOKEN SLOT 1 === \){N}' && python $SCRIPT_NAME" C-m
tmux send-keys -t 1 "clear && echo -e '\( {P}=== TOKEN SLOT 2 === \){N}' && python $SCRIPT_NAME" C-m
tmux send-keys -t 2 "clear && echo -e '\( {P}=== TOKEN SLOT 3 === \){N}' && python $SCRIPT_NAME" C-m
tmux send-keys -t 3 "clear && echo -e '\( {P}=== TOKEN SLOT 4 === \){N}' && python $SCRIPT_NAME" C-m

# Final instructions
echo -e ""
echo -e "\( {G}Session created! \){N}"
echo -e "• Attached na agad → type: \( {W}tmux attach -t mibox \){N}"
echo -e "• Kung gusto mo i-detach muna → Ctrl+B then D"
echo -e "• Kill session kapag tapos → \( {W}tmux kill-session -t mibox \){N}"
echo -e ""
echo -e "\( {C}Good luck sa burst boss! Join channel for updates: \){N}"
echo -e "\( {Y}https://t.me/Cflhax \){N}"

# Auto-attach (kung gusto mo auto pumunta sa tmux pagkatapos mag-run ng script)
# Kung ayaw mo auto-attach, comment out mo yung line na 'to sa baba
tmux attach-session -t mibox
