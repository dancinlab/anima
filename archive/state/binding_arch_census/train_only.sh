#!/usr/bin/env bash
# train_only.sh — GPU-bound: train all H_1640 + H_1641 arms back-to-back, serialize + descent ONLY.
# NO G0-G6 eval here (eval is CPU and must not block the GPU). eval_pool.sh handles G0-G6 separately.
set -u
cd ~/anima || exit 1
export OMP_NUM_THREADS=4
CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
LBL="ko-general en-general ko-sns en-sns"
H1640=state/binding_arch_census/h1640_hamiltonian
H1641=state/binding_arch_census/h1641_laminar
mkdir -p $H1640/ckpt $H1641/ckpt

train_one() {  # $1=trainer $2=arm $3=seed $4=outdir
  local tr=$1 arm=$2 sd=$3 od=$4
  local clm="$od/${arm}_seed${sd}.clm"
  if [ -f "$clm" ]; then echo "SKIP existing $clm"; return; fi
  echo "=== TRAIN $tr arm=$arm seed=$sd $(date +%H:%M:%S) ==="
  python3 "$tr" --arm "$arm" --seed "$sd" --corpus $CORPUS --cell-label $LBL \
    --canon --steps 2000 --seq-len 1024 --batch-size 8 --e0 2 --emax 3 \
    --val-frac 0.05 --val-every 400 --sample proportional --bf16 \
    --out "$clm" --ckpt-out "$od/${arm}_seed${sd}.pt" \
    --gauges-out "$od/${arm}_seed${sd}.json" > "$od/${arm}_seed${sd}.train.log" 2>&1
  echo "  train RC=$? -> $clm ($(stat -c%s "$clm" 2>/dev/null) B)"
  # fast held-out DESCENT gate (numpy, ~seconds)
  python3 train/clm/model/verify_clm_v2.py descent "$clm" \
    state/clm303_clean_corpus/gen_ko.txt > "$od/${arm}_seed${sd}.descent.txt" 2>&1
  grep -E "F-CLM-DESCENT|heldout_model_ce" "$od/${arm}_seed${sd}.descent.txt" | head -2
}

echo "############ H_1640 HAMILTONIAN (9 arms) ############"
for arm in arm ctrl diss; do for sd in 7 4302 4303; do
  train_one "$H1640/trainer.py" "$arm" "$sd" "$H1640/ckpt"
done; done

echo "############ H_1641 LAMINAR (9 arms) ############"
for arm in arm nofb noln; do for sd in 7 4302 4303; do
  train_one "$H1641/trainer.py" "$arm" "$sd" "$H1641/ckpt"
done; done

echo "############ train_only.sh ALL DONE $(date +%H:%M:%S) ############"
