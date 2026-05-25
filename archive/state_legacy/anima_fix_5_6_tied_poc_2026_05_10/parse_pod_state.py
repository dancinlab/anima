"""Parse pod state from `runpodctl pod get <id>` JSON. argv[1] = path."""
import json, sys
data = json.load(open(sys.argv[1]))
# Pod object has desiredStatus or similar
print(data.get("desiredStatus", data.get("status", "UNKNOWN")))
