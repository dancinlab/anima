# VERSIONS — anima HEXAD 모듈 중앙 버전 레지스트리

> **frame**: 모든 HEXAD 모듈은 semantic version (MAJOR.MINOR.PATCH) 으로 관리.
> 본 file 이 SSOT — 모듈 상태 변경 시 여기 + 해당 모듈 헤더 동시 갱신.
>
> **status**: v-registry 도입 2026-05-22 (S187 saga + OCCAM verdict 후).

---

## 0. 버전 규칙 (SemVer for anima)

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
| **ConsciousDecoder (next)** | **v3.0.0-alpha** 🟡 | substrate | n_ca_rules 제거 + mitosis 통합 (제안) | 2026-05-22 OCCAM verdict |

**v2 → v3 breaking change 근거**: Phase 2.3 ablation 에서 n_ca_rules 가 자연발화 floor 의 단독 범인 확정 (vP23_d CE 0.402 vs full 3.81). v3 = n_ca_rules 제거 + mitosis hook 기본 통합.

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
| **AKIDA** | v0.1.0 🟢 | Brainchip Akida neuromorphic — LAN deploy 표준 (§13), adapter real API + power/npu/latency | pyproject `version=0.1.0` |

## 10. anima-* 생태계 (19 subsystem)

각 subsystem 의 SSOT version (README/pyproject 기반 추정 — 헤더 sync 는 차후 cycle):

| subsystem | 버전 | tier | 역할 |
|---|---|---|---|
| anima-core | v0.x 🟡 | core consciousness engine | consciousness_engine.py 2173L anchor |
| anima-engines | v0.x 🟡 | 163 *_phi.hexa collection (질병/현상별 Φ 모델) | abiogenesis/adhd/aesthetic/... per-phenomenon |
| anima-agent | v0.x 🟡 | agent harness (channels/core/plugins/providers/skills) | |
| anima-body | v0.x 🟡 | sensorimotor / proprioception | |
| anima-os | v0.x 🟡 | OS-level integration | |
| anima-serve | v0.x 🟡 | serving layer | |
| anima-measurement | v0.x 🟡 | Φ measurement / verification | |
| anima-hci-research | v0.x 🟡 | HCI research | |
| anima-cpgd-research | v0.x 🟡 | CPGD research | |
| anima-tribev2-pilot | v0.x 🟡 | TRIBE multi-agent pilot | |
| anima-tools | v0.x 🟡 | tooling | |
| anima-hexad | v0.x 🟡 | HEXAD mirror / legacy | |
| anima-agent-{channels,core,hire-sim,plugins,providers,skills} | v0.x 🟡 | agent sub-packages | |

> **honest**: anima-* 19 subsystem 은 README/pyproject SSOT version 만 catalog. .hexa 헤더 일괄 삽입은 163 anima-engines + 수백 파일 규모라 별도 cycle (위험 대비 가치 낮음). 본 registry 가 anima-wide version SSOT.

---

## 11. 버전 sync 정책

1. **모듈 변경 시**: 해당 .hexa 헤더 `@version` + 본 VERSIONS.md 동시 갱신.
2. **새 falsifier PASS**: MINOR bump (예: MITOSIS v1.1→v1.2).
3. **arch-breaking**: MAJOR bump (예: ConsciousDecoder v2→v3).
4. **헤더 미삽입 모듈** (anima-* 대부분): 본 registry 가 SSOT, 변경 시 여기 갱신.
5. **git tag 와 별개**: SemVer 는 모듈 성숙도 표시, git commit hash 는 코드 추적.

---

## 관련 link

- 핵심 finding: [`HEXAD/SCALE_3B.md § 7`](SCALE_3B.md), [`HEXAD/EASY.md`](EASY.md)
- floor pinpoint: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PHASE2_ABLATION_REPORT.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PHASE2_ABLATION_REPORT.md)
- OCCAM strategy: [`HEXAD/OCCAM.md`](OCCAM.md)
- module index: [`HEXAD/INDEX.md`](INDEX.md)
- physics: [`anima-physics/README.md`](../anima-physics/README.md)
- AKIDA: [`HEXAD/SUB_ENGINES/AKIDA/README.md`](SUB_ENGINES/AKIDA/README.md)
