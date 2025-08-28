from typing import List, Dict, Any
import re

from utils.constants import (
    VALID_ROLES, ROLE_SYNONYMS, NAME_ROLE_OVERRIDES, PROVIDER_MAP, CANONICAL_NAME_MAP
) 

def normalize_role(role: str) -> str:
    if not role:
        return "Other"
    r = role.strip()
    if r in VALID_ROLES:
        return r
    mapped = ROLE_SYNONYMS.get(r.lower())
    if mapped and mapped in VALID_ROLES:
        return mapped
    t = r.title()
    return t if t in VALID_ROLES else "Other"

def normalize_name(name: str) -> str:
    n = (name or "").strip()
    if not n:
        return n
    return CANONICAL_NAME_MAP.get(n.lower(), n)

def normalize_services(services: List[Any]) -> List[Dict[str, str]]:
    services_list: List[Dict[str, str]] = []
    seen = set()
    for s in services or []:
        if isinstance(s, str):
            raw_name, role = s, "Other"
        elif isinstance(s, dict):
            raw_name = s.get("name") or ""
            role = normalize_role(s.get("role") or "Other")
        else:
            continue

        name = normalize_name(raw_name)
        if not name:
            continue

        if name in NAME_ROLE_OVERRIDES:
            role = NAME_ROLE_OVERRIDES[name]

        key = (name.lower(), role)
        if key not in seen:
            seen.add(key)
            services_list.append({"name": name, "role": role})
    return services_list

def normalize_flows(flows: List[str]) -> List[str]:
    flows_list, seen = [], set()
    for f in flows or []:
        s = re.sub(r"\s*->\s*", " -> ", (f or "").strip())
        if s and s not in seen:
            seen.add(s)
            flows_list.append(s)
    return flows_list

def normalize_providers(providers: List[str]) -> List[str]:
    providers_list, seen = [], set()
    for p in providers or []:
        norm = PROVIDER_MAP.get((p or "").strip().lower())
        if norm and norm not in seen:
            seen.add(norm)
            providers_list.append(norm)
    return providers_list

def normalize_features(features: List[str]) -> List[str]:
    # lowercase, trim, dedupe
    features_list, seen = [], set()
    for f in features or []:
        s = (f or "").strip().lower()
        if s and s not in seen:
            seen.add(s)
            features_list.append(s)
    return features_list
