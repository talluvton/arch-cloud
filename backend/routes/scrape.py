import logging
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
from fastapi import APIRouter, HTTPException

from scrapers.github_api_and_html_scraper import scrape_url
from services.ai_parser import enrich_with_ai
from services.normalize import (
    normalize_services,
    normalize_flows,
    normalize_providers,
    normalize_features,
)
from models.architecture import Architecture, ScrapeReq
from db import upsert_architecture

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scrape", tags=["Scrape"])


def infer_provider_from_url(url: str) -> Optional[str]:
    try:
        host = urlparse(url).netloc.lower()
        path = urlparse(url).path.lower()
    except Exception:
        return None
    if "aws.amazon.com" in host:
        return "AWS"
    if "cloud.google.com" in host or "/google-cloud/" in path or "/gcp/" in path:
        return "GCP"
    if "azure" in host or "/azure/" in path:
        return "Azure"
    return None


def build_arch(raw: Dict[str, Any], parsed: Dict[str, Any]) -> Architecture:
    """
    Compose the final Architecture from raw scraped doc + AI parse,
    applying all normalizers and URL fallback for provider.
    """
    providers = normalize_providers(parsed.get("providers"))
    provider: Optional[str]
    if len(providers) == 1:
        provider = providers[0]
    elif len(providers) > 1:
        provider = "Multi"
    else:
        provider = infer_provider_from_url(raw.get("source", "") or "")

    services = normalize_services(parsed.get("services", []))
    flows = normalize_flows(parsed.get("flow", []))
    features = normalize_features(parsed.get("features", []))

    return Architecture(
        title=raw.get("title") or "Untitled Architecture",
        source=raw.get("source"),
        provider=provider,
        services=services,
        flow=flows,
        features=features,
    )


@router.post("/", response_model=List[Architecture], response_model_by_alias=False)
def scrape_endpoint(body: ScrapeReq):
    raws = scrape_url(body.url) 
    if not raws:
        raise HTTPException(status_code=404, detail="No results for url")

    architectures_list: List[Architecture] = []
    for raw in raws:
        parsed = enrich_with_ai(raw["text"], raw["tokens"])
        arch = build_arch(raw, parsed)
        saved = upsert_architecture(arch)  
        architectures_list.append(Architecture.model_validate(saved))

    logger.info("/scrape stored %d item(s) for url=%r", len(architectures_list), body.url)
    return architectures_list
