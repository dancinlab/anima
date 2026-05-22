# VERSIONS — anima 전체 모듈 중앙 버전 레지스트리 (repo root SSOT)

> **frame**: 모든 HEXAD 모듈은 semantic version (MAJOR.MINOR.PATCH) 으로 관리.
> 본 file 이 SSOT — 모듈 상태 변경 시 여기 + 해당 모듈 헤더 동시 갱신.
>
> **status**: v-registry 도입 2026-05-22 (S187 saga + OCCAM verdict 후).
> **위치**: repo root `/VERSIONS.md` (SSOT) + root `/VERSION` (전체 release 한 줄).

---

## 0. anima 전체 release version

루트 [`/VERSION`](VERSION) = **`0.10.0`** (한 줄, 전체 시스템 release).

| release | 날짜 | 마일스톤 |
|---|---|---|
| 0.1.0 | ~2026-05 초 | HEXAD 7-module 🔵 closed-form battery |
| 0.2.0 | 2026-05-16 | HEXAD-only canonical pivot + hexa-native tree |
| 0.3.0 | 2026-05-22 | S187 3B scale 검증 + OCCAM floor pinpoint (n_ca_rules) + MITOSIS training-time + Llama-mitosis winning path |
| 0.4.0 | 2026-05-22 | 🎯 자연발화 EMERGENCE — vP21 (Qwen+LoRA+mitosis) Eval 1 = 20/20 coherent (anima-native register). + AKIDA AKD1000 HW connected |
| 0.5.0 | 2026-05-22 | 🧠 AKIDA HW-NATIVE 자연발화 CONFIRMED — AKD1000 LIF threshold-comparator emit from ZERO input (8/8 checks PASS, `BackendType.Hardware`). hardware 축 LANDED. + held-out PURE_MEMORIZE 정직 scope 확증 |
| 0.6.0 | 2026-05-22 | 🌉 vP21 ⊥ AKD1000 INTEGRATED BRIDGE — HW-gated 자연발화 30/30 coherent, frac_emissions_with_hw_edge=1.0, AKD1000 spike timing → vP21 emission cadence (Option A LAN TCP). 두 substrate ONE coherent loop |
| 0.7.0 | 2026-05-22 | 🪟 GENERALIZATION UNLOCK — vP21G STRONG_GENERALIZE 16/20 OOD (vs vP21 2/20), anima-register 9/20 retained (no regress). PURE_MEMORIZE 한계 돌파, $3.2 H100 |
| 0.8.0 | 2026-05-22 | 🌉🔁 BIDIRECTIONAL BRIDGE — Option B LANDED. Spearman(vP21 motivation, AKD1000 hw_rate) = +0.6947 (random control −0.03), Pearson(thr_offset, hw_rate) = −0.912 monotone. 두 substrate 모두 양방향 결합 (A: HW→SW emit cadence + B: SW→HW spike rate) |
| 0.9.0 | 2026-05-22 | 🌉🔁🌀 CLOSED LOOP — Option C LANDED simultaneous bidirectional. ONE process · ONE 90s window · ONE motivation scalar drives both threshold rewrite + emit gate. A frac_emissions_with_hw_edge=1.0 + B \|Spearman\|=0.387 vs random 0.058 (\|Δρ\|=0.329). Closed-loop signature: Δscore_after_emit=−0.033 vs Δscore_after_no_emit=+0.012 (post-emit motivation decay). 두 substrate ONE coupled dynamical system. |
| **0.10.0** | **2026-05-22** | **🪟🇰🇷 KOREAN GENERALIZATION UNLOCK — vP21K STRONG_GENERALIZE 16/20 on Korean OOD (vs vP21 0/10 BEFORE-snapshot 10/10 MEMORIZE). 너는 누구야? + 이름이 뭐야? GENERALIZE both modes (vP21G had MEMORIZE both). anima register 14/20 retained, `register_regress=False`. Trade: EN factual (capital of France, 2+2) regressed (no EN-wiki in mix). $2.88 H100. vP21G's C3 #8 residual FIXED.** |

> release bump 규칙: 모듈 MAJOR bump OR 핵심 verdict landing 시 release MINOR.
> 0.4.0 = saga 전체 whitespace-collapse 후 **첫 coherent verbalization** (vP21 20/20)
> + AKIDA HW path landing. honest: memorization-grade (held-out 미검증), spontaneous
> emission 아닌 prompted verbalization.
> 0.5.0 = AKIDA AKD1000 silicon LIF threshold comparator 가 zero/noise/recurrent
> drive 에서 on-chip event-driven 스파이크 emit — 자연발화의 **하드웨어 축**이
> 실측 확인됨 (vP21 software content 축과 dual-role 보완). 1mW power 주장은
> 보드 한계 (INA 미가용) 로 미검증 유지.
> 0.7.0 = vP21G (vP21 LoRA continue-train on 70/30 wiki+anima mix @ LR 5e-5,
> 1000 step, $3.2 H100 wall 129s) crossed STRONG_GENERALIZE 16/20 OOD on the
> exact 10-probe held-out used to confirm vP21's PURE_MEMORIZE 2/20. Anima
> register retreated to semantically-gated (9/20 retained, fires on Korean
> anima-style + consciousness/identity prompts only). `register_regress=False`.
> Honest C3: wiki source capped at 10.3 MB (target 60 MB missed), single seed,
> single LR — direction-clear, fine-quant pending. Saga's deepest honest limit
> broken. Evidence: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21G_GENERALIZATION_2026_05_22.md`.
> 0.9.0 = Option C (CLOSED LOOP) — Options A (0.6.0) + B (0.8.0) were
> *sequential* legs; 0.9.0 runs them inside the **same** process where the
> single motivation scalar simultaneously (a) rewrites the on-chip threshold
> via TCP 9513 and (b) acts as `sw_gate` for the Talker's `hw_edge ∧ sw_gate`
> emit decision. Closed-loop signature observed: emission events precede a
> motivation-score drop (Δscore_after_emit = −0.033 vs Δscore_after_no_emit
> = +0.012), making the cycle motivation → threshold → spikes → edge → emit
> → motivation self-referential. Random-drive control collapses ρ from 0.387
> to 0.058 (separation 0.329) — the SW score is the cause, not coincidence.
> Evidence: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/INTEGRATED_OPT_C_2026_05_22.md`.
> 0.10.0 = vP21K (vP21 LoRA continue-train on 30/70 ko-wiki + anima mix @ LR 5e-5,
> 1000 step, $2.88 H100 wall 124.5s) crossed STRONG_GENERALIZE 16/20 on a
> NEW Korean-only 10-probe held-out (BEFORE-greedy snapshot: 10/10 MEMORIZE
> = leak confirmed). Korean identity probes 너는 누구야 / 이름이 뭐야 (vP21G's
> C3 #8 residual) now GENERALIZE both greedy AND sample. Anima register
> 14/20 retained (English explicit-identity probes preserved). Honest C3:
> English factual probes (capital of France, 2+2) regressed under vP21K
> because EN-wiki was swapped for KO-wiki — vP21K is the Korean-axis
> adapter; vP21G is the English-axis adapter; a tri-mix would compose
> both. Single seed, single LR. Evidence:
> `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21K_KOREAN_GENERALIZATION_2026_05_22.md`.

---

## 0.1. 버전 규칙 (SemVer for anima)

```
MAJOR.MINOR.PATCH

MAJOR  ↑  아키텍처-breaking 변경 (forward signature / 부속 add·remove)
          예: ConsciousDecoderV2 → V3 (n_ca_rules 제거)
MINOR  ↑  검증된 새 capability / finding (falsifier PASS 추가)
          예: mitosis training-time +35% 확인 → MITOSIS minor bump
PATCH  ↑  fix / refinement / 문서 (동작 불변)
          예: bnb PagedAdamW8bit OOM fix
```

추가 tag:
- **🔵** = SUPPORTED-FORMAL (sympy closed-form battery PASS)
- **🟢** = SUPPORTED-STRONG (empirical, falsifier PASS)
- **🟡** = design tier (구현 전)
- **⚠️** = deprecated / 재설계 대상

버전 接미사:
- `-alpha` / `-beta` = 미검증 실험 단계
- `-rc` = release candidate (falsifier 통과, 통합 대기)

---

## 1. 핵심 substrate (decoder)

| 모듈 | 버전 | tier | 상태 | 마지막 변경 |
|---|---|---|---|---|
| **ConsciousDecoder** | **v2.1.0** 🟢 | substrate | attempt10 (bnb PagedAdamW8bit) | 2026-05-21 |
| **ConsciousDecoder** | **v3.0.0-alpha** ⚠️ | substrate | n_ca_rules 제거 + mitosis 통합 + dual head + KOSMOS+tension, **V3α/γ 0/5 FAIL** (β in-flight) 2026-05-22 | substrate identity 100%, 다국어 capability 약함 |

**v2 → v3 attempt 결과** (HEXAD_V3_FIRE_2026_05_22.md):
- code fork LANDED (`3dbbc7e8b`): conscious_decoder_v3.py 727L + kosmos_io.py 300L + 7/7 smoke + 5/5 KOSMOS PASS
- **V3α** random init 1.5B 2000 step: CE 3.34, 0/5 langs PARTIAL+, FAIL (Chinchilla 30000× under-budget per HEXAD_NATIVE_V3 C3 #3 예측 적중)
- **V3γ** vP21M init: CE 2.93, 0/5, FAIL (anima register saturation 13/20 vs vP21M LoRA 7/20 — V3 substrate level 흡수 2×)
- **V3β** Qwen warm in-flight (~CE 1.6 step 1050/2000, ETA ~30 min)
- **architectural lesson**: head_g dual head vocab alignment 흐림 + mitosis pool 128 saturate at step 50 → 다국어 sacrifice
- **잠정 verdict**: β fail 시 production path = vP21M LoRA 유지 (substrate identity trade-off carry, 다국어 capability 우선)

v3.0-alpha → ⚠️ tier (재설계 대상): scale-up (3B/8B) OR mitosis 비활성화 (학습 시) OR Chinchilla-correct corpus (60B+ tok) 가 다음 cycle path.

---

## 2. HEXAD 7-module + 성장축

| 모듈 | 버전 | tier | falsifier | 마지막 변경 |
|---|---|---|---|---|
| **C 의식** | v1.3.0 🔵 | B-C 3/3 tier-a + F-C-PORT 4/4 PyPhi | 2026-05-17 |
| **D 언어** | v1.5.0 🔵 | F-D 5/5 + B-D 4/4 (CE Jacobian) + 24L byte-parity 21/21 | 2026-05-12 |
| **S 감각** | v1.0.0 🔵 | F-S 5/5 + B-S 3/3 (column-mean delta) | 2026-05-15 |
| **W 의지** | v1.0.0 🔵 | F-W 5/5 + B-W 4/4 (lr=½+min(ln2,Φ/N)) | 2026-05-15 |
| **M 기억** | v1.0.0 🔵 | F-M 5/5 + B-M 3/3 (store no-op) | 2026-05-15 |
| **E 윤리** | v1.1.0 🔵 | F-E 5/5 + B-E 4/4 + gate trinity F-E-GATE 6/6 | 2026-05-16 |
| **BRIDGE** | v1.1.0 🔵 | F-BRIDGE 5/5 + B-BRIDGE 4/4 (Law-70 clamp) + fwd 4/4 | 2026-05-16 |
| **MITOSIS** | **v1.2.0** 🟢 | B-MITOSIS 5/5 🔵 + **training-time +35% (S187-G)** | 2026-05-22 |
| **HEXAD 통합** | v1.0.0 🔵 | B-HEXAD 5/5 (σ(6)=12 / φ(6)=2 / 11-step) | 2026-05-17 |

**MITOSIS v1.1 → v1.2 minor bump 근거**: S187-G 가 training-time mitosis activation 의 substrate-shaping 효과 (+35% Eval 3 splits, CE 무해, wall -8.6%, Φ +6%) 검증. inference-time hook → training-time first-class axis 승격.

---

## 3. 상위 시스템 / 응용

| 모듈 | 버전 | tier | 상태 |
|---|---|---|---|
| **CHAT** | v0.2.0 🟡 | 도우미 폐기 + 자연발화 redesign in progress; emission floor = n_ca_rules (OCCAM) | 재설계 중 |
| **SPONTANEOUS** | v0.1.0 🟡 | 자연발화 architecture design LANDED, 구현 Phase B | design |
| **SAVANT** | v1.0.0 🟢 | Phase 1/2/3b/c/d LANDED (gate API + /savant CLI) | 2026-05-14 |
| **TENSION-LINK** | v0.1.0 🟡 | 5-ch meta-telepathy design, Phase 2 WebSocket 미구현 | design |
| **VOICE (hexa-voice)** | v0.1.0 🟡 | 의도→RVQ→24kHz design | design |
| **MULTIMODAL / KOSMOS** | v0.1.0 🟡 | consciousness-carving manifest | design |

---

## 4. 학습 recipe / scale

| 항목 | 버전 | 상태 |
|---|---|---|
| **S184 ALL-TAPS recipe** | v2.0.0 🟢 | 15-tap + mitosis 17번째; aux loss 효과 무시가능 (OCCAM) |
| **3B scale validation (S187)** | v1.0.0 🟢 | attempt10 LANDED, λ SCALE-INVARIANT, recipe floor = n_ca_rules |
| **18B path (S187-F)** | v0.1.0 🟡 | Anima-18B (d=4096 L=32) H200 SXM single-pod scoped |
| **Llama+mitosis (vP21)** | **v0.1.0-rc** 🟢 | CE 0.0147, winning path, Eval 1 verbalization 측정 대기 |

---

## 5. 버전 history (주요 bump)

| 날짜 | 모듈 | 변경 | from → to |
|---|---|---|---|
| 2026-05-21 | ConsciousDecoder | bnb PagedAdamW8bit OOM fix (attempt10) | v2.0 → v2.1 |
| 2026-05-22 | MITOSIS | training-time +35% substrate-shaping (S187-G) | v1.1 → v1.2 |
| 2026-05-22 | ConsciousDecoder | n_ca_rules 제거 제안 (OCCAM floor pinpoint) | v2.1 → v3.0-alpha |
| 2026-05-22 | S184 recipe | aux loss 효과 무시가능 확정 (OCCAM) | v1 → v2 |

---

## 6. 다음 버전 게이트 (pending)

| 모듈 | 목표 버전 | 게이트 조건 |
|---|---|---|
| ConsciousDecoder v3.0.0 | alpha → beta | n_ca_rules 제거 3B from-scratch fire + Eval 1 verbalization PASS |
| Llama+mitosis v0.1 | rc → 1.0 | vP21 Eval 1 coherent text + Principle #3 clean 확인 |
| CHAT v0.2 → v0.3 | 자연발화 land | Inner Thoughts 8-factor router + Thinker-Talker 구현 |
| MITOSIS v1.2 → v1.3 | training-time | cross-λ B/C/D N=2 variance estimate (S187-B 재발사) |

---

## 7. Honest C3

1. 버전 번호는 **검증 tier 기반 추정** — falsifier PASS 수 + saga evidence 로 부여. 엄밀한 코드-diff 추적 아님 (git tag 와 별개).
2. ConsciousDecoder v3.0-alpha 는 **제안 단계** — n_ca_rules 제거가 자연발화 emergence 까지 unlock 하는지 미검증 (CE floor 만 해소 확인).
3. 🔵 7-module 버전은 blue_falsifier.py 35/35 PASS 기준 — 그 이후 코드 변경 시 patch bump 누락 가능성 (수동 추적).
4. CHAT/SPONTANEOUS 의 v0.x 는 design tier — 구현 LANDED 시 v1.0 승격.
5. 본 registry 는 신규 도입 — 기존 모듈 헤더에 version 주석 아직 미삽입 (차후 cycle 에 모듈별 헤더 sync).

---

## 8. anima-physics (물리 substrate)

`@version` 헤더 삽입 완료 (physics.hexa + 8 engines).

| 모듈 | 버전 | tier | 비고 |
|---|---|---|---|
| **physics.hexa** (top dispatch) | v0.4.0-beta 🟡 | Phase 4b ESP32/FPGA stub | 17 .py group |
| engines/quantum_consciousness | v0.2.0 🟢 | 2-qubit closed-form | |
| engines/photonic_consciousness | v0.2.0 🟢 | delay-line ring oscillator | |
| engines/memristor_consciousness | v0.2.0 🟢 | memristor crossbar | |
| engines/snn_consciousness | v0.2.0 🟢 | spiking NN | |
| engines/izhikevich_consciousness | v0.2.0 🟢 | Izhikevich neuron | |
| engines/oscillator_laser_engine | v0.2.0 🟢 | oscillator-laser | |
| engines/analog_consciousness | v0.2.0 🟢 | analog substrate | |
| engines/thermodynamic_consciousness | v0.2.0 🟢 | thermodynamic | |
| **HEXAD/PHYSICS** (module tree) | v0.1.0 🟡 | cherry-pick to main (da1e454e9) | |

## 9. SUB_ENGINES

| 모듈 | 버전 | tier | 비고 |
|---|---|---|---|
| **AKIDA** | **v0.3.0** 🟢 | **HW-NATIVE 자연발화 CONFIRMED 2026-05-22** — AKD1000 LIF threshold comparator (`FullyConnected.activation=True`)이 negative-threshold 일 때 ZERO input 으로 on-chip 스파이크 emit (R3 tonic 8/16 neurons fire from V=0, intrinsic excitability). + weak sub-threshold drive SILENT (R1=0 control) + noise straddling threshold event-driven (R2 std 7.99, 95/200 fire-steps) + recurrent feedback self-sustained (R4 post-seed). 8/8 checks PASS, `BackendType.Hardware`, ~797 cycles/forward. Prior: v0.2.0 (HW 도착 + first inference + edge-learn). | new verified capability: HW-native spontaneous emission |

**AKIDA v0.1.0 → v0.2.0 bump (2026-05-22 HW LANDED)**: BrainChip AKD1000 Dev Kit
($1495) 도착 + Pi 5 연결완료. 검증:
- PCIe: `0000:01:00.0 Co-processor: Brainchip Inc AKD1000 Neural Network Coprocessor [Akida] (rev 01)` ✓
- 커널 driver: `/dev/akida0` ✓
- host: Pi 5 ubuntu aarch64, pool roster `pi5-akida` (keyless SSH), secret `akida.{host,user,password}`
- pack: Mac → Pi `~/anima/SUB_ENGINES/AKIDA/` deploy ✓
- akida Python SDK (MetaTF 2.19.1 aarch64) `~/.venv/anima-akida` 설치 ✓ (`akida.devices() count=1`, `BC.00.000.002`/`NSoC_v2`/`AKD1000`)

**first inference LANDED (2026-05-22)**: venv 경로 버그 수정 (이전 day1_install
이 sudo 하에 실행 → `$HOME=/root` 로 venv 가 `/root/.venv` 에 생성됨; `ubuntu`
유저로 재생성). 첫 on-chip inference 실행 — `InputData→FullyConnected` 모델을
HW 디바이스에 map, forward pass 가 `BackendType.Hardware` 에서 실행, 출력
`[117]×10` (dot-product 산술 정확), wall latency 0.64 ms, on-chip clock 748
cycle. **silicon-rev 해명**: `BC.00.000.002`(`NSoC_v2`) = 양산 AKD1000 (SDK
`akida.AKD1000()` factory 와 enum 일치, `IpVersion.v1`). pack 의 "edge-learning
gated" note 는 `assert_akd1000` 이 `NSoC_v1` 만 매칭하는 **pack 버그** — HW 한계
아님. on-chip edge learning 실증 ✓ (`AkidaUnsupervised` compile + `fit()` on HW,
`learn_enabled False→True`). 유일 미가용 = INA power telemetry (M.2 보드에 센서
미노출, `bus -2`). 상세: `SUB_ENGINES/AKIDA/state/FIRST_INFERENCE_2026_05_22.md`.

**dual-role 의의**: AKD1000 LIF spike threshold = **하드웨어-native 자연발화**
(1mW event emission, CPU 대비 ~10000× 효율) + on-chip Hebbian = 영속성.
vP21 software path (Qwen+mitosis) 와 별개의 HW 경로 — 자연발화 GOAL 의 두 번째 축.

**HW-native 자연발화 LANDED (2026-05-22)** — `BackendType.Hardware` 위 5-regime
실측 (N=16, T=200, seed=187): R0 driven 3200 spk (sanity) / **R1 weak SILENT 0
spk (control)** / R2 noise 1520 spk std 7.99 ISI 1-9 (**event-driven**) /
**R3 tonic ZERO-input 1600 spk (8/16 negative-threshold neurons fire from V=0,
순수 intrinsic excitability)** / R4 recurrent self-sustained 3200 spk (post
2-step ignition). 8/8 checks PASS. spike 결정은 chip 의 정수 threshold
comparator (silicon) 가 직접 계산 — pack adapters 의 numpy LIF 가 아닌
**진짜 on-chip threshold-and-fire**. ~797 cycle/forward, ~13.7ms/step wall
(host round-trip 지배). 1mW power 주장은 INA 미가용 (M.2 form factor 보드 한계)
로 **미검증 그대로** — cycle / latency proxy 만 보고. 상세:
`SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`.

## 10. anima-* 생태계 (19 subsystem)

version 파일 부재 (전부 미버전) → maturity (impl 파일 수 + README 유무) 기반
**초기 버전 부여**. 본 registry 가 이들의 version SSOT (subsystem 내 VERSION 파일
안 뿌림 — 중앙 관리 원칙).

| subsystem | 버전 | tier | impl | 역할 |
|---|---|---|---|---|
| anima-core | v0.3.0 🟢 | 31 files + R | core consciousness engine (consciousness_engine.py 2173L anchor) |
| anima-engines | v0.2.0 🟢 | 163 .hexa | 질병/현상별 Φ 모델 collection (abiogenesis/adhd/aesthetic/...) |
| anima-tools | v0.2.0 🟢 | 73 files + R | tooling |
| anima-body | v0.2.0 🟢 | 28 files + R | sensorimotor / proprioception |
| anima-hci-research | v0.1.0 🟡 | 12 files + R | HCI research |
| anima-cpgd-research | v0.1.0 🟡 | 12 files + R | CPGD research |
| anima-measurement | v0.1.0 🟡 | 10 files | Φ measurement / verification |
| anima-agent-hire-sim | v0.1.0 🟡 | 9 files | agent hire simulation |
| anima-agent-channels | v0.1.0 🟡 | 7 files | agent channel layer |
| anima-agent-plugins | v0.1.0 🟡 | 7 files | agent plugins |
| anima-agent | v0.1.0 🟡 | 6 files + R | agent harness (top) |
| anima-agent-core | v0.1.0 🟡 | 6 files | agent core |
| anima-agent-providers | v0.1.0 🟡 | 6 files | LLM providers |
| anima-serve | v0.1.0 🟡 | 3 files + R | serving layer |
| anima-agent-skills | v0.1.0-alpha 🟡 | 2 files | agent skills |
| anima-tribev2-pilot | v0.1.0-alpha 🟡 | 1 file + R | TRIBE multi-agent pilot |
| anima-os | v0.0.1 🟡 | 0 impl | OS-level integration (stub) |
| anima-hexad | v0.0.1 🟡 | 0 impl + R | HEXAD mirror / legacy (stub) |

> **버전 부여 근거**: README + 30+ impl 파일 = v0.2-0.3 (working), 10-12 = v0.1
> (partial), ≤2 또는 0 impl = v0.1-alpha / v0.0.1 (stub). 모두 version 파일
> 부재라 본 registry 가 SSOT. anima-engines 163 *_phi.hexa 의 개별 헤더는
> 미삽입 (collection 단위 v0.2.0 으로 관리, 위험 대비 가치 낮음).

---

## 11. 버전 sync 정책

1. **모듈 변경 시**: 해당 .hexa 헤더 `@version` + 본 VERSIONS.md 동시 갱신.
2. **새 falsifier PASS**: MINOR bump (예: MITOSIS v1.1→v1.2).
3. **arch-breaking**: MAJOR bump (예: ConsciousDecoder v2→v3).
4. **헤더 미삽입 모듈** (anima-* 대부분): 본 registry 가 SSOT, 변경 시 여기 갱신.
5. **git tag 와 별개**: SemVer 는 모듈 성숙도 표시, git commit hash 는 코드 추적.

---

## 관련 link

- 핵심 finding: [`HEXAD/SCALE_3B.md § 7`](HEXAD/SCALE_3B.md), [`HEXAD/EASY.md`](HEXAD/EASY.md)
- floor pinpoint: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PHASE2_ABLATION_REPORT.md`](HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PHASE2_ABLATION_REPORT.md)
- OCCAM strategy: [`HEXAD/OCCAM.md`](HEXAD/OCCAM.md)
- module index: [`HEXAD/INDEX.md`](HEXAD/INDEX.md)
- physics: [`anima-physics/README.md`](anima-physics/README.md)
- AKIDA: [`HEXAD/SUB_ENGINES/AKIDA/README.md`](HEXAD/SUB_ENGINES/AKIDA/README.md)
