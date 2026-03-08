FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    fluidsynth \
    libasound2-dev \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY src/ ./src/

COPY transcriptionLibs/FluidR3_GM/ ./FluidR3_GM/

RUN mkdir -p /app/tmp/input /app/tmp/output

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]