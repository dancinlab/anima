#!/usr/bin/env bash
# h1306_fetch_corpus.sh — fetch a MODEST real Korean + English slice from the existing
# anima-7b 5-lang web corpus on Cloudflare R2 (bucket `phanes`). REAL crawled text only
# (NO synthetic Korean, p1-p8). Pulls a few MB via HTTP range — NOT the 9.8GiB shards.
#
# SECRETS (c7): R2 keys are read from the macOS-Keychain-backed `secret` CLI into ENV
# ONLY at call time — header/env-scoped, NEVER echoed, logged, inlined, or committed.
# The endpoint host (account id) is also kept out of stdout.
#
# $0, no GPU. Writes /tmp/ko_slice_raw.bytes (4 MiB) + /tmp/en_slice_raw.bytes (2 MiB).
set -euo pipefail

export AWS_ACCESS_KEY_ID="$(secret get r2.phanes.access_key_id)"
export AWS_SECRET_ACCESS_KEY="$(secret get r2.phanes.secret_access_key)"
ACCT="$(secret get r2.phanes.account_id)"
BUCKET="$(secret get r2.phanes.bucket)"
ENDPOINT="https://${ACCT}.r2.cloudflarestorage.com"

echo "[h1306-fetch] pulling REAL Korean slice (4 MiB) from r2://${BUCKET}/anima-7b/web/kor/shard0000.bytes"
aws s3api get-object --bucket "$BUCKET" --key "anima-7b/web/kor/shard0000.bytes" \
  --range "bytes=0-4194303" --endpoint-url "$ENDPOINT" /tmp/ko_slice_raw.bytes >/dev/null

echo "[h1306-fetch] pulling REAL English slice (2 MiB) from r2://${BUCKET}/anima-7b/web/eng/shard0000.bytes"
aws s3api get-object --bucket "$BUCKET" --key "anima-7b/web/eng/shard0000.bytes" \
  --range "bytes=0-2097151" --endpoint-url "$ENDPOINT" /tmp/en_slice_raw.bytes >/dev/null

echo "[h1306-fetch] done: $(wc -c </tmp/ko_slice_raw.bytes) KO bytes, $(wc -c </tmp/en_slice_raw.bytes) EN bytes"
# scrub keys from env before exit (defensive)
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
