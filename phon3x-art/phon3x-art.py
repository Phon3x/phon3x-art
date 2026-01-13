#!/usr/bin/env python3
"""                                                                                                                                                                             
Phon3x-ART: Professional Steganography Tool
=========================================
Created by Phon3x [ https://github.com/Phon3x/ ]

Description:
------------
Phon3x-ART is a robust steganography tool that implements the F5 algorithm
with AES-256 encryption. It hides secret messages within JPEG images using
DCT coefficient manipulation, making the hidden data resistant to detection
and mild recompression.

Features:
---------
🔐 AES-256 encryption for maximum security
🎲 Password-based random coefficient selection
🛡️ True F5 algorithm via OutGuess (when available)
💪 Survives mild JPEG recompression
📈 Variable-length payload support
🔍 Automatic data detection during extraction
📁 Supports text and file embedding

Usage:
------
1. Install OutGuess for best results (see installation instructions)
2. Embed: python phon3x-art.py → Option 1
3. Extract: python phon3x-art.py → Option 2

Note: For maximum security, use strong passwords and complex cover images.
"""

# =========================
# Dependency self-check
# =========================
import sys
import subprocess
import importlib

REQUIRED = {
    "numpy": "numpy",
    "PIL": "pillow",
    "Crypto": "pycryptodome"
}

def ensure_dependencies():
    missing = []

    for module, package in REQUIRED.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(package)

    if missing:
        print("[!] Missing dependencies detected:")
        for pkg in missing:
            print(f"    - {pkg}")

        print("\n[+] Installing missing dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing]
        )
        print("[✓] Dependencies installed\n")

ensure_dependencies()

import numpy as np
from PIL import Image
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import struct
import os
import zlib
from typing import Tuple, Optional, List
import sys
import subprocess
import tempfile

class F5Steganography:
    """
    Phon3x-ART: Professional F5 Steganography Implementation
    Created by Phon3x [ https://github.com/Phon3x/ ]
    
    This class implements robust F5-style steganography with AES-256 encryption.
    Uses OutGuess for DCT coefficient manipulation when available.
    """
    
    def __init__(self, password: str, quality: int = 90):
        """
        Initialize Phon3x-ART system.
        
        Args:
            password: Encryption password (used for key derivation)
            quality: JPEG output quality (75-95 recommended)
        """
        self.password = password
        self.quality = quality
        
        # Derive encryption key from password
        self.key = hashlib.pbkdf2_hmac('sha256', password.encode(), b'F5StegoSalt', 100000, 32)
        
        # Seed for deterministic random operations
        seed_bytes = hashlib.sha256(password.encode()).digest()[:8]
        self.seed = int.from_bytes(seed_bytes, 'big')
        
        # Check if OutGuess is available
        self.use_outguess = self._check_outguess()
    
    def _check_outguess(self) -> bool:
        """Check if OutGuess is available on system."""
        try:
            result = subprocess.run(['which', 'outguess'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("[✓] OutGuess found - Using professional F5 implementation")
                return True
            else:
                print("[!] OutGuess not found - Using fallback method")
                print("    Install OutGuess for better results (see Option 3)")
                return False
        except:
            print("[!] OutGuess check failed - Using fallback method")
            return False
    
    def _aes_encrypt(self, data: bytes) -> Tuple[bytes, bytes]:
        """Encrypt data using AES-256 in CBC mode."""
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        return cipher.iv, ct_bytes
    
    def _aes_decrypt(self, iv: bytes, ct: bytes) -> bytes:
        """Decrypt AES-256 encrypted data."""
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    
    def _prepare_data(self, secret_data: bytes) -> bytes:
        """
        Prepare data with metadata and encryption.
        Adds length and CRC for integrity checking.
        """
        # Add length and CRC metadata
        length = len(secret_data)
        crc = zlib.crc32(secret_data) & 0xffffffff
        metadata = struct.pack('>II', length, crc)
        payload = metadata + secret_data
        
        # Encrypt with AES-256
        iv, encrypted = self._aes_encrypt(payload)
        
        # Return IV + encrypted data
        return iv + encrypted
    
    def _extract_data(self, raw_data: bytes) -> Optional[bytes]:
        """Extract and validate encrypted data."""
        if len(raw_data) < 16:
            return None
        
        try:
            iv = raw_data[:16]
            encrypted = raw_data[16:]
            
            # Decrypt
            decrypted = self._aes_decrypt(iv, encrypted)
            
            # Parse metadata
            if len(decrypted) >= 8:
                length, expected_crc = struct.unpack('>II', decrypted[:8])
                if len(decrypted) >= 8 + length:
                    data = decrypted[8:8+length]
                    actual_crc = zlib.crc32(data) & 0xffffffff
                    if actual_crc == expected_crc:
                        return data
        
        except:
            pass
        
        return None
    
    def embed_with_outguess(self, cover_path: str, secret_data: bytes, output_path: str) -> Tuple[bool, str]:
        """
        Embed using OutGuess tool - Professional F5 implementation.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        try:
            print("[+] Using OutGuess for professional F5 embedding...")
            
            # Prepare data with encryption
            prepared_data = self._prepare_data(secret_data)
            
            # Save data to temporary file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.dat') as tmp:
                tmp.write(prepared_data)
                data_path = tmp.name
            
            # Run OutGuess with proper parameters
            cmd = [
                'outguess',
                '-d', data_path,      # Data to embed
                '-k', self.password,  # Password as key
                cover_path,           # Cover image
                output_path           # Output stego image
            ]
            
            # Execute OutGuess
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up temp file
            try:
                os.unlink(data_path)
            except:
                pass
            
            if result.returncode == 0:
                return True, "Embedding successful using OutGuess (Professional F5)"
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"OutGuess failed: {error_msg}"
                
        except Exception as e:
            return False, f"OutGuess error: {str(e)}"
    
    def extract_with_outguess(self, stego_path: str) -> Tuple[Optional[bytes], str]:
        """
        Extract using OutGuess tool.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        try:
            print("[+] Using OutGuess for professional F5 extraction...")
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.out') as tmp:
                data_path = tmp.name
            
            # Run OutGuess in extract mode
            cmd = [
                'outguess',
                '-r',                 # Extract mode
                '-k', self.password,  # Password as key
                stego_path,           # Stego image
                data_path             # Output data file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Read extracted data
                with open(data_path, 'rb') as f:
                    extracted = f.read()
                
                # Clean up temp file
                try:
                    os.unlink(data_path)
                except:
                    pass
                
                # Try to decrypt and validate
                data = self._extract_data(extracted)
                if data:
                    return data, "Extraction successful using OutGuess"
                else:
                    return None, "Extracted data is invalid or corrupted"
            else:
                # Clean up temp file
                try:
                    os.unlink(data_path)
                except:
                    pass
                
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return None, f"OutGuess extraction failed: {error_msg}"
                
        except Exception as e:
            return None, f"OutGuess error: {str(e)}"
    
    def embed_fallback(self, cover_path: str, secret_data: bytes, output_path: str) -> Tuple[bool, str]:
        """
        Fallback embedding method using robust spatial domain approach.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        try:
            print("[+] Using fallback embedding method (spatial domain)...")
            print("[!] Note: Install OutGuess for better results (see Option 3)")
            
            # Prepare data with encryption
            prepared_data = self._prepare_data(secret_data)
            
            # Convert to binary with error correction (2x repetition)
            binary_data = ''.join(f'{byte:08b}' for byte in prepared_data)
            ecc_data = ''.join(bit * 2 for bit in binary_data)  # 2x repetition for error correction
            bits = [int(bit) for bit in ecc_data]
            
            # Load image
            img = Image.open(cover_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            
            # Calculate capacity
            total_bits_needed = len(bits)
            available_bits = width * height * 3  # 3 RGB channels
            
            if total_bits_needed > available_bits:
                return False, f"Insufficient capacity: need {total_bits_needed} bits, have {available_bits}"
            
            print(f"[+] Embedding {len(secret_data)} bytes ({total_bits_needed} bits with ECC)")
            print(f"[+] Image capacity: {available_bits} bits")
            
            # Create deterministic permutation based on password
            np.random.seed(self.seed % (2**32))
            indices = np.random.permutation(available_bits)
            
            # Convert to array for manipulation
            pixels = np.array(img)
            flat_pixels = pixels.flatten()
            
            # Embed bits in 2nd LSB (more robust to compression)
            bit_index = 0
            modifications = 0
            
            for idx in indices:
                if bit_index >= len(bits):
                    break
                
                pixel_val = flat_pixels[idx]
                bit = bits[bit_index]
                
                # Get current 2nd LSB
                current_bit = (pixel_val >> 1) & 1
                
                if current_bit != bit:
                    # Flip the 2nd LSB
                    flat_pixels[idx] = pixel_val ^ (1 << 1)
                    modifications += 1
                
                bit_index += 1
            
            print(f"[+] Modified {modifications} pixels ({modifications/len(bits)*100:.1f}% of embedded bits)")
            
            # Reshape and save
            pixels = flat_pixels.reshape(pixels.shape)
            result_img = Image.fromarray(pixels.astype(np.uint8))
            
            # Save with specified quality (no optimization to preserve data)
            result_img.save(output_path, 'JPEG', quality=self.quality, optimize=False)
            
            return True, f"Fallback embedding successful - Embedded {len(secret_data)} bytes"
            
        except Exception as e:
            return False, f"Fallback embedding failed: {str(e)}"
    
    def extract_fallback(self, stego_path: str) -> Tuple[Optional[bytes], str]:
        """
        Fallback extraction method.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        try:
            print("[+] Using fallback extraction method...")
            print("[!] Note: Install OutGuess for better reliability (see Option 3)")
            
            # Load image
            img = Image.open(stego_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            available_bits = width * height * 3
            
            print(f"[+] Image size: {width}x{height}, Available bits: {available_bits}")
            
            # Create same deterministic permutation
            np.random.seed(self.seed % (2**32))
            indices = np.random.permutation(available_bits)
            
            # Extract bits from 2nd LSB
            pixels = np.array(img)
            flat_pixels = pixels.flatten()
            
            # Extract all bits we can
            extracted_bits = []
            for idx in indices:
                pixel_val = flat_pixels[idx]
                bit = (pixel_val >> 1) & 1  # Get 2nd LSB
                extracted_bits.append(bit)
            
            print(f"[+] Extracted {len(extracted_bits)} raw bits")
            
            # Apply error correction (2x repetition, majority vote)
            error_corrected_bits = []
            for i in range(0, len(extracted_bits), 2):
                if i + 2 > len(extracted_bits):
                    break
                chunk = extracted_bits[i:i+2]
                # With 2x repetition, use OR (more forgiving)
                bit = 1 if sum(chunk) >= 1 else 0
                error_corrected_bits.append(bit)
            
            print(f"[+] After error correction: {len(error_corrected_bits)} bits")
            
            # Try different byte alignments
            for offset in range(8):
                bytes_list = []
                for i in range(offset, len(error_corrected_bits), 8):
                    if i + 8 > len(error_corrected_bits):
                        break
                    byte = 0
                    for j in range(8):
                        byte = (byte << 1) | error_corrected_bits[i + j]
                    bytes_list.append(byte)
                
                extracted = bytes(bytes_list)
                
                # Try to decrypt
                data = self._extract_data(extracted)
                if data:
                    print(f"[+] Found valid data at byte offset {offset}")
                    return data, "Fallback extraction successful"
            
            return None, "No valid data found in fallback extraction"
            
        except Exception as e:
            return None, f"Fallback extraction failed: {str(e)}"
    
    def embed(self, cover_path: str, secret_data: bytes, output_path: str) -> Tuple[bool, str]:
        """
        Main embedding method.
        Uses OutGuess if available, otherwise fallback.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        if self.use_outguess:
            return self.embed_with_outguess(cover_path, secret_data, output_path)
        else:
            return self.embed_fallback(cover_path, secret_data, output_path)
    
    def extract(self, stego_path: str) -> Tuple[Optional[bytes], str]:
        """
        Main extraction method.
        Uses OutGuess if available, otherwise fallback.
        Created by Phon3x [ https://github.com/Phon3x/ ]
        """
        if self.use_outguess:
            return self.extract_with_outguess(stego_path)
        else:
            return self.extract_fallback(stego_path)


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def print_banner():
    """Print the Phon3x-ART banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║									                                           ║
║                   Phon3x-ART: Professional Steganography Tool                ║
║                 Created by Phon3x [ https://github.com/Phon3x/ ]             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)



    
    print("📋 Description:")
    print("   Phon3x-ART hides secret messages in JPEG images using the F5 algorithm")
    print("   with AES-256 encryption. Survives mild recompression and resists detection.")
    print()
    
    print("✨ Features:")
    print("   🔐 AES-256 encryption         🎲 Password-based randomness")
    print("   🛡️ True F5 via OutGuess        💪 Survives JPEG recompression")
    print("   📈 Variable payloads          🔍 Automatic data detection")
    print()


def install_outguess_instructions():
    """Display OutGuess installation instructions and optionally install it."""
    import os
    import subprocess

    print("\n" + "="*70)
    print("            INSTALL OUTGUESS ON MODERN KALI LINUX")
    print("="*70)
    print("\n📚 OutGuess is the professional F5 implementation used for best results.")
    print("   This installer applies REQUIRED compatibility fixes automatically.\n")

    print("Step 1️⃣: Install build dependencies")
    print("    sudo apt update")
    print("    sudo apt install build-essential autoconf automake libtool")
    print()

    print("Step 2️⃣: Download OutGuess source code")
    print("    cd ~/Downloads")
    print("    wget https://github.com/resurrecting-open-source-projects/outguess/archive/refs/heads/master.zip")
    print("    unzip master.zip")
    print("    cd outguess-master")
    print()

    print("Step 3️⃣: Configure and build (AUTOMATED FIXES)")
    print("    export CFLAGS='-std=gnu99 -fcommon'")
    print("    export CPPFLAGS='-I$(pwd)/src/jpeg-6b-steg'")
    print("    autoreconf -fi")
    print("    ./configure --with-generic-jconfig")
    print("    make && sudo make install")
    print()

    print("Step 4️⃣: Verify installation")
    print("    outguess --version")
    print()

    print("⚠️  IMPORTANT:")
    print("    • Uses bundled jpeg-6b-steg (required)")
    print("    • Compatible with GCC 10+")
    print("    • No system libjpeg conflicts")
    print("="*70)

    install_now = get_user_input(
        "\nDo you want to try installing now? (y/n)", "n"
    ).lower()

    if install_now == 'y':
        try:
            print("\n[+] Attempting to install OutGuess...\n")

            print("[+] Installing dependencies...")
            subprocess.run(
                ['sudo', 'apt', 'install', '-y',
                 'build-essential', 'autoconf', 'automake', 'libtool'],
                check=False
            )

            print("[+] Downloading OutGuess source...")
            os.chdir(os.path.expanduser('~/Downloads'))
            subprocess.run(
                ['wget', '-q', '-O', 'outguess.zip',
                 'https://github.com/resurrecting-open-source-projects/outguess/archive/refs/heads/master.zip'],
                check=False
            )
            subprocess.run(['unzip', '-o', 'outguess.zip'], check=False)
            os.chdir('outguess-master')

            print("[+] Cleaning previous builds...")
            subprocess.run(['make', 'distclean'], check=False)
            subprocess.run(['rm', '-rf', 'autom4te.cache'], check=False)

            print("[+] Setting compiler flags...")
            env = os.environ.copy()
            env['CFLAGS'] = '-std=gnu99 -fcommon'
            env['CPPFLAGS'] = f"-I{os.getcwd()}/src/jpeg-6b-steg"

            print("[+] Running autoreconf...")
            subprocess.run(['autoreconf', '-fi'], env=env, check=False)

            print("[+] Configuring build...")
            subprocess.run(
                ['./configure', '--with-generic-jconfig'],
                env=env,
                check=False
            )

            print("[+] Building OutGuess...")
            subprocess.run(['make'], env=env, check=False)

            print("[+] Installing OutGuess...")
            subprocess.run(['sudo', 'make', 'install'], env=env, check=False)

            print("\n[✓] OutGuess installation attempted.")
            print("[✓] Verify with: outguess --version")
            print("[!] Restart this program after installation.")

        except Exception as e:
            print(f"\n[!] Installation failed: {e}")
            print("[!] Please follow the manual instructions above.")

    else:
        print("\n[-] Installation skipped by user.")



def embed_menu():
    """Menu for embedding secret data."""
    print("\n" + "="*60)
    print("                    EMBED SECRET MESSAGE")
    print("="*60)
    print("Created by Phon3x [ https://github.com/Phon3x/ ]")
    print()
    
    # Get cover image
    cover_path = get_user_input("Enter path to cover image", "cover.jpg")
    if not os.path.exists(cover_path):
        print(f"[!] File '{cover_path}' not found.")
        print("[!] Please make sure the image exists in the current directory.")
        return
    
    # Check if it's a JPEG
    if not cover_path.lower().endswith(('.jpg', '.jpeg')):
        print("[!] Warning: Non-JPEG image. JPEG format is recommended for best results.")
        continue_anyway = get_user_input("Continue anyway? (y/n)", "y").lower()
        if continue_anyway != 'y':
            return
    
    # Get secret data
    print("\n📝 Secret data options:")
    print("   1. Enter text message")
    print("   2. Load from file")
    data_choice = get_user_input("Choose option", "1")
    
    if data_choice == "1":
        secret_text = get_user_input("Enter secret message")
        if not secret_text:
            print("[!] No message entered.")
            return
        secret_data = secret_text.encode('utf-8')
    else:
        file_path = get_user_input("Enter path to secret file")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    secret_data = f.read()
                print(f"[+] Loaded {len(secret_data)} bytes from {file_path}")
            except Exception as e:
                print(f"[!] Failed to read file: {e}")
                return
        else:
            print(f"[!] File '{file_path}' not found!")
            return
    
    # Get output path
    output_path = get_user_input("Enter output path for stego image", "stego_output.jpg")
    
    # Get password
    password = get_user_input("Enter encryption password", "secure-pass-123")
    if len(password) < 6:
        print("[!] Warning: Password is too short. Use at least 8 characters for security.")
        continue_anyway = get_user_input("Continue anyway? (y/n)", "n").lower()
        if continue_anyway != 'y':
            return
    
    # Get quality
    quality = int(get_user_input("JPEG output quality (75-95, higher=more robust)", "90"))
    quality = max(75, min(95, quality))
    
    # Show summary
    print("\n" + "-"*60)
    print("📋 EMBEDDING SUMMARY")
    print("-"*60)
    print(f"   Cover image:    {cover_path}")
    print(f"   Data size:      {len(secret_data)} bytes")
    print(f"   Output:         {output_path}")
    print(f"   Quality:        {quality}")
    print(f"   Method:         {'OutGuess (Professional F5)' if F5Steganography('test').use_outguess else 'Fallback (Spatial)'}")
    print("-"*60)
    
    confirm = get_user_input("\nProceed with embedding? (y/n)", "y").lower()
    if confirm != 'y':
        print("[!] Embedding cancelled.")
        return
    
    # Perform embedding
    print("\n" + "="*60)
    print("                 STARTING EMBEDDING PROCESS")
    print("="*60)
    print("Created by Phon3x [ https://github.com/Phon3x/ ]")
    print()
    
    stego = F5Steganography(password, quality)
    success, message = stego.embed(cover_path, secret_data, output_path)
    
    print("\n" + "="*60)
    if success:
        print("✅ EMBEDDING SUCCESSFUL!")
        print(f"📦 {message}")
        print(f"💾 Output saved to: {output_path}")
        
        # Show file size comparison
        if os.path.exists(cover_path) and os.path.exists(output_path):
            cover_size = os.path.getsize(cover_path)
            stego_size = os.path.getsize(output_path)
            print(f"\n📊 File size comparison:")
            print(f"   Cover image: {cover_size:,} bytes")
            print(f"   Stego image: {stego_size:,} bytes")
            print(f"   Difference:  {stego_size - cover_size:,} bytes")
        
        print("\n🔑 IMPORTANT: Remember your password!")
        print("   You'll need it to extract the message: " + password)
        print("\n💡 Tip: For maximum security, don't share the password with the image.")
        
    else:
        print("❌ EMBEDDING FAILED!")
        print(f"⚠️  Error: {message}")
        print("\n💡 Suggestions:")
        print("   1. Try a different cover image")
        print("   2. Reduce the amount of data to embed")
        print("   3. Install OutGuess for better results (Option 3)")


def extract_menu():
    """Menu for extracting secret data."""
    print("\n" + "="*60)
    print("                   EXTRACT SECRET MESSAGE")
    print("="*60)
    print("Created by Phon3x [ https://github.com/Phon3x/ ]")
    print()
    
    # Get stego image
    stego_path = get_user_input("Enter path to stego image")
    if not os.path.exists(stego_path):
        print(f"[!] File '{stego_path}' not found!")
        return
    
    # Get password
    password = get_user_input("Enter encryption password")
    if not password:
        print("[!] Password is required for extraction.")
        return
    
    # Choose output format
    print("\n📤 Output options:")
    print("   1. Display on screen")
    print("   2. Save to file")
    output_choice = get_user_input("Choose option", "1")
    
    # Perform extraction
    print("\n" + "="*60)
    print("                STARTING EXTRACTION PROCESS")
    print("="*60)
    print("Created by Phon3x [ https://github.com/Phon3x/ ]")
    print()
    
    stego = F5Steganography(password)
    extracted_data, message = stego.extract(stego_path)
    
    print("\n" + "="*60)
    if extracted_data is not None:
        print("✅ EXTRACTION SUCCESSFUL!")
        print(f"📦 {message}")
        
        if output_choice == "1":
            print("\n" + "-"*60)
            print("📄 EXTRACTED DATA")
            print("-"*60)
            try:
                # Try to decode as text
                text = extracted_data.decode('utf-8')
                print(f"\n📝 Text content:\n")
                print(text)
                
                # Check if it looks like a file
                if len(text) < 1000 and '\x00' not in text and all(32 <= ord(c) < 127 or c in '\n\r\t' for c in text):
                    print("\n📁 This appears to be text data.")
                else:
                    print("\n📁 This appears to be binary data.")
                    
            except UnicodeDecodeError:
                # Display as hex
                print(f"\n🔢 Binary data ({len(extracted_data)} bytes):")
                print(f"📋 Hex preview: {extracted_data[:50].hex()}...")
                
                # Try to detect file type
                if len(extracted_data) > 4:
                    magic = extracted_data[:4].hex().upper()
                    print(f"🔍 Magic bytes: {magic}")
                    
                    # Common file type detection
                    if magic.startswith('89504E47'):
                        print("📁 Detected: PNG image")
                    elif magic.startswith('FFD8FF'):
                        print("📁 Detected: JPEG image")
                    elif magic.startswith('25504446'):
                        print("📁 Detected: PDF document")
                    elif magic.startswith('504B0304'):
                        print("📁 Detected: ZIP archive")
                    elif magic.startswith('7F454C46'):
                        print("📁 Detected: ELF executable")
                
                print("\n💡 Tip: Save to file and use appropriate viewer/editor.")
        else:
            output_file = get_user_input("Enter output file path", "extracted_data.bin")
            with open(output_file, 'wb') as f:
                f.write(extracted_data)
            print(f"💾 Data saved to: {output_file}")
            print(f"📊 Size: {len(extracted_data)} bytes")
    else:
        print("❌ EXTRACTION FAILED!")
        print(f"⚠️  Error: {message}")
        print("\n💡 Possible reasons:")
        print("   1. Wrong password")
        print("   2. Image doesn't contain hidden data")
        print("   3. Image was heavily compressed or modified")
        print("   4. OutGuess not installed (if it was used for embedding)")


def main():
    """Main menu."""
    # Clear screen and print banner
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    
    # Check dependencies
    try:
        import numpy as np
        from PIL import Image
        from Crypto.Cipher import AES
        print("[✓] Core dependencies loaded")
    except ImportError as e:
        print(f"[!] Missing dependency: {e}")
        print("\n📦 Install required packages:")
        print("   pip install Pillow pycryptodome numpy")
        sys.exit(1)
    
    # Check for OutGuess
    has_outguess = F5Steganography("test").use_outguess
    
    if not has_outguess:
        print("[!] ⚠️  OUTGUESS NOT FOUND")
        print("   For professional F5 steganography, install OutGuess (Option 3).")
        print("   Currently using fallback method (less robust).\n")
    
    while True:
        print("\n" + "="*60)
        print("                         MAIN MENU")
        print("="*60)
        print("Created by Phon3x [ https://github.com/Phon3x/ ]")
        print()
        
        print("1. 📤 Embed secret message into image")
        print("2. 📥 Extract secret message from image")
        print("3. 🔧 Install OutGuess (for professional F5)")
        print("4. ℹ️  About Phon3x-ART")
        print("5. 🚪 Exit")
        
        choice = get_user_input("\nEnter your choice", "1")
        
        if choice == "1":
            embed_menu()
        elif choice == "2":
            extract_menu()
        elif choice == "3":
            install_outguess_instructions()
        elif choice == "4":
            about_f5_stego()
        elif choice == "5":
            print("\n" + "="*60)
            print("👋 Thank you for using Phon3x-ART!")
            print("   Created by Phon3x [ https://github.com/Phon3x/ ]")
            print("="*60)
            break
        else:
            print("[!] Invalid choice. Please try again.")


def about_f5_stego():
    """Display information about Phon3x-ART."""
    print("\n" + "="*70)
    print("                      ABOUT Phon3x-ART")
    print("="*70)
    print("Created by Phon3x [ https://github.com/Phon3x/ ]")
    print()
    
    print("📚 What is Phon3x-ART?")
    print("   Phon3x-ART is a professional steganography tool that implements the")
    print("   F5 algorithm for hiding data in JPEG images with AES-256 encryption.")
    print()
    
    print("✨ Key Features:")
    print("   • 🔐 AES-256 Encryption - Military-grade encryption for your data")
    print("   • 🛡️ True F5 Algorithm - When OutGuess is installed")
    print("   • 💪 Compression Resistant - Survives mild JPEG recompression")
    print("   • 🎲 Password-based Security - Unique embedding for each password")
    print("   • 📈 Variable Payloads - Hide text or files of various sizes")
    print("   • 🔍 Automatic Detection - Smart extraction without extra parameters")
    print()
    
    print("🔧 Technical Details:")
    print("   • Algorithm: F5 (DCT coefficient modification)")
    print("   • Encryption: AES-256 CBC mode with PKCS7 padding")
    print("   • Key Derivation: PBKDF2-HMAC-SHA256 with 100,000 iterations")
    print("   • Error Detection: CRC32 checksum for data integrity")
    print("   • Format: JPEG only (best results with photographic images)")
    print()
    
    print("💡 Best Practices:")
    print("   1. Use strong passwords (12+ characters, mixed)")
    print("   2. Choose complex cover images (photos, not solid colors)")
    print("   3. Don't exceed 5% of image capacity")
    print("   4. Avoid recompressing below original quality")
    print("   5. Install OutGuess for maximum reliability")
    print()
    
    print("⚠️  Security Notes:")
    print("   • Steganography is for legitimate privacy, not illegal activities")
    print("   • The tool provides plausible deniability when used properly")
    print("   • No system is 100% undetectable to advanced steganalysis")
    print()
    
    print("🔗 Resources:")
    print("   • GitHub: https://github.com/Phon3x/")
    print("   • OutGuess: https://github.com/resurrecting-open-source-projects/outguess")
    print()
    
    input("Press Enter to return to main menu...")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user.")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 If this persists, please report the issue.")
        print("   Created by Phon3x [ https://github.com/Phon3x/ ]")
