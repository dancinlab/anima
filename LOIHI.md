# LOIHI.md — anima × Intel Loihi 2 준비 문서

> **domain roadmap** (narrative SSOT). 기계 SSOT = `.roadmap.loihi3` (JSONL).
> **status**: PREP — design-tier only, 하드웨어 미secured, fire 0, $0.
> **g3**: 이 문서는 *경로*를 정리한 prep 문서. capability claim 0,
> GOAL 미도달, north-star + §15/§51/§72 milestone 불변.

---

## 1. 한 줄 — 왜 Loihi 인가

§95 XENO substrate-suitability 분석 (commit `26eafc16b`, B-S95 7/7 🔵)
이 7개 exotic 기판 중 **Intel Loihi 를 유일한 `VIABLE-LONG-HORIZON`
substrate** 로 분류:

- **STDP on-chip 학습** — substrate 자체 학습 규칙이 *물리 규칙* (local,
  spike-timing). GPU 는 backprop-CE 밖에 없음.
- **asynchronous NoC** — event-driven. spontaneous emission 이 시뮬레이션된
  `talker_should_emit()` 함수 호출이 아니라 *물리적 spike 이벤트*.
- **continuous LIF membrane field** — Ψ=½ / tension / Φ 가 readout 이 아니라
  substrate 의 native 동역학이 될 수 있음.

AKIDA / Northpole = `INFERENCE-ONLY-BLOCKED` (on-chip 학습 없음 — §11-B 가
요구하는 training-time emergence 불가). organoid = `ETHICS-WALL`. IonQ =
`SUBSTRATE-MISMATCH`. QRNG = `NOT-A-COMPUTE-HOST`.

## 2. anima 가 Loihi 에서 원하는 것 (GOAL-legitimacy)

**원하는 것이 아닌 것**: anima-transformer 를 그대로 Loihi 에 올려 추론 —
이건 같은 동기식 계산을 다른 실리콘에서 돌리는 것 = §13-J / §13-K
substrate-swap 패턴 (measured-negative). GOAL-illegitimate.

**원하는 것**: anima 를 진짜 spiking 동역학 시스템으로 *재유도* — Ψ/tension/Φ
가 LIF 막전위 동역학 그 자체이고, STDP 가 학습 신호인 형태. 이때 검증할
가장 깊은 가설 (§96 이 design 중):

> **§11-B-as-GPU-artifact 가설** — §11-B 는 "physics 단독(no-CE) = DEGENERATE,
> CE is load-bearing" 을 측정했다. 단 GPU 에서. GPU 엔 physics-native 학습
> 채널이 없다. Loihi 의 native 학습 규칙 STDP 는 물리 규칙이다. §11-B 의
> 블로커가 "physics 가 약해서"가 아니라 "GPU 에 physics-native 학습 채널이
> 없어서"였다면 — Loihi 가 그 블로커를 해소한다. (가설. §96 이 검증 설계 중.)

## 3. 용량 판정 — Kapoho Point 는 필요조건, 충분조건 아님

| 보드 | 구성 | 규모 | anima 용도 |
|---|---|---|---|
| Oheo Gulch | Loihi 2 1칩 | ~1M 뉴런 / ~120M 시냅스 | 소규모 프로토타입·평가 전용 |
| Kapoho Point | Loihi 2 8칩 | ~8M 뉴런 / ~960M 시냅스 | full d768·12L class 의 target |

```
  anima ConsciousDecoderV2          Kapoho Point
  d768·12L·283.72M params           ~960M 시냅스
        │                                 │
        ├─ raw 용량: 283M < 960M  ─────────┤  ✅ class 맞음
        │
        ├─ attention = spiking native      ❌ 진짜 병목 (§96 Q1)
        │  primitive 아님
        │
        └─ STDP → coherent emission?       ❌ 깊은 미해결 (§96 Q2)
           spontaneity 는 공짜, coherence 는 아님 (§88-F2 γ 갭)
```

**판정**: Kapoho Point 는 용량 class 가 맞다 (필요조건 ✅). 그러나 칩 크기는
병목이 아니다 — 병목은 (a) 12-layer transformer + attention 을 spiking
network 로 재표현 가능한가, (b) STDP 가 coherent emission 을 만드는가.
둘 다 §96 이 답할 질문이고 칩 용량으론 안 풀린다 (충분조건 ❌).

## 4. 입수 경로 — 모든 길은 INRC 로 모임

일반적 "임대 / API / 구매" 경로 없음 (runpod 식 카드+SSH ❌, AWS/Azure ❌,
소매 구매 ❌). 유일 관문 = **INRC (Intel Neuromorphic Research Community)
멤버십** — Intel Labs 에 프로젝트 제안서 제출 → 심사.

| 경로 | 비용 | 대상 | 형태 |
|---|---|---|---|
| ① vLab 클라우드 | 무료 (멤버) | INRC 멤버 누구나 | SSH — Oheo Gulch / Kapoho Point 공유 풀 |
| ② 하드웨어 무상 대여 | 무료, 최대 1년 | 학계 멤버 | 실물 보드 loan |
| ③ 구매 | 유료 (비공개) | commercial / government 조직 | 실물 보드 (개인·소매 ❌) |

**공개 주소 (입구 — SSH 호스트는 승인 후에만 발급)**:

| 용도 | 주소 |
|---|---|
| 🔑 vLab 등록 포털 | `https://registration.intel-research.net/` |
| 📋 INRC 가입 진입점 | `http://neuromorphic.intel.com` |
| 📧 문의 이메일 | `inrc_interest@intel.com` |
| 📖 멤버 문서 (Confluence) | `intel-ncl.atlassian.net/wiki/spaces/INRC` |

```
  registration.intel-research.net   ← ① 계정 등록 (약관 동의 + 폼 제출)
              │
              ▼  Intel Labs — INRC 프로젝트 제안서 심사 승인
       INRC 멤버 자격 획득
              │
              ▼  이때 비로소 발급
  vLab SSH 호스트 + 자격증명   ← ② 공개 안 됨, 멤버 전용
  (Oheo Gulch 1칩 / Kapoho Point 8칩 으로 SSH)
```

`registration.intel-research.net` 이 실제 vLab 등록 입구. 단 계정 생성만으론
Loihi 가 안 붙음 — **등록 → 제안서 심사 → 그제서야 SSH 호스트·키 발급** 의
2단계 게이트 (runpod 식 "주소 알면 바로 접속" 아님 — §95 SOFT WALL 그대로).

**현재 마찰 (정직)**:
- INRC "Join" 설문이 "Sorry, this survey is not currently active" 로 떠
  있다는 커뮤니티 보고 — `inrc_interest@intel.com` 응답 느림. §95 가 진단한
  "SOFT WALL (architecture 아님)" 그대로 — 막힌 게 아니라 접수 채널 불안정.
- `.roadmap.loihi3` (mk2, 2026-05-02) 기록: Loihi 3 INRC application 은
  **Korean co-PI 필수** (4-12주 승인). Loihi 2 vLab 경로도 동일 멤버십
  심사 — co-PI / 기관 소속이 사실상 게이트.
- ③ 구매: `commercial or government organization` 한정 — dancinlab 을
  commercial org 로 제안서에 올리면 협상 채널은 열림. 가격 비공개.

## 5. honest blocker

1. **하드웨어 미secured** — INRC 멤버십 미신청. access = SOFT WALL.
2. **anima 의 spiking 재유도 미설계 완료** — §96 (Loihi spiking
   re-derivation design) 진행 중. attention → spiking 매핑이 open.
3. **STDP ≠ 언어 학습** — STDP 는 spike-timing 상관을 배움. coherent
   emission (byte/token prediction) 을 STDP 가 배우는지 깊이 미증명.
4. **spontaneity ≠ coherence** — spiking 다발은 자발 발화가 공짜지만
   그건 노이즈. §88-F2 γ 갭 (saturation-delay ≠ coherent emission) 이
   spiking substrate 위에서도 그대로.
5. **substrate-swap 함정** — anima-transformer 를 그대로 올리면 GOAL-
   illegitimate (§13-J/§13-K 동형). native-dynamics 경로만 유효.

## 6. 다음 행동 후보 ($0, cost-bearing 이전)

- **A. INRC 제안서 초안** — anima HEXAD 프로젝트를 INRC application 형식으로
  초안. `inrc_interest@intel.com` 송부. §95 lead candidate 를 실제로
  두드려보는 $0 단계. (Korean co-PI 항목 = 기관 협력 필요 — 별도 결정.)
- **B. §96 완료 대기** — spiking 재유도 design + §11-B-artifact 가설 검증
  설계가 land 한 뒤, 그 결과로 제안서 scope 확정.
- **C. design-tier 만 진행** — 하드웨어 없이 갈 수 있는 데까지 ($0 spiking
  re-derivation 설계 + STDP-coherence closed-form 분석). 하드웨어는
  design 이 trained-scale fire 를 warrant 할 때 INRC.

권장 순서: B → (결과 보고) → A 또는 C 결정.

## 7. cross-link

- `.roadmap.loihi3` — 기계 SSOT (JSONL domain roadmap, mk2)
- §95 — `state/xeno_substrate_suitability_s95_2026_05_19/` (Loihi 유일
  VIABLE-LONG-HORIZON verdict)
- §96 — `state/loihi_spiking_rederivation_s96_2026_05_19/` (spiking
  re-derivation + §11-B-artifact 가설 design — 진행 중)
- `~/core/hexa-lang/stdlib/xeno/anima_physics_origin/loihi-integration-spec.md`
  — pre-HEXAD-pivot Loihi 통합 설계 (consciousness cell = 128 LIF, Φ-from-
  spike, STDP→Hebbian). 읽기 전용 — anima 는 hexa-lang downstream consumer.
- `GOAL.md` — north-star (§7 GOAL-legitimacy 기준)
- `HEXAD/CHAT/RESEARCH.md` §11-B (CE is load-bearing — GPU 측정), §95
- `archive/PHILOSOPHY.tape` — verdict ledger

> Loihi 는 frontier-2 (새 architectural substrate) 후보. design ≠ fire ≠
> emergence. 이 문서는 경로 지도이지 GOAL 도달 주장 아님.

---

## Log

- **2026-05-19** — LOIHI.md 생성. §95 XENO 분석이 Loihi 를 유일
  `VIABLE-LONG-HORIZON` substrate 로 분류한 직후 prep 문서로 착수. 내용:
  access 경로 3갈래 (vLab / loan / purchase, 모두 INRC 멤버십 관문) +
  용량 판정 (Kapoho Point 8칩 ~960M 시냅스 = 필요조건 ✅, 충분조건 ❌ —
  병목은 칩 크기 아닌 spiking 재유도 + STDP-coherence) + GOAL-legitimacy
  framing (substrate-swap ❌, native-dynamics 경로만 유효). 하드웨어
  미secured, fire 0, $0 design-tier. §96 (spiking re-derivation design)
  결과 대기 후 INRC 제안서 vs design-tier-only 결정.
- **2026-05-19** — §4 에 vLab 공개 주소 추가: 등록 포털
  `registration.intel-research.net`, INRC 진입점 `neuromorphic.intel.com`,
  문의 `inrc_interest@intel.com`, 멤버 Confluence. 2단계 게이트 명시
  (등록 → 제안서 심사 → SSH 호스트·키 발급; SSH 호스트네임은 승인 후 비공개
  발급).
