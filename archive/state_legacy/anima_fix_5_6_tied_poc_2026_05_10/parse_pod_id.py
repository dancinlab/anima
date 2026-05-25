"""Parse pod_id from ephemeral-list JSON, filtered by POD_NAME env."""
import json, os, sys
data = json.load(open(sys.argv[1]))
pn = os.environ.get("POD_NAME", "")
cands = [p for p in data.get("pods", []) if pn in p.get("name", "")]
print(cands[0]["pod_id"] if cands else "")
