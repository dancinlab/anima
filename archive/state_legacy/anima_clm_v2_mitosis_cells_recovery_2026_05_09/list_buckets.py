#!/usr/bin/env python3
import sys, json
d = json.load(sys.stdin)
print("success=", d.get("success"))
for b in d.get("result", {}).get("buckets", []):
    print(b["name"], b.get("creation_date", ""))
