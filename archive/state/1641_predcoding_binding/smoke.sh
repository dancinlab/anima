#!/usr/bin/env bash
# H_1641 PREDCODING-BINDING — $0 CPU smoke: tiny (d=64 L=2) train + serialize +
# clm_decodable + g_gates connection for all 3 arms. NO GPU, NO canon.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$HERE"; while [ "$REPO" != "/" ] && [ ! -e "$REPO/cli/train.py" ]; do REPO="$(dirname "$REPO")"; done
cd "$REPO"
OUT="$HERE/ckpt"; mkdir -p "$OUT"; export SMOKE_OUT="$OUT"
echo "=== H_1641 smoke (repo=$REPO) ==="
for OBJ in ce_marginal pc_bind pc_free_energy; do
  echo "--- arm: $OBJ ---"
  python3 "$HERE/trainer.py" --objective "$OBJ" --seed 7 \
    --d 64 --L 2 --steps 6 --seq-len 64 --batch-size 4 \
    --val-every 0 --log-every 2 \
    --out "$OUT/smoke_${OBJ}.clm" --gauges-out "$OUT/smoke_${OBJ}.json"
done
echo "=== g_gates connection check (production core/clm_decode.py mouth load) ==="
cd "$REPO"
python3 - <<'PY'
import sys, os
sys.path.insert(0, os.path.abspath("core"))
import clm_decode as clm
OUT = os.environ["SMOKE_OUT"]
ok_all = True
for obj in ("ce_marginal", "pc_bind", "pc_free_energy"):
    p = os.path.join(OUT, f"smoke_{obj}.clm")
    rb = open(p, "rb").read()
    dec = clm.clm_decodable(p)
    W = clm.clm_load_weights(p); loadok = bool(W.get("ok"))
    cfg = clm.clm_config(p)
    print(f"  {obj:<14s} clm_decodable={dec} load_ok={loadok} "
          f"d={cfg.get('d')} E={cfg.get('E')} L={cfg.get('L')} bytes={len(rb)}")
    ok_all = ok_all and dec and loadok
print("SMOKE_OK" if ok_all else "SMOKE_FAIL")
sys.exit(0 if ok_all else 1)
PY
echo "=== H_1641 SMOKE DONE ==="
