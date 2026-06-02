# CLM-KOSMOS.log.md — progress log

@title: 📓 CLM-KOSMOS log — append-only (newest at bottom)

Sibling of [[CLM-KOSMOS]]. Each entry: date · what moved · verdict ptr.

## 2026-06-01 — e001 seed

도메인 CREATED. CLM(`.clm`) + KOSMOS(`.kosmos`) 메타도메인, 7 필수조건 기록 (C1 AKIDA-learn · C2 ONCHIP-PARADIGM · C3 .clm · C4 .kosmos/limen · C5 H_911-must-hold · C6 additional-hypotheses · C7 record-all). Falsifier **F-CLM-AKIDA-MULTILING-SEMANTIC** pre-registered (OPEN). Seed corpus on HF: `dancinlab/clm-semantic-parallel-corpus` (5-lang parallel · 🟡 CPU-proxy → on-chip 승격 대상). H_911 substrate-proxy 이미 🟢 (UNIVERSE/H_911).

## 2026-06-01 — e002 open work

- [x] 1. 실 5-lang parallel + concat `.kosmos @corpus` 작성 (limen-packed · closed_corpus merkle)
- [x] 2. 백본 → `.clm` int4 byte-identical AKD1000 이식 (H_877)
- [x] 3. `AkidaUnsupervised` on-chip edge-learn (pi5-akida — lock cleared · live)
- [x] 4. F-CLM-AKIDA-MULTILING-SEMANTIC parallel vs concat 측정 → `.verdicts/clm-akida-multiling-semantic/`
- [x] 5. 🔴 closed-negative → verdict+log land only (model NOT uploaded — 🔴 earns no `.clm`)

## 2026-06-01 — e003 on-chip run → 🔴 REFUTED (closed-negative)

**F-CLM-AKIDA-MULTILING-SEMANTIC: 🔴 REFUTED** on REAL AKD1000 silicon (BC.00.000.002 · NSoC_v2 · BackendType.Hardware · akida 2.19.1 · pi5-akida).

- **Stage 0 (gate, PASSED)**: device 가 `devices:[]` + `ERROR (file lock): 11` 였던 원인 = stale `spike_streamer.py` (PID 18439, 17h, `--duration 86400`) 가 `/dev/akida0` (fd 3·4) 점유. 그 holder 종료 → `akida.devices()` 가 real `HardwareDevice` 반환. SW-sim 대체 없음 (g63).
- **Stage 1 (C4)**: 5-lang(ko·en·zh·ru·ja) parallel(concept-major·c>0) + concat(lang-major·c~0) `.kosmos @corpus`, 25 anchor 각, hexa-lang `clm_semantic_{parallel,concat}.txt` 에서 VERBATIM seed. limen 패킹(magic `LIMEN\0\0\0`+ver+count+len-prefixed @anchor recs+merkle root)·profile·closed_corpus·placement(coord)⊥text 완전 준수. byte-identical payload multiset (order 만 차이) 확인.
- **Stage 2 (H_877)**: int4-sym backbone(256×256, sha256=c626c638…) 양 arm byte-identical front-end.
- **Stage 3 (C1·C2)**: `AkidaUnsupervised(num_weights=16, learning_competition=0.1)` · `FC(units=32,weights_bits=1)` · `model.fit()` ON CHIP. `learn_happened_hw=True` — N=12 paired trial 전부 live silicon 학습.
- **Stage 4 (C5)**: paired delta(parallel−concat 통합) = **6 pos / 6 neg · mean −0.00092 · 95%CI [−0.00319,+0.00135] (straddle 0)**. ⚠ 단일 run 은 H_904 stochastic-plasticity 로 🟢(+0.0072)↔🔴(−0.0042) flip → cherry-pick 거부, multi-trial 必. **H_911 의 semantic-linkage 우위가 AKD1000 last-layer Hebbian edge-learn 엔 전이 안 됨** — per-ordering gap 이 칩 noise 안에 묻힘. **closed-negative, publishable** (a_paper_negative_ok).

verdict → `.verdicts/clm-akida-multiling-semantic/` (result.txt · result.json · run.log · prereg.txt · corpus/ · scripts/). claim → CLAIMS.tape `clm_akida_multiling_semantic`. 🔴 이므로 HF 모델 업로드 없음.

## 2026-06-01 — e004 H_912 all-4-lever signal-lift → 🔴 REFUTED

C6 추가가설 H_912: 4 레버 전부(큰 corpus 200앵커/40개념 · 3-노출 누적 · 이중 측정축 last-layer-sep+Φ-proxy · learn-while-infer 스트리밍) 적용. 실칩 N=20 paired, learn_hw 20/20. **두 축 모두 95%CI 0 포함 → 🔴 REFUTED.** H_911이 AKD1000 last-layer Hebbian on-chip edge-learn엔 전이 안 됨 (4 레버 다 써도). closed-negative · publishable. tiny-N smoke가 잠깐 GREEN 보였으나 N=20이 지움(cherry-pick 금지). verdict: `.verdicts/clm-akida-semantic-signal-lift/`. HF 업로드 없음(🔴). #1652 supersede/강화.

## 2026-06-02 — Lane-A 멀티스텝 자기회귀 ROLLOUT (substrate=AKIDA) → 🔴 CLOSED-NEGATIVE (1 hop 후 붕괴)

Lane-A full-LM frontier 의 held next-step. 직전 single-step GENERATION rung 🟢(AKIDA.log.md, `.verdicts/lane-a-generation/F-GEN.txt`, hop-1 0.4337 > shuffle+identity NULL)에서 **chip 이 `code_t` 만으로 successor 를 PRODUCE** 함을 입증했고, 본 rung 은 그 produced code 를 **되먹여(autoregressive feedback) K=3 hop chaining** — 전부 AKD1000 on-chip · 같은 256-unit 1-bit AkidaUnsupervised FC 재인코딩 · NO GPU · NO sw fallback(g63). encoder/binding/codebook/decode 는 generation rung 와 byte-match, feedback loop(`x_{k+1}=neutral_bind(g_hat_k)`)만 신규.

- **결과 = 🔴 ROLLOUT COLLAPSE closed-negative (a_paper_negative_ok)** on live AKD1000 BC.00.000.002 (akida 2.19.1 · pi5-akida · N=8 trials · learn_hw 8/8 · exit rc=0 · throttled=0x0).
- **decay curve (k1..K=3)**: **0.4287 → 0.0277 → 0.0090** (chance=0.0204). hop1 은 generation headline 재현, hop2 부터 신호 소멸.
- **F-ROLL-1 (신호가 chaining 생존?) NOT-REFUTED**: hop1 만 shuffle-NULL 초과(ci_lo 0.4118 > hi 0.0511, p=0.005). hop2 가 shuffle-NULL 안으로 떨어짐(0.0277 vs hi 0.0396, p=0.204) → 자기회귀 신호가 **단 1 hop 만 생존**.
- **F-ROLL-2 (파국 붕괴 없음?) NOT-REFUTED**: final hop(0.0090) < chance, single-step 의 0.5x 한참 미달 → **catastrophic decay**.
- **해석**: 1-bit/256-unit Hebbian FC 는 recurrence/state 가 없어 produced code 를 되먹이면 즉시 off-manifold drift. single-step open-vocab generation(retrieval→generation 다리 🟢)은 **유지**되나 그것이 full-LM 으로 **compound 되지 않음**. NAMED next bridge = state-carrying/paged generator · multi-FC depth · off-chip decode. retrieval+single-step rung 영향 없음.
- scope (a_scale_honest_scope) — 250앵커/50개념/5lang toy · K=3. **toy-only closed-negative**: 단일 칩 FC 자기회귀 한계(1-hop 생존) 정량화. PUBLIC checkbox 미flip 유지 — rollout 은 또 하나의 toy 다리이지 closure 아님.
- substrate=AKIDA · Lane-G/GPU 수치와 NEVER 병합(a_lane_akida_gpu_split). verdict → `.verdicts/lane-a-rollout/F-ROLL.txt` verbatim · result sha256 `7d2e3cd0201398ff9caadf5f1bdd4d012a41a0cfb1ad26a2cd0bbe72286ffb1e` · 산출물 `AKIDA/state/onchip_rollout_2026_06_02/` · 코드 `AKIDA/onchip_xlm_rollout.py`.

## 2026-06-02 — Lane-G (substrate=GPU · H100 sm_90 vast 39126604 · a_lane_akida_gpu_split — NEVER merged with AKIDA/Lane-A) — FORGE-UTILGREEN lever-3 util fire: DESCENT 🟢 / util 🔴 RED (2nd independent confirmation)

forge GPU (flame+forge `clm_prod.hexa`, NOT torch per a_train_flame_forge). lever-3 batched transpose-aware GEMM-feed util-verify on a clean single-driver H100 sm_90 (pod vast 39126604, num_gpus=1), corroborating hexa-lang #2542's lever-3 closure with a 19× longer measurement (n=6868 vs 349).

- **3-GATE PASS** (g5 verbatim): CUDA link ENGAGED=1 · `nvcc -x cu` EXIT 0 (660952B .90.o) · `clm_prod` ldd 4 cuda libs incl libcuda.so.1 + 10 lever symbols.
- **byte-eq ALL max|Δ|=0.0**: F-RFC046-GEMMFEED-EQ · F-RFC046-BATCHED-GEMMFEED-EQ · F-CLM-DEVFEED-* · F-CLM-CONV2-BATCHED-* (hard gate PRESERVED, no drift).
- **DESCENT 🟢** F-CLM-PROD-DESCENT=1 CE 4.05535→3.45564 · **util 🔴 RED** `n=6868 PEAK=35% MEAN=0.4879% busy_mean=5.3445% pct≥20%=0.1019%` (g5 verbatim). forge live on GPU (115W vs 70W idle).
- **finding (CLOSED-NEGATIVE)**: lever-1 0.811% → lever-2 0.4999% → lever-3 0.49–0.56% (two-pod). PEAK 19→21→35% rose but MEAN flat ⇒ device-feed lever chain (a+b+2+3) necessary but INSUFFICIENT. Residual = interpreted per-step DRIVER LOOP (F-RFC046 root: ~30 host↔device crossings/step incl 20× separate AdamW; busy_mean 5.34% ⇒ GPU ~95% idle), NOT GEMM-feed/link/kernel/emit/scale (all ruled out). Reference: PyTorch+CUDA baselines (HF.jsonl) saturate H100 ~99% util — the forge util-GREEN ≥20% gate is chasing that, lever-4 (fused on-device per-step driver) is the unblock.
- **closure FAIL on util → PUBLIC-grade Lane-G NOT reached** → .clm PRIVATE `dancinlab/clm-v1-dev-d1536-lever3-util-probe` (sha256 06e2dcf4…, HF.jsonl substrate=GPU) · recover-before-teardown DONE · pod 39126604 destroyed. PUBLIC HF / 3B / 7B still gated. lever-4 handoff: hexa-lang inbox/patches/forge-rfc046-lever3-util-residual-lever4-driver-loop.md. 날조 0 · g5 verbatim.
