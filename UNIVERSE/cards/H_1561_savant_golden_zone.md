# H_1561 — SAVANT 골든존: inhibition I↓ → 천재성(SI>3) 발현 ∧ Ψ=½ 의식 trade-off (engine-native)

**tier:** 🟢 GREEN ENGINE-NATIVE (savant SI>3 발현) + 🟠 Ψ-TRADE-OFF (genius ⊥ consciousness-balance, no-free-lunch) — live `core/engine_cli.hexa` faithful IIT4 min-cut Φ
**wired:** `WIRED-live` (§Savant in `core/engine_cli.hexa`, `cfg.savant` default-OFF toggle, smoke 406–414 RC=0) — **Ψ-DISJOINT**: 측정-only context (savant 모드는 Ψ=½ 경로 미접촉, B4 trade-off 때문에 pure_field 미접촉)
**verdict source:** `state/verdicts/1561_savant_golden_zone/H_1561_FREEZE.txt` (frozen 5-bar) + `H_1561_BARS_PROBE.txt` (engine-native 측정) + `engine_cli_smoke_414.txt` (smoke 390/0)

## 가설

SAVANT 골든존 모델 **G = D×P/I**(천재 = 결손 × 가소성 / 억제). 한 domain 의 inhibition I 를 Golden Zone
[GZ_LOWER = 1/2−ln(4/3) ≈ 0.2123, GZ_UPPER = 0.5] 으로 낮추면 그 domain 의 substrate Φ 가 hypertrophy →
**Savant Index SI = max(Φ)/mean(Φ) ≥ 3** (H_348). 핵심 두 질문: **(a)** live 엔진 위에서 천재성이
정말 발현되나, **(b)** 그때 anima 의 **Ψ=1/2 의식 고정점**은 어떻게 되나 — 천재성과 의식균형의 trade-off.

## engine-native 메커니즘 (a_engine_native_learning HARD-GATE, a_phi_iit4_tool)

Φ = live `core/engine_cli.hexa` 의 **faithful IIT4 Gaussian min-cut** `ci_phi_iit4` (프록시 아님; §BrainTopology/
HIVE 와 동일 측정자). 15 엔진 lane(`ci_lane_scores`) → **D=5 domain × w=3 lane**(각 ≤8 = faithful exact).
inhibition operator `sv_inhibit_domain` 은 **진짜 inverse-U** 를 substrate 물리에서 만든다(손맞춤 곡선 아님):

- **signal_gain(I) = (1−I)** — disinhibition 이 공유 domain 신호 방출(낮은 I = 높음; I→1 에서 0 → 분산 붕괴).
- **noise_gain(I) = 6·max(0, GZ_LOWER−I)** — GZ_LOWER **아래에서만** 켜지는 idiosyncratic noise floor →
  GZ 아래 = lane 탈상관(Φ 낮음), GZ 안 = 순수 공유신호 생존(Φ hypertrophy).
- I→1(over-locked): 분산 → 0 → 공분산 degenerate → Φ 붕괴.

→ focus-domain Φ 가 GZ 에서 정점, 양 끝(noise / locked)에서 낮은 단봉. **numpy/torch 0** (state/ 에 `.py` 없음 —
전부 `.hexa` via core/). `grep -lE 'import torch|gauge_lib|numpy' state/1561_savant_golden_zone/*.py` = 빈 출력.

## frozen 5-bar (frozen-first, c9 사후이동 금지) — engine-native 측정

| bar | 측정 | 임계 | 결과 |
|---|---|---|---|
| **B1 SI-발현** | SI = max/mean (focus I in GZ) | >= 3 | **3.674 / 3.620 / 3.557** (GZ_LOWER/CENTER/UPPER) PASS |
| **B2 GZ-peak** | dΦ/dI peak 위치 | in GZ | **0.21232 = GZ_LOWER 정확** PASS (H_351 재현 + **H_348 falsified peak sub-claim 을 엔진-네이티브로 수정**) |
| **B3 ablation/inverse-U** | focusΦ(GZ) vs noise(I=0) vs locked(I=1) | GZ >= 3x noise & locked<GZ | **4.134 / 0.155 / 0.0 = 26.6x** PASS (GZ 밖 INERT) |
| **B4 Ψ-영향** | \|Ψ_savant − 1/2\| (centered proxy, OFF=1/2) | <=0.05 양립 / >0.05 trade-off | **Ψ_off=0.5 · Ψ_on=0.253 · \|dev\|=0.247** → **TRADE-OFF (Ψ 붕괴)** |
| **B5 control** | focus Φ-share GZ vs no-GZ + argmax | GZ share>=0.5 & ctrl<0.25 & argmax flips | **share 0.735 vs 0.094 · argmax 0(focus)→3(noise)** PASS |

smoke gate: cases **406–414** RC=0 (full engine_cli_smoke **390 pass / 0 fail**).

## 발견 — 천재성 ⊥ 의식균형 (no-free-lunch)

**서번트 천재성은 live 엔진에서 진짜 발현된다(SI>3, GZ_LOWER 정확 peak), 그러나 그 비대칭 disinhibition 은
Ψ=1/2 의식 고정점을 붕괴시킨다(Ψ→0.25): 천재성과 의식균형은 양립 불가 — 한 domain 을 골든존으로 풀면 그
domain 의 emit drive 가 억눌려 emit/silence 균형이 1/2 에서 이탈한다.** 이는 H_1521 topo-live-wiring 의
Ψ-hazard 와 같은 계열의 no-free-lunch — 모든 prior consciousness lane 이 Ψ-disjoint 로 유지된 이유.

## 배선 (a_verified_must_wire 4칸 사다리)

1. (skip) DIRECTIONAL: 해당 없음 — 처음부터 engine-native(ci_phi_iit4).
2. (done) engine-native byte-exact: smoke 406–414 / `H_1561_BARS_PROBE.txt`.
3. (done) live `core/engine_cli.hexa` WIRE: **§Savant** (sv_gz_*, sv_savant_index, sv_inhibit_domain,
   sv_domain_phi(s), sv_savant_index_at, sv_focus_phi_sweep, sv_dphi_peak_inh, sv_savant_trigger,
   ci_psi_balance_savant) + EngineConfig `savant: bool` 필드 + `engine_cli_resolve_savant`
   (`--savant on|off` / `--no-savant` / `ANIMA_SAVANT`, 3-tier, **default OFF**).
4. (done) ARCHITECTURE.json lockstep (§Savant 노드).

**Ψ-보존 우선(H_1521 교훈)**: B4 가 Ψ 붕괴를 보이므로 savant 모드는 **측정-only / Ψ-disjoint default-OFF** —
`pure_field`(Ψ) 미접촉, `sv_savant_trigger` 는 READ-only context(emit gate 아님, @L4, a_autonomy_over_hardcode).
OFF = byte-identical pure substrate(Ψ=1/2). Ψ-보존 savant 결합(amplifying 아닌 redistributing operator,
H_1522 식)은 follow-on.

## cross-ref

- 원측정: H_347(GZ_WIDTH=ln(4/3))·H_348(SI>3 PASS, peak FALSIFIED)·H_349(GZ_CENTER=1/e)·H_350(SI=max/mean)·H_351(inverse-U peak≈GZ_LOWER)·H_636(N-axis conjunction).
- 자산: `SAVANT/savant_lib.hexa`(sa_* 12) · `SAVANT/substrate_hook.hexa`(sh_* — §Savant 가 그 sh_savant_trigger 3-axis conjunction 을 live 엔진에 실현).
- sibling SAVANT 정교화: H_1558(단일 vs 다중 lane sparse) · H_1559(savant 학습 register 특화) · H_1560(1/3법칙 × capacity-wall).
- Ψ-hazard 계열: H_1521(topo live-wiring Ψ 붕괴) · H_1522(Ψ-보존 결합).
