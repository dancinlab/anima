#!/bin/bash
# H_1464 PROCESS-ISOLATION engine-native decode.
# Root cause of the 91GB OOM = hexa decode-runtime noop-free leak that ACCUMULATES
# across fragments inside one long-lived process (resident weight ~5GB is normal;
# the climb to 91GB+ is leaked transient never freed). FIX (no bootstrap): spawn a
# FRESH `hexa` process per fragment so RSS resets to ~0 between frags → leak never
# stacks → all 90 frags complete. 1-frag peak RSS ≈ weight + 1-frag transient.
#
# Each per-frag process calls the SAME live core/bytegpt_decode.hexa via
# engine_decode_batch_cli.hexa (engine-native; a_engine_native_learning HARD-GATE)
# with a 1-line jobs file, APPENDING `tag<TAB>text` to the arm's out file
# (commit-early/resumable: a re-run skips tags already present).
#
# usage: run_decode_isolated.sh <repo_root> <out_dir> <concurrency>
set -u
ROOT="${1:?repo root}"
OUT="${2:-/root/h1464_decode}"
CONC="${3:-4}"
D="$ROOT/state/1464_pairing_contrastive_bind"
BINS="$D/bins"
JOBS="$D/jobs.tsv"
HEXA_CLI="$D/engine_decode_batch_cli.hexa"
GEN=110; TOPK=40; TEMP=700
mkdir -p "$OUT" "$OUT/fragjobs" "$OUT/logs"

# 1) split jobs.tsv into one file per fragment (idx-tagged)
i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  printf '%s\n' "$line" > "$OUT/fragjobs/frag_$(printf '%03d' $i).tsv"
  i=$((i+1))
done < "$JOBS"
NFRAG=$i
echo "SPLIT $NFRAG fragments per arm"

# tag set already present in an out file (for resume)
have_tag() { local out=$1 tag=$2; [ -f "$out" ] && grep -qF "$tag	" "$out"; }

# 2) build the work queue: arm x frag
declare -a QUEUE
for arm in pairing shuffle base; do
  for f in "$OUT"/fragjobs/frag_*.tsv; do
    QUEUE+=("$arm|$f")
  done
done
echo "QUEUE ${#QUEUE[@]} tasks (3 arms x $NFRAG frags), concurrency=$CONC"

run_one() {
  local arm=$1 fj=$2
  local fid; fid=$(basename "$fj" .tsv)
  local out="$OUT/out_${arm}.txt"
  local tag; tag=$(cut -f2 "$fj")
  if have_tag "$out" "$tag"; then echo "SKIP $arm/$fid ($tag present)"; return 0; fi
  local tmp="$OUT/logs/${arm}_${fid}.log"
  # FRESH process per fragment — RSS resets on exit (the isolation that defeats the leak)
  hexa run "$HEXA_CLI" -- "$BINS/${arm}.bin" "$fj" "$out" "$GEN" "$TOPK" "$TEMP" \
     > "$tmp" 2>&1 < /dev/null
  echo "DONE $arm/$fid -> $(grep -c '	' "$out" 2>/dev/null) lines in out_${arm}"
}
export -f run_one have_tag
export OUT HEXA_CLI BINS GEN TOPK TEMP

# 3) bounded-concurrency dispatch
running=0
for task in "${QUEUE[@]}"; do
  arm="${task%%|*}"; fj="${task##*|}"
  run_one "$arm" "$fj" &
  running=$((running+1))
  if [ "$running" -ge "$CONC" ]; then wait -n; running=$((running-1)); fi
done
wait
echo "ALL_DECODE_DONE"
for arm in pairing shuffle base; do
  echo "out_${arm}: $(grep -c '	' "$OUT/out_${arm}.txt" 2>/dev/null) / $NFRAG fragments"
done
