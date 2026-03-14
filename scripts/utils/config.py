"""
BlockRun Configuration Module.

Handles configuration management, environment variables, and presets.
"""

import json
import os
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path


# Legacy BlockRun wallet location
WALLET_DIR = Path.home() / ".blockrun"
WALLET_FILE = WALLET_DIR / ".session"
SOLANA_WALLET_FILE = WALLET_DIR / ".solana-session"


# Default configuration values
DEFAULTS = {
    "api_url": "https://blockrun.ai/api",
    "default_model": "openai/gpt-5.2",
    "default_image_model": "google/nano-banana",
    "max_tokens": 1024,
    "timeout": 60.0,
    "image_timeout": 120.0,
}


CHAIN_FILE = WALLET_DIR / ".chain"


def get_chain() -> str:
    """
    Get selected chain preference.

    Returns:
        "base" or "solana" (default: "base")
    """
    if CHAIN_FILE.exists():
        chain = CHAIN_FILE.read_text().strip().lower()
        if chain in ("base", "solana"):
            return chain
    return "base"


def _scan_wallet_files(filename: str) -> List[Tuple[str, str, Path]]:
    """
    Scan all ~/.<dir>/<filename> for wallet JSON files.

    Returns:
        List of (privateKey, address, path) sorted by mtime (newest first).
    """
    home = Path.home()
    results = []

    for entry in home.iterdir():
        if not entry.name.startswith(".") or not entry.is_dir():
            continue
        wallet_file = entry / filename
        if not wallet_file.is_file():
            continue
        try:
            data = json.loads(wallet_file.read_text())
            key = data.get("privateKey", "").strip()
            addr = data.get("address", "").strip()
            if key and addr:
                results.append((key, addr, wallet_file))
        except (json.JSONDecodeError, OSError):
            continue

    results.sort(key=lambda r: r[2].stat().st_mtime, reverse=True)
    return results


def scan_wallets() -> List[Tuple[str, str, Path]]:
    """Scan for EVM wallet.json files across all ~/.<provider>/ dirs."""
    return _scan_wallet_files("wallet.json")


def scan_solana_wallets() -> List[Tuple[str, str, Path]]:
    """Scan for solana-wallet.json files across all ~/.<provider>/ dirs."""
    return _scan_wallet_files("solana-wallet.json")


def get_private_key() -> Optional[str]:
    """
    Get private key based on selected chain.

    For base:  scan ~/.*/wallet.json → legacy ~/.blockrun/.session → env vars
    For solana: scan ~/.*/solana-wallet.json → legacy ~/.blockrun/.solana-session → env vars

    Returns:
        Private key string or None
    """
    chain = get_chain()

    if chain == "solana":
        # Scan solana-wallet.json files
        wallets = scan_solana_wallets()
        if wallets:
            return wallets[0][0]

        # Legacy solana session
        if SOLANA_WALLET_FILE.exists():
            key = SOLANA_WALLET_FILE.read_text().strip()
            if key:
                return key

        return os.environ.get("SOLANA_WALLET_KEY")

    else:  # base
        # Scan wallet.json files
        wallets = scan_wallets()
        if wallets:
            return wallets[0][0]

        # Legacy base session
        if WALLET_FILE.exists():
            key = WALLET_FILE.read_text().strip()
            if key:
                return key

        # Legacy wallet.key
        legacy_file = WALLET_DIR / "wallet.key"
        if legacy_file.exists():
            key = legacy_file.read_text().strip()
            if key:
                return key

        return (
            os.environ.get("BLOCKRUN_WALLET_KEY") or
            os.environ.get("BASE_CHAIN_WALLET_KEY")
        )


def get_wallet_source() -> Optional[Dict[str, str]]:
    """
    Get info about which wallet is being used.

    Returns:
        Dict with chain, address, source path, or None if no wallet found.
    """
    chain = get_chain()

    if chain == "solana":
        wallets = scan_solana_wallets()
        if wallets:
            return {"chain": "solana", "address": wallets[0][1], "source": str(wallets[0][2])}
    else:
        wallets = scan_wallets()
        if wallets:
            return {"chain": "base", "address": wallets[0][1], "source": str(wallets[0][2])}

    return None


def get_config() -> Dict[str, Any]:
    """
    Get current configuration from environment and defaults.

    Returns:
        Configuration dictionary
    """
    return {
        "api_url": os.environ.get("BLOCKRUN_API_URL", DEFAULTS["api_url"]),
        "wallet_key_set": bool(get_private_key()),
        "default_model": os.environ.get("BLOCKRUN_DEFAULT_MODEL", DEFAULTS["default_model"]),
        "default_image_model": os.environ.get("BLOCKRUN_IMAGE_MODEL", DEFAULTS["default_image_model"]),
        "max_tokens": int(os.environ.get("BLOCKRUN_MAX_TOKENS", DEFAULTS["max_tokens"])),
        "timeout": float(os.environ.get("BLOCKRUN_TIMEOUT", DEFAULTS["timeout"])),
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

    # Check for wallet key
    chain = get_chain()
    if not get_private_key():
        if chain == "solana":
            errors.append("No Solana wallet found (looking for ~/.*/solana-wallet.json or SOLANA_WALLET_KEY)")
        else:
            errors.append("No Base wallet found (looking for ~/.*/wallet.json or BLOCKRUN_WALLET_KEY)")

    # Show which wallet is being used
    source = get_wallet_source()
    if source:
        warnings.append(f"Using {source['chain']} wallet from {source['source']}")

    # Check API URL format
    api_url = os.environ.get("BLOCKRUN_API_URL", DEFAULTS["api_url"])
    if not api_url.startswith(("http://", "https://")):
        errors.append("Invalid BLOCKRUN_API_URL format")

    # Warnings for non-default settings
    if os.environ.get("BLOCKRUN_API_URL"):
        warnings.append("Using custom API URL (not default)")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def get_presets_dir() -> Path:
    """Get path to presets directory."""
    return Path(__file__).parent.parent.parent / "configs" / "presets"


def list_presets() -> list:
    """
    List available configuration presets.

    Returns:
        List of preset names
    """
    presets_dir = get_presets_dir()
    if not presets_dir.exists():
        return []

    return [
        f.stem for f in presets_dir.glob("*.json")
    ]
