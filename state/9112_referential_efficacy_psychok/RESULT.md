# H_9112 -- Referential-efficacy PSYCHO-K + MRR re-score -- RESULT

**VERDICT: GREEN REFERENTIAL-EFFICACY-MEASURABLE (real emits carry graded referent-legibility beyond shuffle)**

- threshold_real(configs acc>=0.5)=16 - threshold_shuffle=0 - delta=16 (bar>=1: PASS)
- mean_acc_real=0.982 - mean_acc_shuffle=0.125 - delta_sep=0.857 (bar>=0.15: PASS)
- oracle=claude-fable-5 (theta outside anima closure) - emits FROZEN engine-native (H_9111) - tier=DIRECTIONAL-on-external-oracle

## real arm (acc vs difficulty)
  K=2 t=full: acc=1.000 chance=0.500
  K=2 t=32: acc=1.000 chance=0.500
  K=2 t=16: acc=1.000 chance=0.500
  K=2 t=8: acc=1.000 chance=0.500
  K=4 t=full: acc=1.000 chance=0.250
  K=4 t=32: acc=1.000 chance=0.250
  K=4 t=16: acc=1.000 chance=0.250
  K=4 t=8: acc=1.000 chance=0.250
  K=8 t=full: acc=1.000 chance=0.125
  K=8 t=32: acc=1.000 chance=0.125
  K=8 t=16: acc=1.000 chance=0.125
  K=8 t=8: acc=0.857 chance=0.125
  K=14 t=full: acc=1.000 chance=0.071
  K=14 t=32: acc=1.000 chance=0.071
  K=14 t=16: acc=1.000 chance=0.071
  K=14 t=8: acc=0.857 chance=0.071
## shuffle arm
  K=2 t=full: acc=0.357 chance=0.500
  K=2 t=32: acc=0.357 chance=0.500
  K=2 t=16: acc=0.357 chance=0.500
  K=2 t=8: acc=0.286 chance=0.500
  K=4 t=full: acc=0.143 chance=0.250
  K=4 t=32: acc=0.071 chance=0.250
  K=4 t=16: acc=0.214 chance=0.250
  K=4 t=8: acc=0.143 chance=0.250
  K=8 t=full: acc=0.000 chance=0.125
  K=8 t=32: acc=0.000 chance=0.125
  K=8 t=16: acc=0.000 chance=0.125
  K=8 t=8: acc=0.071 chance=0.125
  K=14 t=full: acc=0.000 chance=0.071
  K=14 t=32: acc=0.000 chance=0.071
  K=14 t=16: acc=0.000 chance=0.071
  K=14 t=8: acc=0.000 chance=0.071

self-clone baseline: H_9111 established 0/7 (floor) -- engine-native anima-clone salience decoder.
