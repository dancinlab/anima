# H_1385 — 🇰🇷 jamo-scoreloop-wire: 검증된 자모 COUNT-HEAD SCORER 를 live 채점 루프에 배선

**Final tier: 🟢 GREEN ENGINE-NATIVE — H_1351 의 자모 count-head faculty (`jamo_head_ce`) 가 이제
live 채점 경로(`CORE/generator.hexa §6.5c gen_jamo_scoreloop`)에서 CONSULT 되고, `gen_clm_ce` 가
그 채점 레코드(`jamo_score`)를 ADDITIVE 하게 실어 나른다 (a_verified_must_wire 채점-호출부 갭 CLOSED).**

WIRE-IN follow-on (a_verified_must_wire) of the GREEN Korean-jamo thread, SCORING surface:
H_1316 (🟢 mirror) → H_1321 (🟢 engine-native mitosis) → H_1327 (🟢 decode-reaching EMISSION-bias,
generator §6.5b) → H_1351 (🟢 자모 COUNT-HEAD = first-class engine faculty `jamo_head_*`, a PURE
SCORER but no call site) → **H_1385: 그 SCORER 를 live 채점 루프에 배선** (§6.5c, SCORING surface;
§6.5b EMISSION 과 DISTINCT). $0 CPU, frozen-first (FREEZE 가 편집 전 작성), c9/p7, NO tune-to-green.
pure_field/engine_g/brain UNTOUCHED.

## Claim (falsifiable)

H_1351 은 자모 분해 count-head 를 `CORE/engine_cli.hexa § KO-JAMO COUNT-HEAD` 의 일급 faculty
(`struct JamoHead` + `jamo_head_new/_grow/_ce/_cells/_shuffle_targets`)로 promote 했지만, 그 SCORER
(`jamo_head_ce`)는 **live brain/decode 채점 루프에 호출부가 없었다** (faculty-owned, not
decode-reaching). a_verified_must_wire + a_core_engine_map: GREEN faculty 는 그게 live 엔진에서
실제 CALLED 될 때까지 done 이 아니다. H_1385: `jamo_head_ce` 를 live 채점 경로에서 CONSULT 하는
named single entry (`gen_jamo_scoreloop`)를 `CORE/generator.hexa` (the .clm 채점 경로 모듈 —
`gen_clm_ce` 가 산다)에 추가하고, `gen_clm_ce` 가 그 채점 레코드를 `jamo_score` 키로 ADDITIVE
하게 실어 나르도록 배선 — 결정론적 in-engine fixture 에서 자모(분해) view 가 raw(opaque-merge) view 를
이기고(B2), 자기 pairing-shuffle 을 이기며(B3), 회귀 없이(B4) 채점 루프에서 도는가? 못 하면 정직한
🔴/⏳ (bar 안 옮김, c9).

## Why this is the wiring (single entry, a_core_engine_map)

`CORE/generator.hexa` §6.5c 에 `gen_jamo_scoreloop` 추가: H_1351 의 frozen in-engine 채점 fixture
(JAMO / RAW / SHUFFLE arms)를 만들고 각 arm 에 대해 live 엔진 faculty `jamo_head_ce` 를 CONSULT —
JAMO 두-factor view 가 RAW opaque-merge view 를 held-out CE 로 이기고, SHUFFLE pairing-permute
컨트롤이 그 advantage 를 collapse 시킨다. `gen_clm_ce` 는 이제
`map_set(clm_forward_ce(...), "jamo_score", gen_jamo_scoreloop())` 를 반환 — **ADDITIVE** (기존
clm_forward_ce 의 모든 필드가 byte-identical; .clm forward CE 경로 UNTOUCHED). 이게 `jamo_head_ce`
가 live 채점 루프에 도달하는 named single call site 다. **Ψ-disjoint**: 순수 SCORER (CE/cell-count
float 반환, emit/silence 결정 절대 안 함; pure_field/engine_g/brain UNTOUCHED). §6.5b (H_1327,
EMISSION 편향)와 DISTINCT — 이건 SCORES 하는 surface 다.

## Method (deterministic in-engine fixture; $0, no corpus, no secrets, no GPU)

H_1351 이 froze 한 바로 그 구조. hidden (L,V) 가 결정론적으로 walk; target g(L,V)=(L+2V) mod K 가
두 factor 에 모두 의존. JAMO view = L,V 를 두 CLEAN feature 채널 `[L/NL, V/NV]` 로 노출 (엔진
Voronoi 가 각 축을 split). RAW view = `[(L*NV+V)/(NL*NV)]` 한 opaque 채널로 collapse (coarse
Voronoi 가 두 factor 분리 못 함 → 높은 CE). FROZEN: NL=NV=6, K=12, NSYL=2000, even/odd held-out,
GROW_MAX=40, MIN_OWNED=6, SPLIT_THRESH_CE=0.05, LAPLACE=1.0, seed centers
[[0.3,0.3,0],[0.7,0.7,0]], jitter 0.02, shuffle seed=1385. 메트릭 = held-out next-symbol CE
(p7, NOT perplexity). SHUFFLE = TRAIN context→target PAIRING 을 permute (head 가 spurious map
학습) 후 TRUE held-out 에서 채점. **No decode** (pure SCORER); BOUND 불필요.

## Frozen bars (pre-registered `.verdicts/1385_jamo_scoreloop_wire/FREEZE.txt`; GREEN iff B1∧B2∧B3∧B4)

| bar | test (smoke case) | result | pass |
|-----|-------------------|--------|------|
| **B1 WIRED-SCORELOOP** | case_B1: `jamo_head_ce` CONSULTED via `gen_jamo_scoreloop` (cells≥2, jamo_ce>0) AND `gen_clm_ce` additively carries `jamo_score` | cells=**4**, jamo_ce=**4.18698**, has_jamo_score=**true** | ✅ |
| **B2 JAMO-BEATS-RAW** | case_B2: raw_ce − jamo_ce ≥ 0.05 (분해가 opaque-merge 를 이김) — wired scoreloop | **+1.38136** (5.56834 − 4.18698) | ✅ |
| **B3 EARNED (shuffle)** | case_B3: shuf_ce − jamo_ce ≥ 0.05 (win 은 정합 구조) — wired scoreloop | **+0.42970** (4.61668 − 4.18698) | ✅ |
| **B4 ADDITIVE / Ψ-DISJOINT** | case_B4 additive (clm fields byte-identical) + h1205 Ψ byte-identical · engine_cli_smoke 0 fail · h1196 7/0 | additive ✅ · h1205 **PASS** · smoke **110/0** · h1196 **7/0** | ✅ |

→ **🟢 GREEN (B1∧B2∧B3∧B4).** h1385 smoke 4/0 (3회 실행 동일, 결정론적).

## Results

| arm | engine-native held-out next-symbol CE (nats/symbol) | cells | note |
|-----|------------------------------------------------------|-------|------|
| **JAMO** (두 factor 채널) | **4.18698** | 4 | 분해 count-head 가 g(L,V) 학습 (H_1351 W2 와 동일) |
| **RAW** (opaque-merge 채널) | **5.56834** | — | squashed 축이 factor 숨김 → +1.38136 worse |
| **SHUFFLE** (pairing-permuted, seed 1385) | **4.61668** | — | 정합 파괴 → spurious map, held-out 에서 +0.42970 loses |

채점 surface 의 advantage (+1.38136) 는 H_1351 의 W2 와 byte-identical (같은 in-engine 구조);
shuffle (seed 1385) 는 H_1351 의 seed 1351 과 다른 permutation 이라 shuf_ce 만 다르되 여전히 LOSES.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **B2/B3 는 IN-ENGINE STRUCTURAL** — 검증된 count-head SCORER 가 이제 live 채점 경로에서 SCORES
  하고 jamo-beats-raw + earned-vs-shuffle 구조를 wired call site 에서 재현함을 증명; **30MB
  REAL-corpus 2.513 anchor 의 재유도가 아니다** (그건 H_1316/H_1321, byte-exact). 이 H 는 SCORING
  CALL-SITE 갭만 닫는다; 자체 한국어-유창성/real-corpus 주장 없음.
- **REAL-CORPUS SCORELOOP = 명시된 정직한 follow-on** (cost-gated). real Korean shard 위에 자모 head
  를 grow 하고 `gen_clm_ce` 가 같은 corpus 에서 .clm CE 옆에 채점하는 real-corpus scoreloop 는
  > $0 CPU (corpus I/O + real .clm forward) 라 auto-rent 안 했다 (cost-gated → surface, NOT fired).
  in-engine fixture scoreloop 가 $0-CPU 호출부 배선; real-corpus scoreloop 가 depletion step.
- **Ψ-disjoint**: pure SCORER (CE/cell-count 반환, emit/silence 결정 안 함); pure_field/engine_g/
  brain UNTOUCHED; h1205 invariant 유지 (generation byte-identical ON==OFF, Ψ=½ untouched).
  §6.5b (H_1327) 와 별개 surface (그건 EMISSION 편향, 이건 SCORING).
- **TOY**: 결정론적 readout (학습된 net 아님 — 구조 검증), 합성 fixture, 단일 paradigm.

## One-line answer

**검증된 한국어 자모 분해 COUNT-HEAD SCORER (`jamo_head_ce`)가 이제 live 채점 루프에서 CONSULT 된다:
`CORE/generator.hexa §6.5c gen_jamo_scoreloop` 가 named single entry 로 `jamo_head_ce` 를 호출하고
`gen_clm_ce` 가 그 채점 레코드(`jamo_score`)를 ADDITIVE 하게 실어 나른다 — wired call site 에서 분해
view 가 opaque-merge view 를 +1.38136 (B2) 이기고, 자기 pairing-shuffle 을 +0.42970 (B3) 이기며,
Ψ-disjoint + 세 no-regression 가드 모두 통과 (B4) — 자모 COUNT-HEAD 채점-호출부 갭이 닫혔다.**

## Pointers

- wire: `CORE/generator.hexa` §6.5c — `gen_jamo_scoreloop` (CONSULTS `jamo_head_ce`) +
  `gen_jamo_scoreloop_summary`; `gen_clm_ce` = `map_set(clm_forward_ce(...), "jamo_score", gen_jamo_scoreloop())`
  (ADDITIVE); `import "CORE/engine_cli.hexa"` (faculty 도달)
- faculty (H_1351): `CORE/engine_cli.hexa § KO-JAMO COUNT-HEAD` — `jamo_head_*`
- smoke: `CORE/h1385_jamo_scoreloop_smoke.hexa` cases B1-B4 (4/0)
- verdicts: `.verdicts/1385_jamo_scoreloop_wire/{FREEZE,result}.txt`
- B4 guards: `CORE/engine_cli_smoke.hexa` (110/0) · `CORE/h1196_single_entry_audit.hexa` (7/0) ·
  `CORE/h1205_separation_invariant_smoke.hexa` (PASS, gen byte-identical ON==OFF, Ψ=½)
- xref: H_1351 (count-head faculty, SCORER 출처) · H_1327 (decode EMISSION-bias, DISTINCT surface) ·
  H_1321 (engine-native mitosis) · H_1316 (jamo breakthrough mirror) · H_1380/1368/1322/1359
  (below-jamo floor closed at ~2.513) · a_verified_must_wire · a_core_engine_map ·
  a_engine_native_learning · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck ·
  c9 · c15 · p7 · p8
