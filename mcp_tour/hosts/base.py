"""Shared helpers for installing the MCP server into MCP host applications.

Both :mod:`mcp_tour.hosts.claude_desktop` and :mod:`mcp_tour.hosts.cursor`
generate the same ``uv run`` launch command and write an ``mcpServers`` entry
into a JSON config file; the only differences are the config location and file
name, so the common logic lives here.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Callable, Optional

from mcp_tour import config

# Base packages every host launch command needs, on top of the server's
# declared runtime dependencies.
_BASE_PACKAGES = {"fastmcp", "mcp-tour"}


def get_claude_desktop_config_path() -> Optional[Path]:
    """Return the Claude Desktop config directory for the current platform.

    Returns ``None`` if the directory does not exist, which indicates Claude
    Desktop is not installed or has never been run.
    """
    if sys.platform == "win32":
        config_dir = Path(Path.home(), "AppData", "Roaming", "Claude")
    elif sys.platform == "darwin":
        config_dir = Path(Path.home(), "Library", "Application Support", "Claude")
    elif sys.platform.startswith("linux"):
        config_dir = Path(
            os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"), "Claude"
        )
    else:
        return None
    return config_dir if config_dir.exists() else None


def get_cursor_config_path() -> Optional[Path]:
    """Return the Cursor config directory, or ``None`` if it does not exist."""
    path = Path(Path.home(), ".cursor")
    return path if path.exists() else None


def _build_launch_args() -> list[str]:
    """Build the ``uv run`` arguments that launch the MCP server."""
    packages = _BASE_PACKAGES | set(config.SERVER_RUNTIME_PACKAGES)
    args = ["run"]
    for package in sorted(packages):
        args.extend(["--with", package])
    args.extend(["python", "-m", "mcp_tour.server"])
    return args


def parse_env_vars(env_vars: Optional[list[str]]) -> Optional[dict[str, str]]:
    """Parse ``KEY=VALUE`` strings into a dictionary (``None`` if empty)."""
    if not env_vars:
        return None
    parsed: dict[str, str] = {}
    for env_var in env_vars:
        key, value = env_var.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def update_host_config(
    config_dir: Path,
    config_filename: str,
    server_name: str,
    env_vars: Optional[dict[str, str]] = None,
) -> None:
    """Write or update the MCP server entry in a host's JSON config file.

    Any environment variables already stored for the server are preserved and
    merged with ``env_vars`` (new values take precedence).
    """
    config_file = config_dir / config_filename
    if not config_file.exists():
        config_file.write_text("{}")

    data = json.loads(config_file.read_text())
    servers = data.setdefault("mcpServers", {})

    existing_env = servers.get(server_name, {}).get("env")
    if existing_env:
        env_vars = {**existing_env, **(env_vars or {})}

    server_config: dict[str, object] = {
        "command": "uv",
        "args": _build_launch_args(),
    }
    if env_vars:
        server_config["env"] = env_vars

    servers[server_name] = server_config
    config_file.write_text(json.dumps(data, indent=2))


def install_server(
    host_name: str,
    config_path_getter: Callable[[], Optional[Path]],
    config_filename: str,
    env_vars: Optional[list[str]] = None,
) -> None:
    """Install the MCP server into a host application's configuration.

    Args:
        host_name: Human-readable host name used in error messages.
        config_path_getter: Callable returning the host's config directory.
        config_filename: Name of the host's JSON config file.
        env_vars: Optional ``KEY=VALUE`` strings to store for the server.
    """
    config_dir = config_path_getter()
    if config_dir is None:
        print(
            f"{host_name} configuration directory not found. Ensure {host_name} "
            "is installed and has been run at least once.",
            file=sys.stderr,
        )
        sys.exit(1)

    update_host_config(
        config_dir=config_dir,
        config_filename=config_filename,
        server_name=config.SERVER_NAME,
        env_vars=parse_env_vars(env_vars),
    )
