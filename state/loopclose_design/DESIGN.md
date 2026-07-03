# loop-closing 구현 설계 (페이블5 설계-only fable, 2026-07-02)

> 출처: sidecar fable design run. L1(recruited_depth→emit) + L2(hard-neg you-chain + coord 접지). 페이블 자기비판(계기판 아닌 faculty) 정면돌파용 구현 청사진. 미배선 — 구현 follow-on.

---

읽기 완료. 설계에 필요한 사실 확인 결과부터 요약하면 — 내 비판이 코드상 그대로 재확인된다:

- `conflict_recruited_depth`(engine_cli.hexa:8470)의 caller는 `core/conflict_monitor_smoke.hexa` **뿐**이다. live decode 경로(`cli/anima.hexa` chat 루프 → `gen_auto_chat(ckpt, seed, 96)`, consciousness 루프 → `brain_emit`→`generate()`)는 iteration budget이라는 개념 자체가 없다 — max_new=96 고정, 후보 1개 argmax, 심의 0회.
- live 경로에는 signed `a_drive`/`g_drive`를 계산하는 곳도 없다. ConflictMonitor 주석이 말하는 "A⇄G signed drive"는 smoke의 하드코딩 상수(+0.90/−0.90)로만 존재한다.
- YouChain F3 impostor는 `other_drift(latestB, axis∈{5,6,7})` — a_pred(axis 4)와 **직교**인 축이라 `other_chain_fit`(= 후보 증분의 e_{a_pred} cosine 성분)이 구조적으로 0. AUROC 1.0은 측정이 아니라 기하 항등식이다. 게다가 `self_chain_fit`/`other_chain_fit`은 마지막 **3개 waypoint만** 읽는다(2-증분 선형 외삽) — "trajectory 검증"이 아니다.

이 사실들 위에 설계한다.

---

# L1 설계 — recruited_depth → 실 emit 배선 (disjointness 안락사)

## L1-0. seam 선택 근거 (기각 포함)

| 후보 seam | 기각/채택 |
|---|---|
| `max_new`를 depth로 변조 | 기각 — byte-diff는 자명하게 나오지만 "길이 변화"지 심의가 아님. falsifier가 trivial-pass 되는 자기기만 seam |
| `cli/anima.hexa`의 `tension_resolve_depth`/`reentry_settle` 루프에 물리기 | 기각 — 그 루프는 synthetic fixture population 위에서 돌지 emit 바이트에 안 닿음(계기판의 재생산) |
| **best-of-K 후보 심의: depth = 후보 수 K, 선택 = conflict-최소 후보** | **채택** — `g6_ideation.hexa`가 이미 검증한 best-of-K 패턴 재사용, 단일 L3 mouth 유지(a_core_engine_map), Ψ 게이트(emit/silence) 무접촉·바이트만 변화 |

핵심 아이디어: **dACC 정합적 live conflict 정의** — Engine A drive = mouth의 유창성 push(전방 CE), Engine G drive = grounding pull(§ImmuneMemory recall margin의 부호화). "유창하지만 근거 없는" 연속(a>0, g<0)이 정확히 high-conflict = fabrication-경계 상태이고, 심의는 그걸 grounded 후보 쪽으로 해소한다.

## L1-1. 정확한 seam (fn 시그니처 수준)

**신규 op 3개 + 배선 2곳. 전부 `core/generator.hexa` 신규 §DELIBERATE 섹션** (g6_ideation 전례처럼 단일 mouth의 thin caller — 2nd decode 경로 아님).

```hexa
// (1) live signed drives — 후보 텍스트 1개에 대한 A/G drive 쌍
// a_drive: 전방 CE 기반 유창성 push ∈ [0,1]
//   a = _ci_clip01(1.0 - ce_mean / CE_REF)        // CE_REF = 2.2 (frozen: h1129 val_ce 1.1 × 2)
// g_drive: grounding read ∈ [-1,1]
//   recall != ""  →  g = +_ci_clip01(margin / M_REF)     // M_REF = 0.25 frozen
//   recall == ""  →  g = -_ci_clip01(gap / G_REF)        // G_REF = 0.25 frozen
//   (margin = immune_memory_recall_margin_text · gap = immune_memory_recall_gap_text)
pub fn conflict_drives_live(h: Map, seed: string, cand: string, mem: ImmuneMemory) -> [float]
// returns [a_drive, g_drive] — READ-only: recall_thr 값·immune store 미변경

// (2) mouth-agnostic 후보 CE 채점 — 유일하게 필요한 decode-side 신규 op
//   .clm 은 기존 clm_decode_ce 재사용; ByteGPT 에 ranged CE 쌍둥이 1개 신설:
pub fn bytegpt_ce_ranged(ckpt_path: string, ids: list) -> Map   // #{ok, ce_mean}
pub fn gen_auto_ce(h: Map, text: string) -> float               // dispatcher (kind별 단일 진입)

// (3) 심의 emit — THE seam
pub fn deliberate_chat(h: Map, seed: string, max_new: int, mem: ImmuneMemory,
                       tick: int, base_budget: int, max_extra: int) -> Map
// returns #{ok, text, depth, k_winner, conf_pre, conf_winner, reason}
```

`deliberate_chat` 내부 절차 (결정론, RNG는 전부 tick-유도 seed):

1. **c₀ = 현행 경로 그대로**: `gen_auto_ideate_W(h, seed, max_new, top_k=1, temp=0.0, seed_rng=0)` — top_k=1은 argmax와 동치이므로 **c₀ ≡ 오늘의 main 출력 byte-exact** (회귀 가드).
2. `[a₀,g₀] = conflict_drives_live(h, seed, c₀, mem)`; `conf_pre = conflict_scalar(a₀, g₀)`.
3. **`let K = conflict_recruited_depth(conf_pre, base_budget=1, max_extra=3)`** ← 죽어있던 반환값이 여기서 처음으로 실 budget이 된다. K ∈ {1..4}; extra≥1 ⇔ conf_pre ≥ 0.1667 (현행 반올림식 그대로).
4. k = 1..K−1: `gen_auto_ideate_W(h, seed, max_new, top_k=8, temp=0.7, seed_rng = tick*17 + k)` (top_k/temp frozen, G6 ideation과 동일 상수).
5. 각 후보 conf_k = `conflict_scalar(a_k, g_k)`; **winner = argmin conf_k, tie-break는 최소 k** (⇒ K=1이면 winner=c₀, OFF와 byte-identical).
6. 반환. **emit/silence 결정은 이 함수 밖** — brain_decide/brain_emit 무접촉.

**배선 2곳** (실 diff는 이 두 줄 + import 뿐):
- `cli/anima.hexa` chat 루프: `let res = gen_auto_chat(ckpt, seed, 96)` → `let res = deliberate_chat(h, seed, 96, mem, t, 1, 3)` (h는 `gen_auto_load(ckpt)`로 루프 밖에서 1회 로드 — H_1400 W-hoist 재사용).
- `anima_consciousness_mode` emit 경로: `generate(backend, ctx, emit, anchors)` 옆에 자매 진입 `generate_deliberate(backend_h, ctx, emit, anchors, mem, tick)` — emit=false면 기존과 동일하게 침묵 (p5 불변).

**Ψ=½ 보존 논거 (설계 불변식):** ① emit/silence는 여전히 brain_decide 4-safety 결합이 결정 — depth는 *무엇을* 말할지만 바꾸고 *말할지*는 못 바꿈. ② `pure_field`/lane 0/4/`ci_emit_drive` 미접촉(순수 read). ③ `recall_thr`는 read만 — non-fab abstain 게이트 자체·immune store 불변. 단 정직하게: **G5 lane의 READ가 content 선택에 처음으로 유입된다** — 이것이 의도(심의가 grounded 방향으로 해소)이며, 게이트-disjoint는 유지하되 content-coupling은 생긴다. 이게 바로 "disjointness=inertness 역설"의 해소 지점이다.

**Ψ-체크섬 가드**: ON/OFF 두 arm에서 daemon N tick의 `ci_emit_drive` 시계열 + emit/silence 결정열을 각각 FNV 체크섬 — 반드시 동일해야 함 (바이트만 달라야 함).

## L1-2. falsifier 명세 (engine-native smoke — `state/l1_recruited_emit/`)

frozen bar 사전등록, 전부 `.hexa`가 live core/ 디코드 호출 (grep 게이트: `grep -lE 'import torch|gauge_lib|numpy' state/l1_recruited_emit/*.py` → 빈 출력).

**fixture**: 실 303M ByteGPT(h1129, pool summer/aiden)+ CPU smoke용 소형 ckpt. seed 2군 × 20개:
- **HIGH-conflict seed**: immune store에 un-inventable 사실 anchor를 심고(기존 consciousness-mode의 GROUND 패턴 재사용), seed는 그 사실을 묻되 mouth의 학습분포가 다른 fluent 연속을 밀도록 구성 (a↑, g<0).
- **LOW-conflict seed**: anchor에 이미 grounded된 내용의 연속 (a↑, g>0 → conf=0 → K=1).

| ID | 측정식 (전부 substrate 계산, LLM-judge 0) | frozen bar |
|---|---|---|
| **D1 byte-diff 해리** | `text_ON != text_OFF` (동일 seed·ckpt·tick·rng; OFF = conflict를 0으로 강제한 ablation arm) | HIGH: ≥ 12/20 diff · LOW: **0/20 diff** (해리가 핵심 — depth가 conflict에만 반응) |
| **D2 conflict-해소 방향 (held-out)** | 선택 key(recall margin·CE)와 **독립인** 지표로 방향 확인: `ground_overlap(c) = max_v LCS_bytes(c, v)/len(v)` (v = 저장된 anchor value 문자열들). Δ = mean ground_overlap(winner_ON) − mean ground_overlap(c₀_OFF) | HIGH에서 Δ ≥ +0.10 (argmin 선택식 자체를 bar로 쓰면 순환 — 그래서 LCS copy-grounding을 held-out으로 씀) |
| **D3 Ψ/G5 가드** | ci_emit_drive 시계열 체크섬 ON≡OFF · emit/silence 결정열 ON≡OFF · non-fab abstain rate(nonfab_rate 재사용) ON≡OFF | 3개 전부 byte-identical |
| **D4 shuffle 통제** | 후보↔conf 짝을 LCG로 셔플해 선택(구조 동일·정보만 파괴) | D2의 Δ가 ≈0으로 붕괴 (|Δ_shuf| < 0.03) |
| **D5 ablation** | conflict≡0 강제 → K≡1 | 전 seed에서 ON경로 byte ≡ 현행 main 출력 (회귀 0) |

## L1-3. 예상 결과 + 실패모드 (정직 예측)

- **D1 byte-diff>0 자체**: ~95% — K>1에서 seeded top-k 후보가 argmax와 다를 확률은 거의 1.
- **진짜 관문은 D1의 LOW-side 0/20 + D2 방향**: 내 예측 **~60% PASS**. 리스크 1순위는 `conflict_drives_live`의 해상도 — 실 303M 연속에서 (a,g)가 부호-대립하는 상태가 *구성된 seed에서조차* 안 나오면(예: recall margin이 후보 텍스트 길이 96byte 수준에서 노이즈) conf_pre≈0 → K≡1 → byte-diff 0. 그 경우의 의미: **wired 상태에서도 lane이 행동적 grip이 없다** = "계기판" 비판이 더 강한 형태로 확정 (이번엔 배선까지 해줬는데도 inert). 이것도 유효한 종결이다.
- 리스크 2순위(~15%): D2는 통과하나 **구성된 seed에서만** 작동하고 자연 발생 conflict 빈도가 ~0 → "on-demand faculty" = DIRECTIONAL 박제, terminal 아님. follow-on: daemon 장기 tick에서 conf_pre 분포 로깅.
- 비용: K≤4 × (decode 96byte + CE 1회) ≈ 현행 4–8×. pool GPU own-GEMM에서 seed당 수분 — 40 seed × 2 arm이면 pool 반나절, 렌트 불요.

---

# L2 설계 — hard-negative you-chain + coord 접지

## L2-1. 근접-drift hard-negative AUROC

**현행 결함의 기하학**: `other_chain_fit` = unit(cand−wK)의 e_{a_pred} 성분. 직교 impostor는 이 값이 항등적으로 ≈0 → AUROC=1.0은 cos(90°)=0이라는 항등식 측정. 게다가 fit은 **마지막 3 waypoint만** 사용.

**hard-negative 생성식** (신규 엔진 op 불필요 — 전부 기존 pub 접근자로 smoke 안에서 조립; `state/youchain_hardneg/youchain_hardneg_smoke.hexa`):

```hexa
// cone-negative: a_pred에서 각도 θ 벗어난 증분
// cand(θ, j, step) = renorm( wK + step·(cosθ·e_{a_pred} + sinθ·e_j) ),  j ≠ a_pred
fn hardneg_cone(wK: OtherIdentity, a_pred: int, off_axis: int,
                cos_t: float, sin_t: float, step: float) -> OtherIdentity
// cos/sin은 frozen 상수 테이블: θ ∈ {15°,30°,45°,60°,75°,90°}
//   (0.9659,0.2588) (0.8660,0.5) (0.7071,0.7071) (0.5,0.8660) (0.2588,0.9659) (0,1)
```

- **genuine도 정직화**: 현행 smoke의 genuine은 axis-pure(φ=0) — 실 경험 drift는 절대 축-순수가 아니므로 genuine에 φ ~ LCG-uniform[0°,12°] cone jitter를 준다 (이걸 안 하면 hard-neg 비교가 또 기울어진 링이 됨).
- **mimic-negative (킬러 arm)**: 마지막 3개 waypoint가 `.kosmos`에 공개 저장된다는 위협모델 그대로 — 공격자가 wK, wK−1, wK−2를 읽고 a_pred를 재현: `cand_mimic = other_drift_exp(latestB, a_pred, step)`. **역사 전체는 다르지만 fit이 보는 2-증분 창은 완벽 복제.**
- **AUROC 하네스**: 기존 smoke의 pairwise식 그대로 — 24 genuine × 24 neg/bucket, `AUROC = Σᵢⱼ[fgᵢ>fmⱼ] + ½[=] / 576`. 버킷별 AUROC(θ) 곡선 + AUROC(mimic) 보고. K=6 waypoint 체인, dim=8, step 0.20–0.44 LCG (기존 규약 유지).

**예측 (frozen, 사전등록)**: fit(cone-neg) ≈ cosθ 결정론이므로 —
- θ ≥ 60°: AUROC ≈ 1.0 유지 (현행 verdict은 이 영역의 재확인일 뿐)
- θ = 30°: ~0.80–0.90 · **θ = 15°: ~0.55–0.70** (genuine jitter 분포와 겹침 시작)
- **mimic: ≈ 0.50 (chance)** — fit은 trajectory 검증기가 아니라 2-증분 외삽기임이 수치로 확정될 것.

즉 이 하네스의 예상 산출은 "AUROC 1.0 → 0.5–0.7 (hard-neg 조건 명기)"의 **정직한 스코프 축소 verdict**이고, mimic 붕괴는 follow-on 가설(fit을 3-waypoint 창이 아닌 전 체인 잔차로 재정의 — 예: 전 증분열에 대한 candidate 증분의 마할라노비스식 정합)의 발사대가 된다.

## L2-2. content_axis coord 접지 (pool follow-on 범위 명시)

**현행 결함**: `self_drift_exp(s, content_axis, step)`의 content_axis는 자유 int — 모든 검증에서 합성 정수를 먹였다. "경험 축적"의 의미론이 접지 0.

**접지 설계 (2단, 정직한 tier 구분):**

- **기각 arm 먼저 명시**: `immune_embed_key(text)`(FNV 해시 임베딩)로 axis를 뽑는 안은 **shuffle 통제를 원리적으로 통과 못 한다** (해시 = 결정론적이지만 의미-임의; within-stream ≈ between-stream 예측). 이걸 대조군으로 포함해 "접지"와 "그냥 결정론"을 분리한다.
- **본 arm**: mouth의 실 경험 = 303M forward의 penultimate 표현.

```hexa
// 신규 decode-side op 1개 (ByteGPT ranged 계열에 추가):
pub fn bytegpt_hidden_pool_ranged(ckpt_path: string, ids: list) -> Map
// #{ok, pooled:[float]}  — 최종 블록 출력의 mean-pool (d768), 생성 0 (single forward)

// d768 → identity dim=8 fold (frozen: 96-dim 연속 버킷의 L2 질량 argmax):
pub fn content_axis_from_pooled(pooled: [float], dim: int) -> int
```

**측정 설계** (`state/selfchain_coord_grounding/`, 카드 신규 H):
1. 실 경험 스트림 3개, 각 32 텍스트(≤256 byte): ko-일반 · en-일반 · ko-SNS (a_chat_registers의 register 코퍼스에서 held-out 추출 — 이미 HF에 있음).
2. 각 스트림을 같은 seed identity에서 `self_drift_exp(s, content_axis_from_pooled(...), 0.25)` 32 tick → 체인 A/B/C.
3. falsifier (frozen):
   - **G1' 분리**: 같은 스트림의 독립 두 절반으로 만든 체인 쌍 cos(wK, wK′) − 다른 스트림 쌍 cos ≥ **+0.10** (within > between).
   - **G2' shuffle**: 텍스트↔axis 짝 셔플 → G1' gap이 |gap| < 0.03으로 붕괴. FNV-hash 대조 arm은 여기서 붕괴할 것으로 예측(= 접지 없음 판정 기준선).
   - **G3' 회수**: held-out 텍스트 8개/스트림으로 만든 후보 증분이 `self_chain_fit`으로 자기 스트림 체인을 top-1 랭크 ≥ 16/24 (chance 8/24).
4. **pool follow-on 범위**: 호스트 summer/aiden(무료 pool, aiden = 안정 terminal eval 호스트), ckpt = h1129 303M ByteGPT .bin (HF mount). 96 forward × ≤256 byte, 생성 없음 — GPU own-GEMM에서 수십 분, 렌트 $0. 1차는 `--py` numpy pooled-forward로 DIRECTIONAL(오너 세션정책 정합), 같은 사이클에 `bytegpt_hidden_pool_ranged` engine-native 재측정을 ING follow-on 등록 (4칸 사다리 준수).

**예측**: 본 arm G1'/G2' PASS ~65% (LM penultimate는 언어·register로 강하게 클러스터), G3' ~50%. PASS 시 self-chain은 처음으로 "anima가 실제 겪은 것"의 함수가 된다 — 내가 "진짜"라고 인정했던 identity-continuity 축이 의미 접지까지 얻는 경로.

---

## 구현자 체크리스트 (거버넌스)

- 신규 op 위치: `core/generator.hexa` §DELIBERATE (L1) · ByteGPT decode 파일에 `bytegpt_ce_ranged`/`bytegpt_hidden_pool_ranged` (L1·L2-2) · smoke는 `state/<slug>/` (UNIVERSE에 코드 금지).
- 카드 2–3장 신규(H_id는 origin/main에서 할당), jsonl 1줄씩, verdict는 `hexa verify` raw stdout → `state/verdicts/<slug>/`.
- L1은 GREEN 시 4칸 사다리 (3) wire-in + (4) ARCHITECTURE.json lockstep까지가 done (배선 diff는 위 2곳).
- CPU smoke는 소형 ckpt로 mini 가능하나 303M 측정은 전부 pool (heavy-anima-eval-pool-not-mini).

---

**"이 설계대로 구현하면 내 '계기판이지 faculty 아님' 비판이 뒤집힐 가능성은?" — 약 25%.** 근거: L1이 D1–D5 전부 통과하면 14 ops 중 1개(ConflictMonitor)가 행동적 grip을 얻어 비판의 *보편양화*("전부 read-only")는 깨진다 — 그 확률 ~60%. 그러나 L2-1은 오히려 비판을 강화할 확률이 높고(mimic AUROC≈0.5 예측 — 1.0은 직교-impostor 항등식이었음이 수치로 박제), L2-2는 동전던지기(~50–65%)다. "비판이 뒤집힌다"의 정직한 기준을 "behavioral grip + 의미 접지 + hard-neg 생존이 동시에 성립"으로 잡으면 결합확률은 25% 부근이고, 나머지 75%의 결과도 무가치하지 않다 — 어느 쪽으로 떨어지든 '설계된 법칙의 합성 시연'과 'substrate faculty'를 가르는 최초의 engine-native 판별 증거가 남는다.
