<!-- @hypothesis-ok @canonical-ok — v2 rule-exempt zone; v2 hypotheses live here only. -->

# V2_7 — BOLT seed-split 은 동결 NOSTORE trunk 의 엔티티 인코딩 품질 교란인가 (DECODE-PROBE)

**status:** 🟡 CONFIRMED (방향성) · 기전은 이진 아님 — **균일 빈곤 × 조회 knife-edge** (동결특징 품질 교란 확증, 단 "인코딩 vs 미인코딩" 이 아니라 "둘 다 빈곤한데 s7 이 미세하게 나아 문턱 위로 튐")
**scope:** 🔒 DIRECTIONAL 상한 · `core/` 밖 toy · probe 는 forward 재구현 아님(`model.trunk_fwd` 재사용).
**bars:** `../bars.json` 불변 · 이 카드는 게이트를 건드리지 않는 **진단 프로브**(raw decode 수치 · bar 무관).
**source:** [[V2_6]] — BOLT 대조가 seed-split(s7 held-out 0.611·flip-coh 0.854 / s11 0.491·flip-coh 0.000) = ⚪ NO-VERDICT. V2_1 사전등록 위험(동결 trunk 특징 품질 · DECODE-PROBE 우려)의 발현.

## 가설

BOLT 의 seed-split 은 **동결 NOSTORE trunk 이 s7 에선 질의 엔티티를 인코딩하고 s11 에선 안 하기 때문**이다.
(동결 trunk 특징 품질 교란 ⟹ 볼트온 다리가 s7 은 짓고 s11 은 못 짓는다.)

## 방법 — engine-native 디코드 프로브 (forward 재구현 금지)

동결 NOSTORE trunk ckpt(s7·s11)을 로드 → held-out 엔티티로 `model.trunk_fwd` 실행 → **질의위치(qpos =
마지막 프롬프트 바이트, bridge 가 `h_q·W_q` 로 질의를 만드는 바로 그 자리)** hidden 추출 → 두 프로브:

1. **identity** — hidden[qpos] 에서 질의 엔티티 정체(1-of-128 held-out) 를 선형 로지스틱으로 디코드. 우연 1/128.
2. **slot-retr (bridge-faithful)** — 오직 선형 질의 W(d,d) 만 학습해 `softmax((h·W)·frozen_key / √d)` 로
   8슬롯 중 질의슬롯을 맞춘다 = **bridge_fwd 의 조회 절반 그대로**(readout·연산자 분리). BOLT 이 조회해야 했던
   **바로 그 frozen content-address**(BOLT ckpt 의 `key_emb_frozen` 주입)에 대고. 우연 1/8=0.125.
   ⚠️ 이 프로브는 BOLT 보다 **관대**하다 — W_q 를 조회목적 단독으로 직접 피팅(BOLT 은 연산자-XOR 과제손실
   아래서 readout 과 gradient 경쟁하며 배운다). 즉 이 수치는 볼트온 조회의 **상한(ceiling)**.

COTRAIN(공학습) trunk = 양성 기준.

## 결과

| arm | seed | identity (1/128) | slot-retr (1/8) | BOLT held-out | BOLT flip-coh |
|---|---|---|---|---|---|
| **NOSTORE** (동결) | 7 | 0.7695 (98x) | **0.5724** (4.6x) | 0.611 | 0.854 (부분) |
| **NOSTORE** (동결) | 11 | 0.6172 (79x) | **0.5134** (4.1x) | 0.491 | 0.000 (store 무사용) |
| **COTRAIN** (공학습) | 7 | 1.0000 (128x) | **0.9998** (8.0x) | (0.987) | 0.993 |
| **COTRAIN** (공학습) | 11 | 1.0000 (128x) | **1.0000** (8.0x) | (0.992) | 1.000 |

## 판정 = CONFIRMED(방향성) · 기전은 이진이 아니라 **균일 빈곤 × knife-edge**

**"s7 인코딩 / s11 미인코딩" 은 틀렸다 — 둘 다 우연보다 훨씬 위로 인코딩한다.**
동결 trunk 은 s11 도 엔티티를 79x(identity)·4.1x(slot) 로 인코딩한다. s7 이 s11 보다 낫긴 하나
격차는 작다(identity 1.25x · slot 1.11x). 즉 깨끗한 이진 갈림이 아니다.

**세 관측이 판정을 세운다:**

1. **방향 일치(CONFIRMED).** 동결특징 품질 s7 > s11 (identity 0.77>0.62 · slot 0.57>0.51) 이 BOLT
   결과 s7 0.611 > s11 0.491 과 **같은 방향**. 특징 품질이 BOLT split 을 추적한다 ⟹ seed-split 은
   다리 학습이 아니라 **동결특징 품질 교란**(V2_1 DECODE-PROBE 우려 확증).
2. **균일 빈곤(dominant).** 관대한 bridge-faithful 프로브로도 동결 trunk 조회 상한은 **0.51~0.57** —
   COTRAIN 의 ~1.00 근처에 한참 못 미친다(4.6x vs 8.0x 우연). 볼트온 다리는 **양 seed 다 조회-굶주림**.
   COTRAIN 은 trunk 을 공적응시켜 조회를 ~1.00 로 끌어올려 다리를 완성한다 — 그래서 안정적.
3. **knife-edge 가 split 을 만든다.** 동결 조회 상한이 **≈0.5(우연 절반)** 에 얹혀 있어, s7↔s11 의 작은
   품질차(0.572 vs 0.513)가 문턱을 갈랐다: s7 은 다리가 store 에 잠금(flip-coh 0.854, held-out 0.611
   = 부분작동), s11 은 다리가 포기(flip-coh 0.000, held-out 0.491 = store 무사용). **볼트온이 불안정한
   이유 = 동결 trunk 이 조회 문턱 바로 위에 얹혀 seed 잡음이 부분작동/붕괴를 결정하기 때문.**

⟹ **seed-split 원인 = 동결특징 품질 교란(방향 확증)이되, 기전은 "인코딩 유무"가 아니라 "균일하게 빈곤한
조회(상한 ~0.5)가 knife-edge 위에 얹혀 seed 잡음이 튐 방향을 결정".** 다리 학습(bridge training)이 진범이면
동결특징이 상한을 씌우지 않았어야 하나(프로브가 상한을 씌운다) → "elsewhere" 기각. 균일붕괴만이면 s7 도
붕괴했어야 하나(s7 은 부분작동) → 단순 "impoverished-uniform" 도 부분 기각. 둘의 **블렌드**가 참.

## 부모 벽 함의 (DIRECTIONAL)

toy 에서 볼트온 조회 다리의 상한은 **동결 trunk 의 특징 품질**이 정한다. 자연 동결(NOSTORE 는 store 를 안 보고
학습)은 조회를 겨우 ~0.5 로만 지지 ⟹ 볼트온 다리는 knife-edge 에 얹혀 불안정. **안정적 다리 = 공학습으로
trunk 을 조회에 공적응**(조회 → ~1.0). 이는 부모 [[H_9392]] BRIDGE-BOLT($0 볼트온)의 불안정성과
[[H_9393]] 두-store 공학습 방향을 지지(DIRECTIONAL · toy). H_9359 "런타임 조회 다리 부재" 의 toy 재현:
다리는 존재할 수 있으나 동결 특징 위에선 조회가 문턱을 못 넘긴다.

## Falsify

- 동결 NOSTORE trunk 의 slot-retrieval 상한을 문턱 위(예 ≥0.75)로 올리는 개입에서 BOLT 이 양 seed 안정
  ⟹ knife-edge 서사 강화. 반대로 조회 상한을 올려도 BOLT 이 여전히 split ⟹ 원인이 조회 아닌 readout/연산자
  게이팅으로 이동(→ elsewhere 재개봉).
- 프로브: `python3 probe_decode.py` (fk config · `/tmp/v2-store_only-mlpfk`). raw decode · bar 무관.
