# ============================================================
#   🦚Rᴀᴅʜᴀ♡︎Kʀɪsʜɴᴀ༗🌹 UPLOADER — Colab One-Click Setup
#   Paste each cell in Google Colab and run in order
# ============================================================

# ──────────────────────────────────────────────────────────────
# CELL 1 ─ Extract ZIP
# ──────────────────────────────────────────────────────────────
"""
import zipfile, os

zip_path = '/content/🦚Rᴀᴅʜᴀ♡︎Kʀɪsʜɴᴀ༗🌹_UPLOADER_FAST-V2-modified.zip'
extract_path = '/content/bot_repo'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print('Files extracted to:', extract_path)
%cd {extract_path}
"""

# ──────────────────────────────────────────────────────────────
# CELL 2 ─ Install ALL dependencies in one shot
# ──────────────────────────────────────────────────────────────
"""
import subprocess, sys

# System packages
subprocess.run(['apt-get', 'update', '-q'], check=True)
subprocess.run(['apt-get', 'install', '-y', '-q', 'ffmpeg'], check=True)

# Python packages — single command, no more one-by-one errors
subprocess.run([
    sys.executable, '-m', 'pip', 'install', '-q',
    'pyrogram==2.0.106',
    'pyromod==1.5',
    'tgcrypto',
    'pymongo',
    'motor',
    'certifi',
    'aiohttp',
    'aiofiles',
    'requests',
    'cloudscraper',
    'ffmpeg-python',
    'm3u8',
    'yt-dlp',
    'pytube',
    'pycryptodome',
    'colorama',
    'pillow',
    'pytz',
    'beautifulsoup4',
    'typing_extensions',
], check=True)

print('✅ All dependencies installed successfully!')
"""

# ──────────────────────────────────────────────────────────────
# CELL 3 ─ Set credentials & run bot
# ──────────────────────────────────────────────────────────────
"""
import os, subprocess, sys

os.environ['API_ID']    = 'YOUR_API_ID'       # ← replace
os.environ['API_HASH']  = 'YOUR_API_HASH'     # ← replace
os.environ['BOT_TOKEN'] = 'YOUR_BOT_TOKEN'    # ← replace
os.environ['OWNER_ID']  = 'YOUR_OWNER_ID'     # ← replace

# Write .env file
with open('.env', 'w') as f:
    f.write(f"API_ID={os.environ['API_ID']}\n")
    f.write(f"API_HASH={os.environ['API_HASH']}\n")
    f.write(f"BOT_TOKEN={os.environ['BOT_TOKEN']}\n")
    f.write(f"OWNER_ID={os.environ['OWNER_ID']}\n")

print('✅ Credentials configured.')

# Navigate to bot folder and start
bot_dir = '/content/bot_repo/🦚Rᴀᴅʜᴀ♡︎Kʀɪsʜɴᴀ༗🌹_UPLOADER_FAST-V2-main'
os.chdir(bot_dir)
subprocess.Popen([sys.executable, 'main.py'])
print('✅ Bot started!')
"""
