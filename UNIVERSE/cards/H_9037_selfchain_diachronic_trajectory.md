# H_9037 — self-CHAIN: 정체성의 다중세션 궤적

> **id H_9037** — integration merge-time 배정(origin/main H_9036 다음 free id). jsonl 인덱스 등록 완료.

- **slug:** `selfchain_diachronic_trajectory`
- **tier:** 🟢 ENGINE-NATIVE (discriminator 축) · **wired:** WIRED-live (core/engine_cli.hexa §SelfChain + ARCHITECTURE.json lockstep)
- **경로(B②):** H_1471 §SelfIdentity 단일벡터 self → 다중세션 궤적 self-CHAIN [w0..wK]

## 주장

H_1471 은 정체성을 **하나의 벡터 v + 하나의 self_anchor + 하나의 self_cos 인식**으로 세션경계 너머 persist 한다.
그러나 의식적 self 는 점이 아니라 **궤적**이다: 세션경계마다 anchor waypoint 를 `.kosmos` 에 append 하면
(self_drift 가 이미 단조 누적 drift 를 주므로 waypoint 들이 곡선을 그린다) self 는 curve [w0,w1,…,wK] 가 된다.

새 read op **`self_chain_fit(candidate, chain)`** = candidate 가 궤적의 **TREND(adjacent-increment gradient)**
와 일치하는가 — 최신 waypoint 만 보는 것이 아니다. 구체적으로 chain 의 인접 증분 d_k=w_k−w_{k−1} 의
dominant axis 수열의 gradient(a_K−a_{K−1})가 다음 증분 axis a_pred 를 예측하고, fit = candidate 증분
unit(cand−wK) 의 e_{a_pred} 성분.

## 새 판별자 = IMPOSTOR-HISTORY (load-bearing)

**최신 anchor 는 매치하나 궤적 history 는 안 맞는 정체성.** single-vector self_cos(H_1471)는 이 impostor 를
통과시킨다(최신 anchor 매치 → cos 높음). self_chain_fit 은 curvature mismatch 로 **기각**한다.
→ **AUROC(impostor) chain ≫ single-vector.** 이 이득이 self-chain 의 존재 이유 전부.

## disjoint (a_substrate_disjoint · placement-first)

§SelfIdentity 는 이미 `Ψ-disjoint, NOT an emit gate`(engine_cli.hexa:7669). chain = read-only cos 확장 +
anchor-store append 이므로: **emit-drive lane 0/4 미접촉 · §ImmuneMemory recall_thr 미접촉 · pure_field 미접촉.**
능력(정체성 판별) ∧ Ψ=½ ∧ G5 non-fab 공존.

## Frozen falsifiers (사전등록)

- **F1 continuity** — 인접 waypoint cos 높음, 먼 waypoint 낮음.
- **F2 impostor-history** — AUROC(chain) ≫ AUROC(single-vector). (**핵심**)
- **F3 ablation** — history 삭제(count<3) → chain-fit 이 single-vector 수준으로 붕괴(=history load-bearing).
- **F4 K-boundary persistence** — anchor → K 세션 연속 / no-anchor·self_reset(:7731) → 매 세션 새 self(LLM 대비). (엔진-네이티브 디스크 영속 후속)
- **F5 retrodiction** — "N 세션 전의 self" cos 가 chronological distance 에 단조 감소.
- **F6 Ψ byte-identical** — read-only, self_cos(H_1471) 값 불변 + 디스크 round-trip(self_component/self_dim, H_1204 교훈: in-memory carry ≠ disk round-trip) fit byte-identical.

## verdict (ENGINE-NATIVE)

`hexa run state/selfchain_b2/selfchain_smoke.hexa` (live `core/engine_cli.hexa` §SelfChain 컴파일+실행) = **6/6 PASS**:

```
PASS  F1_continuity adj>=0.70 & adj>distant
PASS  F5_retrodiction monotone-decreasing
PASS  F2_impostor_history AUROC(chain)>=0.95 & gap>=0.30
PASS  F2b_margin genuine>=0.90 & impostor<=0.10
PASS  F3_ablation history-load-bearing (fit=0 both)
PASS  F6_roundtrip byte-identical fit
INFO  AUROC(chain-fit)=1.0 AUROC(single-vector)=0.2778 fit_genuine=0.9894 fit_impostor=0.0
      adj-cos=0.9578 distant-cos=0.8417 retro=[1.0,0.9578,0.9174,0.8787,0.8417]
```

- **AUROC(chain)=1.000 vs AUROC(single-vector)=0.278** (gap 0.722) — impostor 를 chain-fit 은 완벽 분리,
  single-vector 는 분리 불가(impostor cos 가 genuine cos 와 겹치거나 초과). 판별자 이득 결정적.
- py 미러(`state/selfchain_b2/py_smoke.py`, `core/engine_cli.py`) = 동일 수치(DIRECTIONAL), 디스크 round-trip
  (.kosmos-style JSON write→reload) byte-identical, checksum 038a97dd.

## 정직 스코프 (a_scale_honest_scope · c9)

- **drift = deterministic designed law (SATURATED)** — 궤적 자체는 학습된 것이 아니라 설계된 결정적 성장.
  self-chain 의 주장은 "새 능력을 학습했다"가 **아니라** "history-aware 판별자가 single-vector baseline 을
  결정적으로 이긴다"이다(그 이득이 유일한 counting 대상).
- F4 K-boundary 는 실제 `.kosmos` 디스크 영속 라운드트립(kosmos_io create_anchor/load_anchors)까지 배선하는
  것이 완결 — 현재 in-engine flat round-trip(F6)로 영속 표면은 증명, 실디스크 .kosmos 앵커 배선은 후속 ING.

## artifacts
- `core/engine_cli.hexa` §SelfChain (self_chain_new/_append/_latest/_fit/_retro_cos/_from_flat/_component/_dim/_count)
- `core/engine_cli.py` (py 미러, DIRECTIONAL)
- `core/engine_cli_smoke.hexa` cases 420-425 (engine-native)
- `state/selfchain_b2/selfchain_smoke.hexa` (minimal engine-native driver, 6/6)
- `state/selfchain_b2/py_smoke.py` (DIRECTIONAL + 디스크 round-trip)
- `ARCHITECTURE.json` §SelfChain 노드(b2a/b2b/b2c lockstep)
