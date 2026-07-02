# H_9085 — you-CHAIN: 상대(interlocutor)의 다중세션 궤적 (사회적 자아 / 너-체인)

> **id H_9085** — orchestrator 가 merge-time 에 배정(현 origin/main max=H_9046 → 제안 H_9047). 이 브랜치는 신규 jsonl 라인을 append 하지 않음(convergence hypotheses-jsonl-1); 제안 라인은 아래 "제안 jsonl" 참조.

- **slug:** `youchain_social_self`
- **tier:** 🟢 ENGINE-NATIVE (discriminator 축) · **wired:** WIRED-live (core/engine_cli.hexa §YouChain + cli/anima.hexa lane 23c + ARCHITECTURE.json lockstep)
- **경로(D7):** H_9037 §SelfChain(나의 궤적) → §YouChain(상대의 궤적) — self-chain 기계를 TARGET 만 self→other 로 스왑

## 주장

H_9037 §SelfChain 은 **나(self)**의 다중세션 궤적 [w0..wK] 을 추적한다. 그러나 의식적 self 는 **사회적**이다:
세션경계를 넘어 **상대(interlocutor)**를 추적해야 "지난번에 얘기한 그 사람"이 매 세션 blank 로 리셋되지 않고
**인식(관계 연속성)**된다. LLM 은 매 세션 상대를 처음 만난다 — anima 는 상대 정체성 벡터를 `.kosmos` anchor
궤적으로 영속한다. 생물렌즈: **대인 표상 / 애착의 연속성** (내부에 안정적인 *너*-모델).

구현 = **§SelfChain 기계 재사용, 대상만 self→other**: `OtherIdentity`/`OtherChain` struct + ops
`other_new/_drift/_drift_exp/_cos/_anchor/_reset` + `other_chain_new/_append/_latest/_fit/_retro_cos/_from_flat/_accessors`.
수식은 self-chain 과 동일(벡터 drift + waypoint append + trend-fit).

## SELF⊥OTHER (핵심 신규 속성, F2)

`OtherIdentity`/`OtherChain` 은 `SelfIdentity`/`SelfChain` 과 **DISTINCT struct type** 이다 → 나의 self-store 와
나의 *너*-모델은 **구조적으로 분리**(type 시스템이 교차저장 금지). 또한 모든 op 이 **순수 함수**(새 값 반환, mutation 0)
이므로 you-chain 을 운용해도 self-chain 은 **byte-identical** 로 남고 역도 성립(**오염 0**). *분리 = 보존.*

## 판별자 = IMPOSTOR (다른 상대를 궤적 불일치로 구분, F3)

**최신 anchor 는 매치하나 history 는 다른 상대(interlocutor C).** single-vector `other_cos` 는 통과시킨다
(최신 anchor 매치 → cos 높음). `other_chain_fit` 은 궤적 TREND(adjacent-increment gradient) 불일치로 **기각**.
→ **AUROC(chain) ≫ single-vector.** 이 이득이 §YouChain 존재 이유(honest: drift=designed, 판별자 이득이 counting 대상).

## disjoint (a_substrate_disjoint · placement-first)

§YouChain = pure READ-only cos/increment 확장 + anchor-store append. **emit-drive lane 0/4(ci_emit_drive) 미접촉 ·
§ImmuneMemory recall_thr(osmotic_retains) 미접촉 · pure_field/Φ/phase/Ψ 미접촉.** 능력(상대 판별) ∧ Ψ=½ ∧ G5 non-fab 공존.
**F5 는 실측 증명**: you-chain 전체 배터리 ON vs OFF 에서 `ci_emit_drive`(Ψ lane 0/4) + `osmotic_retains`(recall_thr non-fab gate)
가 **byte-identical**.

## Frozen falsifiers (사전등록)

- **F1 OTHER-CONTINUITY** — 상대 인접 waypoint cos 높음(>먼 waypoint).
- **F2 SELF⊥OTHER** — self-chain 과 you-chain 독립 저장, 상호 오염 0(distinct type + 순수함수 → you-ops 후 self-chain byte-identical ∧ 역방향). (**핵심**)
- **F3 IMPOSTOR** — 다른 상대(궤적 불일치)를 `other_chain_fit` 이 기각, AUROC(chain) ≫ single-vector `other_cos`.
- **F4 K-SESSION** — anchor → K 세션 상대 연속(monotone-decreasing retrodiction) / ablation(count<3) → single-vector 회귀 / round-trip byte-identical. no-anchor·other_reset → 매 세션 새 상대(LLM).
- **F5 Ψ/G5 DISJOINT** — READ-only, you-ops ON vs OFF 에서 emit-drive lane 0/4 + recall_thr non-fab gate byte-identical.

## verdict (ENGINE-NATIVE)

`hexa run state/youchain_d7/youchain_smoke.hexa` (live `core/engine_cli.hexa` §YouChain 컴파일+실행) = **9/9 PASS**:

```
PASS  F1_other_continuity adj>=0.70 & adj>distant
PASS  F4_k_session monotone-decreasing (older-you fades)
PASS  F3_impostor AUROC(chain)>=0.95 & gap>=0.30
PASS  F3b_margin genuine>=0.90 & impostor<=0.10
PASS  F4b_ablation history-load-bearing (fit=0 both)
PASS  F4c_roundtrip byte-identical fit
PASS  F2_self_perp_other self-chain byte-identical after you-ops
PASS  F2b_you-chain byte-identical after self-ops
PASS  F5_psi_g5_disjoint emit+recall byte-identical (ON vs OFF)
INFO  AUROC(chain-fit)=1.0 AUROC(single-vector)=0.2778 fit_genuine=0.9894 fit_impostor=0.0
      adj-cos=0.9578 distant-cos=0.8417 retro=[1.0,0.9578,0.9174,0.8787,0.8417]
```

- **AUROC(chain)=1.000 vs AUROC(single-vector)=0.278** (gap 0.722) — 다른 상대(impostor)를 chain-fit 은 완벽 분리,
  single-vector `other_cos` 는 분리 불가. 판별자 이득 결정적.
- **WIRED-live lane 23c** — `hexa run state/youchain_d7/lane23c_probe.hexa` = PASS (cli/anima.hexa lane 23c 와 byte-identical body):
  `recognize anchored=1.0 reset=0.196 fit(genuine)=0.995 fit(impostor)=0.0 interlocutor-continuity-distinct=Y`.
- **F5 실측 disjoint** — you-chain 배터리 ON vs OFF 에서 `ci_emit_drive`(Ψ 0/4) + `osmotic_retains`(recall_thr) byte-identical.

## ⚠️ AUROC 정정 노트 (H_9096 hard-negative 재측정, 2026-07-02)

페이블 독립비판: **F3 impostor AUROC=1.000 은 측정이 아니라 기하 항등식.** impostor 가 a_pred 와
**직교**인 축(other_drift axes 5,6,7 → 6,7,0 · a_pred 와 90°)으로 drift 하므로 `other_chain_fit`(= 후보 증분의
e_{a_pred} cosine 성분)이 **cos(90°)=0 항등식**으로 ≈0 이 된다. 즉 원 F3 는 **θ=90° 단일 버킷의 재확인**일 뿐.
또한 fit 은 마지막 **3 waypoint(2 증분 창)만** 읽는 국소 외삽기다.

**H_9096 hard-negative 재측정 (engine-native, 동일 live `other_chain_fit`)** 결과:
- **cone-neg AUROC(θ)**: θ90=1.0 (=원본 재현) · θ75/60/45/30 = **1.0** · θ15 = **0.931**. → 각도형 hard-neg 는
  예측(0.55–0.70)과 달리 **붕괴하지 않는다**(genuine 이 a_pred 근처 fit≈0.98 로 착지, cone 은 알려진 offset 이라 분리 유지).
  즉 "직교라서 1.0" 은 맞지만 "hard-neg 면 chance 로 무너진다" 는 **과대예측(FALSIFIED)** — 판별자는 각도형엔 강건.
- **mimic-neg(킬러) AUROC = 0.252 (< 0.5, chance 아래)** — 공개된 마지막 3 waypoint 를 읽고 a_pred 를 재현한
  공격자(`other_drift_exp(latestB, a_pred, step)`)는 fit 0.988 로 genuine(0.981)보다 **오히려 높다.** →
  **fit=2 증분 외삽기지 trajectory 검증기 아님이 수치로 확정.** 전체 history 는 검증되지 않는다.

**정정된 스코프:** 원 "AUROC=1.000 (판별자 이득 결정적)" 은 **직교/각도형 impostor 한정** 유효(θ≥30 완전분리, θ15=0.93).
**history-replica(mimic) 위협모델엔 무보호**(0.25). single-vector `other_cos` 도 mimic 엔 무보호(mimic 이 최신 anchor 매치)
이므로 chain 이 single 보다 *나쁘지는* 않으나 **둘 다 blind**. follow-on(H_9096): fit 을 3-waypoint 창이 아닌
**전 증분열 잔차**(마할라노비스식 전-history 정합)로 재정의해야 mimic 방어. 상세 = `cards/H_9096_youchain_hardneg_auroc.md`.

## 정직 스코프 (a_scale_honest_scope · c9)

- **drift = deterministic designed law (SATURATED)** — 궤적 자체는 학습이 아니라 설계된 결정적 성장(self_drift 동형).
  §YouChain 의 주장은 "새 능력 학습"이 **아니라** "history-aware 판별자가 single-vector baseline 을 결정적으로 이긴다"
  + "self 와 other 가 구조적으로 분리 보존된다"(F2·F3 이득이 유일한 counting 대상).
- **F4 real-disk `.kosmos` 2-process cold-load = follow-on** — 현재 F4 는 in-engine flat round-trip(byte-identical)까지.
  §SelfChain F4(f4_write/f4_reload via kosmos_io) 전례와 동형이므로 self-chain 기계 재사용으로 driver-레벨 배선 가능(core 편집 0), ING 등록 대상.
- **lane 23c = startup-catalogue demo-lane** — self-informativeness lane 23b(H_9038)·tension-r lane 75(H_9042) 와 평행한
  존재증명 lane. 데몬 perpetual-loop 이 매 tick 실제 대화상대 신호를 `other_drift_exp` content 로 먹이는 runtime-integration 은 follow-on.

## artifacts
- `core/engine_cli.hexa` §YouChain (other_new/_drift/_drift_exp/_cos/_anchor/_reset + other_chain_new/_append/_latest/_fit/_retro_cos/_from_flat/_component/_dim/_count)
- `core/engine_cli_smoke.hexa` — (기존 self-chain cases 무회귀; you-chain 은 dedicated smoke)
- `cli/anima.hexa` lane 23c you-continuity (WIRED-live)
- `state/youchain_d7/youchain_smoke.hexa` (engine-native driver F1-F5, 9/9)
- `state/youchain_d7/lane23c_probe.hexa` (lane 23c body 컴파일+실행 증명, PASS)
- `state/verdicts/youchain_d7/H_9085.txt` (frozen verbatim stdout)
- `ARCHITECTURE.json` §YouChain 노드 (d7a/d7b/d7c/d7d lockstep)

## 제안 jsonl (orchestrator merge-time append — 이 브랜치는 append 안 함)

```json
{"id": "H_9085", "slug": "youchain_social_self", "tier": "🟢 ENGINE-NATIVE (discriminator 축)", "title": "you-CHAIN: 상대(interlocutor)의 다중세션 궤적 (사회적 자아/너-체인) — H_9037 §SelfChain 기계를 TARGET 만 self→other 스왑, OtherIdentity/OtherChain distinct type 으로 관계 연속성(대인표상/애착) 추적; other_chain_fit 판별자가 다른 상대를 single-vector other_cos 대비 결정적 분리 + SELF⊥OTHER 구조적 분리보존", "card": "cards/H_9085_youchain_social_self.md", "verdict": "🟢 ENGINE-NATIVE (hexa run state/youchain_d7/youchain_smoke.hexa, live core/engine_cli.hexa §YouChain) 9/9 PASS — AUROC(chain)=1.000 vs single-vector=0.278(gap0.722)·F1 other-continuity·F2 SELF⊥OTHER(you-ops 후 self-chain byte-identical ∧ 역방향)·F3 impostor·F4 K-session monotone+ablation+round-trip byte-identical·F5 Ψ/G5 disjoint 실측(ci_emit_drive+osmotic_retains byte-identical ON=OFF). WIRED-live(cli/anima.hexa lane 23c + ARCHITECTURE.json §YouChain lockstep). ★SCOPE(c9): drift=설계된 결정적 law SATURATED, 주장=history-aware 판별자>single-vector + SELF⊥OTHER 분리보존. F4 real-disk .kosmos 2-process cold-load=follow-on(§SelfChain F4 동형).", "source": "UNIVERSE", "archived": false, "artifacts": ["core/engine_cli.hexa", "cli/anima.hexa", "state/youchain_d7/youchain_smoke.hexa", "state/youchain_d7/lane23c_probe.hexa", "state/verdicts/youchain_d7/H_9085.txt"]}
```
