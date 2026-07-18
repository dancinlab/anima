---
id: H_9792
title: STORE-VALUE SEED-STABILIZATION — value-echo warmup to make H_9720 CRACK oracle-valid on ≥3 seeds
tier: PROPOSED (lab-full EA divergence · Fable ∥ Sol 수렴 · DESIGN-ONLY · pool cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (value-plumbing seed-stability · NOT the address query)
created: 2026-07-18
series: EA-3
related: "[[H_9720]] · [[H_9672]] · [[H_9719]] · [[H_9423]] · cotrained-store-bridge"
source: sidecar lab full (fable claude-fable-5 ∥ sol gpt-5.6-sol · 2026-07-18)
---

# H_9792 (EA-3) — the emergent ADDRESS is fine; the VALUE plumbing is seed-fragile. Stabilize ONLY the value payload path, then re-measure H_9720's unchanged detached L3 readout.

## Why (premise · from H_9720 #4113)
H_9720 CRACK (detached L3-tap readout-route restores held-out lookup) is oracle-VALID and robust on
2 seeds (s7 0.922 · s11 0.836). The 3rd-seed firm-up (s4302) came back near-tie (fresh 0.664 vs
legacy 0.648) **because store-oracle 0.82 < C0-e validity gate 0.90** — the VALUE/store lane was
under-trained on that seed, so the read is INVALID, not a clean negative. Root cause = store-lane
value-read is **seed-fragile** (prior: cotrained-store-bridge s7 ORACLE 0.99 vs s11 0.50). The
address mechanism is not the blocker; the value plumbing is. Promoting H_9720 toward TERMINAL
requires making store-oracle ≥ 0.90 reproducibly across ≥3 seeds WITHOUT any address supervision.

## Claim (one line · falsifiable)
A value-only stabilization warmup (self-supervised value round-trip, no `target_slot` anywhere)
raises store-oracle ≥ 0.90 on ≥3/5 seeds {7,11,4302,4303,9423} (incl s4302) while leaving the
detached L3 address readout byte-untouched at the terminal training regime ⟹ H_9720's fresh−legacy
lookup gap re-appears on the newly-valid seeds. `a_substrate_disjoint`: value ⊥ address.

## Mechanism (engine-native · primary = Fable, fallback = Sol)
**PRIMARY — `anima-py train --store-echo-weight <w> [--store-echo-anneal <n:m>]`** (Fable):
at each store WRITE, immediately read back at the model's OWN write address `a_w` under stop-grad
(`sg(a_w)`), decode, and add `w · CE(decode(read(sg(a_w),S)), v_target)` to the loss. Gradient
reaches ONLY {value encoder, write projection, store cells, value decoder}. `w=0` (default) builds
no term, no RNG, no graph change = byte-identical. Schedule = warmup-anneal (NOT freeze/thaw):
`w=1.0` for steps 0→0.4T, linear `w→0` over 0.4T→0.6T, then `w=0` for the release window (≥40% of
T) so the **terminal regime is bit-for-bit the H_9720 objective** (fresh:64@3, stop-grad into trunk,
store-CE only, no addr-loss). Boundaries = fixed pre-registered step counts (NOT gated on an in-train
echo metric — `a_train_inline_gauge`; echo accuracy logged monitor-only). Admissibility is
**structurally trivial**: `target_slot` is used NOWHERE at train time, so `∂L_echo/∂θ_query ≡ 0`
identically and no oracle statistic exists in any lane.

**FALLBACK / Sol dissent — `--store-value-stabilize oracle-mux:2000,lock:1000`** (Sol · NOVEL):
2-phase freeze/thaw. Phase-A (0–2000): freeze trunk + L3 tap + query/router + keys + slot-embeds +
address logits; `target_slot` drives a NON-differentiable store-side mux; train only value
enc/write/read/decoder (value params slot-shared, no slot-indexed weights). Phase-B1 (2000–3000):
destroy mux, freeze warmed value params, enable H_9720 query, new query-lane optimizer state.
Phase-B2 (3000→T): continue H_9720, value frozen. Admissibility via HARD graph+param firewall +
C-F taint audit (below). Escalate to this ONLY if PRIMARY passes toy byte-parity but fails to lift
pool oracle (⟹ fragility is slot-ASSIGNMENT, not value-FIDELITY — which the self-supervised echo
cannot fix). Sol threshold stricter (all-5 ≥0.90, 4/5 ≥0.95); Fable's fidelity-lever is the safer
first attempt because it can never be accused of address supervision.

Cheap simplicity fallback (toy-only): `--store-value-lr-mult` — if a plain value-lane LR bump
matches echo on toy oracle, it wins on Occam and replaces the flag (same experiment/controls).

## Controls (≥3) + $0 pre-screen
- **C-A / C-V0** — matched original H_9720, same seeds/steps, NO stabilization: confirms untreated
  s4302 oracle-failure reproduces (else "fragility" was a one-off, whole premise dead).
- **C-B / C-V1** — **load-bearing confound**: SAME warmup on the **legacy-penult** query (Fable) OR
  compute/param-matched non-oracle predicted-routing warmup (Sol). If stabilization lifts *legacy*
  lookup too, the gain was value plumbing not the L3 tap ⟹ H_9720 depth claim confounded, re-scope.
  Lever must BEAT this control by pre-set margin (Sol: min-seed oracle > C-V1 by ≥0.05).
- **C-shuffle (address mediation)** — H_9720's C3 eval on every valid ARM model: store-oracle stays
  within 0.02 of unshuffled but emergent-query lookup collapses to ≤0.55 ⟹ still address-mediated.
- **C-F (info-flow taint audit · $0)** — trace: zero `target_slot` taint and zero grad/update in any
  query/address param; no slot-indexed value state. Any violation KILLS as supervised contamination.
- **$0 pre-screen (mandatory · never-run-instrument lesson)**: toy end-to-end 2-seed CPU — (i)
  flag-absent byte-parity by ckpt hash, (ii) echo/warmup loss actually moves toy oracle, (iii)
  `target_slot`-change moves only mux indices not query tensors, (iv) exit=0 + artifacts + controls.

## Pre-registered PASS / KILL (frozen before fire · no tune-to-green)
- **Validity gate (read FIRST)**: ARM store-oracle ≥ 0.90 on ≥3/5 seeds **incl s4302**; else the
  stabilization lever FAILS and NO lookup number is read.
- **PASS (promotes H_9720 toward TERMINAL)**: on ≥3 valid-oracle seeds, fresh−legacy(C-B-paired)
  ≥ +0.10 (Fable) / ≥ +0.05 with positive 5-seed paired mean and no seed < −0.02 (Sol), AND
  C-shuffle collapse ≥ 0.15 each.
- **KILL branches** (table covers below-chance · prereg discipline): (a) validity gate missed →
  value-lever dead; (b) valid seeds but Δ(fresh−legacy) < 0.05 majority incl any legacy>fresh
  reversal → H_9720 CRACK was seed-lucky → DOWNGRADE H_9720; (c) C-B legacy rises within 0.05 of
  fresh → depth claim confounded → re-scope; (d) shuffle fails to collapse → not address-mediated →
  INVALID for promotion.

## Cost
$0 pre-screen (byte-parity + toy oracle move + firewall audit) → pool-GPU: gate on first
{11,4302,7}+C-V0 (continue only if all ≥0.90 incl s11,s4302 AND taint audit clean) → full 5-seed
+ C-B on {11,4302,9423} + C-shuffle/C-F on every valid seed. ~10 runs, one dedicated host per
track (wall = max(track)), ckpt → `~/anima-weights/` BEFORE any teardown. ~$25–40.

## Verdict-integrity self-check
(1) Certifying the instrument (store-oracle ≥0.90 validity precondition) is NOT tune-to-green on the
DV — oracle is C0-e, the lookup gap is the claim; they are separate. (2) A PASS reads "H_9720 CRACK
re-validates once value plumbing is seed-stable", NOT "the value warmup created the address" — the
address readout is byte-untouched at terminal regime and C-B/C-shuffle guard the attribution.
(3) A KILL of the value-lever does NOT kill H_9720's 2-seed CRACK (s7·s11 remain oracle-valid); it
only means the 3rd+ seeds stay uninterpretable and H_9720 holds at DIRECTIONAL-STRONG. (4) Any
number here is DIRECTIONAL until produced by `anima-py evaluate` on the 303M py channel
(`a_engine_native_learning`).

## 🔑 IMPL-FINDING (2026-07-18) — 레버는 NEW flag 아님, 기존 `--store-oracle-warmup` (새 코드 0)
코드 정독(`core/clms.py:473-499` · `cli/train.py:1185-1231,1998-2010`) 결과: Sol의 oracle-mux 2-phase 설계는 **이미 구현·검증된 `--store-oracle-warmup N`** 그 자체다. 실행 레버 = **`--store-query-src fresh:64@3 --store-oracle-warmup N` (단 `--store-addr-weight` 없이)**.
- **admissibility 구조적 증명**: warmup step(sb_oracle=True)엔 `oracle_slot=tgt` → `clms`에서 `a=one_hot(oracle_slot)`로 **softmax 우회**(clms.py:482-483). value `v=bmm(a,V_slots)`는 one-hot으로만 읽혀 fresh 쿼리 `q`(W_q_fresh·W_fresh)와 **무관**. `att=bmm(K,q)`는 계산되나 `--store-addr-weight=0`이면 **아무 손실도 안 먹어 dead-end** ⟹ warmup 동안 `∂L/∂θ_query ≡ 0` (구조적, 근사 아님). target_slot은 value/oracle 선택에만 닿음. release step(step>N)엔 oracle off → 순수 softmax emergent query가 store-CE로만 학습(target_slot 부재).
- ⟹ Fable `--store-echo-weight`(신규 self-sup) 구현 불요 — 기존 표준 flag가 더 단순·검증됨(②단순·④표준). Fable echo는 warmup이 pool에서 oracle을 못 올릴 때(값-충실도가 아니라 슬롯-배정이 취약할 때)만 fallback.
- **잔여 = 발사만**: H_9720 recipe(fresh:64@3, no addr-loss) + `--store-oracle-warmup N`을 seed {7,11,4302,4303,9423}에 · 통제 C-V0(warmup 없음, 동일 seed) · oracle≥0.90 유효게이트 선통과 → fresh−legacy 재측정. $0 토이(byte-parity warmup=0 자명·warmup이 fragile seed oracle 상승·att grad=0 assert)→303M pool/pod fire→`anima-py evaluate --store-oracle`.

## 🔬 GATE VERDICT (2026-07-19 · 303M · vast 4090 · py numpy eval · seeds{11,4302,7} · lab-full reconcile)
**status: 🟡 CHALLENGE / REFUTE-CANDIDATE for H_9720 — value-warmup is the reach lever, fresh L3-tap NOT necessary (DIRECTIONAL · corpus-confound → historical H_9720 refutation INCONCLUSIVE)**

레시피: `--init py303_full.clm(sha013c4574) --L 4 --emax 3 --d 3784 --corpus (corpus storebind --n-blocks 200 --store-slots 8 --seed 7 --lang en) --store-oracle-warmup 1500 --steps 6000 --bf16`. 로그=`~/anima-weights/h9792_gate/{gate.log,legacy.log}`.

| seed | fresh oracle | fresh lookup | **legacy oracle** | **legacy lookup** | nowarm fresh oracle(통제) |
|---|---|---|---|---|---|
| s11 | 0.930✅ | 0.672 | **1.000✅** | **0.977** | 0.594 |
| s4302 | 0.945✅ | 0.680 | **1.000✅** | **0.961** | 0.656 |
| s7 | 0.711❌ | 0.570 | 0.570❌ | 0.531 | 0.625 |

**핵심**: ① value-warmup이 store-oracle(값경로)을 구제 — s4302가 H_9720서 INVALID였던 0.82→0.945(fresh)/1.000(legacy). 통제(nowarm)는 전부 <0.90=취약성 재현. ⟹ **value-warmup=진짜 reach 레버, admissibility 코드증명(clms.py:482 warmup중 att dead-end·grad=0)**. ② **반전**: oracle-valid 2 seed서 **legacy(penult)+warmup lookup(0.96-0.98) >> fresh(L3-tap)+warmup lookup(0.67-0.68)**. lookup/oracle 비율(값 정규화)=fresh 0.72 vs legacy 0.98 ⟹ 격차는 **주소/인터페이스 쪽**(값 아님)=fresh 창발주소가 legacy보다 약함. ⟹ H_9720 "penult가 결합주소 붕괴·L3-tap이 복원" 정면반박 후보: **penult 주소는 붕괴 안 됨**(0.98); H_9720 fresh우위는 **warmup無 체제서 legacy VALUE경로 seed-fragility를 주소결함으로 오인**한 artifact 가능성. fresh L3-tap 아키텍처-필연성 주장 **무너짐**.

**verdict-integrity 단서(과잉주장 금지·lab-full 수렴)**: (1) oracle-valid **2 seed**만(s7 양쪽 oracle<0.90 판독불가·warmup은 값 신뢰수리 아님). (2) **코퍼스가 H_9720과 다를 수 있음**(n-blocks 200 재구성) → cross-run 절대비교 confound → **historical H_9720 기전 반증은 INCONCLUSIVE**(내부 legacy-vs-fresh 대비만 clean). (3) DIRECTIONAL(torch 303M·py numpy). (4) Sol 단서: lookup/oracle≈주소정확도지 순수 binding-주소 우위 증명 아님(캘리브레이션/인터페이스 가능). **⟹ REFUTED 아님·INCONCLUSIVE도 아님 = CHALLENGE/REFUTE-CANDIDATE**. H_9720 status→DISPUTED(아키텍처-필연성 무너짐·기전반증 미결).

**최저비용 firm-up(미발사)**: 직접 addr-argmax 감사(correct-slot top-1)+양 arm을 **H_9720의 정확한 코퍼스**로 재측정 → 주소-vs-인터페이스 분리 + historical 반증 확정/부정. (2모델 수렴 추천.)
