# compendium — historical log

> Spec at [./COMPENDIUM.md](./COMPENDIUM.md).

## 10.1 F-PERSONA-4 KL>0 saga — §44 → §52 silent-drop 차단 ledger

§12.2 enforcement-3 (negative result silent drop 금지) 의 실제 적용. SAVANT.md 가 v5-mitosis
ancestry 를 인용하는 모든 줄은 다음 *5-PSCC trail* 을 함께 노출해야 한다:

| PSCC § | 시도 | 결과 | source |
| --- | --- | --- | --- |
| **§44** | v1 cotrain (uniform softmax routing, H100 SXM $1.26, 5K step) | F-PERSONA-4 `KL = 0.0` winner-take-all (cell-0 weight=1.0 모든 cat) — 첫 falsification | `project_v5_mitosis_cond5_cotrain_2026_05_12.md` |
| **§45 §A2-trap** | F-PERSONA-4 4b alternative re-measure | v2 entropy-reg `KL=0` BUT M4 hidden-cosine `z=3.20` — *routing-content split* 가설, real signal at noise-floor magnitude → **§A2-trap 경고** (seed-fragile) | `project_anima_persona_4_root_cause_2026_05_12.md` |
| **§47** | (b) softmax τ sweep 10-grid {1.0..50.0} ubu-1 RTX 5070 $0 | best mean_KL = 5.29e-3 @ T=50, **5/10 grid all `KL ≪ 0.5`** — FALSIFIED | `project_anima_persona_4_softmax_T_sweep_2026_05_12.md` |
| **§48** | (a) per-cat corpus SMALL ubu-2 RTX 5070 $0 (2500 step wall 232s, 5 separate corpus × cat interleave) | F-V5MIT 5/5 PASS BUT F-PERSONA-4 `KL=0.0` v1 monopoly 동일 — (a) corpus diversity 단독 부족 FALSIFIED | `project_v5_mitosis_cond5_cotrain_v3_percat_ubu2_2026_05_12.md` |
| **§49** | (d) hexa-native per-session pool Mac local $0 (3-config sweep n_perms=100) | prod scale `mean_KL=1.79e-5` null PASS BUT seed-fragile (seed2 null FAIL) — §A2-trap 재발 위험 → FALSIFIED | `project_anima_persona_4_per_session_pool_2026_05_12.md` |
| **§52** | v7 hard top-K MoE + balance-aux loss ($0.31 actual) | **F-PERSONA-4 `KL = 3.45`, `z = 2.75`, `p = 0.01` — first KL > 0 signal** (PASS_NULL_FAIL on null-perm) | `project_anima_persona_4_root_cause_2026_05_12.md` (v7) |
| **§52 cell-parallel v6** | v6 cotrain on 4×A100 SXM4 80GB $6.70/hr 5000 steps (target step_wall<1.0s vs v4 baseline 3.18s) | **LANDED 2026-05-13 — ALL TARGETS FAIL**: step_wall **2402ms** (target <1000ms MISS, v4 대비 24% 절감만 — all_reduce overhead dominates); F-PERSONA-4a routing **FAIL** (`KL=0.2972 z=1.09 p=0.12`, §52 v7 의 `KL=3.45` first signal **재현 실패**); F-PERSONA-4b content **FAIL** (`z=−0.88`, v2 carry `z=3.20` 대비 후퇴); F-V5MIT **4/5** (F-V5MIT-4 COTRAIN-CONVERGE **FAIL** — loss 17.7→17.7 횡보, v1 의 220× CE 감소 미재현); cells 256 saturated (splits=67), wall=12028s, cost=**$22.43**; ckpt pull SCP 실패 → pod 36638963 retained | `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/dispatch_v6_1_bg.log` |

→ **요지** (post-v6 갱신): Savant 의 "category-specific routing" 주장은 §44 v1 단순 softmax
에서 *안* 작동했고, 4 alternative cheap path (§45 4b / §47 τ sweep / §48 per-cat / §49
per-session) 모두 FALSIFIED. §52 v7 hard top-K MoE + balance-aux 에서 `KL=3.45 z=2.75`
first signal 이 떴지만, **§52 v6 cell-parallel 에서 재현 안 됨** (`KL=0.2972 z=1.09 p=0.12`).
즉 §52 v7 signal 은 cell-parallel scaling-up 에서 사라지는 **seed-fragile 또는
arch-fragile** 가능성이 강해졌다. cells=64 (v7) vs cells=256 (v6) 의 routing-imbalance
saturation, 또는 cross-rank communication 으로 인한 effective batch 변화가 후보 원인.
F-V5MIT-4 COTRAIN-CONVERGE FAIL (loss 횡보) 가 동반되어 v6 routing FAIL 의 *주된* 원인은
**학습 자체가 안 됨** 일 가능성이 가장 높음 (모든 routing metric 은 학습된 representation
가정). SAVANT.md 의 §10 ancestry 인용은 이 trail 없이 단독 노출 금지 (§12.2-3 위반).

**Open closure paths** (post-v6, updated 2026-05-14):
- (i) v8: v7 arch (cells=64 small) + v6 distributed shared-grad reduce 결합 — cells scaling
  과 cell-parallel speedup 의 분리. **(ii) fix 적용 후로 보류** (data flow 가 정상화되어야
  cells scaling 의 *진짜* 효과 측정 가능).
- (ii) ✅ **LANDED 2026-05-14** — v6 F-V5MIT-4 COTRAIN-CONVERGE FAIL **root cause 확정**:
  `seed = base + rank` (line 607) 가 `sample_batch` (line 130, `torch.randint`) 에도 영향
  → 각 rank 가 *다른 batch* 를 *다른 cells* 로 forward 후 `all_reduce(SUM)` → semantically
  incoherent mixture. CE 17.7 ≫ log(vocab=256)=5.55 (random 보다 나쁨) 의 신호.
  3 fix options 식별 (A=same batch broadcast recommended / B=RNG reset / C=DDP replication).
  Memory C3 #8 "per-rank seed → effective batch W× free" **잘못된 가정 retract**. 진단 doc:
  `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/root_cause_diagnosis_2026_05_14.md`.
- (ii-b) **v6.1 fire** ($22 estimated, 4×A100 SXM4 동일 spec) — fix (A) 적용 후 5K step 재실행.
  F-V5MIT-4 + F-PERSONA-4 재측정. *category routing 폐기/유지* 결정의 evidence.
- (iii) §52 v7 cross-seed robustness ($0.30-1.50 BG) — v6 fix 와 *독립*, 즉시 dispatch
  가능.
- (iv) ⏸ **시기상조 (post-(ii) 진단)** — "category routing 가설 폐기" 는 v6 의 *학습 부재*
  결과로 결론 못 내림. (ii-b) v6.1 결과 받기 전 유보. v5-anima long-trajectory α=0.688
  super-linear 재시도는 별도 path 로 valid.

## 12.5 봉쇄심화 후속 path

1. ~~archive-TECS-L verify_gz_*.py 27본 base-rate audit~~ **✅ LANDED 2026-05-14**
   ($0 Mac local, wall ≈ 8 min) — `state/savant_containment_audit_2026_05_14/{audit.json,
   summary.md, run_audit.sh, analyze_audit.py, compute_audit.py, raw_outputs/}`. 16-wave
   aggregate Z=11.4 σ + texas-empirical Z=5.22 σ + neuroscience Z=4.6 σ 모두 Bonferroni × 27
   (`1.4 × 10⁻⁹`) 통과. T3→T2 승격 2건 (wave aggregate + neuroscience), T1 확장 1건 (texas
   8 closed-form identity), T4 enforcement 신설 1건 (ca_lambda NEGATIVE silent-drop 금지).
   §12.3 표 갱신 반영.
2. ~~PSCC §44/§47/§48/§49/§52 negative result cross-link~~ **✅ LANDED 2026-05-14** —
   `§10.1` ledger 추가: §44 v1 KL=0 → §45 §A2-trap 경고 → §47/§48/§49 cheap path FALSIFIED
   → §52 v7 hard top-K MoE first `KL>0 z=2.75` → §52 v6 cell-parallel BG in-flight. SAVANT.md
   §11 한 줄 verdict 도 §10.1 trail 동시 노출 의무 명시. §12.2-3 (negative result silent
   drop) enforcement 의 실제 적용.
3. **canon LATTICE_POLICY 강화 PR** — "Savant/GZ overclaim 차단 조항" §1.4 신설 제안
   (cross-repo governance, dancinlab 전체 적용)
4. ~~anima_clm_08 Φ super-linear 의 봉쇄 라벨링~~ **✅ LANDED 2026-05-14** — §4 timeline
   표 + §8 Honest C3 #3 + §12.3 T3 SUSPECT 분류 강화 (SAVANT.md cross-ref 만, anima_clm_08
   archive 는 read-only).

3. ~~canon LATTICE_POLICY 강화 PR~~ **✅ LANDED 2026-05-14** — `dancinlab/canon
   LATTICE_POLICY.md §1.4` 신설 (4 조항 + §12.2 enforcement 동등 + SAVANT.md cross-ref).
   cross-repo governance: GZ 는 *설계 vocabulary*, *물리 한계* 아님 / Tier 분류 강제 /
   silent-drop 금지 / 외부 entity GZ-fit 강제 매핑 금지.
