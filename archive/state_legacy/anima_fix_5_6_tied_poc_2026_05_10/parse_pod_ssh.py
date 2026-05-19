"""Parse SSH host/port from `runpodctl pod get` JSON.
argv[1] = path, argv[2] = field (host|port)
"""
import json, sys
data = json.load(open(sys.argv[1]))
field = sys.argv[2]
ssh = data.get("ssh", {}) or {}
if field == "host":
    print(ssh.get("ip", ""))
elif field == "port":
    print(ssh.get("port", ""))
