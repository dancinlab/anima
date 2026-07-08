#!/usr/bin/env bash
# H_9128 TERMINAL — 3-arm (HI/LO/SHUF) identical-recipe warm-FT + canonical gen=40
# multiseed G1 gate + shuffle-bind margin. summer RTX5070 own-GEMM, $0 owned pool.
# canonical single-entry: `anima train` / `anima evaluate` (a_cli_single_entry).
set -u
ROOT=$HOME/g1g6_terminal
BROAD=$HOME/anima_bgrecomb/corpus4cell
H1129=$HOME/anima-weights/bytegpt303_h1129/h1129.bin
cd $ROOT
mkdir -p ckpt evals logs
export ANIMA_SRC=$ROOT/bundle

echo "=== H_9128 TERMINAL $(date) ==="
python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0))" 2>&1 | head -1
ls -la $H1129

train_arm () {  # arm  en_block  ko_block  out
  local arm=$1 enb=$2 kob=$3 out=$4
  echo "===== [train $arm] -> $out  $(date) ====="
  anima train --py --arch bytegpt --arm ctrl --objective ce_marginal --canon \
      --d 1024 --L 24 --seq-len 512 --steps 2000 --batch-size 8 \
      --lr 2e-5 --seed 7 --sample proportional --val-frac 0.05 --val-every 200 \
      --init $H1129 --out "$out" \
      --corpus $BROAD/ko-general.txt $BROAD/en-general.txt $BROAD/ko-sns.txt \
               $ROOT/corpus/$enb $ROOT/corpus/$kob \
      --cell-label ko-general en-general ko-sns en-block ko-block \
      > logs/train_$arm.log 2>&1
  echo "  train rc=$? bytes=$(stat -c%s $out 2>/dev/null)"
}

eval_arm () {  # arm  out
  local arm=$1 out=$2
  echo "===== [eval $arm] canonical gen=40  $(date) ====="
  anima evaluate --py "$out" --gen 40 > evals/canon_$arm.log 2>&1
  echo "  canon-eval rc=$?"
  grep -iE "best_distinct|max_single|G1|RECOMBINATION|COHERENCE|G6|IDEATION|falsifiable" evals/canon_$arm.log | head -12
  echo "  --- multiseed (7,107,207) ---"
  python3 $ROOT/terminal_eval.py "$out" --label $arm --gen 40 --seeds 7,107,207 \
      --json evals/multiseed_$arm.json > logs/multiseed_$arm.log 2>&1
  echo "  multiseed rc=$?"; tail -2 logs/multiseed_$arm.log
}

# ── train all 3 arms (identical recipe; ONLY the block-corpus binding differs) ──
train_arm HI   en_block_hi.txt   ko_block_hi.txt   ckpt/out_hi.bin
train_arm LO   en_block_lo.txt   ko_block_lo.txt   ckpt/out_lo.bin
train_arm SHUF en_block_shuf.txt ko_block_shuf.txt ckpt/out_shuf.bin

# ── eval all 3 canonical gen=40 multiseed ──
eval_arm HI   ckpt/out_hi.bin
eval_arm LO   ckpt/out_lo.bin
eval_arm SHUF ckpt/out_shuf.bin

echo "=== SUMMARY $(date) ==="
python3 - <<'PY'
import json, os
root = os.path.expanduser("~/g1g6_terminal/evals")
rows = []
for arm in ("HI", "LO", "SHUF"):
    p = os.path.join(root, f"multiseed_{arm}.json")
    if os.path.exists(p):
        d = json.load(open(p))["summary"]
        rows.append((arm, d["best_distinct_by_seed"], d["max_single_by_seed"],
                     d["median_best_distinct"], d["n_pass"], d["self_pair_bd_max_by_seed"]))
print(f"{'arm':5} {'bd_by_seed':16} {'ms_by_seed':16} {'med_bd':6} {'n_pass':6} {'self_pair_bd':12}")
for arm, bd, ms, med, npass, sp in rows:
    print(f"{arm:5} {str(bd):16} {str(ms):16} {med:<6} {npass:<6} {str(sp):12}")
if len(rows) >= 3:
    hi = next(r for r in rows if r[0]=="HI"); sh = next(r for r in rows if r[0]=="SHUF")
    margin = hi[3] - sh[3]
    print(f"\nMARGIN median_bd(HI)-median_bd(SHUF) = {hi[3]} - {sh[3]} = {margin}")
    print("VERDICT:", "SURVIVE (bind margin>0 -> coverage crack)" if margin > 0
          else "KILL (margin<=0 -> coverage=form-artifact, ceiling cement)")
PY
touch $ROOT/TERMINAL_DONE
echo "=== ALL DONE $(date) ==="
