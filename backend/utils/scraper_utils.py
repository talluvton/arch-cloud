from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from fastapi import HTTPException
import logging
import re

from utils.constants import DEFAULT_GH_PER_PAGE, MAX_GH_PER_PAGE

logger = logging.getLogger(__name__)

def assert_valid_url(url: str) -> None:
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail="Input must be a valid HTTP/HTTPS URL")


def ensure_per_page(api_url: str) -> str:
    """
    Ensure a reasonable per_page for GitHub search URLs.
    - Requires q=
    - Adds per_page if missing
    - Clamps per_page to MAX_GH_PER_PAGE
    """
    parsed_url = urlparse(api_url)
    query_str = dict(parse_qsl(parsed_url.query, keep_blank_values=True))

    if "q" not in query_str or not query_str["q"].strip():
        raise HTTPException(status_code=400, detail="GitHub search URL must include a non-empty 'q=' parameter")

    if "per_page" in query_str:
        try:
            n = int(query_str["per_page"])
        except ValueError:
            n = DEFAULT_GH_PER_PAGE
        query_str["per_page"] = str(max(1, min(MAX_GH_PER_PAGE, n)))
    else:
        query_str["per_page"] = str(DEFAULT_GH_PER_PAGE)

    final = urlunparse(parsed_url._replace(query=urlencode(query_str, doseq=True)))
    logger.info("[scraper] GitHub API URL -> %s", final)
    return final


def to_raw_url(html_url: str) -> str:
    # convert 'github.com/.../blob/...' -> 'raw.githubusercontent.com/.../...'
    return html_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()