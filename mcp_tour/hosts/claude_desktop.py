"""Install the Korea Tourism MCP server into Claude Desktop's configuration."""

from __future__ import annotations

from mcp_tour.hosts import base

CLAUDE_DESKTOP_CONFIG_FILENAME = "claude_desktop_config.json"


def install_to_claude_desktop(env_vars: list[str] | None = None) -> None:
    """Add or update the MCP server entry in Claude Desktop's config file.

    Args:
        env_vars: Optional ``KEY=VALUE`` strings (e.g. ``TOUR_API_KEY=...``)
            to store for the server in the generated config.
    """
    base.install_server(
        host_name="Claude Desktop",
        config_path_getter=base.get_claude_desktop_config_path,
        config_filename=CLAUDE_DESKTOP_CONFIG_FILENAME,
        env_vars=env_vars,
    )


def _main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Install the MCP server into Claude Desktop.")
    parser.add_argument(
        "--env",
        "-e",
        action="append",
        help="Environment variable to set for the server (KEY=VALUE).",
    )
    args = parser.parse_args()
    install_to_claude_desktop(env_vars=args.env)


if __name__ == "__main__":
    _main()
