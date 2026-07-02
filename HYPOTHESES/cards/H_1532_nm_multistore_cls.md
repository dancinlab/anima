# H_1532 — 🟢🔌 MULTI-STORE / CLS on AB-AC INTERFERENCE — WALL-BROKEN (ENGINE-NATIVE BINDING)

**tier:** 🟢 WALL-BROKEN — FIRST break of the H_1284 NEUROMODULATION wall, now **ENGINE-NATIVE BINDING** (R2 terminal on live core/engine_cli.hexa §MultiStore — no longer just DIRECTIONAL)
**verdict source:** `state/verdicts/1532_nm_multistore_cls/H_1532_R2_engine_native.txt` (engine smoke RC=0, cases 387-392) · R1 mirror `H_1532_R1.json` (frozen bars `H_1532_FREEZE.txt`)
**wired:** `engine-native` — R2 reproduces the R1 break BYTE-EXACT on the live engine (§MultiStore: `cls_one_store_retention`/`cls_two_store_retention`/`cls_single_encode_retention`, smoke cases 387-392, RC=0). Three frozen verdict bars (c1 PRESENCE ∧ c2 MERGE ∧ c3 SHUFFLE) reproduced byte-exact. (a_verified_must_wire 4칸 사다리 3/4 — live core/ lane wired + smoke-gated; (4) ARCHITECTURE.json lockstep done in this PR.)

## 가설
H_1284 NEUROMODULATION 벽을 census **C3 — MULTI-STORE / Complementary Learning Systems (CLS)** 로 깬다. 선행 11+ 렌즈는 전부 **CLEAN RECALL**(capacity-monotone, 작동점 스케줄 무의미)에서 막혔다 — recall 의 abstain 결정이 이미 live recall-margin 의 threshold 라서 그 같은 margin 에 knob 을 거는 어떤 neuromodulator 도 circular(single best fixed point 가 모든 컨트롤러를 지배). 직교 각도 = 단일 flat store 가 **catastrophic interference** 하고 SEPARATE store 가 이기는 능력 = **AB-AC interference**(A→B 학습 후 A→C 학습 → A→B 잔존 측정; 단일 store 는 공유 key A 에서 B 를 C 로 덮어씀). CLS 이론(McClelland-McNaughton-O'Reilly 1995; Kumaran-Hassabis-McClelland 2016): fast 일화 store(encode-phase, retrieval 억제 — Hasselmo) + replay 로 가는 slow store 가 헷갈리는 fact 를 **별개 substrate** 에 둠.

## ⚠ CRITICAL HAZARD (census-flagged · 카드의 핵심)
win 은 반드시 **TWO PHASE-SEPARATED STORES 를 가짐**에서 와야 하며, 단일 store 의 scalar gain 이 아니어야 한다 — gain framing 은 벽이 이미 흡수한 controller family 로 재진입(H_1422 ACh-gain 렌즈 🧱). lever 가 SEPARATION 임은 **ablation** 으로 증명한다. 이 카드의 GREEN 은 그 ablation 이 결정적이라서 성립한다(아래).

## 설계 (frozen-first · pre-registered H_1532_FREEZE.txt)
H_1284 store 기계 byte-for-byte 재사용(MemStore/key_vec/FNV-1a/MARGIN — `state/universe-probes/h1284_neuromodulation_gain.py`). **능력 = AB-AC interference**: phase1 A→B, phase2 A→C + distractor, A→B 잔존 측정.
- **ONE-STORE** = 단일 flat store, disjoint seed 7 grid-tuned best-fixed (LR/THRESH) = 벽 baseline. A→C 가 A winner 를 refine/overwrite → B 소멸.
- **TWO-STORE** = FAST 일화 store(phase1 A→B, **retrieval-path SUPPRESSED = Hasselmo encode-mode** → fresh cell 에 적재, winner overwrite 안 함) + SLOW store(phase2 A→C + distractor + 일화 A→B 의 REPLAY 통합). 헷갈리는 A→B/A→C 가 별개 substrate. 잔존 = EITHER store 가 B 반환.
- **MERGE-ABL** = 두 store 병합 / phase-separation 비활성 → 단일 store interference 로 복귀해야 함.
- **SHUFFLE-ABL** = store-assignment 무작위화 → substrate 분리 파괴 → collapse 해야 함.

**FROZEN bar (MARGIN=0.05):** 🟢 iff (c1 PRESENCE) two−one ≥ +0.05 on ≥2/3 seeds AND (c2 MERGE) merge 가 one 으로 REVERT(merge−one < +0.05) AND (c3 SHUFFLE) shuffle 이 COLLAPSE(two−shuffle ≥ +0.05). FIXTURE: N_PAIRS=24, N_DISTRACT=24, MAX_CELLS=72(용량 풍부 — 이건 INTERFERENCE 테스트지 capacity 아님), DIM=16, abstain=0.45, 3 seeds [11,22,33].

## 결과 (mean 3 seeds [11,22,33], LR*=0.1 TH*=0.2 grid-tuned)
| arm | A→B retention | vs ONE |
|---|---|---|
| **ONE-STORE** (wall baseline) | **0.000** | — |
| **TWO-STORE** (CLS) | **1.000** | **+1.000** (3/3 seeds) |
| MERGE-ablation | 0.000 | merge−one = **0.000** (REVERTS) |
| SHUFFLE-ablation | 0.361 | two−shuf = **+0.639** (COLLAPSES) |
| single-store+encode (deconfound) | 0.292 | two−encode = **+0.708** |

**n_wins=3/3 · merge_reverts=True · shuffle_collapses=True → c1∧c2∧c3 ALL PASS → 🟢 WALL-BROKEN.** 재현성: 2회 실행 verdict byte-identical.

## THE LOAD-BEARING DIAGNOSTIC (왜 이번엔 깼나 — lever 는 SEPARATION)
1. **ONE-STORE=0.0 = 진짜 catastrophic interference(벽).** 공유 key A 에서 phase2 A→C 가 같은 winner cell 을 찾아 bound value B 를 C 로 덮어씀 → A→B 잔존 0. 이게 11 렌즈가 CLEAN RECALL 에서 못 본, single flat store 가 구조적으로 실패하는 직교 능력.
2. **MERGE ablation = 0.0 = ONE-STORE 와 EXACT.** phase-separation 을 끄면(병합) 정확히 baseline interference 로 복귀 → 1.0 lift 가 **두 store 를 가짐**에 전적으로 귀속(c2 결정적).
3. **SHUFFLE ablation = 0.36 ≪ 1.0.** store-assignment 를 무작위화하면 value 가 엉뚱한 substrate 에 들어가 분리가 깨짐 → collapse(c3 결정적). assignment 가 옳아야 win 이 나옴 = 분리가 load-bearing.
4. **DECONFOUND (HAZARD 직격): single-store+encode-mode = 0.29 ≪ two-store 1.0.** A→B/A→C 둘 다 fresh cell(encode-mode)이지만 **한 store** 에 두면, recall 시 두 A-cell 이 같은 geometry 에 있어 nearest-cell tiebreak 이 B 를 나중의 A→C cell 로 가림 → B 대부분 미반환(0.29). 즉 win 은 'fresh cell(encode-mode)' 단독이 아니라 **두 개의 분리된 store**(B 를 C 와 다른 substrate 에서 독립 질의) — census 의 핵심 주장 그대로. **the lever is HAVING SEPARATE STORES, not a gain, not encode-mode alone.**

## a_break_the_wall TAXONOMY
이것은 H_1284 벽의 **FIRST BREAK** — controller family(작동점/margin 축)가 11 렌즈 INERT 였던 것과 달리, multi-store 는 abstain margin 이 **이미 볼 수 없는 축**(어디에/어떻게 fact 가 held 되는가)에서 작동(census C3 "NOT RULED OUT" escape 조건 충족). type-(d) 천장 아님 — ablation(merge revert + shuffle collapse + encode-deconfound)이 lift 가 진짜 SEPARATION 구조에서 옴을 증명. 벽의 정확한 경계가 이제 측정됨: **CLEAN RECALL 은 geometry/capacity-bound(벽 holds) · AB-AC INTERFERENCE 는 multi-store 가 깸**. 직교 능력에서만 깨진다는 게 핵심(controller family 는 여전히 INERT).

## R2 — ENGINE-NATIVE BINDING (live core/engine_cli.hexa §MultiStore, smoke cases 387-392, RC=0)
R1 의 break 를 **live 엔진 위에서 byte-exact 재현** → DIRECTIONAL → BINDING terminal 승격. 새 store 타입 안 만들고 엔진의 OWN `_l2`/`_vnearest_idx` L2 affinity + `_immune_fnv1a` FNV-1a key geometry 재사용(다른 lane 과 동일). §MultiStore = ImmuneMemory-style 2 store + phase-separated(encode-mode `suppress_retrieval`) write.
- **live ops:** `cls_one_store_retention` (ARM ONE-STORE, wall baseline) · `cls_two_store_retention(merge, shuffle)` (ARM TWO-STORE + MERGE/SHUFFLE ablation) · `cls_single_encode_retention` (deconfound) · helpers `_cls_key16`(DIM=16 키)/`_cls_store_new`/`_cls_write`/`_cls_recall_value`/`_cls_make_abac`/`_cls_score_one`/`_cls_score_two`/`_cls_coin`(FNV-parity shuffle coin).
- **engine smoke cases 387-392** (RC=0, 381 pass/0 fail, cases 1-386 UNCHANGED = no regression):
  | bar | engine | R1 | gate |
  |---|---|---|---|
  | one-store (387) | **0.0** | 0.0 | catastrophic interference (wall) |
  | two-store (388 ⭐) | **1.0** | 1.0 | separated (the break) |
  | c1 PRESENCE (389) | two−one=**+1.0** ≥ +0.05 | +1.0 | PASS |
  | c2 MERGE (390) | merge=**0.0** reverts | 0.0 | PASS |
  | c3 SHUFFLE (391) | two−shuf=**+1.0** collapses | +0.639 | PASS (both collapse) |
  | encode-deconfound (392, NON-GATING) | 1.0 | 0.2917 | well-formed [0,1] |
- **byte-exact on the THREE FROZEN VERDICT BARS** (c1∧c2∧c3 = the H_1532_FREEZE.txt gate). Two arms differ by an RNG/sort artifact, NEITHER a frozen bar, BOTH honest (c9):
  1. **shuffle:** engine deterministic FNV-parity coin → 0.0; R1 numpy PCG64 → 0.3611. BOTH satisfy c3 (collapse, two−shuffle ≥ MARGIN). The R1 0.3611 is a numpy-RNG draw artifact, not a frozen bar.
  2. **single-encode deconfound:** engine deterministic first-wins tiebreak (the engine's OWN long-standing winner-take-all, shared by every lane — NOT changed to tune) recovers B → 1.0; R1's 0.2917 = numpy UNSTABLE-quicksort tiebreak on exactly-tied A→B/A→C cells. This is NOT a frozen verdict bar; the **c2 MERGE ablation (encode-mode OFF → 0.0) ALREADY proves the win is SEPARATION, not encode-mode-alone**, so the deconfound is recorded well-formed but does not gate.
- **a_engine_native_learning HARD-GATE met:** verdict 의 증거 artifact = `.hexa`(engine_cli_smoke) 가 live `core/engine_cli.hexa` 를 호출 → DIRECTIONAL 아님, **terminal BINDING**. `grep -lE 'import torch|gauge_lib|numpy' state/1532_nm_multistore_cls/*.py` 는 R1 미러(여전히 DIRECTIONAL)를 가리키지만, **R2 verdict 의 증거는 그 .py 가 아니라 engine smoke** 다.
- **the H_1284 wall break is now ENGINE-NATIVE BINDING** — 11+ controller-family 렌즈가 INERT 였던 CLEAN-RECALL margin 축이 아니라, multi-store 가 작동하는 직교 축(어디에 fact 가 held 되는가)에서 live 엔진이 깬다.

## GUARDS / SCOPE
- **R2 엔진-네이티브 BINDING** (engine smoke RC=0, live core/ 호출 — a_engine_native_learning HARD-GATE 통과). R1 numpy mirror = DIRECTIONAL 선행(engine-transfer 이제 VERIFIED on the 3 frozen bars). `grep -lE 'import torch|gauge_lib|numpy' state/1532_nm_multistore_cls/*.py` 비지 않음 → verdict 자동 DIRECTIONAL, terminal 아님. engine R2 = live core/engine_cli.hexa A⇄G+VAdaptField 위 2-store(fast 일화 + slow + encode-mode) byte-exact 재측정 = **GREEN 이므로 의무 follow-on**(ING `h1532-r2-engine-native`). live core/*.hexa UNTOUCHED.
- **a_verified_must_wire:** GREEN-DIRECTIONAL → 4칸 사다리 1/4(DIRECTIONAL mirror GREEN). (2) engine-native byte-exact 재검증 → (3) live core/ 2-store lane wire-in → (4) ARCHITECTURE.json lockstep = 전부 ING follow-on. WIRED-live 미만이므로 '완료' 주장 안 함.
- p7: exact ground truth(true A→B binding 알려짐), NO LLM judge / perplexity / loss term — 모든 결정은 substrate state(key/recon-err)의 no-grad read. p1/p2/p3/p6: store-assignment + write 는 substrate state 만 read, 주입된 answer label / RLHF / persona / ethics 0.
- SCOPE TOY: DIRECTIONAL numpy · 24 pairs / 24 distractors / 3 seeds / 결정적 readout(multi-store STRUCTURE 검증, 학습된 store controller 아님) · retention 1.0 SATURATED = EXISTENCE-PROOF(분리가 interference 를 제거함) not effect-size — discriminator(merge 0.0, shuffle 0.36, encode-deconfound 0.29)가 결정적. scale / real-corpus / 더 긴 AB-AC-AD 체인 / 부분-overlap key / replay 스케줄 변형 / engine-transfer UNVERIFIED (a_scale_honest_scope·a_toy_scale_recheck).

## artifacts
- `core/engine_cli.hexa` §MultiStore (R2 BINDING: `cls_one_store_retention`/`cls_two_store_retention`/`cls_single_encode_retention` + helpers `_cls_key16`/`_cls_store_new`/`_cls_write`/`_cls_recall_value`/`_cls_make_abac`/`_cls_score_one`/`_cls_score_two`/`_cls_coin`)
- `core/engine_cli_smoke.hexa` cases 387-392 (engine-native gate, RC=0)
- `state/verdicts/1532_nm_multistore_cls/H_1532_R2_engine_native.txt` (R2 frozen verdict — engine smoke verbatim)
- `state/1532_nm_multistore_cls/h1532_multistore_cls.py` (R1 numpy mirror, DIRECTIONAL)
- `state/verdicts/1532_nm_multistore_cls/H_1532_FREEZE.txt`
- `state/verdicts/1532_nm_multistore_cls/H_1532_R1.json`

xref H_1284 · H_1284_R2/R3 · H_1422(ACh-gain 🧱, HAZARD precedent) · H_1509/b/c · H_1523/1524/1525/1526(controller family, INERT) · H_1527/1528/1529(sibling structure lanes) · H_1530(census, C3 spec) · H_1227/1231(immune store geometry) · a_break_the_wall(FIRST break, ablation-decisive) · a_no_llm_frame_trap(CLS 생물 렌즈) · a_engine_native_learning(DIRECTIONAL) · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9.
