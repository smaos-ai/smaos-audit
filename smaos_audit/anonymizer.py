"""Stage 0: EDPB 02/2026 Compliant PII Anonymizer (anonymizer.py)

Strips and salt-hashes personal identifiable information (PII) 
prior to trace ingestion, ensuring zero-egress data privacy.
"""

import hashlib
import re
from typing import Any, Dict

DEFAULT_SALT = "smaos-audit-salt-v0.1"

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
IBAN_REGEX = re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b")
CARD_REGEX = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

def hash_identifier(value: str, salt: str = DEFAULT_SALT) -> str:
    """Computes a truncated HMAC-style SHA-256 hash for pseudonymization."""
    return "anon_" + hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()[:12]

def anonymize_text(text: str, salt: str = DEFAULT_SALT) -> str:
    """Detects and pseudonymizes emails, IBANs, and credit card numbers in strings."""
    text = EMAIL_REGEX.sub(lambda m: hash_identifier(m.group(0), salt), text)
    text = IBAN_REGEX.sub(lambda m: hash_identifier(m.group(0), salt), text)
    text = CARD_REGEX.sub(lambda m: hash_identifier(m.group(0), salt), text)
    return text

def anonymize_trace_record(record: Dict[str, Any], salt: str = DEFAULT_SALT) -> Dict[str, Any]:
    """Recursively traverses and sanitizes trace JSON payloads."""
    anonymized = {}
    for key, val in record.items():
        if isinstance(val, str):
            anonymized[key] = anonymize_text(val, salt)
        elif isinstance(val, dict):
            anonymized[key] = anonymize_trace_record(val, salt)
        elif isinstance(val, list):
            anonymized[key] = [anonymize_text(x, salt) if isinstance(x, str) else x for x in val]
        else:
            anonymized[key] = val
    return anonymized
