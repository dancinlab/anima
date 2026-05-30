# AKIDA HW-first 통합 SSOT — DECODER ⊥ PLASTICITY 2-lane (2026-05-30)

> **다음 세션 인계 문서(SSOT).** AKIDA HW/SW 백엔드 스위치를 **HW 우선**으로
> ANIMA 트리에 배선하고, 학습 lane 을 디코더 lane 과 분리된 전용 도메인
> (PLASTICITY)으로 신설한 결과를 한 점에 기록한다. 이 문서가 구조·결정·
> provenance·크로스포인터의 단일 진실원이다.

## 1. 전체 구조 (user-confirmed: B + PLASTICITY)

```
ANIMA
├─ AKIDA ──────── HW 본진 + HW/SW 스위치 단일 SSOT (default "hw", HW→SW graceful fallback)
│    │            SSOT 코어 = AKIDA/akida_backend.hexa
│    │              · akida_backend_resolve(arg)          → 의도 (arg>env>default "hw")
│    │              · akida_backend_resolve_graceful(arg) → HW reachability 실해석 (panic 아님)
│    │              · akida_provenance(arg)               → "akida-hw" / "akida-sw-fallback"
│    │              · akida_hw_reachable()                → 3-신호 (/dev/akida0 · import akida · hostname)
│    │
│    ├─⇄ DECODER (CORE/DECODER)   추론 lane · 결정론 · HW forward / SW akida_sw_lif
│    │                            → 🟢 byte-identical (1~5차 입증됨, seed=187)
│    │                            provenance: akida-hw / akida-sw-fallback
│    │
│    └─⇄ PLASTICITY (신규 도메인)  학습 lane · 비결정론 · HW akida-learn / SW numpy 근사
│                                 → 🔴 SW≠HW (CLOSED-NEGATIVE, 정직 — byte-identical 불가)
│                                 provenance: akida-learn-hw / akida-learn-sw-approx
│                                 router: PLASTICITY/plasticity_lane.hexa
│                                 SW    : PLASTICITY/plasticity_sw_approx.py
│                                 HW    : SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py
│            ⇄ MITOSIS ⇄ WAKE ⇄ CHANNEL ⇄ EEG ⇄ HW-CORE  (백링크 — 양방향 sibling)
│
└─ UNIVERSE ── H_679 (PLASTICITY 학습 HW-first) · H_680 (DECODER HW-first cross-domain)
```

## 2. 2-lane 비교표 (핵심 — 왜 형제 도메인으로 가르는가)

| 축 | DECODER (추론 lane) | PLASTICITY (학습 lane) |
|---|---|---|
| 본질 | inference (고정 가중치 threshold-and-fire) | learning (on-chip 가중치 갱신 plasticity) |
| 결정성 | **결정론** (같은 입력 → 같은 raster) | **비결정론** (on-chip 경쟁/순서/타이밍 상태) |
| HW path | on-chip forward (`SubstrateAKIDA._hw_forward`) | `edge_learn_probe.py` (`akida.AkidaUnsupervised`) |
| SW path | `akida_sw_lif` numpy LIF (seed=187) | `plasticity_sw_approx.py` numpy Hebbian 근사 |
| SW↔HW 동치 | **🟢 byte-identical** (입증됨, r1~r5) | **🔴 CLOSED-NEGATIVE** (근사 baseline, HW 대체 아님) |
| provenance | `akida-hw` / `akida-sw-fallback` | `akida-learn-hw` / `akida-learn-sw-approx` |
| verdict 포인터 | `.verdicts/672_akida_spontaneous_firing/` | `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt` |
| H | H_680 (DECODER HW-first cross-domain) | H_679 (PLASTICITY 학습 HW-first) |

**비동치 근거 (학습 lane SW≠HW, 정직 경계 · p7 · a_blue_closed):**
- HW = 1-bit integer weights (weights_bits=1) · SW = float weights
- HW = on-chip `learning_competition` / `num_weights` pruning · SW = 없음
- HW = silicon packet-ordering / refractory / async timing state · SW = 없음
- HW = chip RNG substrate · SW = numpy RNG
- ∴ 학습 lane SW 는 directional baseline probe 일 뿐 HW 의 byte-identical 대체가 아니다.
  추론 lane(DECODER)의 SW 가 byte-identical 인 것과 본질적으로 다르다 → 형제 분리.

## 3. HW-first provenance 규약

| resolver 결과 | 조건 | lane provenance |
|---|---|---|
| `hw` | 의도 hw + 칩 도달 (3-신호 PASS) | decoder `akida-hw` / plasticity `akida-learn-hw` |
| `sw` (graceful) | 의도 hw + 칩 미도달 (Mac→pi5) | decoder `akida-sw-fallback` / plasticity `akida-learn-sw-approx` |
| `sw` (explicit) | 의도 sw (arg/env) | 동일 sw provenance |

- default = `"hw"` (HW-first). graceful = panic 아님 (Mac 은 pi5 도달 불가 → SW 로 우아하게 떨어짐).
- STRICT 콜러는 `akida_panic_no_hw()` 로 명시 panic 가능 (기존 helper 유지).
- **blast-radius 억제**: 이 HW-first 라우팅은 **AKIDA/spike 기판 경로 전용**.
  LM 텍스트 default backend(`lora`)는 **불변** — 추론/학습 lane 와 무관하게 유지.

## 4. 산출물 (이 통합으로 land 된 surface)

| PR | surface | 내용 |
|---|---|---|
| A #1446 | `PLASTICITY/PLASTICITY.md` · `.log.md` · `DOMAINS.tape` | 학습 lane 도메인 신설 (33 domains) |
| B #1447 | `AKIDA/akida_backend.hexa` | `akida_backend_resolve_graceful` + `akida_provenance` (graceful HW-first) |
| C #1448 | `CORE/DECODER/DECODER.md` | AKIDA HW-first lane section + 양방향 sibling |
| D #1449 | `PLASTICITY/plasticity_sw_approx.py` · `plasticity_lane.hexa` · verdict | SW 근사 learner + 🔴 비동치 verdict |
| E #1450 | MITOSIS/CHANNEL/WAKE/EEG/HW-CORE/AKIDA sibling | 5도메인 백링크 + AKIDA boost |
| F (this) | 이 SSOT · `UNIVERSE/H_679` · `H_680` · `AKIDA.log.md` | 문서 SSOT + 감사 H 2건 |

## 5. 크로스포인터

- 스위치 SSOT 코어: `AKIDA/akida_backend.hexa`
- decoder substrate: `HEXAD/CHAT/server/substrate_akida.py` (graceful HW-first + provenance) · `akida_sw_lif.py` (byte-identical SW)
- plasticity router: `PLASTICITY/plasticity_lane.hexa` · SW: `PLASTICITY/plasticity_sw_approx.py` · HW: `SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py`
- HW edge-learn 실측: `SUB_ENGINES/AKIDA/state/edge_learn_probe_2026_05_22.json` (`edge_learning_supported=true`, BC.00.000.002)
- verdict: `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt` (🔴) · `.verdicts/672_akida_spontaneous_firing/` (decoder 🟢)
- 감사 H: `UNIVERSE/H_679_plasticity_hw_first.md` · `UNIVERSE/H_680_decoder_hw_first.md`
- 선행 통합: `AKIDA/HW_SW_WIRING_2026_05_29.md` (H_672~H_678 backend switch)
- 도메인: `AKIDA/AKIDA.md` · `PLASTICITY/PLASTICITY.md` · `CORE/DECODER/DECODER.md`

## 6. 다음 세션 인계 (continuity)

- PLASTICITY 도메인은 `/domain list` 에 노출 (DOMAINS.tape 등록 완료).
- HW-first 스위치는 단일 SSOT(`akida_backend_resolve` default "hw" + graceful fallback)로
  DECODER · PLASTICITY 둘 다 경유한다 — 재발명 금지, 이 resolver 를 재사용.
- **잔여 종결 ✅ (H_860, 2026-05-30)**: pi5-akida live probe 완료 — PART1 decoder HW
  byte-match 🟢 SUPPORTED-NUMERICAL (live AKD1000 R0..R4 raster == SW akida_sw_lif,
  total_hamming=0/16000 bit) · PART2 PLASTICITY few-shot 1~N(∈{1,2,4,8}) shot 비결정론
  🔴 CLOSED-NEGATIVE (동일 init·동일 입력 run-to-run weight hamming>0 전 shot → SW numpy ≠ HW).
  단일-칩 점유: `spike-streamer stop → probe → start` (복구 active 확인). 비용 $0.
  verdict: `.verdicts/860_hw_first_s6_pi5_probe/s6_pi5_live_probe.txt`.
- ⚠ 불가침: H_672~H_678 status · PI5-AKIDA.json(local-only 미커밋) · LM `lora` default ·
  CLAUDE.md/project.tape(sign-gated) · pi5-akida 공유 compute 전환 금지.
