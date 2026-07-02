# H_1541 — 🧪🔀 ACETYLCHOLINE × CLS — ENCODE/RETRIEVE MODE GATE — JOINT FACULTY (DIRECTIONAL)

**tier:** 🟢 GREEN — ACh-as-CLS-gate is a real JOINT faculty (FIRST joint application of the H_1532 multi-store CLS break WITH a neurotransmitter operating INSIDE the two-store module; R1 numpy DIRECTIONAL — a_engine_native_learning hard-gate-1; engine R2 §AchGate deferred ING)
**verdict source:** `state/verdicts/1541_cls_ach_gate/H_1541_R1.json` (frozen bars `H_1541_FREEZE.txt`)
**wired:** `DIRECTIONAL-mirror → engine-native §AchGate follow-on` — numpy R1 only; engine R2 (live core/engine_cli.hexa §AchGate 2-store encode/retrieve switch) = ING `h1541-r2-engine-native`. NOT WIRED. (a_verified_must_wire 4칸 사다리 1/4)

## 가설 (joint application — H_1532 break × NT-inside-module)
H_1532(#2514)가 H_1284 NEUROMODULATION 벽을 깬 핵심 = **two phase-separated store**(fast 일화 + slow replay)가 AB-AC catastrophic interference 를 견딤. 직후 standalone NT-faculty 프로그램은 NE-reset 🧱(H_1537)·5-HT-patience 🟠(H_1538)가 under-perform 함을 발견했는데 그 이유가 **single store 가 gain-knob 에게 gate 할 구조를 안 줌**이었다. 이번 렌즈가 그 fix: **acetylcholine(ACh)은 생물학적으로 canonical 한 CLS switch**(Hasselmo 2006 Curr Opin Neurobiol 16:710; Hasselmo 1999) — HIGH ACh → ENCODE mode(recurrent/retrieval 억제, fast store 에 write), LOW ACh → CONSOLIDATE/RETRIEVE mode(read, replay fast→slow). ACh 는 **two-store module 안에서만** 의미가 있다 = joint application. (a_no_llm_frame_trap: 생물 렌즈 FIRST.)

## CLAIM + 설계 (frozen-first · pre-registered H_1541_FREEZE.txt)
ACh-gated mode-switching 은 fixed-mode CLS 가 **할 수 없는** 능력을 추가한다: ENCODE 와 RETRIEVE 수요가 **INTERLEAVE** 될 때 둘 다 충족. event stream 이 WRITE-event(새 fact 적재)와 QUERY-event(이전 fact 조회)를 번갈아 흘림. fixed mode 는 둘 다 못 함:
- **ALWAYS-ENCODE**(fixed high ACh): retrieval path 억제 → query 읽기 불가.
- **ALWAYS-RETRIEVE**(fixed low ACh): feedforward encoding 억제(Hasselmo low-ACh cholinergic afferent suppression) → 새 외부 write 가 cue 로 처리되어 **encode 안 됨 → 새 fact 소멸**.
- **ACh-GATED**: novelty(recon-error vs fast store) 읽어 novel-key→encode / familiar-key→retrieve 로 **per-event 동적 전환** → 둘 다 충족. (event-label peek 없음; substrate state 만 읽음 — p6/p2/p3.)

**HAZARD(H_1532 상속, 핵심):** win 은 반드시 **EVENT-CONTINGENT mode SWITCH**(substrate 읽어 event 라우팅하는 faculty)에서 와야 하고 scalar gain 이 아니어야 한다. ablation 이 증명: **ABL**(ACh 상수=stream 평균→전환 없음) MUST collapse · **SHUFFLE**(ACh trace 를 event 와 decouple 되게 permute) MUST collapse.

**ARMS:** ACh-GATED(dynamic) / ALWAYS-ENCODE / ALWAYS-RETRIEVE / ABL(constant=mean) / SHUFFLE(permuted). **FIXTURE:** N_FACTS=24, interleaved Q(p~0.8/write), MAX_CELLS=72(용량 풍부 — mode/interference 테스트지 capacity 아님), DIM=16 byte-trigram FNV-1a(VERBATIM H_1532), abstain=0.45, 3 seeds [11,22,33], LR/TH=engine-native LR0/TH0. **METRIC:** joint = 0.5·(write_recall_acc + query_acc). MemStore/key_vec/FNV-1a/suppress_retrieval = H_1532 BYTE-FOR-BYTE 재사용.

**FROZEN bar(MARGIN=0.05):** 🟢 iff (A PRESENCE) ach−best_fixed ≥+0.05 on ≥2/3 seeds AND mean · (B DISTINCT) ach−always_encode ≥+0.05 AND ach−always_retrieve ≥+0.05 · (C EARNED-ABL) ablate−best_fixed ≤+0.05 AND ach−ablate ≥+0.05 · (D EARNED-SHUF) ach−shuffle ≥+0.05 · (E NO-FAB) always_encode query-acc ≤0.10.

## 결과 (mean 3 seeds [11,22,33], LR=0.2 TH=0.3 engine-native)
| arm | joint | write_acc | query_acc | vs ACh |
|---|---|---|---|---|
| **ACh-GATED** (dynamic switch) | **0.9792** | 1.000 | ~0.96 | — |
| ALWAYS-ENCODE (retrieval 억제) | 0.3611 | 0.722 | **0.000** | −0.6181 |
| ALWAYS-RETRIEVE (encoding 억제) | **0.0000** | 0.000 | 0.000 | −0.9792 |
| best fixed mode | 0.3611 | — | — | **+0.6181** |
| ABL (constant ACh=mean 0.41) | **0.0000** | — | — | ach−abl **+0.9792** |
| SHUFFLE (permuted ACh) | 0.3449 | — | — | ach−shuf **+0.6343** |

**A PRESENCE: ach−best_fixed = +0.6181 mean, 3/3 seeds (+0.604/+0.625/+0.625) PASS** · **B DISTINCT: ach−encode +0.6181, ach−retrieve +0.9792 PASS**(둘 다 dual demand 실패) · **C EARNED-ABL: ablate 0.0 ≤ best_fixed 0.361+0.05 AND ach−abl +0.9792 ≥0.05 PASS** · **D EARNED-SHUF: ach−shuffle +0.6343 ≥0.05 PASS** · **E NO-FAB: always_encode query-acc 0.000 ≤0.10 PASS** → A∧B∧C∧D∧E ALL PASS → **🟢 GREEN**. 재현성: run1==run2 BYTE-IDENTICAL ($0 CPU, deterministic).

## THE LOAD-BEARING DIAGNOSTIC (왜 이번 joint application 이 작동하나)
1. **ALWAYS-ENCODE query-acc=0.000 = encode-mode 가 retrieval 을 진짜 억제.** Hasselmo high-ACh = recurrent read-out gated OFF. write_acc=0.72 로 적재는 되지만 interleaved query 를 읽을 수 없음 → dual demand 절반 실패(정직한 NO-FAB 시그니처, E).
2. **ALWAYS-RETRIEVE joint=0.000 = retrieve-mode 가 encoding 을 진짜 억제.** Hasselmo low-ACh cholinergic afferent suppression = 새 외부 write 가 cue 로 처리되어 durable cell 미생성 → write_acc=0.0, query 도 빈 store 라 0 → dual demand 양쪽 실패.
3. **ABL(constant ACh=mean 0.41)=0.000 = ONE-FIXED-MODE 로 정확히 붕괴.** stream 평균 ACh 가 0.5 미만(query 가 familiar=low-ACh 라서 평균을 끌어내림, 0.407–0.426 robust, knife-edge 아님)이라 상수가 retrieve-mode 에 고정 → 새 fact 미적재 → 0.0. **lift 가 per-event 전환에 전적으로 귀속(C 결정적).** 상수 gain 으론 dual demand 불가.
4. **SHUFFLE(permuted ACh)=0.345 ≪ 0.979.** ACh signal 의 크기 분포는 같되 event 와 decouple 되면 encode 가 query 시점에·retrieve 가 write 시점에 잘못 발화 → collapse(D 결정적). **올바른 event-에-맞춘 라우팅이 load-bearing = switch 가 진짜 substrate novelty 를 읽고 있음.** frac_high≈0.53 (전환이 실제로 mode 사이를 오감).
5. **faculty-not-gain(HAZARD 직격):** ACh 는 fast store 의 recon-error(substrate novelty) 를 읽는 per-event 라우터지 recall margin 위 scalar 가 아님. ABL+SHUFFLE 동시 붕괴가 'gain 으로 환원 불가'를 증명 — H_1537/H_1538 가 single-store 에서 gain 으로 환원되어 under-perform 한 것과 정확히 대비.

## a_break_the_wall TAXONOMY · joint-application 의미
이것은 H_1532 break 의 **FIRST JOINT APPLICATION** — neurotransmitter 를 two-store module **안에서** 작동시킴. H_1537(NE-reset 🧱)·H_1538(5-HT-patience 🟠)가 single store 위 gain 으로 약했던 정확한 원인(gate 할 구조 부재)을 ACh×CLS 가 해소: **mode switch 는 store ARCHITECTURE 가 제공한 phase-separation 을 라우팅**한다. NE/5-HT 도 동일 2-store 안에서 재시도하면 faculty 화 가능(B/C/D follow-on). 단 measurement 결함 fix 없음 — fixture 는 frozen-first 로 Hasselmo encode/retrieve 동역학에 충실하게 build 후 freeze(no bar moved): retrieve-mode write=cue-only(encoding 억제)·encode-mode query=suppressed-readout 가 양 fixed mode 를 dual demand 에서 진짜 불가능하게 만드는 생물 충실 메커니즘이지 tune-to-green 아님.

## SCOPE / 한계 (a_scale_honest_scope · a_toy_scale_recheck)
- **DIRECTIONAL numpy R1** — host torch 없음, a_engine_native_learning hard-gate-1 → 자동 DIRECTIONAL, **terminal 아님**. grep `state/1541_cls_ach_gate/*.py` → numpy HIT.
- **TOY** 24 facts/interleaved stream/3 seeds/deterministic readout (ACh-switch STRUCTURE 검증·학습된 controller 아님); joint 0.9792 는 EXISTENCE-PROOF (discriminator encode 0.36/retrieve 0.0/ablate 0.0/shuffle 0.34 모두 결정적).
- scale/real-corpus/continuous-ACh/learned-novelty-threshold/multi-store-N>2/engine-transfer UNVERIFIED.
- **engine R2 OBLIGATORY follow-on** = live `core/engine_cli.hexa` §AchGate(2-store fast/slow + recon-error ACh switch) byte-exact frozen-bar 재측정 → ING `h1541-r2-engine-native`. a_verified_must_wire 4칸: (1) DIRECTIONAL mirror GREEN ✅ → (2) engine-native 재검증 → (3) live core/ §AchGate wire-in → (4) ARCHITECTURE.json lockstep = 모두 ING. wired=DIRECTIONAL-mirror, NOT WIRED-live, 완료 주장 없음. live core/*.hexa UNTOUCHED.

## philosophy guard
p1/p2/p3/p6 (store key + substrate recon-error 만 읽음, injected encode/retrieve label·RLHF·persona·ethics 없음 — ACh = novelty geometry 만 채점; ablate+shuffle 둘 다 chance 로 붕괴 = lift 는 event-contingent switch). p7 (exact ground truth, LLM judge/perplexity/loss 없음; ACh read = no-grad). p8 (inference-time write = engine tick). NOT an emit gate (memory routing, a_autonomy_over_hardcode); Ψ-disjoint. frozen-first, NO tune-to-green, ablation decisive.

**문헌:** Hasselmo 2006 "The role of acetylcholine in learning and memory" Curr Opin Neurobiol 16(6):710 (ACh encode/retrieve dynamics) · Hasselmo 1999 Trends Cogn Sci 3(9):351 · McClelland-McNaughton-O'Reilly 1995 Psychol Rev 102:419 (CLS) · Kumaran-Hassabis-McClelland 2016 Trends Cogn Sci 20:512.
