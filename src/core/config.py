"""
Configuration settings loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from .env file (look in project root)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Ollama settings
OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY", "")  # Optional for cloud

# Audio Processing settings
SOUNDFONT_PATH: str = os.getenv("SOUNDFONT_PATH", "/app/FluidR3_GM/FluidR3_GM.sf2")

# Server settings
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
UI_PORT: int = int(os.getenv("UI_PORT", "3000"))

# Logging
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TMP_INPUT_PATH: str = os.getenv("TMP_INPUT_PATH", str(PROJECT_ROOT / "tmp" / "input"))
TMP_OUTPUT_PATH: str = os.getenv("TMP_OUTPUT_PATH", str(PROJECT_ROOT / "tmp" / "output"))


def validate_config() -> dict[str, bool]:
    """Validate that required configuration is present."""
    return {
        "ollama_host": bool(OLLAMA_HOST),
        "ollama_model": bool(OLLAMA_MODEL),
        "soundfont_path": bool(SOUNDFONT_PATH) and Path(SOUNDFONT_PATH).exists() if SOUNDFONT_PATH.startswith("/") else True,
    }


def get_config_summary() -> dict:
    """Get a summary of current configuration."""
    return {
        "ollama": {
            "host": OLLAMA_HOST,
            "model": OLLAMA_MODEL,
            "has_api_key": bool(OLLAMA_API_KEY),
        },
        "audio": {
            "soundfont_path": SOUNDFONT_PATH,
        },
        "server": {
            "api_host": API_HOST,
            "api_port": API_PORT,
            "ui_port": UI_PORT,
        },
        "logging": {
            "level": LOG_LEVEL,
        },
    }
