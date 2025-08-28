import json
import re 
import logging
from typing import List, Dict, Any
from fastapi import HTTPException
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from settings import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = """
You extract cloud architecture facts.

Return ONLY valid JSON with keys:
- providers: array of "AWS" | "Azure" | "GCP"
- services: array of {name, role}; role ∈ {Compute, Storage, Database, Networking, Security, Monitoring, Integration, Analytics, DevOps, Other}
- flow: array of "A -> B -> C"
- features: array of short keywords (e.g., serverless, ha, streaming, multi-region, autoscaling)

Use canonical names & roles (AWS/Azure/GCP). Prefer specific roles; dedupe services.
Never invent providers/services not implied by the text/code.
"""

USER_TEMPLATE = """TEXT (may be truncated):
{TEXT}

TOKENS (hints): {TOKENS}
"""

def ensure_shape(obj: dict) -> dict:
    return {
        "providers": obj.get("providers") or [],
        "services": obj.get("services") or [],
        "flow": obj.get("flow") or [],
        "features": obj.get("features") or [],
    }

def enrich_with_ai(text: str, tokens: List[str]) -> Dict[str, Any]:
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY missing")
        raise Exception("GEMINI_API_KEY missing")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=SYSTEM_INSTRUCTIONS.strip())
        prompt = USER_TEMPLATE.format(TEXT=text[:16000], TOKENS=tokens[:200])

        # strict JSON
        try:
            resp = model.generate_content(
                prompt,
                generation_config={"temperature": 0.0, "response_mime_type": "application/json"},
            )
            content = (resp.text or "").strip()
            if content:
                return ensure_shape(json.loads(content))
        except Exception as e:
            logger.info("Gemini strict JSON failed: %s", e)

        # lenient fallback
        try:
            resp = model.generate_content(prompt, generation_config={"temperature": 0.0})
            content = (resp.text or "").strip()
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.I | re.S)
            if content:
                return ensure_shape(json.loads(content))
        except Exception as e:
            logger.info("Gemini lenient parse failed: %s", e)

        logger.warning("Gemini returned nothing parsable")
        raise HTTPException(
            status_code=502,
            detail="AI parsing returned empty for all results; nothing was stored."
        )

    except GoogleAPIError as e:
        logger.error("Gemini API error: %s", e)
        raise HTTPException(
            status_code=502,
            detail="AI parsing returned empty for all results; nothing was stored."
        )
    except Exception as e:
        logger.exception("Unexpected AI error")
        raise HTTPException(
            status_code=502,
            detail="AI parsing returned empty for all results; nothing was stored."
        )
