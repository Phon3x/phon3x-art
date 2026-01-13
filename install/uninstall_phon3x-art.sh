#!/bin/bash

# ==============================================
# Phon3x-ART Uninstaller
# ==============================================

set -e

# ---------------- Configuration ----------------
PROJECT_DIR="$HOME/Phon3x-ART"
DESKTOP_FILE="$HOME/.local/share/applications/phon3x-art.desktop"
ICON_FILE="/usr/share/icons/hicolor/256x256/apps/phon3x-art.png"
BIN_CMD="/usr/local/bin/phon3x-art"

# ---------------- Colors ----------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ---------------- UI Functions ----------------
print_step()    { echo -e "${YELLOW}[+]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error()   { echo -e "${RED}[!]${NC} $1"; }
print_info()    { echo -e "${BLUE}[i]${NC} $1"; }

# ---------------- Root Check ----------------
if [[ $EUID -ne 0 ]]; then
    print_info "Some steps require sudo privileges"
fi

echo ""
print_info "Phon3x-ART Uninstaller"

# ---------------- Confirmation ----------------
read -rp "Are you sure you want to uninstall Phon3x-ART? (y/N): " CONFIRM
CONFIRM=${CONFIRM,,}  # convert to lowercase
[[ "$CONFIRM" != "y" ]] && { echo "Uninstallation cancelled."; exit 0; }

echo ""

# ---------------- Remove Desktop File ----------------
if [[ -f "$DESKTOP_FILE" ]]; then
    print_step "Removing desktop entry..."
    rm -f "$DESKTOP_FILE"
    print_success "Removed: $DESKTOP_FILE"
else
    print_info "No desktop entry found"
fi

# ---------------- Remove Icon ----------------
if [[ -f "$ICON_FILE" ]]; then
    print_step "Removing icon..."
    sudo rm -f "$ICON_FILE"
    print_success "Removed: $ICON_FILE"
else
    print_info "No icon file found"
fi

# ---------------- Remove PATH Command ----------------
if [[ -f "$BIN_CMD" ]]; then
    print_step "Removing terminal command..."
    sudo rm -f "$BIN_CMD"
    print_success "Removed: $BIN_CMD"
else
    print_info "No terminal command found"
fi

# ---------------- Remove Project Directory ----------------
if [[ -d "$PROJECT_DIR" ]]; then
    read -rp "Do you want to remove the project directory and all its contents? (y/N): " DEL_CHOICE
    DEL_CHOICE=${DEL_CHOICE,,}
    if [[ "$DEL_CHOICE" == "y" ]]; then
        print_step "Removing project directory..."
        rm -rf "$PROJECT_DIR"
        print_success "Removed: $PROJECT_DIR"
    else
        print_info "Project directory preserved"
    fi
else
    print_info "No project directory found"
fi

# ---------------- Optional OutGuess Removal ----------------
read -rp "Do you want to remove OutGuess installed by this tool? (y/N): " OUT_CHOICE
OUT_CHOICE=${OUT_CHOICE,,}
if [[ "$OUT_CHOICE" == "y" ]]; then
    if command -v outguess &>/dev/null; then
        OUT_DIR="$PROJECT_DIR/outguess/outguess-master"
        if [[ -d "$OUT_DIR" ]]; then
            print_step "Removing OutGuess..."
            sudo make -C "$OUT_DIR" uninstall || true
            print_success "OutGuess uninstall command executed"
        fi
        sudo rm -rf "$PROJECT_DIR/outguess"
        print_success "OutGuess removed from project directory"
    else
        print_info "OutGuess not found in system"
    fi
fi

# ---------------- Refresh Desktop Menu ----------------
print_step "Refreshing desktop menu..."
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
fi
if command -v kbuildsycoca5 &>/dev/null; then
    kbuildsycoca5 2>/dev/null || true
fi
print_success "Desktop menu refreshed"

echo ""
print_success "Phon3x-ART uninstallation complete!"
echo ""
