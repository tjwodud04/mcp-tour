"""Async HTTP client for the Korea Tourism Organization Open API.

This module isolates all HTTP concerns (SSL configuration, request building,
error handling) so the MCP tool layer in :mod:`mcp_tour.server` stays thin.
"""

from __future__ import annotations

import ssl
import sys
from typing import Any, Optional

import httpx

from mcp_tour import config


def _build_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that tolerates the TourAPI's legacy ciphers."""
    context = ssl.create_default_context()
    context.set_ciphers(config.SSL_CIPHER_SECLEVEL)
    return context


class TourApiClient:
    """Typed wrapper around the Korea Tourism Organization API endpoints.

    The client owns the shared SSL context, the API service key, and the
    request timeout, keeping every HTTP detail out of the tool definitions.
    """

    def __init__(
        self,
        service_key: str,
        timeout: float = config.REQUEST_TIMEOUT_SECONDS,
    ) -> None:
        self._service_key = service_key
        self._timeout = timeout
        self._ssl_context = _build_ssl_context()

    async def _get(self, url: str, params: dict[str, Any]) -> str:
        """Send a GET request with the service key injected and return the body.

        Errors are logged to stderr and re-raised so the MCP host can surface
        them to the user.
        """
        request_params = {"serviceKey": self._service_key, **params}
        async with httpx.AsyncClient(verify=self._ssl_context) as client:
            try:
                response = await client.get(
                    url, params=request_params, timeout=self._timeout
                )
                response.raise_for_status()
                return response.text
            except Exception as exc:
                print(f"TourAPI request to {url} failed: {exc}", file=sys.stderr)
                raise

    def _related_base_params(
        self,
        area_code: str,
        signgu_code: str,
        content_type_id: Optional[str],
        size: int,
    ) -> dict[str, Any]:
        """Build the parameters shared by the related-spots endpoints."""
        params: dict[str, Any] = {
            "numOfRows": min(size, config.MAX_AREA_BASED_ROWS),
            "pageNo": config.DEFAULT_PAGE_NO,
            "MobileOS": config.MOBILE_OS,
            "MobileApp": config.MOBILE_APP,
            "baseYm": config.current_base_ym(),
            "areaCd": area_code,
            "signguCd": signgu_code,
            "_type": config.RESPONSE_TYPE_JSON,
        }
        if content_type_id:
            params["contentTypeId"] = content_type_id
        return params

    async def area_based_list(
        self,
        area_code: str,
        signgu_code: str,
        content_type_id: Optional[str] = None,
        size: int = config.DEFAULT_AREA_BASED_SIZE,
    ) -> str:
        """Fetch area-based related tourist spots."""
        url = f"{config.RELATED_TOUR_API_BASE_URL}/{config.AREA_BASED_LIST_PATH}"
        params = self._related_base_params(
            area_code, signgu_code, content_type_id, size
        )
        return await self._get(url, params)

    async def search_by_keyword(
        self,
        keyword: str,
        area_code: str,
        signgu_code: str,
        content_type_id: Optional[str] = None,
        size: int = config.DEFAULT_AREA_BASED_SIZE,
    ) -> str:
        """Search related tourist spots by keyword."""
        url = f"{config.RELATED_TOUR_API_BASE_URL}/{config.SEARCH_KEYWORD_PATH}"
        params = self._related_base_params(
            area_code, signgu_code, content_type_id, size
        )
        params["keyword"] = keyword
        return await self._get(url, params)

    async def standard_tour_list(
        self,
        page_no: int = config.DEFAULT_STANDARD_PAGE_NO,
        num_of_rows: int = config.DEFAULT_STANDARD_ROWS,
        tourist_spot_name: Optional[str] = None,
        address: Optional[str] = None,
    ) -> str:
        """Fetch tourist spots from the National Standard Tourism Data API."""
        params: dict[str, Any] = {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "type": config.RESPONSE_TYPE_JSON,
        }
        if tourist_spot_name:
            params["trrsrtNm"] = tourist_spot_name
        if address:
            params["rdnmadr"] = address
        return await self._get(config.STANDARD_TOUR_API_URL, params)
