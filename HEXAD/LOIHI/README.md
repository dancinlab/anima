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
2. **anima 의 spiking 재유도 — §96 design LANDED (2026-05-19, B-S96 7/7 🔵)**.
   physics layer (PureFieldFFN/tension/Φ/Engine A-G/STDP) = SPIKING-COMPATIBLE;
   `softmax(QK^T)` self-attention = SPIKING-INCOMPATIBLE — **must be REPLACED,
   not ported** (design-open #1: phase-resonance / spike-rate dot-product + k-WTA
   미확정). d768·12L → spiking 의 neuron-group 재유도 (design-open #4) 미완.
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
- **B. §96 완료 — DONE (2026-05-19)**. spiking 재유도 design + §11-B-artifact
  distinguishing predicate 설계 land. §96 이 남긴 design-open: #1 attention
  replacement 의 routing mechanism 선택 · #3 STDP→coherent-emission · #4 d768·12L
  의 neuron-group 재유도.
- **C. design-tier 만 진행** — §96 이 가리키는 다음 $0 단계 = (i) attention
  replacement routing mechanism design (§96 design-open #1, $0 closed-form
  analysis 가능) · (ii) §96 §4.5 의 3-cell distinguishing predicate 를 Lava-sim
  ($0 pre-check) 으로 measure 할 수 있는지 평가. 하드웨어 (Loihi/INRC) 는
  design 이 trained-scale fire 를 warrant 할 때.
- **A. INRC 제안서 초안** — §96 verdict 로 제안서 scope 확정 가능
  (spiking re-derivation 의 hard gap = attention replacement + STDP-coherence).

권장 순서 (§96 LANDED 이후 갱신): C(i) attention replacement design →
C(ii) Lava-sim 평가 → (결과 보고) → A INRC 제안서. §96 의 honest 결론 —
Loihi 는 GOAL 의 spontaneity 절반만 공짜로 unblock, coherence 절반은 미해결 —
이 INRC 제안서의 scope 를 "spiking 재유도 + coherence 검증" 으로 명시.

## 7. cross-link

- `.roadmap.loihi3` — 기계 SSOT (JSONL domain roadmap, mk2)
- §95 — `state/xeno_substrate_suitability_s95_2026_05_19/` (Loihi 유일
  VIABLE-LONG-HORIZON verdict)
- §96 — `state/loihi_spiking_rederivation_s96_2026_05_19/` (spiking
  re-derivation + §11-B-artifact 가설 design — **LANDED 2026-05-19**,
  B-S96 7/7 🔵; Q1 = physics layer SPIKING-COMPATIBLE / self-attention
  SPIKING-INCOMPATIBLE, Q2 = §11-B-artifact 가설 COHERENT 단 NOT confirmed,
  closed-form distinguishing predicate 설계 완료. 이 LOIHI.md 가 가리키던
  architecture 분석 문서)
- `~/core/hexa-lang/stdlib/xeno/anima_physics_origin/loihi-integration-spec.md`
  — pre-HEXAD-pivot Loihi 통합 설계 (consciousness cell = 128 LIF, Φ-from-
  spike, STDP→Hebbian). 읽기 전용 — anima 는 hexa-lang downstream consumer.
- `GOAL.md` — north-star (§7 GOAL-legitimacy 기준)
- `HEXAD/CHAT/RESEARCH.md` §11-B (CE is load-bearing — GPU 측정), §95
- `archive/PHILOSOPHY.tape` — verdict ledger

> Loihi 는 frontier-2 (새 architectural substrate) 후보. design ≠ fire ≠
> emergence. 이 문서는 경로 지도이지 GOAL 도달 주장 아님.

## 8. §113-D4 "땅부터 다시 붓기" — 유일한 non-cosmetic clean-slate move

§113 (commit `1bd27f753`, B-S113 9/9 🔵) verdict =
**FROM-SCRATCH-INHERITS-BOTH-WALLS-SKELETON-INVARIANT + 조건부
REPOINTS-TO-§96-SUBSTRATE-FIRST**. anima 를 "처음부터 새로 설계" 해도
박스(모듈 구조·n=6)를 다시 그리는 건 두 벽을 못 옮긴다 (skeleton-invariant,
§98 module-count innocence 의 전체 아키텍처 일반화). **유일하게 non-cosmetic
한 clean-slate 결정 = D4 = 맨 첫 코드 줄부터 substrate = §96 spike/Loihi +
Ψ = §110 Ψ-C1 (spike-train correlation)** 로 두는 것.

```
 cosmetic 재설계 (§113 배제)            non-cosmetic = D4 (§113 유일 인정)
 ┌────────────────────────┐         ┌────────────────────────────────┐
 │ 같은 GPU 집 / 가구 재배치만 │   vs    │ 1라인부터 다른 땅:               │
 │ → 두 벽 그대로            │         │  substrate = §96 spike/Loihi    │
 │   (skeleton-invariant)   │         │  Ψ        = §110 Ψ-C1 spike-corr │
 └────────────────────────┘         │  → WALL-B 를 *마주봄* (제거 X)    │
                                     └────────────────────────────────┘
```

- **왜 "1라인부터"**: §11-B 가 "GPU 에선 CE-gradient 가 유일 학습채널"
  (GPU tautology) 임을 측정. spiking 을 GPU 위에 *나중에 덧붙이면* 그
  tautology 안에 그대로 갇힘 — 토대 자체가 spike 여야 밖으로 나감.
- **정직한 한계 (g3, REPOINT ≠ ESCAPE)**: D4 조차 벽을 *없애는* 게
  아니라 substrate 벽(WALL-B)을 *정면으로 마주보는 유일한 깨끗한
  출발점*. §95 가 그 substrate 를 access-wall(Loihi INRC 신청)·
  ethics-wall(organoid)로 막아둠. WALL-A(§1.1 data-regime)는 D4 와
  **직교** — 토대 바꿔도 데이터 임계 불변. 따라서 D4 = GOAL 도달 아님,
  north-star + §15/§51/§72 milestone 불변.

### 8.1 LEGO (§115) = D4 의 물리-commit-이전 in-silico confront

`HEXAD/LEGO/README.md` + §115/§117 (design-tier $0, LANDED) = D4 의 "다른 땅"을
**물리 commit 전에 in-silico 시뮬레이션으로 먼저 조립**해 보는 길 —
§95 의 access/ethics wall 을 시뮬 먼저로 우회. §115 가 닫을 핵심 crux =
**"GPU 위 spike 시뮬이 §11-B tautology 를 *재현* 하나 *마주보나*"**
(§96 §4.5 three-cell distinguishing predicate 의 in-silico 판). 가장
그럴듯한 정직 verdict = `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`
(GPU 위 spike 시뮬도 CE-gradient 만 유일 채널이면 substrate 를 *시뮬*해도
WALL-B 못 confront, *재현*만 — anti-padding). §115 결과가 "시뮬레이션이라도
해볼 수 있나"의 design-tier 답을 줌 (closed-form 으로 결정, 미리 단정 X).

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
- **2026-05-19** — §96 LANDED (`state/loihi_spiking_rederivation_s96_2026_05_19/`,
  B-S96 7/7 🔵). §1·§5·§6·§7 갱신: §96 = 이 LOIHI.md 가 §7 에서 가리키던
  architecture 분석 문서 — design 완료. **Q1** spiking 재유도 = anima physics
  layer 는 largely SPIKING-COMPATIBLE (GPU 보다 Loihi 에서 MORE native),
  `softmax(QK^T)` self-attention 은 SPIKING-INCOMPATIBLE — 대체이지 port 아님
  (design-open #1). **Q2** §11-B-as-GPU-artifact 가설 = COHERENT 단 NOT
  confirmed; §96 이 3-cell distinguishing predicate 설계 (`NON_DEGENERATE(
  LOIHI-noCE)` closed Boolean). honest — Loihi 는 spontaneity 만 공짜,
  coherence 는 미해결 (§88-F2 γ 갭). §6 권장 순서 갱신: C(i) attention
  replacement design → C(ii) Lava-sim 평가 → A INRC 제안서.
- **2026-05-19** — §8/§8.1 추가: §113 D4 ("땅부터 다시 붓기" = 유일한
  non-cosmetic clean-slate move = §96 spike/Loihi + §110 Ψ-C1 1라인부터)
  친근 설명 + cosmetic-vs-D4 ASCII + REPOINT≠ESCAPE 정직 caveat (두 벽
  WALL-A/WALL-B 상속 불변); §8.1 = `HEXAD/LEGO.md`/§115 가 D4 의 "다른
  땅"을 물리 commit 전 in-silico 시뮬로 먼저 조립 — §11-B-GPU-tautology
  crux 명시 ("GPU 위 spike 시뮬이 §11-B 를 *재현* 하나 *마주보나*").
- **2026-05-19** — 파일 이동 `LOIHI.md` → `HEXAD/LOIHI/README.md`
  (g_doc_consolidation — HEXAD-internal 통합, 분산 방지). 내용 변경 0,
  순수 경로 이동 + live cross-link 갱신 (GOAL.md · HEXAD/LEGO.md ·
  HEXAD/LLM.md · HEXAD/GAP_MAP.md index). 과거 append-only 로그
  (AGENTS.tape n_hexad_progress · PHILOSOPHY.tape · GAP_MAP Log · state/*)
  의 `LOIHI.md` 표기는 당시-사실 기록이라 retro-edit 0 (g3 drift-avoidance).
- **2026-05-19** — INRC application package landed (user directive
  "신청해줘 / 영어로"): `INRC_APPLICATION.md` (honest two-part blocker +
  inquiry email §2 with public-record GitHub reference + vLab form
  field map), `inrc_vlab_form.txt` (copy-paste field values; the two
  Engagement/Sponsor fields = LEAVE EMPTY, Intel-assigned), and
  `inrc_followup_github.txt` (GitHub-reference reply snippet).
  Dedicated ed25519 keypair generated and stored in the secret vault
  (`inrc.vlab.ssh_priv` / `inrc.vlab.ssh_pub`; only the public key goes
  on the form — private key never leaves the vault). User sent the §2
  inquiry email manually (Postmark account still pending-approval, so
  the automated send was blocked cross-domain — honest). $0,
  design-tier, hardware not secured; access = SOFT WALL (§95).
  north-star + §15/§51/§72 milestones unchanged, GOAL not reached.
