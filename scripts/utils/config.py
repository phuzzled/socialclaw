"""
SocialSwag Configuration Module.

Handles API key management, environment variables, and configuration.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path


CONFIG_DIR = Path.home() / ".socialswag"
API_KEY_FILE = CONFIG_DIR / "api_key"

# Default configuration values
DEFAULTS = {
    "api_base_url": "https://api.x.com/2",
    "timeout": 30.0,
    "max_results": 100,
}


def get_api_key() -> Optional[str]:
    """
    Get X API Bearer Token.

    Checks in order:
    1. X_API_BEARER_TOKEN environment variable (preferred)
    2. TWITTER_BEARER_TOKEN environment variable (legacy fallback)
    3. ~/.socialswag/api_key file

    Returns:
        Bearer token string or None
    """
    key = (
        os.environ.get("X_API_BEARER_TOKEN") or
        os.environ.get("TWITTER_BEARER_TOKEN")
    )
    if key:
        return key

    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text().strip()
        if key:
            return key

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
        "api_base_url": os.environ.get("X_API_BASE_URL", DEFAULTS["api_base_url"]),
        "api_key_set": bool(get_api_key()),
        "openai_key_set": bool(get_openai_key()),
        "openrouter_key_set": bool(get_openrouter_key()),
        "openrouter_model": get_openrouter_model(),
        "google_key_set": bool(get_gemini_key()),
        "timeout": float(os.environ.get("X_TIMEOUT", DEFAULTS["timeout"])),
        "max_results": int(os.environ.get("X_MAX_RESULTS", DEFAULTS["max_results"])),
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

    if not get_api_key():
        errors.append(
            "No X API Bearer Token found. "
            "Set X_API_BEARER_TOKEN environment variable "
            "or save your token to ~/.socialswag/api_key. "
            "Get yours at https://developer.x.com/"
        )

    api_url = os.environ.get("X_API_BASE_URL", DEFAULTS["api_base_url"])
    if not api_url.startswith(("http://", "https://")):
        errors.append("Invalid X_API_BASE_URL format")

    if os.environ.get("X_API_BASE_URL"):
        warnings.append("Using custom X API base URL (not default)")

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
