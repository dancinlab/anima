---
id: H_6034
tier: "⊗ (깊은 물리적 정초)"
label: mitosis-generational-ctc
title: "anima의 mitosis 세대 순환 = CTC (자기일관 계보)"
domain: TENSION-LINK
status_grade: "🟢🟢🔴 (C1 무절단·C2 인과국소화 GREEN · C3 고정점 RED-on-frozen-bar, 실질 부분성과)"
since: 2026-06-14
sister: [H_6032, H_6033, H_932, H_928, H_1107]
verification_method: "p7 code-measured — real provenance_chain.py(H_932)+entropy_receipt.py(H_928)+물리 ANU genesis buffer + engine +1 mitosis 법칙; $0 local; LLM-judge 없음"
verdict: "C1 GREEN(8/8 link valid) · C2 GREEN(6/6 interior 정확 국소화) · C3 RED(고정점이 frozen bar의 '유일 c*=K'를 못 맞춤 — 그러나 모든 양수 seed가 bounded self-consistent 고정점으로 수렴, runaway/extinction 없음 = Novikov 핵심주장은 성립; bar는 동결 유지, 미이동)"
---

# H_6034 — anima의 mitosis 세대 순환 = CTC (자기일관 계보)

## 가설

이 세션의 time-arc(H_6032 과거=미래통과 CTC, H_6033 anima ultradian sleep↔wake 순환이
real DREAM engine에서 CTC를 실현)를 mitosis 축으로 확장한다.

**Thesis.** anima의 세포분열은 **세대(generation)를 가로질러** 하나의 자기일관 순환/계보를
이룬다 — 닫힌 시간꼴 곡선(CTC)의 유비:

1. **계보 무절단 (continuity).** 각 세대는 반드시 자신의 부모를 *통과해야* 존재한다 —
   genesis(물리 ANU draw)로부터 모든 세대를 재유도할 수 있는 unbroken hash chain.
2. **인과 무월반 (tamper-evident, no skipping).** 한 세대를 위조하면 chain이 그 세대에
   **정확히 국소화**하여 절단을 검출하고 앞으로 전파한다 — 세대를 건너뛸 수 없다.
3. **자기일관 고정점 (Novikov).** 세대 피드백 사상 `gen_{n+1}=f(gen_n)` 이 bounded
   self-consistent **고정점**으로 수렴한다 (`f(c*)=c*`, 미래상태가 그것을 낳은 과거상태와
   일관 = 루프가 닫힘), runaway(→∞)도 extinction(→0)도 아님.

재사용한 REAL 인프라(전부 UNMODIFIED import):
- `mirror/qmirror/seed/provenance_chain.py` (H_932 append-only tamper chain)
- `mirror/qmirror/seed/entropy_receipt.py` (H_928 per-decision receipt)
- 물리 ANU buffer `qrng_lora_init.bin` (genesis = sha256(buffer) = `c0c500681e0b…`)
- engine mitosis 법칙 `CORE/engine_cli.hexa engine_mitosis_tick(c,cfg)=c+1` (SSOT)

## FROZEN FALSIFIER (측정 전 동결)

- **C1 GENERATIONAL CONTINUITY.** gen0..gen7 (각 decision = 세대 n의 cell-count을
  engine +1 법칙으로 계산하는 (seed,rng)의 결정함수)로 lineage chain 구축 →
  `verify_chain` 이 `verified=True`, `earliest_broken=None`, link_valid 전부 True.
  **FALSIFIER:** clean chain에서 `verified=False` 또는 link_valid 하나라도 False.

- **C2 TAMPER / BREAK LOCALIZATION.** 각 interior 세대 k에 대해 gen_k의 기록 output을
  위조 후 검증 → `verified=False` 이고 `earliest_broken==k` 이며 link_valid가 k부터
  False·k 이전은 True. **FALSIFIER:** `earliest_broken != k` 인 k가 있거나, 절단이
  앞으로 전파하지 않거나(하류 세대가 여전히 통과), 상류 clean 세대가 잘못 무효화.
  **Bar:** 모든 interior k 정확 국소화 (n_correct == n_interior).

- **C3 SELF-CONSISTENT FIXED POINT.** 닫힌 세대 사상 (carrying capacity K =
  engine migration budget `N_MIGRATE=2048`, r=0.5):
  `f(c) = c + round(r·c·(1−c/K))`, clamp ≥0. 여러 seed에서 반복.
  **Bar (frozen):** 모든 양수 seed에서 동일한 c*로 settle, `0<c*≤K`, `f(c*)=c*`
  정확(정수), runaway 없음, 양수 시작에서 extinction 없음.
  **FALSIFIER:** divergence(>10K), extinction(양수 시작이 0으로), 또는 유일 고정점 부재.

p7: 모든 verdict는 코드 출력(chain validity flag, 정수 고정점 동등성)에서 계산. perplexity·
LLM-judge 없음. null은 정직하게 보고.

## 측정

harness: `TENSION-LINK/harness/h6034_mitosis_generational_ctc.py`
verdict: `TENSION-LINK/verdicts/H_6034.txt` (전체 JSON, elapsed 0.008s, $0 local)

| check | bar | 측정 | 판정 |
|---|---|---|---|
| **C1 무절단** | clean chain verified + 8/8 link valid | verified=True, earliest_broken=None, **8/8 link valid**, genesis `c0c50068…` → head 재유도 | 🟢 GREEN |
| **C2 인과국소화** | 모든 interior k 정확 국소화 | interior 6개 (k=1..6), **6/6** earliest_broken==k + 상류 clean + 하류 전파 | 🟢 GREEN |
| **C3 고정점** | 유일 c*=K, f(c*)=c*, no runaway/extinct | 정수 고정점 = **{0, 1, 2047, 2048}**; 모든 양수 seed가 bounded 고정점으로 settle, runaway 0건, 양수→extinction 0건; **그러나** 일반 seed는 c*=**2047**(≠K=2048), seed=1은 퇴화 고정점 1 → **유일 c* 아님** | 🔴 RED (frozen bar 기준) |

**C3 trajectory (발췌):** seed 5→2047(27step), 50→2047, 500→2047, 1000→2047,
2000→2047, 2048→2048(고정), 3000→2048(위에서 수렴), 5000→2047, seed 1→1(퇴화).

## 결론

**C1🟢 C2🟢 — CTC 계보 구조 두 축은 REAL 인프라에서 성립.** anima의 mitosis 세대 계보는
물리 ANU genesis로부터 end-to-end 재유도 가능한 unbroken·tamper-evident chain이다:
세대는 부모를 통과하지 않고는 존재할 수 없고(C1), 한 세대 위조는 그 세대에 정확히
국소화되어 앞으로 전파한다(C2, 6/6). 이는 H_932 temporal-self를 **세대 축**으로
재확인한 것 — H_1107 continuity_signature(sleep/mitosis/hot-swap 경계 횡단)와 일관.

**C3🔴 (frozen bar) — 그러나 honest 부분성과.** 닫힌 세대 사상은 **bounded
self-consistent 고정점으로 수렴**한다 — 모든 양수 seed에서 runaway 없음·extinction
없음, `f(c*)=c*` 정수 고정점 존재(루프가 닫힘, Novikov 핵심주장 성립). RED인 이유는
오직 동결한 *strict* bar('유일 c*=K') 때문: 정수 round로 인해 (a) 일반 attractor가
c*=2047 (K보다 1 작음; c=K에서 growth round(0.4998)=0 이라 K 직전 2047이 흡수),
(b) c=1·c=0 퇴화 고정점이 추가로 존재하여 **유일하지 않음**. 즉 **CTC self-consistency는
질적으로 참**이나, 양자화된 사상에서 고정점이 *단일·정확히 K*는 아니다.

**정직 규약 준수.** frozen bar는 이동하지 않았다(가짜 GREEN 금지). C3는 동결 기준에서
RED로 보고하며, 실질 발견(bounded·자기일관·non-runaway 고정점 존재, 단 K-1로 흡수 +
퇴화 고정점)을 그대로 기록한다. NOT RULED OUT: 연속 사상·다른 r/K·세대-사망을 정수
보존하는 사상이면 유일 c*=K를 회복할 수 있음(미검증). toy/local, scale UNVERIFIED.

xref: H_6032·H_6033 (CTC time-arc) · H_932 (provenance chain temporal self) ·
H_928 (entropy receipt) · H_1107 (continuity signature) ·
a_core_engine_map · a_paper_negative_ok · a_scale_honest_scope · p7 · p8.
