# H_1368 — 🇰🇷 ko-data-richness: NOVEL-context CE 가 코퍼스 윈도가 커질수록 jamo 2.51335 floor 로 내려가는가?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1368_ko_data_richness` · **Tier:** 📉 DESCENDING-UNSATURATED — novel-context CE 가 윈도와 함께 **단조 감소**(3.153→2.882, 3.75→30MB), 30MB 의 2.882 는 saturated floor 가 **아니라** 여전히 내려가는 데이터-풍부도 곡선 위의 한 점. **data-richness lever 는 LIVE** (H_1359 가 못 닫고 남겨둔 마지막 레버가 살아있음). 단 4-rung 으로 asymptote 를 못 박음 — floor 까지는 추가 ~4 window-doublings(~470MB) 필요. asymptote 가 floor 의 AT/ABOVE/BELOW 인지는 **UNRESOLVED** (>30MB 사다리 필요, NO over-claim of GREEN, c9).

DIRECTIONAL numpy · REAL R2 KO 코퍼스 sha `c47b6808…` (== H_1316/H_1344/H_1359, byte-fair) · $0 CPU (11.0s) · frozen-first (FREEZE 가 scoring 전에 작성) · λ·표상·novel-filter **모두 H_1359 와 동일 FROZEN** (rung 마다 재튜닝 안 함, anti-Goodhart) · c9/p7 NO tune-to-green · live CORE UNTOUCHED.

## Claim (falsifiable, 마지막 레버)
한국어 압축 arc 는 두 레버가 닫혔다: 표상(H_1322 featural 🧱)·interpolation(H_1359 JM=암기 🧱, 2.513 jamo floor 진짜·novel context CE=2.882>floor 확인). 남은 ONE 레버 = **data-richness**. H_1359 가 NEXT-1 로 명시: 코퍼스 윈도가 커지면 novel-context CE(30MB 의 2.882)가 floor 쪽으로 **내려가는가**? 2.513 이 hard floor 인가, 아니면 30MB 가 내려가는 곡선 위에 우연히 앉은 지점인가?
- 내려간다 → floor 는 아래로부터 hard 가 아님 = data-richness lever 살아있음 (loudly).
- 안 내려간다(flat/증가) → 2.513 은 세 레버 전부에서 hard floor 로 확정, lane DEPLETED (honest 🧱, c9).

## Method (frozen-first; H_1359 기계 verbatim 재사용)
- **REAL Korean only**: 30MB R2 KO 윈도, sha256 ASSERTED `c47b6808…`(== H_1316 floor baseline/H_1344/H_1359). 각 rung 은 이 **동일 코퍼스의 PREFIX 서브윈도**. sha mismatch → STOP, NO synthetic.
- **jamo 표상 (H_1316/H_1359 동일)**: Hangul→NFD jamo(id 256+rank), non-Hangul→raw byte; n_bytes 합산=원본 UTF-8 byte(byte-fair). jamo vocab 은 FULL 30MB 에서 한 번 고정(rung 간 vocab drift 없음), Vj=323.
- **JM (H_1344/H_1359 동일)**: frozen-λ Jelinek-Mercer recursive interpolation, λ=[1,2,4,8,16]/31, nmax=5, Laplace 1.0. **rung 마다 재튜닝 X** (anti-Goodhart).
- **NOVEL filter (H_1359 TEST A 동일)**: 각 rung 에서 stride=300 even=TRAIN/odd=TEST, TEST 위치 중 top-order(4-jamo) context 가 TRAIN top-order set 에 **없는** 위치만 점수 = genuine-generalization 슬라이스.
- **DATA-RICHNESS LADDER (4 rung)**: 3.75 / 7.5 / 15 / 30 MB prefix 서브윈도. 30MB rung 은 H_1359 의 novel-CE 2.88190(±0.02) 을 **재현해야** sanity anchor 통과(아니면 STOP, methodology drift).

## Frozen bars (FREEZE verbatim, 사후 이동 없음)
| bar | test | result | pass |
|-----|------|--------|------|
| **c1 CURVE** | ≥3 rung 점수 + 30MB anchor 재현(|Δ|≤0.02 vs 2.88190) | 4 rung, 30MB=**2.88190** (|Δ|=**0.00000**) | ✅ |
| **c2 DIRECTION** (사전등록) | novel-CE 가 윈도와 단조 **감소**? (각 step Δ≤−0.001) | step ΔCE=[**−0.0818, −0.1170, −0.0719**] → **DECREASING** | ✅ DECREASING |
| **c3 ASYMPTOTE** | 두 estimator 로 asymptote 추정 + floor 대비 분류 | log-fit b=**−0.0929**/doubling (r²0.992); power-fit c_inf=1.099 **UNRELIABLE**(floor 한참 아래=비물리) → **UNDETERMINED** | (honest) |
| **c4 EARNED** (anti-Goodhart) | shift surrogate 가 모든 rung 에서 반대로(shift−novel≥0.05) | [**+2.45, +2.55, +2.76, +2.93**] | ✅ all 4 earned |

→ **📉 DESCENDING-UNSATURATED** (c1✅ ∧ c4✅ ∧ c2=DECREASING ∧ c3=UNDETERMINED). FREEZE 의 사전등록 분기 — tune-to-green 아님.

## Results
| rung (윈도) | stream len | novel_frac | **novel-CE** | Δ vs 2.51335 floor | shift surrogate | shift−novel |
|---|---|---|---|---|---|---|
| 3.75MB | 3,192,955 | 0.609 | **3.15254** | +0.63919 | 5.60066 | +2.448 |
| 7.5MB | 6,387,044 | 0.494 | **3.07077** | +0.55742 | 5.62226 | +2.551 |
| 15MB | 12,753,603 | 0.395 | **2.95376** | +0.44041 | 5.71864 | +2.765 |
| **30MB** | 25,501,291 | 0.299 | **2.88190** | **+0.36855** | 5.81040 | +2.928 |

- jamo floor(locked) = 2.51335 · raw-byte ceiling = 2.95342 (참조).
- 30MB novel-CE=**2.88190** 는 H_1359 TEST A 와 **정확히 일치**(|Δ|=0.0) → 기계 동일성 확인.
- **단조 감소 monotone**: 윈도 8× 키우면 novel-CE 가 +0.639→+0.369 (floor 위 격차가 **42% 축소**). 즉 30MB 의 2.882 는 floor 가 아니라 **여전히 내려가는 곡선 위의 점**.
- log-linear 추세: −0.0929 nats/window-doubling (r²0.992). 이 추세로 floor 를 **닿으려면** 30MB 에서 **~3.97 추가 doublings (~470MB)** 필요.
- power-law fit(c_inf=1.099)는 4-point 라 **under-constrained** → c_inf 가 raw-ceiling 보다도 아래(비물리)라 RELIABILITY GUARDRAIL 이 **UNRELIABLE** 플래그 → asymptote **UNDETERMINED** (GREEN over-claim 차단, c9).

## ⚠ HONEST SCOPE — 무엇이 확정되고 무엇이 아닌가 (c9)
- **확정**: novel-context CE 는 코퍼스 윈도와 함께 **단조 감소**한다 — [3.75, 30]MB 전 구간에서 (shift control 이 모든 rung 에서 earned). 따라서 H_1359 의 2.882 는 **saturated floor 가 아니다**; 그건 내려가는 data-richness 곡선 위의 30MB 지점일 뿐. **data-richness lever 는 LIVE** — H_1359 가 닫지 못하고 NEXT-1 로 남겨둔 레버가 살아있음을 확인.
- **확정 아님 (UNRESOLVED)**: 진짜 asymptote 가 2.51335 floor 의 **AT/ABOVE/BELOW** 중 어디인지. 4-rung 으로는 power-law tail 이 under-constrained(c_inf 비물리) → 못 박음. log-linear 추세는 floor 도달에 ~470MB 를 요구 = 이 30MB-bounded 사다리가 담을 수 없는 양. 표상 레버가 "데이터로" 재오픈되는지(BELOW)는 아직 미해결.
- **확정 아님 (scope)**: DIRECTIONAL numpy, toy stride-300 byte-substrate next-symbol CE(fluent decoder 아님, 한국어 유창성 주장 없음). 사다리는 **ONE 30MB 코퍼스의 PREFIX 서브윈도**(>30MB 풍부도는 미검증, 상한 bounded). 단일 frozen λ·단일 stride·단일 표상(jamo). asymptote=4-point 외삽 추정(wide CI). engine-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).

## 결론 / next angle
**2.51335 floor 는 아래로부터 hard 가 아니다** — novel-context CE 는 더 많은 데이터로 계속 내려간다(30MB 에서도 미포화, 격차 −0.0929/doubling). 한국어 압축 arc 의 세 번째 레버(data-richness)는 **닫히지 않고 LIVE**. 다만 floor 도달/돌파 여부는 이 30MB 사다리로는 미해결.
- **NEXT-1 (a_break_the_wall · a_fire_autonomous)**: >30MB 사다리 (60/120/240/480MB, R2 KO 추가 shard fetch). log-linear 추세가 ~470MB 에서 floor 를 닿는다고 예측 → 480MB rung 이 floor 의 AT/ABOVE/BELOW 를 결정. asymptote 가 진짜로 floor 아래로 가면 **표상 레버가 데이터로 재오픈**(H_1322 🧱 우회) = 🟢 후보.
- **NEXT-2 (a_engine_native_learning)**: 이 곡선은 DIRECTIONAL numpy mirror — 곡선이 진짜면 engine-native(CORE VAdaptField count-MLE)에서 재확인해야 verdict. 단 더 큰 데이터가 필요한 결론이라 엔진-transfer 전에 데이터 사다리부터.

## Pointers
- 카드: `UNIVERSE/cards/H_1368_ko_data_richness.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1368)
- 코드: `state/ko-data-richness/h1368_ko_data_richness.py`
- 증거: `.verdicts/1368_ko_data_richness/{H_1368_FREEZE.txt, result.txt, H_1368.txt}`
- CLAIMS: `CLAIMS.tape` @C h1368_ko_data_richness
- xref: h1359(JM=암기, novel-CE 2.882 anchor·이 카드가 NEXT-1)·h1344(JM GREEN=암기)·h1316(jamo floor 2.513)·h1322(featural 🧱)·h1307(raw ceiling)·a_no_llm_frame_trap·a_break_the_wall·a_fire_autonomous·a_engine_native_learning·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c9·c15
