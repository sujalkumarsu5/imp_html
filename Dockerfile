# ═══════════════════════════════════════════════════════════════
#  🦚Rᴀᴅʜᴀ♡︎Kʀɪsʜɴᴀ༗🌹 UPLOADER — RAM-Optimized Dockerfile
#  Compatible: Heroku, Render (Free 512MB), Koyeb
# ═══════════════════════════════════════════════════════════════

FROM python:3.11-slim-bookworm

# ─── Working Dir ──────────────────────────────────────────────
WORKDIR /app

# ─── System Packages (minimal — only what's needed) ───────────
# gcc/g++/cmake/make only for Bento4 build, removed after build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ cmake make \
    libffi-dev \
    ffmpeg \
    aria2 \
    wget curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ─── Bento4 mp4decrypt (DRM support) ─────────────────────────
RUN wget -q https://github.com/axiomatic-systems/Bento4/archive/refs/tags/v1.6.0-639.zip \
    && unzip -q v1.6.0-639.zip \
    && cd Bento4-1.6.0-639 \
    && mkdir cmakebuild && cd cmakebuild \
    && cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    && make -j$(nproc) mp4decrypt \
    && cp mp4decrypt /usr/local/bin/ \
    && cd /app && rm -rf Bento4-1.6.0-639 v1.6.0-639.zip \
    # Remove build tools after compile to save image size
    && apt-get purge -y --auto-remove gcc g++ cmake make

# ─── Python Dependencies ──────────────────────────────────────
COPY itsgolubots.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r itsgolubots.txt \
    # Clean pip cache to reduce container size
    && pip cache purge

# ─── App Source ───────────────────────────────────────────────
COPY . .

# ─── Aria2 Config (optimized for 512MB RAM) ───────────────────
# Connections reduced: 16→8 per server, splits 16→8
# file-allocation=none : skip pre-alloc (saves RAM on startup)
# max-concurrent-downloads=5 : less parallel = less RAM
RUN mkdir -p /etc/aria2 && printf \
"disable-ipv6=true\nfile-allocation=none\noptimize-concurrent-downloads=true\nmax-concurrent-downloads=5\nmax-connection-per-server=8\nsplit=8\nmin-split-size=1M\ncontinue=true\ncheck-integrity=false\n" \
> /etc/aria2/aria2.conf

# ─── /tmp Downloads dir (tmpfs = OS manages, no RAM waste) ────
RUN mkdir -p /tmp/downloads

# ─── Port (Render/Koyeb need a bound port for health check) ───
ENV PORT=8000

# ─── Python memory optimizations ──────────────────────────────
# MALLOC_ARENA_MAX=2  : glibc malloc arenas limit → less fragmentation
# PYTHONMALLOC=malloc : use system malloc (more predictable on low RAM)
# PYTHONDONTWRITEBYTECODE=1 : no .pyc files → saves disk/RAM
# PYTHONUNBUFFERED=1  : immediate stdout/stderr flush
ENV MALLOC_ARENA_MAX=2 \
    PYTHONMALLOC=malloc \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ─── Startup ──────────────────────────────────────────────────
# gunicorn: 1 worker, 1 thread (Flask keep-alive only, minimal RAM)
# aria2c: daemon with config file
CMD aria2c --enable-rpc --rpc-listen-all --daemon=true --conf-path=/etc/aria2/aria2.conf \
    && gunicorn --bind 0.0.0.0:${PORT} \
       --workers 1 --threads 1 --timeout 120 app:app \
       --daemon \
    && python3 main.py
