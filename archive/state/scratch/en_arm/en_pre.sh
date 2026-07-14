set -u
# EN pretrain — the base the whole EN arm rests on. It has to learn TWO things from C34-EN:
#   (a) the polarity of the 20 SEEN stems, from the 960 arrow lines
#   (b) the NEGATION OPERATOR, from the 480 negated arrow lines
# and it must NOT have seen a held-out stem in an arrow line or in any negated context (I1/I2, which
# the corpus builder verified and an independent grep re-verified).
#
# The positive control comes right after: SEEN flip1 must be alive on this base BEFORE any CPT runs.
# If the operator did not install, the EN arm is INVALID and no CPT number from it means anything —
# that is the gate H_9322 never had.
A=$HOME/decon/venv/bin/anima-py
cd $HOME/en_arm; export OMP_NUM_THREADS=4 PYTHONUTF8=1
for S in 7 11; do
  $A train --arch clm --canon --emax 3 --e0 2 \
     --corpus c34_en_s${S}.txt --cell-label en-general \
     --steps 20000 --batch-size 8 --seq-len 128 --lr 3e-4 --bf16 --seed $S \
     --out en_c34_s${S}.clm > pre_s${S}.log 2>&1
  echo "PRETRAIN_s${S}_DONE rc=$?"
done
echo "EN_PRETRAIN_ALL_DONE"
