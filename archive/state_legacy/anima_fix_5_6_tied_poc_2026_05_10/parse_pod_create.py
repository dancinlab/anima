"""Parse pod_id from `runpodctl pod create` JSON output. argv[1] = path."""
import json, sys
data = json.load(open(sys.argv[1]))
# runpodctl pod create returns single pod object
print(data.get("id", ""))
