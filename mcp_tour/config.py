"""Configuration and constants for the Korea Tourism MCP server.

Every externally tunable value (API endpoints, request defaults, and the name
of the environment variable holding the API key) is defined here so the rest of
the package is free of hardcoded literals.
"""

from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv

# Load variables from a local ``.env`` file if one exists. Calling this on
# import is safe: it only augments ``os.environ`` and never overrides values
# that are already set.
load_dotenv()

# --- MCP server identity -------------------------------------------------
SERVER_NAME = "Korea Tourism API"
SERVER_INSTRUCTIONS = "Access Korea Tourism Organization's tourism data API"

# --- Credentials ---------------------------------------------------------
API_KEY_ENV_VAR = "TOUR_API_KEY"

# --- API endpoints -------------------------------------------------------
# "Related tourist spots" service (TarRlteTarService).
RELATED_TOUR_API_BASE_URL = "https://apis.data.go.kr/B551011/TarRlteTarService"
AREA_BASED_LIST_PATH = "areaBasedList"
SEARCH_KEYWORD_PATH = "searchKeyword"

# National Standard Tourism Data service.
STANDARD_TOUR_API_URL = "https://api.data.go.kr/openapi/tn_pubr_public_trrsrt_api"

# --- Request defaults ----------------------------------------------------
MOBILE_OS = "ETC"
MOBILE_APP = "mcp-tour"
RESPONSE_TYPE_JSON = "json"
BASE_YM_FORMAT = "%Y%m"

DEFAULT_PAGE_NO = 1
MAX_AREA_BASED_ROWS = 50
DEFAULT_AREA_BASED_SIZE = 50
DEFAULT_STANDARD_PAGE_NO = 1
DEFAULT_STANDARD_ROWS = 100

REQUEST_TIMEOUT_SECONDS = 30.0

# The data.go.kr endpoints negotiate legacy TLS ciphers, so the OpenSSL
# security level has to be lowered for the handshake to succeed.
SSL_CIPHER_SECLEVEL = "DEFAULT@SECLEVEL=1"

# Packages injected via ``uv run --with ...`` when generating host configs.
SERVER_RUNTIME_PACKAGES = ("httpx", "python-dotenv", "pydantic")


def get_api_key() -> str:
    """Return the TourAPI service key from the environment.

    Raises:
        ValueError: If the API key environment variable is not set.
    """
    api_key = os.environ.get(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"{API_KEY_ENV_VAR} environment variable is not set")
    return api_key


def current_base_ym() -> str:
    """Return the current year-month (``YYYYMM``) for the TourAPI ``baseYm``."""
    return datetime.now().strftime(BASE_YM_FORMAT)
