#!/usr/bin/env python3
"""Ask an LLM to assess three sample signal-and-evidence packets."""

import json
from pprint import pprint

from openai import OpenAI


SYSTEM_PROMPT = """You are the intelligence step in an ecosystem signal monitor.
Decide whether the supplied signal deserves the user's attention. Reason only
from the supplied signal and evidence. Never invent missing facts, and keep
unknown exposure unknown.

Prefer high recall while the system is being calibrated: if evidence is truly
insufficient to dismiss a signal, surface it. However, use nah with high
confidence when available evidence is sufficient to establish little
relevance. Severity alone does not establish relevance; ecosystem reach can
outweigh moderate severity. Highly critical or actively exploited issues may
still deserve attention with small reach.

Do not request enrichment merely because it could be interesting. Use
investigate only when additional evidence could plausibly change the decision.
Surfacing and investigation may happen simultaneously.

Calibration:
- A critical contributed-module vulnerability with anonymous access, 165
  reporting sites, ecosystem position around 5,386, and unknown Acquia
  exposure is nah/high, inbox other, no snoop action, user no_action.
- A moderately critical Drupal core XSS affecting default/common
  configurations is relevant/high, inbox priority, no snoop action, user
  awareness.
- An advance PSA for an undisclosed widely used module, many advisories, at
  least one Critical issue, and possible anonymous/default exposure is
  holy_crap/high, inbox priority, snoop investigate, user monitor. Here,
  holy_crap expresses the urgency and breadth of the attention decision; it
  does not mean the Drupal severity category Highly Critical.
"""

ASSESSMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "assessment": {
            "type": "object",
            "properties": {
                "attention": {
                    "type": "string",
                    "enum": ["nah", "relevant", "important", "holy_crap"],
                },
                "confidence": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                },
            },
            "required": ["attention", "confidence"],
            "additionalProperties": False,
        },
        "presentation": {
            "type": "object",
            "properties": {
                "inbox": {"type": "string", "enum": ["other", "priority"]}
            },
            "required": ["inbox"],
            "additionalProperties": False,
        },
        "summary": {"type": "string"},
        "why": {"type": "array", "items": {"type": "string"}},
        "snoop_actions": {
            "type": "array",
            "items": {"type": "string", "enum": ["investigate"]},
        },
        "user_actions": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["no_action", "awareness", "monitor"],
            },
        },
    },
    "required": [
        "assessment",
        "presentation",
        "summary",
        "why",
        "snoop_actions",
        "user_actions",
    ],
    "additionalProperties": False,
}

SAMPLE_PACKETS = [
    {
        "name": "Ultimate Table Field",
        "signal": {
            "type": "security_advisory",
            "title": "Ultimate Table Field - Critical - Access bypass",
            "url": "https://www.drupal.org/sa-contrib-2026-example",
            "published_at": "2026-09-01T00:00:00Z",
            "facts": {
                "project_type": "contributed_module",
                "risk": "Critical 15/25",
                "anonymous_access_possible": True,
            },
        },
        "evidence": [
            {
                "type": "ecosystem_usage",
                "source": "https://www.drupal.org/project/usage",
                "sensitivity": "public",
                "facts": {"reporting_sites": 165, "listing_position": 5386},
            },
            {"type": "product_exposure", "status": "unknown"},
            {"type": "customer_exposure", "status": "unknown"},
            {"type": "organizational_interest", "status": "unknown"},
        ],
    },
    {
        "name": "Drupal core / CKEditor",
        "signal": {
            "type": "security_advisory",
            "title": "Drupal core - Moderately critical - Third-party libraries",
            "url": "https://www.drupal.org/sa-core-2026-013",
            "published_at": "2026-09-16T17:00:00Z",
            "facts": {
                "project_type": "drupal_core",
                "risk": "Moderately Critical 13/25",
                "affected_configuration": "default_or_common",
                "vulnerability": "XSS targeting privileged CKEditor users",
            },
        },
        "evidence": [
            {"type": "product_exposure", "status": "unknown"},
            {"type": "customer_exposure", "status": "unknown"},
            {"type": "organizational_interest", "status": "unknown"},
        ],
    },
    {
        "name": "September 21 security PSA",
        "signal": {
            "type": "security_psa",
            "title": "Upcoming critical contributed project security release",
            "url": "https://www.drupal.org/psa-2026-09-21",
            "published_at": "2026-09-21T09:56:09Z",
            "facts": {
                "source": "Drupal Security Team",
                "advance_warning": True,
                "project_disclosed": False,
                "reach": "significant portion of Drupal sites",
                "advisories_expected": "significant number",
                "highest_expected_risk": "Critical",
                "anonymous_or_default_exposure_possible": True,
                "related_projects_may_be_affected": True,
            },
        },
        "evidence": [
            {"type": "product_exposure", "status": "unknown"},
            {"type": "customer_exposure", "status": "unknown"},
            {"type": "organizational_interest", "status": "unknown"},
        ],
    },
]


def assess(packet: dict) -> dict:
    response = OpenAI().responses.create(
        model="gpt-6-astra",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(packet, indent=2)},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "intelligence_assessment",
                "strict": True,
                "schema": ASSESSMENT_SCHEMA,
            }
        },
    )
    return json.loads(response.output_text)


if __name__ == "__main__":
    for sample in SAMPLE_PACKETS:
        print(f"\n{'=' * 80}\n{sample['name']}\n{'=' * 80}")
        pprint(assess(sample), sort_dicts=False)
