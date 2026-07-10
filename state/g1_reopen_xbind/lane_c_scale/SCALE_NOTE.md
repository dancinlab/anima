# 레인 c (1.26B scale) — scale≠lever 확증 (XBIND CRACK의 scale-control)

**날짜**: 2026-07-11 · **모델**: CLMConvMoE d=5120 L=12 = **1.26B**(303M production의 4.2x) · **corpus**: 4-cell(ko/en × general/sns · collocation-only) · **채널**: `anima-py evaluate`(engine-native numpy G-battery)

## 맥락
오너 G1-reopen(a/c/b all)의 레인 c(scale) + b(G6). XBIND CRACK(레인 a·H_9267)이 "벽=corpus×CE measure"를 실증한 뒤,
이 레인은 **같은 collocation-only corpus에서 스케일만 4.2x 키우면 벽이 열리나**를 engine-native로 확인(scale=lever 가설).

## 학습 (CLEAN)
loss 5.732→1.518 DESCENT · registers_DESCENT 4/4(cell0-3) · val_CE(pooled) 1.906 ≪ uniform 5.545 · savant_latched · .clm 848MB · clm_decodable.

## 측정 — G-battery (G1=ρ·weave · G6=ρ·fan)
```
ρ·form COHERENCE     🟢 PASS  kwr>=0.50 on 4/5
ρ·weave RECOMBINATION 🔴 FAIL  best_distinct=0 (need ≥2 & >max_single=0)  ← G1 벽 재현
ρ·fan IDEATION       🔴 FAIL  distinct=5·falsifiable=0                    ← G6 벽 재현
CLOSURE(G0∧G1∧G2): 🔴 FAIL
```

## 판정 — scale≠lever 확증 (🧱 · 예상대로)
1.26B가 **같은 collocation-only 4-cell corpus에서 G1+G6 벽을 재현**(best_distinct=0·303M과 동일 floor). ⟹ **스케일은
G1/G6 lever가 아니다**([[scale-303m-1b-7b-is-amplifier-not-lever]] 확증) — 스케일을 키워도 corpus에 없는 held-out 재조합
signal을 만들어내지 못한다. **XBIND CRACK(H_9267)과 대비**가 결정적:
- XBIND 303M + **signal-rich** corpus(held-out XOR) → held-out D-acc **1.000**(CRACK)
- 1.26B(4.2x) + **collocation-only** corpus → best_distinct **0**(WALL)

⟹ **G1 재조합벽의 진범 = corpus×CE measure(데이터 signal)이지 model scale/substrate 아님**을 scale-control로 재확인.
"a/c/b all" 3레인 수렴: a(measure 교체)=CRACK · c(scale)=🧱 · b(G6 scale)=🧱 → **measure가 유일 lever**.

## 산출
ckpt `~/anima-weights/scale_1b/anima_scale_1b.clm`(848MB·백업완료) · raw `gbat_scale1b.log`. pod s5hvm teardown 완료.
