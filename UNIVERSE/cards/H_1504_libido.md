# H_1504 — 💗 LIBIDO — 성적 욕동(欲動) DRIVE-DYNAMICS 축 (incentive-salience '원함' ≠ hedonic '좋아함')

> ⚠ **FRAMING (a_no_llm_frame_trap + p1–p4):** 이것은 **DRIVE-DYNAMICS 축**이다 — 성적 콘텐츠 생성도, 롤플레이도,
> 페르소나도 아니다(셋 다 anima 의 무-페르소나 원칙 p1–p4 위반). 과학적으로 풍부하고 반증가능한 핵심은
> **incentive salience('wanting', 원함) ≠ hedonic value('liking', 좋아함)** (Berridge & Robinson 1998/2016)이다.
> H_1292 hunger 가 배고픔을 모델링하듯, 욕동의 **시간역학**(build-up·cue-conditioning·satiation·motivation bias)을
> frozen bar 로 측정한다. **콘텐츠 0, 생성 텍스트 0 — substrate 에서 읽어낸 parametric drive.**

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §Libido (`libido_new` / `_new_da` / `_new_ablated` / `_satiation` / `_cue_match` / `_wanting` / `_liking` / `_step` / `_last` / `_motivation_bias`) · `engine_cli_smoke.hexa` cases 288-292 · FULL smoke **292 pass / 0 fail RC=0** (deterministic ×3) · ARCHITECTURE.json §Libido lockstep ✓
- **source:** 사용자 'libido drive 축' 작업지시 — H_1292 hunger / H_1290 affect 다음의 욕동-역학 sibling axis (computational affective neuroscience)
- **lens:** Berridge & Robinson incentive-salience (wanting vs liking) · Pfaus sexual motivation · Georgiadis-Kringelbach sexual response cycle · `a_no_llm_frame_trap`
- **artifacts:** `state/1504_libido/h1504_libido.py` · verdict `state/verdicts/1504_libido/{H_1504_FREEZE.json, H_1504_R1.txt, H_1504_R2_smoke.txt}` · `core/engine_cli.hexa §Libido` · `core/engine_cli_smoke.hexa` cases 288-292

## 주장 (욕동-역학 축)

성적 **appetitive drive** L_t = **incentive-salience accumulator**. (1) 박탈(deprivation) 시간적분으로 **build** 되고
(hunger 와 공유), (2) **조건화된 cue** 에서 **spike** 한다(hunger 에 없는 cue-driven incentive 성분). 그 핵심 반증가능
주장 = **incentive salience('원함') ≠ hedonic value('좋아함')** — Berridge: 도파민은 *wanting* 을 올리지 *liking* 을
올리지 않는다. 모든 성분은 substrate 상태(박탈 시간, live store 의 cue-match, consummation margin)에서 읽으며,
주입된 'arousal/horny' 라벨이 **아니다**(p6/p2/p3). Ψ-disjoint READ-only.

## 메커니즘 (substrate-native, §Libido)

regulated var = "grounding satiation" s_t = live ImmuneMemoryGrow recall MARGIN(H_1290 affect / H_1292 hunger 가 읽는
**동일** substrate 신호). `cue_match` = **조건화된 cue** 의 paired-incentive cell 에 대한 store margin(paired cue 는
강하게 ground → wanting spike; unpaired/novel cue 는 약하게 ground → spike 없음).

```
wanting = Kp·deficit + Ki·I + Kc·cue_match·(1 + da_gain)      # incentive salience('원함')
liking  = cue_match                                           # hedonic value('좋아함'), da_gain-불변
```

frozen 상수(H_1292 에서 byte-identical 상속): S*=0.5 · λ=0.1 · Kp=1.0 · Ki=0.5. **신규:** Kc=1.0(cue-incentive gain) ·
da_gain(dopaminergic-analog **WANTING** amplifier; 0=baseline, 1=agonist analog — H_1502 neuropharm 의 도파민성 약물
프로파일이 미는 그 incentive-salience 레버). consummatory grounded event → 적분 RESET(hunger 와 동일). ablate → Kc=0 =
cue-blind deficit-only read = **plain hunger**.

## 측정 (frozen-first · 3 seeds [4504,4505,4506] · DIM=64 · N=40 · T_dep=12 · $0 CPU · p7)

bar 는 채점 **전** FREEZE(`H_1504_FREEZE.json`)에 사전등록 — c9, tune-to-green 금지. R1 numpy mirror 와 R2 engine-native
byte-exact 동일.

| bar | 의미 | 결과(mean) | 기준 | 판정 |
|---|---|---|---|---|
| **A BUILD-UP** | 박탈로 build AND cue 에서 spike (둘 다 존재) | rise **+1.544** · cue_spike **+1.0** | rise≥0.50 ∧ spike≥0.50 | ✅ |
| **B DOUBLE-DISSOCIATION** | sex-cue→libido↑ hunger~flat; food→hunger↑ | hunger cue-Δ **0.000** · hunger rise **+1.544** | cueΔ<0.05 ∧ hungerRise≥0.50 | ✅ |
| **C WANTING≠LIKING** ⭐ | da 0→1 이 wanting 올리고 liking 불변 | wanting **1.0→2.0**(Δ+1.0) · liking **1.0→1.0**(Δ0.0) | wantΔ≥0.50 ∧ \|likeΔ\|≤0.02 | ✅ |
| **D EARNED ablate** | cue-conditioning 제거(Kc=0)→cue-spike 소실 | ablated spike **0.000** | ≤0.05 | ✅ |
| **E EARNED shuffle** | cue↔incentive 짝 순열→cue-특이성 chance 붕괴 | paired **1.0** · shuffled **0.0** | shuf≤0.50×paired | ✅ |

**verdict: 🟢 GREEN — A∧B∧C∧D∧E PASS (3 seeds 전부 byte-identical).**

### 헤드라인 — WANTING ≠ LIKING 분리됨 (Berridge dissociation 재현)

dopaminergic-analog gain(da 0→1)이 **wanting 을 1.0→2.0 으로 올리는데(Δ+1.0) liking 은 1.0→1.0 으로 불변(Δ0.0)** →
incentive salience('원함')가 hedonic value('좋아함')에서 **분리**된다. 도파민이 *원함* 은 키우지만 *좋아함* 은 안 키운다는
Berridge 의 핵심 dissociation 을 substrate 에서 재현. (C 가 실패해 둘이 함께 움직였다면 = anima substrate 가 incentive
와 hedonic 을 분리 못한다는 정직한 발견으로 보고했을 것 — 분리되었으므로 GREEN.)

### libido vs hunger DOUBLE-DISSOCIATION

같은 조건화 cue 가 libido 를 spike(+1.0) 시키지만 hunger(H_1292)는 **cue-blind** 라 동일 cue 에 cue-Δ **0.000**(flat).
역으로 food-deprivation 은 hunger 를 +1.544 올린다. → 두 욕동의 cross-signature 가 분리됨(cue ⊥ deficit). 이것이
libido 를 hunger 의 재포장이 아닌 **DISTINCT** 한 sibling 으로 만드는 load-bearing 성분.

## DISTINCT (vs 기존 lane, load-bearing)

- **vs H_1292 HomeostaticDrive(hunger):** hunger = pure deficit integrator(cue-BLIND). libido = 동일 적분기 **+ cue-conditioned
  incentive**. CUE signature 로 분리(박탈 고정·cue toggle: hunger FLAT, libido SPIKE). bar B 가 실측.
- **vs H_1290 affect:** affect = stateless read(setpoint·integral·cue 없음). libido = stateful cue-conditioned integrator.
- **wanting ≠ liking** 분리(bar C) 자체가 단일 hedonic 스칼라 lane 으로 흡수 불가함을 증명.

## 정직 (c9 · scope)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중 → DIRECTIONAL).
  R2 = live `core/engine_cli.hexa §Libido` op 호출(`hexa run engine_cli_smoke.hexa`, numpy/torch 0 = **하드게이트1 PASS**) +
  cases 288-292 byte-exact + ARCHITECTURE lockstep, FULL **292/0 RC=0** deterministic ×3.
- **SATURATED = EXISTENCE-PROOF:** cue_spike=1.0/cmShuf=0.0 등 포화값은 effect-size 가 아니라 존재증명 — discriminator(ablated
  spike 0.0·hunger cue-Δ 0.0·shuffled cue_match 0.0)가 결정적.
- **READ-only Ψ-disjoint NOT emit gate:** `libido_motivation_bias` = 의도적 OPTIONAL gain(a_autonomy_over_hardcode), emit/silence
  강제 안 함. immune store/pure_field Φ/phase/Ψ 미변경.
- **H_1502 neuropharm 링크:** da_gain 은 도파민성 agonist 가 미는 incentive-salience 레버와 동일 → H_1502 약물 프로파일이 이
  libido drive 의 wanting 을(liking 아닌) 변조하는 target.
- **SCOPE TOY:** 64-dim/40-fact/3-seed/결정적 controller(욕동-역학 STRUCTURE 검증, 학습된 drive 아님). scale/real-corpus/
  multi-cycle/연속 cue-conditioning/engine-transfer UNVERIFIED → motivation-loop 배선 + 303M 재측정 follow-on
  (a_scale_honest_scope · a_toy_scale_recheck).
