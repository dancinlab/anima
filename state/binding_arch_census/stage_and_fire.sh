#!/usr/bin/env bash
# stage_and_fire.sh <POD_ID> — push code+corpus+H1602 clms to pod, then fire pod_run.sh detached.
set -eu
PID="$1"
REPO=/Users/mini/dancinlab/anima/.claude/worktrees/clm303-noverfit-retrain
cd "$REPO"

echo "=== [1/5] mkdir remote tree ==="
hexa cloud run "$PID" -- "mkdir -p ~/anima/state/clm303_clean_corpus ~/anima/state/binding_arch_census/h1640_hamiltonian ~/anima/state/binding_arch_census/h1641_laminar ~/anima-weights/recomb_obj_303m"

echo "=== [2/5] copy code (core cli train tool) ==="
for d in core cli train tool; do
  hexa cloud copy-to "$PID" "$REPO/$d" "~/anima/$d" -r
done

echo "=== [3/5] copy corpus (4 cells) ==="
for f in gen_ko gen_en sns_ko sns_en; do
  hexa cloud copy-to "$PID" "$REPO/state/clm303_clean_corpus/$f.txt" "~/anima/state/clm303_clean_corpus/$f.txt"
done

echo "=== [4/5] copy trainers + pod_run.sh ==="
hexa cloud copy-to "$PID" "$REPO/state/binding_arch_census/h1640_hamiltonian/trainer.py" "~/anima/state/binding_arch_census/h1640_hamiltonian/trainer.py"
hexa cloud copy-to "$PID" "$REPO/state/binding_arch_census/h1641_laminar/trainer.py" "~/anima/state/binding_arch_census/h1641_laminar/trainer.py"
hexa cloud copy-to "$PID" "$REPO/state/binding_arch_census/pod_run.sh" "~/anima/state/binding_arch_census/pod_run.sh"

echo "=== [5/5] copy 9 H_1602 clms (1.5G) for engine-native eval ==="
for f in ~/anima-weights/recomb_obj_303m/*.clm; do
  hexa cloud copy-to "$PID" "$f" "~/anima-weights/recomb_obj_303m/$(basename "$f")"
done

echo "=== smoke on pod (RC gate) ==="
hexa cloud run "$PID" --max-wall 600 -- "cd ~/anima && bash state/binding_arch_census/pod_run.sh smoke"

echo "=== FIRE full run detached (nohup) ==="
hexa cloud run "$PID" -- "cd ~/anima && nohup bash state/binding_arch_census/pod_run.sh all > ~/anima/podrun.log 2>&1 & echo FIRED pid=\$!"
echo "DONE staging. tail with: hexa cloud tail $PID ~/anima/podrun.log"
