#!/usr/bin/env python3
"""
PULSE Swarm Incident Generator (Task C3)
Fires N matching PAYMENT_CAPTURED_ORDER_NOT_CREATED events to POST /events/ingest
to trigger incident INC-0042 in the live correlator during the demo.
"""

import sys
import time
import argparse
import urllib.request
import json
from datetime import datetime, timezone


def run_swarm(
    count: int = 50,
    interval: float = 0.05,
    base_url: str = "http://localhost:8000",
    signature: str = "PAYMENT_CAPTURED_ORDER_NOT_CREATED",
):
    url = f"{base_url.rstrip('/')}/events/ingest"
    print(f"[*] Starting swarm of {count} operational mismatch events to {url} (interval={interval}s)...")
    print(f"[*] Signature: {signature}")

    success_count = 0
    incident_triggered = False

    for i in range(1, count + 1):
        payment_ref = f"TX-{100 + i}"
        event = {
            "type": signature,
            "payment_ref": payment_ref,
            "ts": datetime.now(timezone.utc).isoformat(),
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(event).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                success_count += 1
                if body.get("incident_opened") and not incident_triggered:
                    incident_triggered = True
                    print(f"\n[🔥 INCIDENT TRIGGERED] {body.get('incident_id')} opened at event #{i} ({payment_ref})!")
                else:
                    print(f"\r[>] Sent event #{i}/{count} ({payment_ref}) - HTTP {resp.status}", end="", flush=True)
        except Exception as e:
            print(f"\n[-] Event #{i} failed: {e}")

        if interval > 0:
            time.sleep(interval)

    print(f"\n[+] Swarm finished: {success_count}/{count} events ingested.")
    if incident_triggered:
        print("[+] Active Incident successfully opened on backend!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PULSE Swarm Event Generator")
    parser.add_argument("--count", type=int, default=50, help="Number of mismatch events to fire")
    parser.add_argument("--interval", type=float, default=0.05, help="Delay between events in seconds")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend base URL")
    args = parser.parse_args()

    run_swarm(count=args.count, interval=args.interval, base_url=args.base_url)
