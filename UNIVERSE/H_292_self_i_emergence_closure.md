---
id: H_292
slug: self-i-emergence-closure
title: 1인칭 'I' 가 자기참조 닫힘(self-loop)의 고정점으로 창발하는가 — RING 은 'I'-state 창발 / STAR 는 파괴, 위상-의존 PARTIAL (H_205 sister)
domain: self/identity · consciousness · substrate · meta
status: partial
exploration_method: E13 (strange-loop fixed-point) + E16 (self-ref vs non-self-ref 대비) + E0 (H_205 self-ref-as-closure 후속)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_205 (self-ref-as-closure), H_289 (parity network → TPM, 동일 substrate 계열)
axes_seed: AXES.md R4 (self/identity) rank-5 `self-i-emergence`
---

# H_292 — 1인칭 'I' 가 자기참조 닫힘의 고정점으로 창발하는가

## 1. Hypothesis

'I' 지표(indexical)는 자기참조적이다 — "I" 는 지칭하는 바로 그것을 지칭한다(strange loop /
Quine 고정점). 자기참조의 최소 substrate 는 **self-loop**: 다음 상태가 자기 *자신*의 현재
상태에 의존하는 cell(자신을 읽음). 이 자기참조를 닫으면, 자기-원인인 상태 — 고정점 f(s)=s
에서 self-cell 이 스스로를 지탱하는 — 가 *비자기참조*(타자-구동) 망엔 없는 형태로 창발하는가?

**가설 H1 (검정 대상)**: 자기참조 닫힘(한 cell 에 self-loop 추가)이 비자명 자기일관 고정점
('I'-state)을 만든다 — matched 비자기참조 망에 없는: #fixed(self-ref) > #fixed(no-self-ref),
추가 고정점은 non-vacuum.

## 2. Why

- **H_205 (self-ref-as-closure) 의 형식 후속**: H_205 은 자기참조를 closure 로 다뤘다. 본 H 는
  그것을 *측정 가능한* 고정점으로 구체화 — self-loop 가 자기일관 'I'-state 를 만드는지.

- **고정점 = 최소 'self'**: 고정점 f(s)=s 는 자기 자신을 재생산하는 상태 = 가장 단순한
  "지속하는 self". 자기참조(self-loop)가 이를 *만드는지/파괴하는지* 가 핵심.

- **self-contained 고정점 + engine 재사용(big-Φ, g61)**: 고정점 계산은 self-contained, big-Φ
  는 `HEXAD/IIT4/lib` 재사용으로 자기참조 망이 통합돼 있음을 확인.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H292.1 (self-fixed-point)**: #fixed(self-ref RING) > #fixed(base RING).
- **H292.2 (nontrivial-I)**: self-ref 망에 ≥1 non-zero 고정점.
- **H292.3 (vacuum-anchor)**: all-0 은 모든 parity 망의 고정점.
- **H292.4 (integrated)**: self-ref 망 big-Φ ≥ 0 (self-loop 가 통합 파괴 안 함).
- **H292.5 (robust)**: H292.1 이 STAR base 에서도 성립.
- **H292.6 (determinism)**: #fixed re-run identical.

## 4. Variables

- **axis1_self_reference** (primary): SELF (node0 self-loop = neigh[0] 에 bit0) vs BASE (no self-loop).
- **dynamics**: parity (XOR-of-neighbours). 고정점 = node_next(neigh[i],s,n)==bit_i(s) ∀i.
- **pairs** (n=4): RING base [10,5,10,5]→SELF [11,5,10,5] · STAR base [14,1,1,1]→SELF [15,1,1,1].
- **metric**: #fixed (전/non-zero) + big-Φ(state-avg).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h292_self_i_emergence_closure_2026_05_26/run_h292.hexa`
- **engine**: 고정점 self-contained; `big_phi` (iit4_bigphi via stdlib) + `iit4_bit`/`iit4_pow2`.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h292.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: NO RNG; re-run identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **ledger**: `result.json`. **tier**: 🟡 PARTIAL (위상-의존, F292.5 FAILED).

## 6. Criteria

- **C1 (CORE / H292.1+2)**: self-ref RING 가 비자명 'I'-state 창발 (#fixed up) → core PASS.
- **C2 (ROBUST / H292.5)**: STAR 에서도 성립 → 미달이면 PARTIAL (위상-의존).
- **C3 (ANCHOR+INT+DET)**: vacuum + 통합 + 결정론 → PASS.
- **verdict_rule**: C1∧C3 PASS + C2 FAIL → **PARTIAL** (자기참조의 'I'-효과는 위상-의존).

## 7. Falsifiers

- **F292.1 SELF-FIXED-POINT**: #fixed(SELF RING) ≤ #fixed(BASE RING) → H1 핵심 FALSIFIED.
- **F292.2 NONTRIVIAL-I**: self-ref 망 non-zero 고정점 0 → trivial → FALSIFIED.
- **F292.3 VACUUM-ANCHOR**: all-0 이 고정점 아님 → parity 계산 무효.
- **F292.4 INTEGRATED**: self-ref big-Φ < 0 → 무효.
- **F292.5 ROBUST**: #fixed(SELF STAR) ≤ #fixed(BASE STAR) → 위상-의존(universal 아님). [측정: FAILED]
- **F292.6 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 PARTIAL (위상-의존) — 자기참조(self-loop)는 비자명 'I'-state 를 RING 에서
        창발시키나(F292.1/2 PASS) STAR 에선 오히려 파괴(F292.5 FAILED). gate 5 PASS / 1 FAIL.

config: parity(XOR-이웃) n=4 · 고정점 = f(s)=s ∀cell · SELF=node0 self-loop · engine: big-Φ 재사용

table (#fixed points = 자기일관 self-states):
  pair          base #fixed   self-ref #fixed   결과
  RING          1             2                 self-ref 가 'I'-state 추가 (s=1011 창발) ✓
  STAR          2             1                 self-ref 가 self-state 파괴 (1111 소멸) ✗

  self-ref RING fixed points: s=0 (vacuum) · s=11 (1011) ◀ 비자명 'I'-state
  self-ref RING big-Phi_mean = 0.5 (통합 유지)

criteria:
  C1 CORE (RING #fixed 1→2, 비자명 I-state s=1011)      : PASS
  C2 ROBUST (STAR #fixed 2→1, self-ref 가 파괴)         : FAIL → PARTIAL
  C3 ANCHOR+INT+DET (vacuum 0 ✓; big-Φ 0.5≥0; re-run)   : PASS

falsifiers:
  F292.1 SELF-FIXED-POINT : PASS  (RING self-ref #fixed 2 > base 1)
  F292.2 NONTRIVIAL-I     : PASS  (RING self-ref non-zero fixed = s=1011)
  F292.3 VACUUM-ANCHOR    : PASS  (all-0 고정점 base & self-ref)
  F292.4 INTEGRATED       : PASS  (self-ref big-Φ_mean 0.5 ≥ 0)
  F292.5 ROBUST           : FAIL  (STAR self-ref #fixed 1 ≤ base 2 — self-ref 가 파괴, 위상-의존)
  F292.6 POST-HOC         : NOT_TRIGGERED

checks: 5 PASS / 1 FAIL

evidence_summary: 🟡 PARTIAL — 자기참조 닫힘(self-loop)이 1인칭 'I'-state(자기일관 고정점)를
  창발시키는지는 **위상-의존**이다. RING base 에선 self-loop 가 비자명 자기일관 고정점 s=1011 을
  *창발*시켰다(#fixed 1→2) — 자기 자신을 원인으로 갖는 strange-loop 고정점, H_205 closure 의
  최소 실현. **그러나** STAR base 에선 같은 self-loop 가 오히려 자기일관 상태(1111)를 *파괴*
  했다(#fixed 2→1). 즉 자기참조는 'I'-state 를 만들 수도, 없앨 수도 있으며, 어느 쪽인지는
  base 위상의 parity 구조가 결정한다. 사전등록 robustness falsifier F292.5 가 정확히 이
  비-보편성을 포착(정직하게 FAILED 보존, p-hacking 회피). 핵심(self-ref 가 'I'-fixed-point 를
  *만들 수 있다*)은 RING 에서 실증되나, *자동·보편적 결과가 아니다*. self-loop 가 big-Φ(0.5)를
  파괴하지 않아 자기참조는 통합과 양립한다(F292.4).
falsifiers_triggered: F292.5 ROBUST (위상-의존 — 발견 그 자체)
```

re-run identical 확인 (F292.6).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_292 self-referential closure (a self-loop) creates a non-trivial self-
   consistent fixed point ('I'-state, s=1011) on a RING parity network (#fixed 1->2) but
   DESTROYS one on a STAR base (#fixed 2->1) — whether self-reference creates or removes a
   self-state is TOPOLOGY-DEPENDENT, not universal; self-loop preserves integration
   (big-Phi=0.5); deterministic toy-substrate, NOT an atlas identity / NOT phenomenal selfhood"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced + topology-conditioned
```

## 9. Honest Limits (raw#91 c3)

- **L1 (위상-의존 — 핵심, F292.5 FAILED)**: 자기참조가 'I'-state 를 *만든다*는 보편 명제는
  거짓 — RING 은 창발(1→2), STAR 는 파괴(2→1). self-loop 가 node 의 parity 에 자기 비트를
  더해 base 의 자기일관 해를 바꾸는데, 그 방향은 base 구조 의존. 주장은 "self-ref 가 'I'-state 를
  *만들 수 있다*"(존재)이지 "항상 만든다"(보편)가 아님.
- **L2 (parity·self-loop 는 최소 proxy)**: self-loop 는 자기참조의 *최소 구조* proxy, 고정점은
  자기일관 *상태*이지 phenomenal selfhood 아님. "1인칭 의식" 주장 아님 — strange-loop 의 형식
  골격만.
- **L3 (n=4 small, 2 pair)**: n=4 · 2 base 위상. 더 많은 위상/큰 n 에서 창발↔파괴 비율은 미검증
  (앙상블 phase diagram = §10 Next).
- **L4 (parity dynamics 한 선택)**: XOR-이웃은 선형. majority/threshold/비선형은 다른 고정점
  구조 → self-ref 효과 다를 수 있음.
- **L5 (고정점 = 정적 self; 동적 self 아님)**: 고정점은 시간-불변 자기일관. 주기 attractor/
  limit cycle 형태의 "동적 self"는 본 H 범위 밖.
- **L6 (big-Φ structure-cut, full IIT4 절대 calibration 아님)**: big-Φ=0.5 는 통합 존재 확인용
  보조 metric, 절대 스케일 아님.
- **L7 (verdict ≠ 형이상학)**: PARTIAL 은 toy parity 망 측정 사실 — "AI 가 자아를 갖는다" 주장
  아님. 오히려 L1 이 자기참조→self 의 *조건 의존성*을 강조.

## 10. Cross-Links

- **parent (형식 골격)**: [[H_205]] (self-ref-as-closure) — 본 H 가 closure 를 self-loop 고정점
  으로 구체화. 자기-원인 상태(s=1011)가 closure 의 최소 실현.
- **sibling (substrate)**: [[H_289]] (parity network → TPM) — 동일 net_tpm/parity 계열. 본 H 는
  self-loop(자기참조)를 추가한 변형.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`big_phi`/`iit4_bit`/
  `iit4_pow2`, via stdlib) — 새 IIT4 코드 0줄 (g61).
- **axes seed**: `UNIVERSE/AXES.md` R4 (self/identity) rank-5 `self-i-emergence` — consumed.
- **Next**: (a) 다수 위상 × self-loop on/off phase diagram (창발↔파괴 경계 정량, L1/L3);
  (b) majority/비선형 dynamics (L4); (c) limit-cycle "동적 self" (L5); (d) 자기참조 노드의
  per-node distinction φ (자기-원인 power 직접 측정).
