#!/bin/bash

# ==============================================
# Phon3x-ART Professional Installer
# Kali Linux / Ubuntu
# ==============================================

set -e

# ---------------- Configuration ----------------
PROJECT_DIR="$HOME/Phon3x-ART"
VENV_DIR="$PROJECT_DIR/venv"
RUN_SCRIPT="$PROJECT_DIR/run_phon3x-art.sh"
PYTHON_SCRIPT="phon3x-art.py"
REPO_URL="https://raw.githubusercontent.com/Phon3x/phon3x-art/main/phon3x-art"
ICON_URL="https://raw.githubusercontent.com/Phon3x/phon3x-art/main/phon3x-art/assets/icon.png"
ICON_DEST="/usr/share/icons/hicolor/256x256/apps/phon3x-art.png"
DESKTOP_FILE="$HOME/.local/share/applications/phon3x-art.desktop"

# ---------------- Colors ----------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ---------------- UI Functions ----------------
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║             Phon3x-ART Professional Installer            ║"
    echo "║      Advanced Steganography Tool - F5 + AES-256          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step()    { echo -e "${YELLOW}[+]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error()   { echo -e "${RED}[!]${NC} $1"; }
print_info()    { echo -e "${BLUE}[i]${NC} $1"; }

# ---------------- Root Check ----------------
if [[ $EUID -eq 0 ]]; then
    print_error "Do NOT run this installer as root!"
    exit 1
fi

print_header
print_info "GitHub: https://github.com/Phon3x"
echo ""

# ---------------- System Dependencies ----------------
print_step "Installing system dependencies..."
sudo apt update -y
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    unzip \
    build-essential \
    autoconf \
    automake \
    libtool
print_success "System dependencies installed"

# ---------------- Project Directory ----------------
print_step "Creating project directory..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
print_success "Project directory ready"

# ---------------- Virtual Environment ----------------
print_step "Setting up Python virtual environment..."
if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# ---------------- Download App ----------------
print_step "Downloading Phon3x-ART..."
curl -fsSL "$REPO_URL/$PYTHON_SCRIPT" -o "$PYTHON_SCRIPT" || { print_error "Failed to download main script"; exit 1; }
chmod +x "$PYTHON_SCRIPT"
print_success "Application downloaded"

# ---------------- Python Dependencies ----------------
print_step "Installing Python dependencies..."
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet pillow pycryptodome numpy
deactivate
print_success "Python dependencies installed"

# ---------------- Create run_phon3x-art.sh ----------------
print_step "Creating launcher script..."
cat > "$RUN_SCRIPT" << EOL
#!/bin/bash
cd "$PROJECT_DIR" || exit 1
source "$VENV_DIR/bin/activate"
python3 "$PYTHON_SCRIPT"
EOL
chmod +x "$RUN_SCRIPT"
print_success "Launcher script created: $RUN_SCRIPT"

# ---------------- Download Icon ----------------
print_step "Downloading icon..."
sudo mkdir -p "$(dirname "$ICON_DEST")"
sudo curl -fsSL "$ICON_URL" -o "$ICON_DEST" || { print_error "Failed to download icon"; exit 1; }
print_success "Icon installed: $ICON_DEST"

# ---------------- Create .desktop file ----------------
print_step "Creating .desktop file..."
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Phon3x-ART
GenericName=Steganography Tool
Comment=Advanced Steganography Tool (F5 + AES-256)
Exec=$RUN_SCRIPT
Icon=$ICON_DEST
Terminal=true
Categories=Utility;X-Security;
Keywords=steganography;encryption;security;
StartupWMClass=Phon3x-ART
StartupNotify=true
EOL
chmod +x "$DESKTOP_FILE"
print_success ".desktop file created: $DESKTOP_FILE"

# ---------------- Refresh Desktop Menu ----------------
print_step "Refreshing desktop menu..."
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
fi
if command -v kbuildsycoca5 &>/dev/null; then
    kbuildsycoca5 2>/dev/null || true
fi
print_success "Desktop menu refreshed"

# ---------------- Add to PATH ----------------
BIN_SCRIPT="/usr/local/bin/phon3x-art"
if [[ -f "$BIN_SCRIPT" ]]; then
    read -rp "'phon3x-art' already exists in PATH. Overwrite? (y/N): " PATH_CHOICE
    PATH_CHOICE=${PATH_CHOICE,,}
    [[ "$PATH_CHOICE" != "y" ]] && { print_info "Skipped adding command to PATH"; BIN_SCRIPT=""; }
fi

if [[ -n "$BIN_SCRIPT" ]]; then
    sudo tee "$BIN_SCRIPT" > /dev/null <<EOL
#!/bin/bash
"$RUN_SCRIPT" "\$@"
EOL
    sudo chmod +x "$BIN_SCRIPT"
    print_success "Command 'phon3x-art' added to PATH. You can now run 'phon3x-art' from any terminal."
fi

# ---------------- Optional OutGuess ----------------
install_outguess() {
    echo ""
    print_info "OutGuess provides professional F5 steganography support"
    read -rp "Do you want to install OutGuess now? (y/N): " OUTGUESS_CHOICE
    OUTGUESS_CHOICE=${OUTGUESS_CHOICE,,}
    [[ "$OUTGUESS_CHOICE" != "y" ]] && { print_info "OutGuess installation skipped"; return; }

    OUT_DIR="$PROJECT_DIR/outguess"
    print_step "Downloading OutGuess source to $OUT_DIR..."
    rm -rf "$OUT_DIR"
    mkdir -p "$OUT_DIR"
    cd "$OUT_DIR"

    wget -q -O outguess.zip \
        https://github.com/resurrecting-open-source-projects/outguess/archive/refs/heads/master.zip || { print_error "Failed to download OutGuess"; return; }
    unzip -q outguess.zip

    # GitHub zip usually extracts to outguess-master
    cd outguess-master || { print_error "Outguess folder missing"; return; }

    print_step "Applying compiler compatibility fixes..."
    export CFLAGS="-std=gnu99 -fcommon"
    export CPPFLAGS="-I$(pwd)/src/jpeg-6b-steg"

    print_step "Preparing build system..."
    autoreconf -fi

    print_step "Configuring OutGuess..."
    ./configure --with-generic-jconfig

    print_step "Building OutGuess..."
    make

    print_step "Installing OutGuess (sudo required)..."
    sudo make install

    print_success "OutGuess installed successfully"
    print_info "Verify with: outguess --version"
}

install_outguess

# ---------------- Done ----------------
echo ""
echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              INSTALLATION COMPLETE!                      ${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📁 Project:${NC} $PROJECT_DIR"
echo -e "${BLUE}🖥 Desktop launcher:${NC} $DESKTOP_FILE"
echo -e "${BLUE}🖥 Terminal command:${NC} phon3x-art"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo " • You can launch from the Applications Menu"
echo " • Or run: $RUN_SCRIPT"
echo " • Or type 'phon3x-art' in any terminal"
echo ""
