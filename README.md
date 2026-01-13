# 🎨 Phon3x-ART: Professional Steganography Tool

> **Advanced F5 Steganography with AES-256 Encryption**  
> *Hide data in plain sight with military-grade security*
<div align="center">
  
![Demo](https://raw.githubusercontent.com/Phon3x/phon3x-art/main/phon3x-art/assets/demo.gif)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-AGPL%203.0-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Kali%20|%20Ubuntu-orange.svg)](https://www.kali.org)
[![Steganography](https://img.shields.io/badge/Steganography-F5%20Algorithm-purple.svg)](https://en.wikipedia.org/wiki/F5_steganography)

</div>

---
## 🚀 Overview

**Phon3x-ART** is a professional-grade steganography tool that implements the **F5 algorithm** with **AES-256 encryption** to securely hide sensitive data within JPEG images. Unlike basic steganography tools, Phon3x-ART is designed to survive modern content platforms and maintain data integrity.

Originally developed for **personal use**, it enables:

- Uploading images to social platforms like Facebook and Messenger
- Storing encrypted data on public or private cloud drives
- Sending secret messages safely over common messaging platforms

---
## Table of Contents

- [🚀 Overview](#-overview)
- [🔥 Key Advantages](#-key-advantages)
- [✨ Features](#-features)
- [🎯 Why Phon3x-ART?](#-why-phon3x-art)
- [🌐 Platform Bypass Capabilities](#-platform-bypass-capabilities)
- [📊 Performance Metrics](#-performance-metrics)
- [📦 Installation](#-installation)
  - [⚡Quick Installation (Kali/Ubuntu/Unix)](#-quick-installation)
  - [🔧 Manual Installation](#-manual-installation)
  - [🗑️ Uninstall](#-uninstall)
- [🏗️ Technical Architecture](#-technical-architecture)
- [🚨 Legal & Ethical Use](#-legal-ethical-use)
- [⭐ Support](#-support)

---
## 🔥 **Key Advantages**

✅ **Bypasses Platform Detection** - Successfully bypasses Facebook upload processing, Messenger file handling, ImgBB compression, and other common content platforms  
✅ **Private Hosting Compatible** - Works flawlessly with self-hosted servers, private drives, and cloud storage  
✅ **Military-Grade Encryption** - AES-256 with PBKDF2 key derivation ensures maximum security  
✅ **Compression Resistant** - Embedded data survives JPEG recompression and platform processing  
✅ **Dual-Mode Operation** - Professional F5 via OutGuess or robust fallback method  

---
## ✨ Features

| Feature | Description | Advantage |
|---------|-------------|-----------|
| **🔐 AES-256 Encryption** | Military-grade encryption for hidden data | Unbreakable security layer |
| **🛡️ True F5 Algorithm** | Uses OutGuess for authentic F5 implementation | Maximum stealth and capacity |
| **💪 Platform Bypass** | Survives Facebook, Messenger, ImgBB processing | Real-world usability |
| **🎲 Password-Based** | Unique embedding for each password | Plausible deniability |
| **📈 Variable Payload** | Hide text or files up to image capacity | Flexible usage |
| **🔍 Auto-Detection** | Smart extraction without additional parameters | User-friendly operation |
| **🌐 Cross-Platform** | Works on Kali Linux, Ubuntu, and other Linux distros | Wide compatibility |

---
## 🎯 **Why Phon3x-ART**

Traditional steganography tools fail on modern platforms due to aggressive recompression and processing. Phon3x-ART is specifically engineered to:

- **Bypass Facebook's** image processing pipeline
- **Survive Messenger's** file compression
- **Evade ImgBB's** optimization algorithms
- **Work on private** hosting solutions and cloud drives
- **Maintain integrity** through multiple upload/download cycles

---
## 🌐 Platform Bypass Capabilities

![Last Updated](https://img.shields.io/badge/Last%20Updated-January%2012%2C%202026-lightgrey)

Phon3x-ART has been tested and proven to function across multiple platforms while preserving payload integrity.

| Platform         | Status Badge | Notes |
|------------------|-------------|-------|
| **Facebook Uploads** | ![Working](https://img.shields.io/badge/Status-Working-brightgreen) | Survives FB's image processing |
| **Messenger Files** | ![Working](https://img.shields.io/badge/Status-Working-brightgreen) | Maintains integrity through compression |
| **ImgBB** | ![Working](https://img.shields.io/badge/Status-Working-brightgreen) | Bypasses optimization algorithms |
| **Private Hosting** | ![Working](https://img.shields.io/badge/Status-Working-brightgreen) | Works on any self-hosted solution |
| **Cloud Drives** | ![Working](https://img.shields.io/badge/Status-Working-brightgreen) | Google Drive, Dropbox, and similar |
| **Discord** | ![Limited](https://img.shields.io/badge/Status-Limited-yellow) | Requires original quality uploads |
| **Telegram** | ![Limited](https://img.shields.io/badge/Status-Limited-yellow) | May fail under heavy compression |

---
## 📊 Performance Metrics

| Metric                     | 🖼 OutGuess Mode                                                             | 🔄 Fallback Mode                                                    |
| -------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Capacity**               | Up to 15% of image                                                           | Up to 5% of image                                                   |
| **Compression Resistance** | ![Excellent](https://img.shields.io/badge/Resistance-Excellent-brightgreen)  | ![Good](https://img.shields.io/badge/Resistance-Good-yellow)        |
| **Detection Resistance**   | ![Very High](https://img.shields.io/badge/Detection-Very%20High-brightgreen) | ![Moderate](https://img.shields.io/badge/Detection-Moderate-yellow) |
| **Platform Survival Rate** | 95%+                                                                         | 80%+                                                                |
| **Processing Speed**       | ![Fast](https://img.shields.io/badge/Speed-Fast-brightgreen)                 | ![Very Fast](https://img.shields.io/badge/Speed-Very%20Fast-blue)   |

---
## 📦 Installation

### ⚡ **Quick Installation**

For the fastest setup, use our one-line installer:

```bash
# One-command installation (Kali/Ubuntu)
curl -sSL https://raw.githubusercontent.com/Phon3x/Phon3x-ART/main/install/install_phon3x-art.sh | sudo bash
```

Or download and run manually:

```bash
# Download the installer from the repository
wget https://raw.githubusercontent.com/Phon3x/Phon3x-ART/main/install/install_phon3x-art.sh

# Make executable and run
chmod +x install_phon3x-art.sh
sudo ./install_phon3x-art.sh
```

_The Phon3x-ART installer automatically performs the following steps:_

| Step | Action                   | Result                                        |
| ---- | ------------------------ | --------------------------------------------- |
| 1️⃣  | **System Check**         | Verifies Python 3.8+ and dependencies         |
| 2️⃣  | **Dependencies**         | Installs required system packages             |
| 3️⃣  | **Project Setup**        | Creates `~/Phon3x-ART/` directory             |
| 4️⃣  | **Virtual Environment**  | Sets up isolated Python environment           |
| 5️⃣  | **Application Download** | Fetches latest Phon3x-ART scripts             |
| 6️⃣  | **Python Packages**      | Installs Pillow, PyCryptodome, NumPy          |
| 7️⃣  | **Desktop Integration**  | Creates launcher and menu entry               |
| 8️⃣  | **PATH Setup**           | Adds `phon3x-art` command to terminal         |
| 9️⃣  | **OutGuess (Optional)**  | Installs professional F5 steganography engine |
| 🔟   | **Verification**         | Validates installation and shows usage        |

> After completing these steps, Phon3x-ART is ready for use directly from the terminal or desktop launcher.

### 🔧 **Manual Installation**

```bash
# Create the environment
python3 -m venv phon3x-art

# Activate it
source phon3x-art/bin/activate

# Clone repository
git clone https://github.com/Phon3x/Phon3x-ART.git
cd Phon3x-ART

# Install Python dependencies
pip install pillow pycryptodome numpy

# Run the tool
python3 phon3x-art.py

# Install OutGuess
python3 phon3x-art.py
# choose Option 3

## I provide full manual install instruction or input 'y' and it will automatically install OutGuess
```

### 🗑️ Uninstall

To completely remove Phon3x-ART from your system, run the following commands:

```bash
# Download the uninstaller
wget https://raw.githubusercontent.com/Phon3x/Phon3x-ART/main/install/uninstall_phon3x-art.sh

# Make it executable
chmod +x uninstall_phon3x-art.sh

# Run the uninstaller
sudo ./uninstall_phon3x-art.sh
```

---
## 🏗️ Technical Architecture

```text
Phon3x-ART Architecture
├── 🔐 Encryption Layer (AES-256-CBC)
│   ├── PBKDF2 Key Derivation (100k iterations)
│   ├── Secure Random IV Generation
│   └── PKCS7 Padding
│
├── 🖼️ Steganography Layer
│   ├── 🎯 Professional Mode (OutGuess F5)
│   │   ├── DCT Coefficient Manipulation
│   │   ├── Matrix Encoding
│   │   └── Error Correction
│   │
│   └── 🛠️ Fallback Mode (Spatial Domain)
│       ├── 2nd LSB Manipulation
│       ├── Password-Based Permutation
│       └── 2× Repetition Error Correction
│
└── 🧪 Integrity Layer
|    ├── CRC32 Checksum Validation
|    ├── Payload Length Verification
|    └── Auto-Detection Algorithms
│
└── 📦 Installation System
    ├── Automatic Dependency Management
    ├── Virtual Environment Isolation
    ├── Desktop Menu Integration
    └── Clean Uninstall Support
```

---
## 🚨 Legal & Ethical Use

<div align="center">

![Legal](https://img.shields.io/badge/Use-Legal%20Only-red)
![Ethics](https://img.shields.io/badge/Ethics-Required-important)
![Responsibility](https://img.shields.io/badge/Responsibility-User--Owned-orange)

</div>

Phon3x-ART is provided **for legitimate purposes only**. Users are responsible for complying with all applicable laws.  

```text
✅ Allowed Uses:  
- Privacy protection  
- Security research  
- Educational use  
- Authorized penetration testing  
- Digital forensics training  

❌ Prohibited: 
- Illegal activities  
- Unauthorized data access or surveillance  

> Note: Misuse may violate laws. Authors are not liable for unlawful use.
```

---
## ⭐ Support

If you find Phon3x-ART useful, you can support the project by:

- ⭐ **Starring** the repository on GitHub  
- 🐛 **Reporting issues or bugs**  
- 💡 **Suggesting features or improvements**  
- 🔄 **Sharing** with the community  
- 📚 **Contributing** to the documentation



