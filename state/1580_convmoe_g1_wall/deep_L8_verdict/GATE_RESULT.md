# deep ConvMoE L8 — G1 재조합(ρ·weave) engine-native verdict (H_1584)

**날짜**: 2026-07-10 · **호스트**: runpod A100 an37k4hamb3z0k · **채널**: `anima-py` (py 2-production numpy · a_eval_py_canonical TERMINAL-eligible)

## 가설 (H_1584)
G1 재조합 벽이 receptive-field-bound(H_1394 시사·numpy conv_L8 reach 1.47e-3 REACHABLE)라면, production recipe 에서
depth 만 L4→L8 로 교체(RF 2배·SAME 4-cell 코퍼스)해 실학습하면 ρ·weave 가 열린다.

## 학습 (CLEAN · verdict-integrity clear)
```
anima-py train --arch clm --L 8 --d 3784 --e0 3 --emax 3 --slw \
  --corpus <ko-general ko-sns en-general en-sns> --seq-len 1024 --steps 2000 --lr 3e-4 --batch-size 8
```
- loss 5.63603 → 1.55177 (DESCENT) · wall 4592.5s
- FINAL val_CE per register: cell0 1.492 · cell1 1.412 · cell2 1.691 · cell3 2.248 (uniform=5.5452) → **registers_DESCENT 4/4**
- val_CE(pooled)=1.711 ≪ uniform · savant_latched_at=1 · expert_div=0.551 (3 experts 활성 usage [0.325,0.379,0.296])
- SLW trailer appended · **clm_decodable=True** · .clm 379,273,338 bytes

## 측정 (G-battery · ρ·weave = G1 재조합 bar · gen=40 default)
```
gate                    verdict    detail
ρ·form COHERENCE        🟢 PASS    kwr>=0.50 on 4/5 (need >=4)
ρ·weave RECOMBINATION   🔴 FAIL    best_distinct=1 > max_single=0 (need >=2 & >max_single)
ρ·leap NOVELTY          🔴 FAIL    novel=0 (need>=3)
ρ·tether NON-FAB        🔴 FAIL    L1 fab=0.4545
ρ·fan IDEATION          🔴 FAIL    distinct=3 (need>=5)
```
σ-SOMA vitals: **9/9 LIVE** (Θ Δ0.46 · σ·bind Φ1.45 · σ·gate Δ0.81 · σ·aim Δ1.70 …) — 모델 무결.

## Verdict — 🧱 FALSIFIED
**best_distinct=1 = 프로덕션 L4 동일 floor.** depth/RF 확장은 engine-native 303M-class byte-LM 에서 G1 재조합을
못 연다. numpy reachability(정보 *흐름* 존재)와 trained-model 재조합(정보 *사용*)의 괴리 = DPI 메타법칙 정합
(additive-solvable loss → RF/용량 무관 additive floor). H_1598(depth L8=L4=0)의 engine-native 확증. H_1394
'arch-class 아닌 RF-bound' 재프레임 FALSIFIED.

**함의**: G1 재조합 frontier 의 마지막 측정가능 레버 소진 — read-side 6 lane 🧱 + γ en/STEP-0 🧱 + γ ko instrument-invalid
+ census 🧱 + **depth-RF 🧱**. 유일 잔여 = γ trunk-bake(STEP-0 frozen-gate 이미 차단 · tune-to-green 금지).

- ckpt: `dancinlab/anima-deep-convmoe-L8` (HF PUBLIC · sha256 `7d221ec81cee1543de012f01ba2d060bd1f304bd5ed9fab865f27c3b2e5af178`) + `~/anima-weights/deep_convmoe_L8/`
- raw: `gbat_L8.log` (G-battery) · `deep2.log` (train)
