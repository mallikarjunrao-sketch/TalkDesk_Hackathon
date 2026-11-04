#!/usr/bin/env python3
"""
PULSE End-to-End Demo Script (Task C7)
Executes the full 7-minute story over HTTP against the backend:
1. Reset (/admin/reset)
2. Seed transactions & hero case Priya (/admin/seed)
3. Propose refund resolution for Priya (CASE-2041, TX-101, INR 4299)
4. Execute refund resolution (mock refund accepted, status ACKNOWLEDGED)
5. Run verifier (settlement NOT_FOUND -> status transitions to AT_RISK!)
6. Run swarm of mismatch events -> Incident INC-0042 opens
7. Flip settlement toggle to FOUND (/admin/settlement-mode)
8. Run verifier again -> status transitions to VERIFIED!
"""

import sys
import time
import argparse
import urllib.request
import json
from typing import Dict, Any


def http_post(url: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_e2e_flow(base_url: str = "http://localhost:8000"):
    base = base_url.rstrip("/")
    print("=" * 70)
    print("PULSE END-TO-END DEMO TEST SCRIPT")
    print("Pitch: 'We make AI agents prove the refund actually arrived.'")
    print("=" * 70)

    # 1. Health check
    print("\n[Step 1] Checking /health...")
    try:
        health = http_get(f"{base}/health")
        print(f" -> Backend healthy: {health}")
    except Exception as e:
        print(f"[-] Backend not reachable at {base}/health: {e}")
        return False

    # 2. Reset system
    print("\n[Step 2] Resetting system to clean start state (/admin/reset)...")
    res = http_post(f"{base}/admin/reset")
    print(f" -> Reset result: {res}")

    # 3. Seed demo data
    print("\n[Step 3] Seeding transactions (/admin/seed)...")
    from seed import generate_seed_data
    seed_payload = generate_seed_data()
    res = http_post(f"{base}/admin/seed", seed_payload)
    print(f" -> Seeded: {res}")

    # 4. Propose resolution for hero case Priya
    print("\n[Step 4] Proposing resolution for Priya (CASE-2041, TX-101, INR 4,299)...")
    prop = http_post(f"{base}/resolutions/propose", {
        "case_id": "CASE-2041",
        "remedy": "REFUND",
        "amount": 4299,
    })
    print(f" -> Decision: {prop.get('decision')} (Rule: {prop.get('rule_id')}), CMT: {prop.get('commitment_id')}")
    cmt_id = prop.get("commitment_id", "CMT-001")

    # 5. Execute resolution
    print(f"\n[Step 5] Executing refund for {cmt_id}...")
    exec_res = http_post(f"{base}/resolutions/execute", {"commitment_id": cmt_id})
    print(f" -> Mock Refund Result: {exec_res.get('status')} (Action Ref: {exec_res.get('action_ref')})")
    print(f" -> Customer Message Hint: \"{exec_res.get('customer_message_hint')}\"")

    # 6. Verify with settlement mode NOT_FOUND (The Aha Moment: AT_RISK)
    print(f"\n[Step 6] Running independent verification while settlement is NOT_FOUND...")
    http_post(f"{base}/admin/settlement-mode", {"mode": "NOT_FOUND"})
    v_res = http_post(f"{base}/verification/run", {"commitment_id": cmt_id})
    print(f" -> Verifier Status: {v_res.get('status')} (Settlement: {v_res.get('settlement')})")
    print(f" -> Verifier Evidence: \"{v_res.get('evidence')}\"")
    assert v_res.get("status") == "AT_RISK", f"Expected AT_RISK, got {v_res.get('status')}"
    print(" -> [PASS] PULSE refused to mark refund complete! False success caught.")

    # 7. Swarm mismatch events -> INC-0042 opens
    print("\n[Step 7] Ingesting swarm of mismatch events...")
    opened = False
    for i in range(1, 10):
        ing_res = http_post(f"{base}/events/ingest", {
            "type": "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
            "payment_ref": f"TX-SWARM-{i}",
        })
        if ing_res.get("incident_opened"):
            opened = True
            print(f" -> Incident opened at event #{i}: {ing_res.get('incident_id')}")
            break
    print(f" -> Incident detection active: {opened}")

    # 8. Flip settlement to FOUND and re-verify
    print("\n[Step 8] Bank settlement recovered -> Toggling FOUND and re-verifying...")
    http_post(f"{base}/admin/settlement-mode", {"mode": "FOUND"})
    v_res_2 = http_post(f"{base}/verification/run", {"commitment_id": cmt_id})
    print(f" -> Verifier Status: {v_res_2.get('status')} (Settlement: {v_res_2.get('settlement')})")
    assert v_res_2.get("status") == "VERIFIED", f"Expected VERIFIED, got {v_res_2.get('status')}"
    print(" -> [PASS] Independent verifier confirmed settlement. Customer truthfully notified!")

    print("\n" + "=" * 70)
    print("ALL E2E CHECKS PASSED SUCCESSFULLY (G4 / G5 Ready)")
    print("=" * 70)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PULSE End-to-End Demo Test")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend base URL")
    args = parser.parse_args()

    success = run_e2e_flow(args.base_url)
    sys.exit(0 if success else 1)
