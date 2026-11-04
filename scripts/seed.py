#!/usr/bin/env python3
"""
PULSE Seed Script (Task C3)
Seeds 50 transactions (TX-101 onwards, mismatches among them), 8 customers, 8 commitments.
Hero case: Priya, CASE-2041, TX-101, refund INR 4,299, refund ref RF-8821.
Target demo outcome: 6 VERIFIED, 2 AT_RISK. All labelled SIMULATED.
"""

import sys
import argparse
import urllib.request
import json
from typing import Dict, Any, List


def generate_seed_data() -> Dict[str, Any]:
    transactions = []
    
    # Hero case TX-101: captured payment, order missing (mismatch)
    transactions.append({
        "payment_ref": "TX-101",
        "customer_name": "Priya Sharma",
        "case_ref": "CASE-2041",
        "payment_status": "CAPTURED",
        "order_status": "NOT_CREATED",
        "amount": 4299,
        "currency": "INR",
        "mismatch": True,
        "incident_id": "INC-0042",
        "simulated": True,
    })

    # Customers 2-8
    customers = [
        ("Rahul Verma", "CASE-2042", 1850),
        ("Ananya Sen", "CASE-2043", 3499),
        ("Vikram Patel", "CASE-2044", 2999),
        ("Sneha Reddy", "CASE-2045", 4999),
        ("Arjun Kapoor", "CASE-2046", 1200),
        ("Meera Joshi", "CASE-2047", 7500),
        ("Karan Malhotra", "CASE-2048", 2499),
    ]

    for idx, (name, case, amt) in enumerate(customers, start=102):
        tx_ref = f"TX-{idx}"
        transactions.append({
            "payment_ref": tx_ref,
            "customer_name": name,
            "case_ref": case,
            "payment_status": "CAPTURED",
            "order_status": "NOT_CREATED",
            "amount": amt,
            "currency": "INR",
            "mismatch": True,
            "incident_id": "INC-0042",
            "simulated": True,
        })

    # Transactions 109 to 150 (remaining 42 transactions: a mix of normal orders and mismatches)
    for idx in range(109, 151):
        is_mismatch = (idx % 3 != 0)  # ~30 mismatches to reach 50 total affected
        transactions.append({
            "payment_ref": f"TX-{idx}",
            "customer_name": f"Customer {idx}",
            "case_ref": None,
            "payment_status": "CAPTURED",
            "order_status": "NOT_CREATED" if is_mismatch else "COMPLETED",
            "amount": 1000 + (idx * 25),
            "currency": "INR",
            "mismatch": is_mismatch,
            "incident_id": "INC-0042" if is_mismatch else None,
            "simulated": True,
        })

    # 8 Initial Commitments matching hero flow
    commitments = [
        {
            "id": "CMT-001",
            "case_ref": "CASE-2041",
            "customer_name": "Priya Sharma",
            "payment_ref": "TX-101",
            "amount": 4299,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8821",
            "status": "AT_RISK",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:32:05; settlement not found at 10:32:41",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-002",
            "case_ref": "CASE-2042",
            "customer_name": "Rahul Verma",
            "payment_ref": "TX-102",
            "amount": 1850,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8822",
            "status": "AT_RISK",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:32:17; settlement not found at 10:32:45",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-003",
            "case_ref": "CASE-2043",
            "customer_name": "Ananya Sen",
            "payment_ref": "TX-103",
            "amount": 3499,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8823",
            "status": "AWAITING_VERIFICATION",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:32:32; polling bank verification",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-004",
            "case_ref": "CASE-2044",
            "customer_name": "Vikram Patel",
            "payment_ref": "TX-104",
            "amount": 2999,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8824",
            "status": "AWAITING_VERIFICATION",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:32:44; awaiting bank batch settlement",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-005",
            "case_ref": "CASE-2045",
            "customer_name": "Sneha Reddy",
            "payment_ref": "TX-105",
            "amount": 4999,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8825",
            "status": "AT_RISK",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:32:50; settlement missing at clearinghouse",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-006",
            "case_ref": "CASE-2046",
            "customer_name": "Arjun Kapoor",
            "payment_ref": "TX-106",
            "amount": 1200,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8826",
            "status": "AWAITING_VERIFICATION",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:33:02; awaiting settlement confirmation",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-007",
            "case_ref": "CASE-2047",
            "customer_name": "Meera Joshi",
            "payment_ref": "TX-107",
            "amount": 7500,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": None,
            "status": "APPROVAL_PENDING",
            "policy_rule": "R3 (Amount > 5000 INR requires supervisor approval)",
            "evidence": "Supervisor approval required per policy limit; pending review",
            "incident_id": "INC-0042",
            "simulated": True,
        },
        {
            "id": "CMT-008",
            "case_ref": "CASE-2048",
            "customer_name": "Karan Malhotra",
            "payment_ref": "TX-108",
            "amount": 2499,
            "currency": "INR",
            "remedy": "REFUND",
            "action_ref": "RF-8828",
            "status": "AT_RISK",
            "policy_rule": "R3",
            "evidence": "Refund API accepted at 10:33:18; settlement not found at 10:33:45",
            "incident_id": "INC-0042",
            "simulated": True,
        },
    ]

    return {
        "transactions": transactions,
        "commitments": commitments,
    }


def seed_database(base_url: str = "http://localhost:8000"):
    payload = generate_seed_data()
    url = f"{base_url.rstrip('/')}/admin/seed"
    print(f"[*] Posting seed payload ({len(payload['transactions'])} transactions, {len(payload['commitments'])} commitments) to {url}...")

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_body = response.read().decode("utf-8")
            print(f"[+] Database seeded successfully: {res_body}")
            return True
    except urllib.error.URLError as e:
        print(f"[-] Backend offline or endpoint not ready: {e}")
        print("[i] Saving local seed fixtures to scripts/seed_fixtures.json instead...")
        with open("scripts/seed_fixtures.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print("[+] Wrote scripts/seed_fixtures.json for offline use.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed PULSE transaction and commitment data")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of backend")
    args = parser.parse_args()

    seed_database(args.base_url)
