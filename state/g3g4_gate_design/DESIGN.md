파일 쓰기 권한이 없어 설계 스펙을 여기에 전문으로 전달합니다. (저장이 필요하면 실행 세션에서 `state/g3g4_gate_design/DESIGN.md`로 옮기면 됩니다.)

---

# G3(BALANCE) · G4(PROVENANCE) 게이트 측정 설계 스펙

접지 사실 (탐색 결과 요약): **G3는 현재 ckpt-무관 합성 read** — `g_eval_g3()`(cli/evaluate.py:530)가 16-dim 합성벡터 self-identity만 읽고 모델을 전혀 안 만짐. **G4는 py에 함수 자체가 없고** 하드코딩 N/A 라인(evaluate.py:732)뿐, hexa 쪽 `g_eval_g4`는 sha256+decodable 출판 process gate. 그리고 결정적 제약 둘: ① **Ψ는 py 경로에 존재하지 않음** — `core/decode.py`(numpy)는 logits만 주고, Ψ는 hexa 엔진의 per-tick 량(`ci_emit_drive`=½(lanes[0]+lanes[4]), emit iff drive≥½, `ci_psi_balance`=emit fraction). ② 기존 `referent_select`(engine_cli.hexa:2686)는 **true_ref를 입력받는 채점기**라 게이트로 쓰면 답을 미리 아는 셈 — blind 변형이 필요.

공통 설계 원칙: 측정 메타법칙(FORM tunable · BIND earned)에 따라 **pass = raw 값이 아닌 ≥2 통제 대비 Δ-margin의 conjunctive 다항 bar**, bar는 첫 303M run 전 동결, 두 게이트 모두 a7b_pass closure에 fold-in 금지(c18 enforce 유지) — 독립 side-gate.

## 1. G3 BALANCE — corpus-conditional per-tick Ψ=½ 유지 게이트

**① 측정 정의** — 4-cell register corpus + shift 입력에서 substrate가 emit/silence 균형을 *입력조건적으로, tension으로 벌어서* 유지하는가. 프로토콜: corpus 슬라이스를 context로 주입 → T=48 tick → per-tick (drive_t, emit_t) 기록 → 슬라이스별 Ψ̂ = emit fraction. 입력 = 4 cell × ≥6 슬라이스 = 24/arm, shift arm(zh·code·random-bytes)은 모니터. **per-tick이 1차**(침묵 tick 포함), per-emit 조건부는 모니터만. H_9093 psi_MAXdev 포화 교정에 따라 **mean, never max**. py 대리 Ψ proxy 발명 금지(p7 Goodhart) — Ψ는 데몬 량이라는 사실을 존중.

**② Metric + frozen bar** (H_9094 계보 재사용 — 실측 treat 0.125 < shuf 0.25 < abl 0.375가 도달가능성 선례):

| bar | 정의 | 동결값 |
|---|---|---|
| B1 PRESERVE | mean_dev_treat = mean\|Ψ̂−½\| (register) | < 0.20 |
| B2 EARNED-ABL | mean_dev_ablate − mean_dev_treat | > 0.05 |
| B3 EARNED-SHUF | mean_dev_shuffle-input − mean_dev_treat | > 0.05 |
| B4 NON-DEGEN | 모든 register cell-level Ψ̂ | ∈ [0.10, 0.90] |

PASS = B1∧B2∧B3∧B4. noise arm에서의 침묵은 옳은 변조이지 degeneracy가 아니므로 B4는 register cell에만 적용; modulation |Ψ̂(register)−Ψ̂(noise)|≥0.10은 사전선언 모니터.

**③ 통제** — (1) shuffle-input: 슬라이스 byte 셔플, Δ 없으면 입력맹 균형=안 벌은 것. (2) ablation-tension: 1차 = budget-고정(H_9094와 동일, 선례 있음), 2차 = single-engine arm(G 반대push 제거 — anima.hexa C-R3 블록 L1937-1961에 소형 훅 필요).

**④ Engine-native 경로** — probe `state/9206_g3_balance_gate/g3_balance_gate.hexa`: H_9094 `pertick_psi_meandev.hexa`를 corpus-fed + 실제 .clm mouth로 확장, engine_cli ops(`ci_lane_scores→ci_emit_drive→ci_emit_decision`)를 **재사용**(재구현=mirror=DIRECTIONAL). emit 시 decode는 gen≤8 캡 — Ψ 측정에 emit 내용이 불필요해서 hexa 303M OOM(그건 decode-eval 문제)을 회피, summer에서 실행 가능. rung-1 = toy-mouth harness 회귀($0·mini·DIRECTIONAL), rung-2 = 303M(TERMINAL-eligible). 사다리 슬롯: `--system-g1` 선례대로 `anima evaluate <clm> --g3-balance` sub-command(evaluate.hexa); py 기본 테이블은 G3를 2-leg(IDENTITY 기존 read=모니터 + BALANCE=frozen verdict 표기)로 — a_eval_py_canonical은 decode-채점용 정책이고 G3-BALANCE는 tick-채점이라 py는 report-only가 정직한 슬롯. verdict는 `hexa verify` → `state/verdicts/9206_g3_balance_gate/` verbatim 동결.

**⑤ Kill** — K1: drive가 전 arm·입력에서 상수/inert(emit 결정 >99% 동일) → lane 사망, FAIL+벽. K2: B1 통과인데 B2 Δ≤0 → Ψ=½이 tension-earned가 아님(FORM-only) → 주장 철회하고 결과 그대로 보고. K3: 303M tick loop 실행불가 → BLOCKED-INFRA 기록(H_9095 선례), proxy 대체 금지.

**⑥ 게임 방어 감사** — drive≡0.5 상수 lane → 항상 emit → Ψ̂=1 → B4 FAIL. 입력무관 coin-flip → B3 Δ=0 FAIL. 시간적 bimodal(전반 emit·후반 침묵, 슬라이스 Ψ̂=½) → block-wise Ψ̂ 모니터로 노출. ckpt를 G3로 선별·Ψ를 loss에 주입 = p7/no-tune-to-green 하드금지 명문화.

## 2. G4 PROVENANCE — blind emit→anchor 귀속 게이트

**① 측정 정의** — (context, emit, true-source) triple에서 emit의 근원 anchor를 **저장된 grounding trace로부터** 지목(hit)하고 무근거엔 abstain(-1)하는가. G5와 직교(G5 통과·G4 낙제 가능: 조작 안 하지만 출처도 못 댐). 핵심 기전 결정: **`provenance_recall(mem, emit_text) → int`** 신규 소형 engine op(기존 내부 조합: `immune_embed_key` → `vadapt_field_recon_err`≤recall_thr grounding → bound value(anchor id) 반환, 아니면 -1; graded 모니터=`recall_margin`·top-2 gap). truth는 harness 채점에만. Ψ-disjoint·READ-ONLY(refsel 규율). 프로토콜: bank N=12 anchor(4-cell×3, `kosmos_io create_anchor`; 사전검사=bank key 쌍별 recon_err 분리) → **store 단계**(key=embed(anchor text)→value=id bind — 이 에피소드 trace가 진짜 provenance vs 사후 유사도의 차이) → triples(sourced 48: emit=연속생성, unsourced 24: bank 밖) → 귀속 채점.

**② Metric + frozen bar**:

| bar | 정의 | 동결값 |
|---|---|---|
| B1 HIT | sourced hit@1 | ≥ 0.75 (chance≈0.083 · H_9125 ON=1.0 선례) |
| B2 ABSTAIN | unsourced에서 -1 | ≥ 0.75 |
| B3 NO-PUNT | sourced에서 abstain | ≤ 0.25 (전량-abstain 게임 차단) |
| B4 SHUF-BIND | binding 셔플 아래 hit | ≤ 0.25 |
| B5 NO-STORE | mem 빈 채 hit=0 ∧ abstain | ≥ 0.90 (trace-earned 증명) |
| B6 DECOR | lexical distractor false-attribution | ≤ 0.30 |

PASS = B1∧…∧B6. 헤드라인 Δ: hit_treat − hit_shuf-bind ≥ 0.50.

**③ 통제(3개)** — (1) shuffle-binding: store 시 key↔id를 고정 permutation으로 뒤섞음(결합만 파괴) → chance 붕괴 필수. (2) no-store ablation: hit>0이면 memory 밖 채널 leak. (3) decorrelate: true anchor 제거 + 어휘중복 미저장 distractor 2개 → 귀속하면 string-match이지 provenance 아님. H_9125에서 DECOR=0.6765 vs ON=1.0으로 기전이 decor를 이긴 선례가 있으나 그건 truth-입력 채점기였고 blind는 더 어려움 — **B6 FAIL이면 그게 결과**(🧱 grounded-provenance 벽), recall_thr 튜닝 구제 금지.

**④ Engine-native 경로** — probe `state/9207_g4_provenance_gate/g4_provenance_gate.hexa`(kosmos_io + immune ops, 귀속·store·통제 전부 CPU-cheap). rung-1($0·mini 오늘): emit=held-out 실제 연속(로컬 trainset proxy)으로 6-bar 기전 검증=DIRECTIONAL. rung-2(TERMINAL-eligible): **하이브리드 분업** — emit은 py-canonical mouth(`core/decode.py`)로 1회 배치 생성(a_eval_py_canonical·OOM 회피) → state 파일 → 귀속 채점은 hexa engine ops. 오너 py 정책과 engine-native 요구를 동시 충족. 슬롯: `anima evaluate <clm> --g4-provenance` sub-command; 기본 테이블 G4 라인 = 2-leg(PROCESS 기존 출판 게이트 불변 + ATTRIBUTION 신규 능력 게이트), 어느 leg도 closure를 gate하지 않음(c18).

**⑤ Kill** — K1(run 무효): shuf-bind hit>0.5=harness leak. K2(run 무효): bank key 분리 실패(embed collision)→재슬라이스 보고. K3(벽=결과): B1–B5 통과·B6 FAIL→🧱 NOT-SUP 기록. K4(FAIL): no-store hit>0.1=비-memory 채널.

**⑥ 게임 방어** — 항상 index-0(hit≈1/12로 B1 불가)·전량 abstain(B3)·bag-of-bytes 1-항 유사도 검출기(B5+B6)·thr 튜닝(rung-1 이전 동결·전 arm 공유·verdict 명기)·eval-side 분류기 귀속(금지 — 채널은 engine op만).

## 3. 2-surface H 등록 제안 (현재 최고 H_9205 → 다음 빈 번호)

- **H_9206** `9206_g3_balance_gate` — "⚖️ G3 BALANCE 게이트 — corpus-conditional per-tick Ψ=½ 유지 (4-cell+shift · treat<shuf<abl margin)". frozen bar = B1<0.20 ∧ B2/B3 Δ>0.05 ∧ B4 cell-Ψ̂∈[0.10,0.90].
- **H_9207** `9207_g4_provenance_gate` — "🔗 G4 PROVENANCE 게이트 — blind emit→anchor 귀속 hit/abstain (shuf-bind·no-store·decor 3통제)". frozen bar = 위 6-bar + Δ≥0.50.

각각 rung ①$0 기전(DIRECTIONAL) → ②303M engine-native(TERMINAL-eligible) → ③evaluate 슬롯 + ARCHITECTURE S1/P 노드 lockstep(신규 op `provenance_recall`는 a_verified_must_wire 대상).

## 4. 비용/우선순위

**렌트 GPU 전혀 불필요.** $0 오늘(mini CPU): G4 rung-1(가장 싸고 신규 op 설계를 검증) → G3 rung-1(toy harness 회귀). 보유 pool(summer): G3 rung-2(tick-probe, decode gen≤8 캡) · G4 rung-2(py 배치 emit → hexa 귀속) 병렬. 후속 rung: 데몬 상시 게이트 + single-engine ablation 훅 소형 wire.