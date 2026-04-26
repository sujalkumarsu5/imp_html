import os
import sys
from os import environ

# ═══════════════════════════════════════════════════════════════
#  vars.py — Environment Variable Configuration
#  All sensitive values MUST come from environment variables.
#  Set them in: Heroku Config Vars / Render Env / Koyeb Secrets
# ═══════════════════════════════════════════════════════════════

# ─── Telegram API ─────────────────────────────────────────────
API_ID   = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ─── Owner & Admins ───────────────────────────────────────────
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
_admins_env = os.environ.get("ADMINS", "")
ADMINS = [int(x) for x in _admins_env.split() if x.strip().isdigit()] if _admins_env else ([OWNER_ID] if OWNER_ID else [])

# ─── MongoDB ──────────────────────────────────────────────────
DATABASE_URL  = os.environ.get("DATABASE_URL", "")
# MongoDB database name max 38 bytes — emoji/unicode exceed करते हैं
# Safe ASCII default: RadhaKrishna_db (14 bytes ✓)
DATABASE_NAME = os.environ.get("DATABASE_NAME", "RadhaKrishna_db")
MONGO_URL     = DATABASE_URL  # alias used by db.py

# ─── Bot Config ───────────────────────────────────────────────
CREDIT          = os.environ.get("CREDIT", "𝗞𝗘𝗦𝗔𝗩")
PREMIUM_CHANNEL = os.environ.get("PREMIUM_CHANNEL", "")
THUMBNAILS      = list(map(str, os.environ.get("THUMBNAILS", "").split()))

# ─── Web Server (Render / Koyeb need a bound port) ────────────
PORT       = int(os.environ.get("PORT", 8000))
WEB_SERVER = os.environ.get("WEB_SERVER", "true").lower() == "true"
WEBHOOK    = True

# ─── Auth Messages ────────────────────────────────────────────
AUTH_MESSAGES = {
    "subscription_active": (
        "<b>🎉 Subscription Activated!</b>\n\n"
        "<blockquote>Your subscription has been activated and will expire on {expiry_date}.\n"
        "You can now use the bot!</blockquote>\n\nType /start to start uploading"
    ),
    "subscription_expired": (
        "<b>⚠️ Your Subscription Has Ended</b>\n\n"
        "<blockquote>Your access to the bot has been revoked as your subscription period has expired.\n"
        "Please contact the admin to renew your subscription.</blockquote>"
    ),
    "user_added": (
        "<b>✅ User Added Successfully!</b>\n\n"
        "<blockquote>👤 Name: {name}\n"
        "🆔 User ID: {user_id}\n"
        "📅 Expiry: {expiry_date}</blockquote>"
    ),
    "user_removed": (
        "<b>✅ User Removed Successfully!</b>\n\n"
        "<blockquote>User ID {user_id} has been removed from authorized users.</blockquote>"
    ),
    "access_denied": (
        "<b>⚠️ Access Denied!</b>\n\n"
        "<blockquote>You are not authorized to use this bot.\n"
        "Please contact the admin to get access.</blockquote>"
    ),
    "not_admin":      "⚠️ You are not authorized to use this command!",
    "invalid_format": "❌ <b>Invalid Format!</b>\n\n<blockquote>Use format: {format}</blockquote>",
}

# ─── Startup Validation ───────────────────────────────────────
_missing = []
if not API_ID:       _missing.append("API_ID")
if not API_HASH:     _missing.append("API_HASH")
if not BOT_TOKEN:    _missing.append("BOT_TOKEN")
if not OWNER_ID:     _missing.append("OWNER_ID")
if not DATABASE_URL: _missing.append("DATABASE_URL")

if _missing:
    print(f"❌ MISSING REQUIRED ENV VARS: {', '.join(_missing)}")
    print("   Set them in Heroku Config Vars / Render Env / Koyeb Secrets")
    sys.exit(1)

print(f"✅ Config loaded — Bot Owner: {OWNER_ID} | Admins: {ADMINS}")
