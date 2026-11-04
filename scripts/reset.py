#!/usr/bin/env python3
"""
PULSE Demo Reset Script (Task C3)
Calls POST /admin/reset to return the entire system to start-of-demo state.
"""

import sys
import argparse
import urllib.request
import json


def reset_demo(base_url: str = "http://localhost:8000"):
    url = f"{base_url.rstrip('/')}/admin/reset"
    print(f"[*] Resetting PULSE demo state at {url}...")
    
    req = urllib.request.Request(
        url,
        data=json.dumps({}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_body = response.read().decode("utf-8")
            print(f"[+] Demo successfully reset: {res_body}")
            return True
    except urllib.error.URLError as e:
        print(f"[-] Failed to reset (is backend running?): {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset PULSE demo state")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of backend")
    args = parser.parse_args()
    
    success = reset_demo(args.base_url)
    sys.exit(0 if success else 1)
