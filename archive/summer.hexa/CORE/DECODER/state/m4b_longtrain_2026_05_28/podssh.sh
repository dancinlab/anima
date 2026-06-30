#!/usr/bin/env bash
# podssh.sh — raw ssh/scp helper to M4b H100 pods (hexa cloud exec is buggy for
# these RunPod pods — raw ssh to the IP works + passes cloud-guard IP-form).
# usage:
#   podssh.sh exec <host> <port> '<remote cmd>'
#   podssh.sh put  <host> <port> <local> <remote>
#   podssh.sh putr <host> <port> <localdir> <remotedir>   (recursive)
#   podssh.sh get  <host> <port> <remote> <local>
KEY=/Users/ghost/.ssh/id_ed25519
OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=25 -o ServerAliveInterval=30 -o ServerAliveCountMax=4"
verb="$1"; host="$2"; port="$3"
case "$verb" in
  exec) ssh $OPTS -i "$KEY" -p "$port" "root@$host" "$4" ;;
  put)  scp $OPTS -i "$KEY" -P "$port" "$4" "root@$host:$5" ;;
  putr) scp $OPTS -r -i "$KEY" -P "$port" "$4" "root@$host:$5" ;;
  get)  scp $OPTS -i "$KEY" -P "$port" "root@$host:$4" "$5" ;;
  *) echo "unknown verb $verb"; exit 2 ;;
esac
