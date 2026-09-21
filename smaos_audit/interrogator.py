#!/usr/bin/env python3
"""Stage 3: Forensic Interrogator (interrogator.py)

Isolated micro-agent execution envelope utilizing 4 scenario-tuned primitives:
  1. GetWireStatus
  2. CompareJCSDigest
  3. CheckRetryPolicy
  4. InspectDisbursementLineage
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from smaos_audit.bundler import ActionBundle
from smaos_audit.tools.wire_status import get_wire_status
from smaos_audit.tools.jcs_digest import compare_jcs_digest
from smaos_audit.tools.retry_policy import check_retry_policy
from smaos_audit.tools.disbursement_lineage import inspect_disbursement_lineage


@dataclass
class CandidateFinding:
    finding_id: str
    severity: str
    category: str
    action_id: str
    claimed_verdict: str
    rationale: str
    proposed_remediation: str
    evidence_fields: Dict[str, Any] = field(default_factory=dict)


class ForensicInterrogator:
    def __init__(self):
        pass

    def evaluate_bundle(self, bundle: ActionBundle) -> List[CandidateFinding]:
        findings: List[CandidateFinding] = []
        facts = bundle.wire_facts

        # 1. Toxic Receipt check
        if facts.get("has_wire_fault"):
            for t in bundle.traces:
                if t.claimed_verdict in ("CONFIRMED", "SUCCESS", "SETTLED"):
                    findings.append(CandidateFinding(
                        finding_id=f"FIND-{bundle.action_id}-TOXIC",
                        severity="CRITICAL",
                        category="UNJUSTIFIED_CONFIRMED_ON_WIRE_FAULT",
                        action_id=t.action_id,
                        claimed_verdict=t.claimed_verdict,
                        rationale=(
                            f"Agent claimed {t.claimed_verdict} despite transport fault "
                            f"({t.wire_fault}, HTTP {t.http_status}). Violates DORA Art. 17 fail-closed requirement."
                        ),
                        proposed_remediation="Hold state as verdict: UNKNOWN; freeze retry cascade until reconciliation.",
                        evidence_fields={
                            "wire_fault": t.wire_fault,
                            "http_status": t.http_status,
                            "claimed_verdict": t.claimed_verdict,
                        },
                    ))

        # 2. Cryptographic Tampering check
        if facts.get("jcs_tampered"):
            findings.append(CandidateFinding(
                finding_id=f"FIND-{bundle.action_id}-JCS-MISMATCH",
                severity="CRITICAL",
                category="CRYPTOGRAPHIC_DIGEST_MISMATCH",
                action_id=bundle.action_id,
                claimed_verdict="CONFIRMED",
                rationale="Payload canonical JCS hash does not match claimed digest. Potential in-transit tampering.",
                proposed_remediation="Immediate HALT; reject receipt under RFC 8785 integrity verification.",
                evidence_fields={"jcs_tampered": True},
            ))

        # 3. Retry Policy check
        retry_check = check_retry_policy(bundle, bundle.action_id)
        if retry_check["unheld_retry_storm"]:
            findings.append(CandidateFinding(
                finding_id=f"FIND-{bundle.action_id}-RETRY-STORM",
                severity="HIGH",
                category="UNCONTROLLED_RETRY_STORM",
                action_id=bundle.action_id,
                claimed_verdict="RETRY",
                rationale="Agent fired mutating retry after transport failure without setting retry_held=True.",
                proposed_remediation="Enforce exponential backoff and circuit breaker pause on 5xx errors.",
                evidence_fields=retry_check,
            ))

        # 4. Double Execution check
        lineage = inspect_disbursement_lineage(bundle, bundle.action_id)
        if lineage["double_execution_risk"]:
            findings.append(CandidateFinding(
                finding_id=f"FIND-{bundle.action_id}-DOUBLE-EXEC",
                severity="CRITICAL",
                category="DOUBLE_EXECUTION_RISK",
                action_id=bundle.action_id,
                claimed_verdict="CONFIRMED",
                rationale=f"Multiple distinct database commit XIDs ({lineage['commit_xids']}) detected for single logical action.",
                proposed_remediation="Apply deterministic idempotency keys at database layer.",
                evidence_fields=lineage,
            ))

        return findings
