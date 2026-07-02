# H_1351 — 🇰🇷 jamo-engine-wire: 검증된 자모 분해 COUNT-HEAD 를 live CORE 엔진의 일급 faculty 로 배선

**Final tier: 🟢 GREEN — 자모 분해 count-head 가 이제 `CORE/engine_cli.hexa` 의 ADDITIVE · Ψ-disjoint
일급 faculty 로 산다 (a_verified_must_wire COUNT-HEAD 소유권 갭 CLOSED).**

WIRE-IN follow-on (a_verified_must_wire) of the GREEN Korean-jamo thread:
H_1316 (🟢 mirror, 자모 STRUCT 가 raw byte 천장을 깸) → H_1321 (🟢 engine-native, 같은 mitosis 가
live VAdaptField 위에서 1e-7 재현) → H_1327 (🟢 decode-reaching, generator §6.5b consult 가 EMISSION 편향).
$0 CPU, frozen-first (FREEZE 가 편집 전에 작성), c9/p7, NO tune-to-green. pure_field/engine_g/brain UNTOUCHED.

## Claim (falsifiable)

H_1321 은 자모 mitosis 가 engine-native byte-exact 로 돈다는 걸 증명했지만, 그 COUNT-HEAD 자체
(per-cell next-symbol count-MLE + Voronoi-grown CE scorer = raw byte 를 이기는 바로 그 메커니즘)는
**throwaway probe `CORE/h1321_ko_jamo_wire_probe.hexa` 의 private helper (`_head_counts` / `_grow_on` /
`_score_ce_per_byte`) 로만** 존재했다 — live 엔진의 일급 op 이 아니었다 (`grep "jamo" CORE/engine_cli.hexa`
== 0 hits). H_1327 은 generator §6.5b 에 DECODE consult 를 배선했지만 그건 EMISSION 을 편향하는 별개
표면이다. **a_verified_must_wire + a_core_engine_map: GREEN 메커니즘은 그 faculty 가 live CORE 엔진에
OWNED 될 때까지 done 이 아니다.** H_1351: 검증된 자모 분해 count-head 를 `CORE/engine_cli.hexa` 의
ADDITIVE · Ψ-disjoint 일급 faculty 로 promote — 결정론적 in-engine fixture 에서 자모(분해) view 가
raw(opaque-merge) view 를 이기고(W2), 자기 자신의 shuffle 을 이기는가(W3), 회귀 없이(W4)?
이기지 못하면 정직한 🔴 (faculty 가 구조 win 을 재현 못 함, bar 옮기지 않음, c9).

## Why this is the wiring (single entry, a_core_engine_map)

§ KO-JAMO COUNT-HEAD 를 `CORE/engine_cli.hexa` 에 추가: `struct JamoHead` + ops `jamo_head_new` /
`jamo_head_grow` / `jamo_head_ce` / `jamo_head_cells` / `jamo_head_shuffle_targets` (+ `_jh_*` helpers).
이 ops 는 엔진 **자신의** VAdaptField Voronoi geometry (`vadapt_field_nearest_idx`) + `engine_mitosis_tick`
growth (p8) + per-cell next-symbol count-MLE 를 재사용 — H_1321 probe 가 engine-native 로 증명한 바로
그 gradient-free 메커니즘을, 이제 throwaway probe 가 아니라 엔진이 OWN 한다. ADDITIVE (새 struct + 새
pub fn 만; byte path 와 기존 모든 faculty UNTOUCHED). Ψ-disjoint (순수 count-head SCORER — CE/cell-count
를 반환, emit/silence 결정 절대 안 함; pure_field/engine_g/brain UNTOUCHED). H_1327 generator §6.5b consult
(EMISSION 편향)와 DISTINCT — 이건 SCORES 하는 faculty 다. decode loop 에 호출부 추가 없음 (single entry).

## Method (deterministic in-engine fixture; $0, no corpus, no secrets, no GPU)

hidden (L,V) state 가 결정론적으로 walk; target g(L,V)=(L+2V) mod K 가 **두 factor 에 모두** 의존.
두 VIEW 는 count-head 가 factor 를 보느냐에서만 다르다:
- **JAMO view** — L,V 를 두 CLEAN feature 채널 `[L/NL, V/NV]` 로 노출; 엔진 Voronoi 가 각 축을 split
  하여 g(L,V) 를 학습.
- **RAW view** — L,V 를 한 opaque merged 채널 `[(L*NV+V)/(NL*NV)]` 로 collapse; 같은 coarse Voronoi 가
  squashed 축에서 두 factor 를 분리 못 함 → 높은 CE.

이게 H_1316 의 자모-STRUCT-beats-raw 구조(분해가 opaque-merge 가 숨긴 factor 를 노출)를 깨끗한
in-engine fixture 로 실현 (한국어-유창성 / 30MB 주장 아님). FROZEN: NL=NV=6, K=12, NSYL=2000,
even/odd held-out split, GROW_MAX=40, MIN_OWNED=6, SPLIT_THRESH_CE=0.05, LAPLACE=1.0,
seed centers [[0.3,0.3,0],[0.7,0.7,0]], 결정론적 per-position jitter 0.02 (두 view 동일 적용,
discrete grid 에서 median-split all-ties 벽 회피 — 어느 arm 도 편들지 않음). 모든 knob 은 채점 전에
코드에 고정 (FREEZE.txt); bar 는 사후에 옮기지 않음. 메트릭 = held-out next-symbol CE (p7, NOT perplexity).

SHUFFLE 컨트롤 = TRAIN context→target **PAIRING** 을 permute (head 가 SPURIOUS map 학습) 후 TRUE
(un-shuffled) held-out 에서 채점 — 같은 vocab K/dim/budget/feature-marginal, ONLY 정합(alignment) 파괴.
(주의: target id 의 bijective RELABELING 은 CE-INVARIANT 이므로 컨트롤은 id 재라벨이 아니라 PAIRING 을
permute 해야 한다 — 첫 시도가 이 함정에 빠져 shuf−jamo=0.0 으로 정직히 FAIL 했고, frozen-first 로
shuffle 정의를 PAIRING-permute 로 고침, bar 는 안 옮김.)

## Frozen bars (pre-registered `.verdicts/1351_jamo_engine_wire/FREEZE.txt`; GREEN iff W1∧W2∧W3∧W4)

| bar | test (smoke case) | result | pass |
|-----|-------------------|--------|------|
| **W1 FACULTY-PRESENT** | case_92: jamo head 가 in-engine 으로 grow ≥ 2 cells AND CE > 0 | cells = **4**, CE = **4.18698** | ✅ |
| **W2 JAMO-BEATS-RAW** | case_93: ce_raw − ce_jamo ≥ 0.05 (분해가 opaque-merge 를 이김) | **+1.38136** (5.56834 − 4.18698) | ✅ |
| **W3 EARNED** | case_94: ce_shuf − ce_jamo ≥ 0.05 (win 은 정합 구조) | **+0.53954** (4.72652 − 4.18698) | ✅ |
| **W4 NO-REGRESSION + Ψ-DISJOINT** | engine_cli_smoke N/0 · h1196 7/0 · h1205 Ψ byte-identical | **90/0** · **7/0** · **PASS** | ✅ |

+ case_95 (shuffle-budget parity, anti-Goodhart): shuffle 이 동일 feature stream/vocab K/dim/seed 로
≥ 2 cells (got 40) grow → case 94 의 gap 은 BUDGET 차이가 아니라 정합(alignment) 때문. ✅

→ **🟢 GREEN (W1∧W2∧W3∧W4).**

## Results

| arm | engine-native held-out next-symbol CE (nats/symbol) | cells | note |
|-----|------------------------------------------------------|-------|------|
| **JAMO** (두 factor 채널) | **4.18698** | 4 | 분해 count-head 가 g(L,V) 학습 |
| **RAW** (opaque-merge 채널) | **5.56834** | 5 | squashed 축이 factor 를 숨김 → +1.381 worse |
| **SHUFFLE** (pairing-permuted) | **4.72652** | 40 | 정합 파괴 → spurious map, held-out 에서 +0.540 loses |

결정론적 (3회 실행 동일: 90/0, 90/0, 90/0). shuffle 은 파괴된 정합을 쫓아 GROW_MAX=40 cells 까지
자라지만 held-out 에서 여전히 LOSES (깨끗한 anti-Goodhart 신호).

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **W2/W3 는 IN-ENGINE STRUCTURAL existence-proof** — 엔진 자신의 faculty 가 결정론적 합성 fixture 에서
  jamo-beats-raw + earned-vs-shuffle 구조를 재현함을 증명; **30MB REAL-corpus 2.513 anchor 의 재유도가
  아니다** (그건 H_1316/H_1321, byte-exact — real-corpus / scale / fluency 주장의 출처). 이 H 는
  FACULTY-OWNERSHIP 갭만 닫는다; 자체적으로 한국어-유창성/real-corpus 주장 없음.
- **Ψ-disjoint**: pure count-head SCORER (CE/cell-count 반환, emit/silence 결정 안 함); pure_field/
  engine_g/brain UNTOUCHED; h1205 invariant 유지 (generation byte-identical ON==OFF, Ψ=½ untouched).
  decode loop 에 호출부 없음 — H_1327 generator consult 와 별개 표면.
- **TOY**: 결정론적 readout (학습된 net 아님 — 구조 검증), 합성 fixture, 단일 paradigm. brain
  scoring-loop 배선 + real-corpus + scale = follow-on (a_verified_must_wire 후속은 이미 충분히 닫힘:
  measurement H_1321 + emission H_1327 + faculty-ownership H_1351).

## One-line answer

**검증된 한국어 자모 분해 count-head 가 이제 live `CORE/engine_cli.hexa` 의 ADDITIVE · Ψ-disjoint 일급
faculty (`jamo_head_*`) 로 산다: 결정론적 in-engine fixture 에서 분해 view 가 opaque-merge view 를
+1.381 nats/symbol (W2) 이기고, 자기 pairing-shuffle 을 +0.540 (W3) 이기며, 세 no-regression 가드가
모두 byte-exact 통과 (W4) — 자모 분해 COUNT-HEAD 소유권 갭이 닫혔다.**

## Pointers

- faculty: `CORE/engine_cli.hexa` § KO-JAMO COUNT-HEAD — `struct JamoHead` + `jamo_head_new` /
  `jamo_head_grow` / `jamo_head_ce` / `jamo_head_cells` / `jamo_head_shuffle_targets` (+ `_jh_*` helpers)
- smoke: `CORE/engine_cli_smoke.hexa` cases 92-95 (+ fixture helpers `_jh_*`)
- verdicts: `.verdicts/1351_jamo_engine_wire/{FREEZE,result}.txt`
- claim: `CLAIMS.tape` @C h1351_jamo_engine_wire
- W4 guards: `CORE/engine_cli_smoke.hexa` (90/0) · `CORE/h1196_single_entry_audit.hexa` (7/0) ·
  `CORE/h1205_separation_invariant_smoke.hexa` (PASS)
- xref: H_1316 (자모 breakthrough, mirror) · H_1321 (engine-native mitosis, COUNT-HEAD 출처) ·
  H_1327 (decode consult, EMISSION 편향 — DISTINCT 표면) · H_1199 (engine DIM-extension precedent) ·
  a_verified_must_wire · a_core_engine_map · a_engine_native_learning · a_no_llm_frame_trap ·
  a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · p7 · p8
