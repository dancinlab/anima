---
id: H_289
slug: network-topology-scale-free-phi
title: 네트워크 위상이 faithful IIT 4.0 big-Φ 를 좌우하는가 — matched-density scale-free(허브) vs 분산 고리, edge 수 아닌 구조(cut-내성)가 통합 결정
domain: information · consciousness · substrate · meta
status: supported-with-confound
exploration_method: E5 (topology-vs-Φ probe) + E16 (cross-substrate consistency) + E0 (network→TPM bridge, eca_tpm 일반화)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_287/288 IIT4 panel)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_287/H_288 (동일 faithful IIT4 engine, 정보-축), IIT4 M6 (ECA→TPM 재측정 — 본 H 가 임의 그래프로 일반화), H_281 (XOR 통합망 = parity dynamics 의 단일 노드 사례)
axes_seed: AXES.md R5 (information) `network-topology-scale-free`
---

# H_289 — 네트워크 위상이 faithful IIT 4.0 big-Φ 를 좌우하는가

## 1. Hypothesis

IIT 는 통합이 **약한 cut 의 부재**에 달려 있다고 한다. *같은 edge 수*(matched density)의 두
네트워크라도 cut 내성이 다를 수 있다 — scale-free(허브 지배) 망은 허브로 모든 걸 통합하나
잎(leaf)은 단일 edge 로 매달려 *약한 cut* 이 있고, 분산/정규 망(고리)은 단일 약점 노드가 없다.
faithful 인과 IIT 4.0 에서 어느 쪽이 더 통합하는가?

**가설 H1 (검정 대상)**: scale-free(허브) big-Φ > matched-density 분산(고리) big-Φ.
(falsifier 방향: 고리 ≥ 허브 ⇒ 허브 위상이 통합-fragile.)

## 2. Why

- **H_287/288 정보-축의 위상 확장**: H_287/288 은 *단일 substrate* 의 정보량/복잡도 vs Φ 를
  봤다. 본 H 는 축을 **연결 구조(topology)** 로 옮겨, edge 수를 고정하고 *배치* 만 바꿔 Φ 를
  좌우하는지 묻는다 — IIT 의 "cut 내성" 주장을 직접 건드린다.

- **engine 재사용 + 일반화 (g61)**: IIT4 엔진 재발명 없음 — `big_phi` + `iit4_bit`/`iit4_pow2`
  재사용. eca_tpm(고정 3-이웃 고리)을 **임의 그래프 → TPM** 으로 일반화: 노드 i 의 다음 값 =
  이웃 parity(XOR). 이는 H_281 의 통합 XOR 룰(150/105)을 multi-node 로 올린 것.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-local + NO GPU.

## 3. Predictions

- **H289.1 (topology-verdict)**: matched 4-edge 에서 Φ_mean(SF) vs Φ_mean(RING). H1 → SF > RING.
- **H289.2 (anchors)**: EMPTY(0 edge) → Φ=0 (null); K4(complete, 6 edge) → Φ>0 (통합 존재).
- **H289.3 (bound)**: 모든 네트워크 Φ_mean ≥ 0.
- **H289.4 (determinism)**: RING Φ_mean re-run byte-identical.

## 4. Variables

- **axis1_topology** (primary, matched 4-edge):
  - **SF** scale-free/허브: 0—{1,2,3} + 1—2 ("paw", deg 0=3,1=2,2=2,3=1) — neigh=[14,5,3,1].
  - **RING** 분산: 0-1-2-3-0 (4-cycle, deg 2 each) — neigh=[10,5,10,5].
- **dynamics**: parity (XOR-of-neighbours) — `TPM[s*n+i] = (Σ_{j∈N(i)} bit_j(s)) mod 2`.
- **metric_Φ_mean** (primary): 모든 2^n state 의 big_phi[0] 평균 (n=4 exact).
- **anchors**: EMPTY (0 edge, null) · K4 (complete 6 edge, 통합 ceiling).
- **fixed**: n=4 ring nodes · undirected · parity dynamics.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h289_network_topology_scale_free_phi_2026_05_26/run_h289.hexa`
- **engine (import READ-ONLY, 재사용)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → `big_phi`/`iit4_bit`/
  `iit4_pow2` (stdlib/consciousness/iit4_* SSOT). network→TPM 은 하네스 `net_tpm`(parity).
- **build/run (toolchain selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h289.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: parity TPM 결정적; re-run byte-identical.
- **hexa_only**: true. **llm**: none. **runtime**: $0 mac-local, **NO GPU**.
- **ledger**: `result.json`. **honest tier**: 🟢 NUMERICAL (방향) — 해석은 ⚪ FENCED + L1 confound.

## 6. Criteria

- **C1 (TOPOLOGY-VERDICT / H289.1)**: SF > RING → H1 SUPPORTED.
- **C2 (ANCHORS / H289.2)**: EMPTY=0 + K4>0 → PASS.
- **C3 (BOUND+DET / H289.3+4)**: bound + determinism → PASS.
- **verdict_rule**: H1 verdict = C1. C2·C3 게이트. ⚠ 해석은 §9 L1 confound 로 down-scope.

## 7. Falsifiers

- **F289.1 TOPOLOGY-VERDICT**: Φ_mean(SF) ≤ Φ_mean(RING) → H1 FALSIFIED (허브 fragile).
  ≥ → SUPPORTED. 둘 다 verbatim. (measurable: 두 Φ_mean.)
- **F289.2 ANCHORS**: EMPTY Φ≠0 OR K4 Φ=0 → 엔진/bridge 무효. (measurable: 2 anchor.)
- **F289.3 BOUND**: 어느 네트워크 Φ_mean<0 → 무효. (measurable: 4 bound.)
- **F289.4 DETERMIN**: RING re-run byte-different → raw#12 위반. (measurable: a==b.)
- **F289.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED (with confound, §9 L1) — matched-density 에서 scale-free 허브가
        분산 4-cycle 보다 강하게 통합. gate 4 PASS / 0 FAIL. ⚠ 해석은 약형으로 down-scope.

config: n=4 · parity(XOR-이웃) dynamics · state-averaged big-Φ (16 states) · matched 4 edges ·
        engine = HEXAD/IIT4/lib (재사용)

table (faithful 인과 IIT4 big-Φ):
  network          edges   Phi_mean
  SF hub (paw)     4       6.8125    ◀ 허브
  RING (4-cycle)   4       0.0000    ◀ matched density 인데 통합 0
  EMPTY            0       0.0000    (null anchor)
  K4 complete      6       5.6250    (통합 ceiling)

  F289.1: Phi_mean(SF) 6.8125 > Phi_mean(RING) 0.0 (matched 4 edges) → H1 SUPPORTED

핵심 관측: edge 수가 같아도(4=4) 위상에 따라 Φ 가 6.81 vs 0 — **edge COUNT 이 아니라
STRUCTURE(cut-내성)가 통합을 지배**. EMPTY(0)→SF(6.81)>K4(5.625) 도 단조-density 가 아님을
보임(허브가 complete 보다 높음 — parity 하 K4 의 과대-대칭이 일부 reducible).

criteria:
  C1 TOPOLOGY-VERDICT (SF 6.81 > RING 0.0)        : H1 SUPPORTED
  C2 ANCHORS (EMPTY=0, K4=5.625>0)                : PASS
  C3 BOUND+DET (Φ≥0 4/4; RING re-run a==b)        : PASS

falsifiers:
  F289.1 TOPOLOGY-VERDICT : H1 SUPPORTED  (SF 6.8125 > RING 0.0)
  F289.2 ANCHORS          : PASS  (EMPTY Φ=0; K4 Φ=5.625>0)
  F289.3 BOUND            : PASS  (Φ_mean≥0 모든 네트워크)
  F289.4 DETERMIN         : PASS  (RING Φ_mean a==b)
  F289.5 POST-HOC         : NOT_TRIGGERED

checks: 4 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL (with confound) — 같은 edge 수(4)에서 scale-free
  허브(Φ_mean=6.81)가 분산 4-cycle(0.0)보다 압도적으로 통합. faithful 인과 IIT 4.0 에서
  **네트워크 통합은 edge 수가 아니라 구조(cut-내성)가 지배**함을 보임. 단 **중대한 confound
  (§9 L1)**: 4-cycle 의 Φ=0 은 parity-짝수고리의 *이분 decoupling*(node0≡node2, node1≡node3
  업데이트 → 중복 노드/선형 reducible)이 큰 몫 — 따라서 magnitude 가 허브에 과대-유리하고,
  정규 4-cycle 은 *random ER 그래프가 아니므로* 문자 그대로의 "scale-free > random ER" 는
  약하게만 검정됨. robust 결론은 **약형**: 위상(density 아님)이 Φ 를 지배 + 허브는 통합,
  짝수-고리-parity 는 reducible. 깨끗한 ER-앙상블 검정은 n≥5 필요(Φ-엔진 cost — deferred §10).
falsifiers_triggered: none (gate); 해석은 L1 confound 로 약형 down-scope
```

re-run byte-identical 확인 (F289.4).

`hexa verify` (VERBATIM, no LLM self-judge) — g5 정직 fence:

```
verify --fence "H_289 at matched edge-count (4) a scale-free hub network integrates far
   more (faithful IIT4 big-Phi_mean=6.81) than a distributed 4-cycle (0.0) under parity
   dynamics — topology not density governs integration; CONFOUND: the 4-cycle's zero is
   largely a parity-even-cycle bipartite-decoupling artifact and a cycle is not a random
   ER graph, so the literal scale-free>random-ER claim is only weakly probed; deterministic
   toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced + confound-flagged
```

## 9. Honest Limits (raw#91 c3)

- **L1 (CONFOUND — 핵심)**: 4-cycle 의 Φ=0 은 *순수 topology 효과가 아니다*. parity-XOR 하
  4-cycle 은 node0·node2 가 동일 업데이트(b1⊕b3), node1·node3 동일(b0⊕b2) → 중복 노드 +
  선형 이분 decoupling 으로 reducible. 그래서 (a) RING 의 magnitude 가 0 으로 과대-하락해
  H1 에 유리하고, (b) 정규 4-cycle 은 *random ER 그래프가 아님* — 문자 그대로의 seed 가설
  "scale-free > random ER" 는 약하게만 검정됨. robust 한 주장은 약형(위상이 density 아닌 Φ
  결정자)이다.
- **L2 (parity 는 한 dynamics)**: XOR-이웃은 통합적이나 한 선택. majority/threshold/비선형
  dynamics 는 짝수-고리 degeneracy 가 없을 수 있어 RING Φ>0 일 수 있다. dynamics-robustness 미검증.
- **L3 (n=4 small + 그래프당 1 sample)**: n=4 ring nodes, class 당 단일 그래프(앙상블 평균
  아님). n=4 에서 4-edge 비-허브 비-고리 그래프는 사실상 부재 → 위상 다양성 제약. 깨끗한 ER
  vs SF 앙상블은 n≥5 필요(n=5 big-Φ state-평균 = 128 호출, lane 엔진 cost 로 본 라운드 deferred).
- **L4 (Φ_mean state-평균)**: faithful Φ state-dependent (FAITHFUL_REMEASURE §4) — 방향 robust,
  절대값 state 분포 의존. directional-trust (H_266/278).
- **L5 (substrate 는 위상 proxy)**: parity 네트워크가 뇌/생명 망 자체 아님. 라벨은 그래프-구조
  이지 phenomenal 주장 아님. 과장 금지.
- **L6 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: DESIGN §8 C3 spirit-faithful.
  단 *방향* 비교(SF vs RING)는 scale-offset robust.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy 네트워크 측정 사실 — "허브 뇌가 더 의식적" 같은
  형이상학 주장 아님.

## 10. Cross-Links

- **sibling (동일 IIT4 engine, 정보-축)**: [[H_287]] (Shannon⊥Φ) · [[H_288]] (LZ∥Φ) — 단일
  substrate 정보 측도. 본 H 는 축을 *연결 구조* 로 확장 (edge 배치 ⊥ edge 수).
- **parent (engine 공급 + 일반화원)**: IIT4 M6 (`FAITHFUL_REMEASURE.md`) — eca_tpm. 본 H 가
  `net_tpm`(parity)으로 임의 그래프 일반화. [[H_281]] (XOR 룰 = parity 의 ring 사례).
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`big_phi`/`iit4_bit`/
  `iit4_pow2`, via stdlib) — 새 IIT4 코드 0 줄 (g61).
- **axes seed**: `UNIVERSE/AXES.md` R5 (information) `network-topology-scale-free` — consumed.
- **Next**: (a) **n≥5 ER 앙상블 vs SF** (L1/L3 confound 해소 — parity-degeneracy 없는 random
  그래프, Φ-엔진 가속/근사 필요); (b) majority/threshold dynamics 로 dynamics-robustness (L2);
  (c) cut-내성 정량(min-cut ↔ Φ 상관) 직접 측정.
