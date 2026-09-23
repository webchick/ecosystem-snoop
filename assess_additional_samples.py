#!/usr/bin/env python3
"""Run five additional Drupal security records through the M1 classifier."""

from pprint import pprint

from assess_signal import assess


def unknown_evidence() -> list[dict]:
    return [
        {"type": "ecosystem_usage", "status": "unknown"},
        {"type": "product_exposure", "status": "unknown"},
        {"type": "customer_exposure", "status": "unknown"},
        {"type": "organizational_interest", "status": "unknown"},
    ]


SAMPLES = [
    {
        "name": "SafeDelete",
        "signal": {
            "type": "security_advisory",
            "title": "SafeDelete - Moderately critical - Cross-site scripting",
            "url": "https://www.drupal.org/sa-contrib-2026-140",
            "published_at": "2026-09-09T17:19:26Z",
            "facts": {
                "project_type": "contributed_module",
                "project_machine_name": "safedelete",
                "risk": "Moderately Critical 12/25",
                "risk_vector": "AC:Basic/A:User/CI:Some/II:Some/E:Theoretical/TD:Uncommon",
                "vulnerability": "persistent cross-site scripting",
                "affected_versions": "<1.0.88",
                "cve": "CVE-2026-87942",
                "mitigation": "Attacker needs permission to create content configured for the orphaned nodes report.",
            },
        },
        "evidence": unknown_evidence(),
    },
    {
        "name": "Patreon",
        "signal": {
            "type": "security_advisory",
            "title": "Patreon - Critical - Unsupported",
            "url": "https://www.drupal.org/sa-contrib-2026-139",
            "published_at": "2026-09-09T17:18:07Z",
            "facts": {
                "project_type": "contributed_module",
                "project_machine_name": "patreon",
                "risk": "Critical 16/25",
                "risk_vector": "AC:Complex/A:Admin/CI:All/II:All/E:Theoretical/TD:All",
                "status": "unsupported",
                "cve": "CVE-2026-87941",
                "description": "Known security issue is unfixed and the project is unsupported.",
            },
        },
        "evidence": unknown_evidence(),
    },
    {
        "name": "CSP log",
        "signal": {
            "type": "security_advisory",
            "title": "CSP log - Critical - SQL Injection",
            "url": "https://www.drupal.org/sa-contrib-2026-136",
            "published_at": "2026-09-09T17:16:33Z",
            "facts": {
                "project_type": "contributed_module",
                "project_machine_name": "csp_log",
                "risk": "Critical 15/25",
                "risk_vector": "AC:Basic/A:Admin/CI:All/II:Some/E:Theoretical/TD:All",
                "vulnerability": "SQL injection",
                "affected_versions": "<1.0.2",
                "cve": "CVE-2026-87938",
                "mitigation": "Attacker needs an account with Access CSP reports permission.",
            },
        },
        "evidence": unknown_evidence(),
    },
    {
        "name": "amazee.ai Private AI Provider",
        "signal": {
            "type": "security_advisory",
            "title": "amazee.ai Private AI Provider - Critical - SQL injection",
            "url": "https://www.drupal.org/sa-contrib-2026-134",
            "published_at": "2026-09-09T17:14:00Z",
            "facts": {
                "project_type": "contributed_module",
                "project_machine_name": "ai_provider_amazeeio",
                "risk": "Critical 17/25",
                "risk_vector": "AC:Complex/A:None/CI:All/II:Some/E:Proof/TD:Default",
                "vulnerability": "SQL injection",
                "affected_versions": "<1.3.7 || >=1.4.0 <1.4.3",
                "cve": "CVE-2026-87936",
                "exploit_evidence": "Publicly documented methods for developing exploits exist.",
                "affected_configuration": "Postgres/pgvector backend with a reachable non-string index filter.",
            },
        },
        "evidence": unknown_evidence(),
    },
    {
        "name": "Unpublished Node Permissions",
        "signal": {
            "type": "security_advisory",
            "title": "Unpublished Node Permissions - Critical - Access bypass",
            "url": "https://www.drupal.org/sa-contrib-2026-132",
            "published_at": "2026-09-02T16:38:32Z",
            "facts": {
                "project_type": "contributed_module",
                "project_machine_name": "unpublished_node_permissions",
                "risk": "Critical 15/25",
                "risk_vector": "AC:None/A:None/CI:Some/II:None/E:Theoretical/TD:All",
                "vulnerability": "access bypass",
                "affected_versions": "<1.8.0",
                "cve": "CVE-2026-84920",
                "description": "Published-content access can override other access-control mechanisms.",
            },
        },
        "evidence": unknown_evidence(),
    },
]


if __name__ == "__main__":
    for sample in SAMPLES:
        print(f"\n{'=' * 80}\n{sample['name']}\n{'=' * 80}")
        pprint(assess(sample), sort_dicts=False)
