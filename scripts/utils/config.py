"""
SocialSwag Configuration Module.

Handles API key management, environment variables, and configuration.
Supports loading from .env file.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path


CONFIG_DIR = Path.home() / ".socialswag"
API_KEY_FILE = CONFIG_DIR / "api_key"

# Default configuration values
DEFAULTS = {
    "bsky_base_url": "https://api.bsky.app",
    "timeout": 30.0,
    "max_results": 100,
    "default_model": "x-ai/grok-4.20-beta",
}


def _load_env_file() -> None:
    """Load environment variables from .env file if it exists."""
    # Look for .env in multiple locations (in order of preference)
    env_paths = [
        Path.cwd() / ".env",  # Current working directory
        Path(__file__).parent.parent.parent / ".env",  # Project root (relative to this file)
        Path.home() / ".socialswag" / ".env",  # ~/.socialswag/.env
        Path.home() / "socialswag" / ".env",  # ~/socialswag/.env (legacy)
    ]

    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        if key and value and not os.environ.get(key):
                            os.environ[key] = value
            break  # Stop after first .env file found


# Load .env file on module import
_load_env_file()


def get_bluesky_credentials() -> Optional[tuple]:
    """
    Get Bluesky credentials (handle and app password).

    Checks in order:
    1. BLUESKY_HANDLE and BLUESKY_APP_PASSWORD environment variables

    Returns:
        Tuple of (handle, app_password) or None
    """
    handle = os.environ.get("BLUESKY_HANDLE")
    app_password = os.environ.get("BLUESKY_APP_PASSWORD")

    if handle and app_password:
        return (handle, app_password)

    return None


def get_openai_key() -> Optional[str]:
    """Get OpenAI API key for optional AI analysis features."""
    return os.environ.get("OPENAI_API_KEY")


def get_openrouter_key() -> Optional[str]:
    """Get OpenRouter API key for AI analysis via OpenRouter."""
    return os.environ.get("OPENROUTER_API_KEY")


def get_openrouter_model() -> str:
    """Get OpenRouter model to use. Default is x-ai/grok-4.20-beta."""
    return os.environ.get("OPENROUTER_MODEL", "x-ai/grok-4.20-beta")


def get_gemini_key() -> Optional[str]:
    """Get Google/Gemini API key for Nano Banana 2 image generation."""
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


def get_config() -> Dict[str, Any]:
    """
    Get current configuration from environment and defaults.

    Returns:
        Configuration dictionary
    """
    return {
        "bsky_base_url": os.environ.get("BSKY_BASE_URL", DEFAULTS["bsky_base_url"]),
        "bluesky_creds_set": bool(get_bluesky_credentials()),
        "openai_key_set": bool(get_openai_key()),
        "openrouter_key_set": bool(get_openrouter_key()),
        "openrouter_model": get_openrouter_model(),
        "google_key_set": bool(get_gemini_key()),
        "timeout": float(os.environ.get("BSKY_TIMEOUT", DEFAULTS["timeout"])),
        "max_results": int(os.environ.get("BSKY_MAX_RESULTS", DEFAULTS["max_results"])),
    }


def validate_config() -> Dict[str, Any]:
    """
    Validate configuration and return status.

    Returns:
        Dict with validation results:
        {
            "valid": bool,
            "errors": list of error strings,
            "warnings": list of warning strings,
        }
    """
    errors = []
    warnings = []

    # Bluesky can work without auth for public data, but some features need it
    if not get_bluesky_credentials():
        warnings.append(
            "No Bluesky credentials found. Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD "
            "for full access. Public data is still accessible without credentials."
        )

    if get_openai_key():
        warnings.append("OpenAI API key found — AI analysis features enabled")

    if get_openrouter_key():
        model = get_openrouter_model()
        warnings.append(f"OpenRouter API key found — Using {model} for AI analysis")

    if get_gemini_key():
        warnings.append("Google API key found — Nano Banana 2 image generation enabled")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
