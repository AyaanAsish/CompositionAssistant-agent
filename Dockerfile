# Dockerfile.api
FROM python:3.11

# Install system dependencies including ca-certificates
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    fluidsynth \
    libasound2-dev \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

WORKDIR /app

# Layer 1: Upgrade pip with trusted hosts (for corporate networks with SSL inspection)
RUN pip install --no-cache-dir --upgrade pip \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org

# Layer 2: Copy and install requirements (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org

# Layer 3: Copy source code (rebuilt on any code change)
COPY src/ ./src/

# Layer 4: Copy SoundFont files into container
COPY transcriptionLibs/FluidR3_GM/ ./FluidR3_GM/

# Layer 5: Create tmp directories
RUN mkdir -p /app/tmp /app/input

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
