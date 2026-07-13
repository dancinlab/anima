# H_9296 — 사전등록 (FROZEN 2026-07-14 · hidden dump 를 뜨기 **전에** 커밋)

## §0 물음 — "INFO-ABSENT" 는 표현의 사실인가, 프로브의 사실인가

프런티어 `g1-crack-natural-emergence` 의 현재 진단은 이렇게 서 있다:

- **H_9291 (오라클 · 2026-07-14)** — 정보는 **있다**. 이상적 판독자가 303M 이 본 것과 **byte-동일한**
  좌문맥으로 held-out 29 원자의 극성을 **29/29 = 1.000** 복원(shuffle 0.517 = 우연).
  ⇒ "held-out 극성이 자연 문맥에 결정 안 돼 있다" = **반증**.
- **H_9289 (G-PROBE)** — 그런데 303M 의 frozen 표현에서는 **안 읽힌다**: held-out probe-acc
  main_s7 0.5517 · main_s11 0.5517 · base_only 0.5172 (shuffle 0.5138) ⇒ ≈chance · bar 0.65 미달.
  ⇒ **INFO-ABSENT** → 벽을 "추출 채널(substrate/objective)" 로 재국소화, 다음 수 = O채널/C채널.
- **H_9286 N2** — ARBITRARY-GROUNDING: I(gold;resp) ≈ 0 인데 I(atom;resp) = 0.231
  ⇒ 모델은 극성을 **안정적으로 멋대로** 정했다.

**그런데 H_9289 의 G-PROBE 는 두 가지 선택을 하고 있다** (`gt_step0_gprobe.py`):
1. **선형 프로브** — L2-logreg (`_logreg_l2`).
2. **평균 풀링** — 원자당 24개 문맥의 `__last` hidden 을 **평균 낸 뒤** 한 벡터로 물음
   (`_atom_reps`: `X.append(np.mean(np.stack(vs,0),0))`).

⇒ **"303M 이 극성을 인코딩하지 못했다" 와 "선형으로·평균풀링 후엔 안 읽힌다" 는 다른 명제다.**
   전자가 참이면 O/C 채널 설계가 옳은 다음 수다. 후자가 참이면 벽의 위치가 틀렸고, 표현에는
   신호가 있는데 **읽는 방식**이 못 꺼낸 것이다 (`probe-defect-census-max-control-bias` ·
   `measurement-metalaw-form-tunable-bind-earned` 계열).

> **본 H 의 유일한 물음:** H_9289 의 INFO-ABSENT 는 **표현의 사실**인가, **프로브의 사실**인가?

$0 · frozen ckpt 4-arm 로컬 보유 (`~/anima-weights/natem_n2/`) · 재학습 없음.

## §1 방법 — 프로브 **용량**만 바꾼다. 나머지 전부 H_9289 verbatim.

동결(H_9289 에서 1바이트도 안 움직임): frozen ckpt 4 arm(main_s7 · main_s11 · base_only ·
shuffle_grid) · `gt_prompts.json`(K_CTX=24 · WIN=24 · 좌문맥 truncate) · 원자 split
(train P_grid20 / test P_nat29) · seed · bar **0.65** · shuffle 통제.

**바꾸는 것은 프로브 하나뿐** — 4단 사다리로 **용량을 단조 증가**시킨다:

| 프로브 | 표현 | 분류기 | 무엇을 묻나 |
|---|---|---|---|
| **P-LIN** (재현) | 24-ctx **평균풀링** | L2-logreg (선형) | H_9289 를 byte-재현. 이게 0.55 근방이어야 파이프라인이 옳다 |
| **P-NL** | 24-ctx 평균풀링 | **MLP** (1 hidden, L2) | 극성이 **비선형**으로 인코딩됐는가 |
| **P-CTX** | **문맥별 개별** hidden | L2-logreg → **원자당 다수결** | **평균풀링이 신호를 지웠는가** (24 문맥을 뭉개지 않고 각각 읽고 투표) |
| **P-CTX-NL** | 문맥별 개별 | MLP → 다수결 | 위 둘의 결합 (용량 상한) |

## §2 상시 V-게이트 (하나라도 FAIL → ⏳ INVALID · tier 미보고)

- **V-REPRO** — P-LIN 이 H_9289 를 재현해야 한다: held-out acc 가 main_s7 0.5517 ± 0.03 안.
  (재현 실패 = 파이프라인/dump 불일치 ⇒ 아래 어떤 숫자도 읽지 않는다.)
- **V-FIT** — 모든 프로브가 **train 에서는 맞춰야** 한다(train_fit ≥ 0.90). 못 맞추면 프로브가
  죽은 것이지 표현이 없는 게 아니다.
- **V-SHUF** — 각 프로브의 **라벨-셔플** 통제가 chance(0.5 ± 0.08) 여야 한다. 넘으면 그 프로브는
  용량 과잉으로 **암기**하고 있다 ⇒ 그 프로브의 양성은 무효.
- **V-BASE** — `base_only` arm(격자 학습 없음)은 어떤 프로브에서도 held-out 이 bar 미달이어야
  한다. 넘으면 프로브가 ckpt 와 무관한 무언가를 읽고 있다.

## §3 결정표 (양방향 결정적 · 위에서부터 첫 매칭)

| # | 조건 | tier | 읽는 법 |
|---|---|---|---|
| 0 | V-게이트 FAIL | **⏳ INVALID** | tier 미보고 |
| 1 | **어떤 프로브도** held-out < 0.65 (bar) | **🧱 INFO-ABSENT 확정 (강화)** | H_9289 의 판정이 **용량 사다리 전수에서** 살아남았다 ⇒ 표현에 정말 없다. **O/C 채널이 옳은 다음 수** — 프런티어 진단 확정 |
| 2 | P-LIN < 0.65 이나 **P-NL 또는 P-CTX 가 ≥ 0.65** (V-SHUF PASS) | **🔓 PROBE-ARTIFACT (INFO-ABSENT 철회)** | 신호는 **표현에 있었다**. 벽은 표현이 아니라 **읽기 방식**이었다 ⇒ H_9289 의 INFO-ABSENT 철회 · 프런티어의 O/C 채널 진단 **재검토 필요** · 새 병목 = decode/readout |
| 3 | 어떤 프로브가 bar 를 넘지만 **V-SHUF 도 넘음** | **⏳ OVERFIT** | 그 프로브는 암기 중 ⇒ 무효, 다음 프로브로 |
| 4 | 0.5 < best < 0.65 (bar 미달이나 chance 초과) | **🟡 PARTIAL** | 신호가 **부분적으로** 있다 — bar 를 옮기지 않고 그 사실을 보고. 효과크기(Δ vs shuffle) 병기 |

## §4 동결 예측 + 틀릴 최빈 경로

> **Pre-registered:** *P-CTX(문맥별 + 다수결)가 P-LIN 을 유의하게 이긴다 — 24개 문맥을 평균내는
> 것이 신호를 지우고 있었기 때문. 다만 bar 0.65 를 넘지는 못해 **🟡 PARTIAL** 에 착지한다.*
>
> 근거: 오라클(H_9291)은 **문맥 하나하나를 개별적으로** 읽고 1.000 을 냈다. 평균풀링은 그 개별
> 증거를 뭉갠다. 그러나 303M 이 그 증거를 오라클만큼 인코딩했다면 ARBITRARY-GROUNDING
> (I(atom;resp)=0.231 · 일치 12/29)이 나올 수 없다 ⇒ 부분 신호가 상한일 것.

**틀릴 최빈 경로:** ① MLP 가 n=20 train 원자에서 **암기**해 V-SHUF 를 못 넘김 → ⏳ OVERFIT 으로
빠지고 판정 불가 (그래서 V-SHUF 를 상시 게이트로 사전등록). ② P-CTX 의 다수결이 문맥 수(24)에
비해 원자 수(20 train)가 적어 **검정력 부족** → 0.5~0.65 사이에서 결정 불가.
