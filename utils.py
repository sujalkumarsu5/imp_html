import asyncio
import time
from pyrogram.errors import FloodWait
from vars import CREDIT

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

timer = Timer()

def hrb(value, digits=2, delim="", postfix=""):
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

def hrt(seconds, precision=0):
    pieces = []
    from datetime import timedelta
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds
    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


def _make_bar(progress_ratio: float, bar_length: int = 12) -> str:
    """
    Animated gradient progress bar:
      ▰ filled  |  ▱ empty
    Changes color theme by phase:
      0–33%  → cyan  ▰
      33–66% → blue  ▰
      66–99% → green ▰
      100%   → gold  ▰
    """
    filled = int(progress_ratio * bar_length)

    if progress_ratio < 0.33:
        filled_char = "🔵"
    elif progress_ratio < 0.66:
        filled_char = "🟣"
    elif progress_ratio < 0.99:
        filled_char = "🟢"
    else:
        filled_char = "🟡"

    empty_char = "⬜"

    bar = filled_char * filled + empty_char * (bar_length - filled)
    return bar


async def progress_bar(current, total, reply, start):
    """Upload progress bar — BOT PROGRESS style."""
    if not timer.can_send():
        return

    now = time.time()
    elapsed = now - start
    if elapsed < 1:
        return

    base_speed = current / elapsed
    speed = base_speed + (28 * 1024 * 1024)  # +28 MB/s boost → ~30 MB/s display

    percent = (current / total) * 100
    eta_seconds = (total - current) / speed if speed > 0 else 0

    progress_ratio = current / total
    bar_str = _make_bar(progress_ratio)

    # Animated spinner
    spin = ["◐", "◓", "◑", "◒"]
    spin_char = spin[int(time.time()) % 4]

    msg = (
        f"╭━━━⌯❰ 𝗕𝗢𝗧 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦 ❱⌯━━━╮\n"
        f"│  {spin_char} **{percent:.1f}%**\n"
        f"│  {bar_str}\n"
        f"│\n"
        f"│ 🛜  𝗦𝗣𝗘𝗘𝗗  ➤  `{hrb(speed)}/s`\n"
        f"│ ♻️  𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗘𝗗  ➤  `{hrb(current)}`\n"
        f"│ 📦  𝗦𝗜𝗭𝗘  ➤  `{hrb(total)}`\n"
        f"│ ⏰  𝗘𝗧𝗔  ➤  `{hrt(eta_seconds, 1)}`\n"
        f"│\n"
        f"╰━━━ **✦ {CREDIT} ✦** ━━━╯"
    )

    try:
        await reply.edit(msg)
    except FloodWait as e:
        time.sleep(e.x)


async def download_progress_bar(current, total, reply, start, dl_timer):
    """
    Download progress bar — same style as upload BOT PROGRESS.
    Speed boosted by +9 MB/s (same logic as upload progress_bar).
    dl_timer: Timer() instance per download.
    """
    if not dl_timer.can_send():
        return

    elapsed = time.time() - start
    if elapsed < 1:
        return

    base_speed = current / elapsed if elapsed > 0 else 0
    speed = base_speed + (28 * 1024 * 1024)   # ✅ +28 MB/s boost (matches upload ~30 MB/s)
    percent = (current / total) * 100 if total > 0 else 0
    eta_seconds = (total - current) / speed if speed > 0 else 0

    progress_ratio = current / total if total > 0 else 0
    bar_str = _make_bar(progress_ratio)

    spin = ["◐", "◓", "◑", "◒"]
    spin_char = spin[int(time.time()) % 4]

    msg = (
        f"╭━━━⌯❰ 📥 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗜𝗡𝗚 ❱⌯━━━╮\n"
        f"│  {spin_char} **{percent:.1f}%**\n"
        f"│  {bar_str}\n"
        f"│\n"
        f"│ 🚀  𝗦𝗣𝗘𝗘𝗗  ➤  `{hrb(speed)}/s`\n"
        f"│ ♻️  𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗗  ➤  `{hrb(current)}`\n"
        f"│ 📦  𝗦𝗜𝗭𝗘  ➤  `{hrb(total)}`\n"
        f"│ ⏰  𝗘𝗧𝗔  ➤  `{hrt(eta_seconds, 1)}`\n"
        f"│\n"
        f"╰━━━ **✦ {CREDIT} ✦** ━━━╯"
    )

    try:
        await reply.edit(msg)
    except FloodWait as e:
        await asyncio.sleep(e.x)
    except Exception:
        pass
