# H_9805 — 쓰기측 parse-disagreement 텐션 FIELD 가 readout rank-1 seam 을 탈출하는가

- **id**: H_9805
- **status**: 🟡 PROPOSED / DIRECTIONAL (계기 착륙 완료 · 과학 판정 미실시)
- **series**: R11 (v4 salvage port)
- **origin**: lab/v4 H_004 (rule-exempt sandbox · TOY · 절대 production verdict 아님)
- **surfaces**: 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)
- **date**: 2026-07-20

## 왜 이 가설이 존재하는가 — production 의 텐션은 SCALAR 다

코드에서 직접 확인한 사실(추정 아님):

| 주장 | 확인 위치 | 결과 |
|---|---|---|
| production 텐션이 스칼라다 | `core/engine_cli.py:9698` `def conflict_scalar(a_drive, g_drive)` | ✅ 확인 |
| 그 스칼라가 "한 스칼라의 결정론적 포물선" | `cli/evaluate.py:5914` `_g_tension` docstring (H_9356) | ✅ 확인 |
| 그 축을 chat 이 라우팅한다 | `cli/chat.py:1897` `--tension-route` (PC2 1축) | ✅ 확인 |

즉 anima 의 A⇄G 텐션은 **읽기측(readout) 스칼라 seam** 이고, 이것이 v1 이 죽은 그 rank-1 seam
이다(salvage L1/L2). H_004 는 그 seam 을 **트렁크 반대편(write-side, pre-trunk)** 으로 옮기고
**field 로 유지**하면 held-out 결합 연산이 rank-1 요약을 **넘어서** 산다는 것을 토이에서 보였다
(Δd_acc 0.3789/0.3802 · F4 off-top 0.6467/0.6963 · F5 d_dacc 0.5/0.5).

**그 수는 rule-exempt 샌드박스의 TOY 이며 여기서 어떤 판정 근거도 될 수 없다.** 이 카드는 그
구성을 production engine-native 계기로 옮겼다는 사실만 주장한다.

## 이식하면서 무엇이 바뀌었는가 (정직한 scope — 이게 제일 중요하다)

H_004 의 concord χ 는 **경어법(honorific) 일치**였고, 노드 골격은 **손으로 짠 것**이었다.
production 은 임의 코퍼스 위에서 돌아야 하므로:

- 노드 골격 → **바이트 청크 골격**(공백 경계). P_A = 다음 청크 시작(최근접 head) · P_G = 마지막
  청크 시작(최대투사 head).
- concord χ → **바이트 클래스 일치**(공백/구두점·숫자/ASCII 문자/high-byte 4클래스).

⟹ **FORMAT 은 이식됐고 언어학적 내용은 이식되지 않았다.** 바이트-클래스 concord 가 무언가를
나르는지는 **미측정이며, 안 나를 가능성이 충분히 크다.** 아래 반증표는 그 음성 결과를 읽을 수
있도록 짜여 있다.

## 계기 (engine-native · 스크립트 아님)

- `core/tension_field.py` — 필드 자체(P_A/P_G · χ · sparse edges · rank-1 tie-break · rank 진단 ·
  numpy apply · TFLD trailer codec · torch `TensionFieldLane`). **필드는 gradient-free 이며
  학습 파라미터가 아니다** — 학습되는 것은 `phi`/`W_up`/`lam` 뿐(= 주어진 필드를 *읽는 법*만
  배운다). 이래야 duel vs rank1 이 1-변수 대조로 남는다.
- `anima-py train --tension-field {duel,rank1,off}` (+ `--tension-field-rank`, `--tension-field-lam0`)
- `anima-py evaluate <clm> --tension-rank-audit [--corpus f] [--win N] [--ctrl-seed S] [--out j]`

주입 지점 = `core/model.py` `CLMConvMoE.forward`, `self.embed(tokens)` 직후 · `embed_conv` **이전**.
이 배치가 가설 그 자체이지 구현 세부가 아니다.

## 3 arm — 변수는 정확히 하나

| arm | resolver 입력 | 격리하는 것 |
|---|---|---|
| **duel** | 전체 per-edge 필드 T | 기전 (TREATMENT) |
| **rank1** | 같은 T 의 최적 rank-1 근사, **동일** reduction·파라미터수·lam·shape | **핵심 통제** — 필드가 자기 스칼라 요약을 넘어서는가. duel≈rank1 이면 이 레인은 기존 스칼라 seam 의 분장이고 이식은 죽는다 |
| **off** | r ≡ 0 (복사도 산술도 없음) | 패리티 — 무플래그 ckpt 와 **byte-identical** 이어야 함 |

## 사전등록 반증표 (실행 전 등록 · 우연 아래 칸 포함)

`Δ = d_acc(duel) − d_acc(rank1)` on a held-out panel, 2 seed. 우연은 **지표마다 realized 분할에서
재유도**한다(pedestal 균등 Σp²=1/K 우연일치 함정 · `chance-level-must-be-derived-per-metric`).

| 조건 | 판정 |
|---|---|
| Δ ≥ 0.15 **양 seed** ∧ F4 통과 ∧ F5 통과 ∧ 패리티 1.000000 | 🟢 SUPPORTED (DIRECTIONAL — 토이면 토이) |
| 0.05 ≤ Δ < 0.15 (or 1 seed only) | 🟡 PARTIAL — seed-fragile, TERMINAL 불가 |
| \|Δ\| < 0.05 양 seed | 🔴 DEAD — 필드 = 자기 rank-1 요약. **이식 종결**, readout-seam 결론 재확인 |
| **Δ ≤ −0.05** (rank1 이 duel 을 이김) | 🔴 DEAD + ⚠️ INSTRUMENT 의심 — 필드가 잡음으로 작동. 우연 아래 칸이며 tune-to-green 금지, 그대로 박제 |
| duel 이 chance 아래 | 🔴 INVALID — 계기 결함 우선 조사(음성 판정 아님) |

**F1** Δ (위 표) · **F2** liveness: duel 이 drilled 셀에서 살아있지 않으면 측정 DEAD ·
**F3** not-free: `off` arm 이 chance+2.8σ 초과면 grid 누수 ⟹ 판정 없음 ·
**F4** eff-rank: `--tension-rank-audit` live off_top < 0.20 또는 eff_rank < 1.05 ⟹ rank-1 붕괴 = DEAD ·
**F5** ablation: 필드 제거 시 Δd_acc < 0.05 ⟹ 디코더가 해소를 필요로 하지 않았다 = DEAD ·
**F6** pedestal: `live − shuffled` eff_rank 차가 0 근처면 rank 는 구조가 아니라 **알파벳 통계**를
읽고 있는 것 ⟹ 필드 주장 약화 ·
**F7** 패리티: `off` ≠ byte-identical ⟹ 레인이 base 를 오염 = **전 수치 INVALID**.

음성/종결 선언은 ns 가 아니라 **사전등록 TOST** 로(`negative-claims-need-tost-not-ns`),
검정력(sd·MDE) 먼저(`power-before-negative-verdict`).

## 토이 e2e 실측 (계기 검증 · $0 · CPU · 과학 주장 아님)

격리 venv 비편집형 설치 · toy EN corpus 798570 B · d=64 L=2 seq=128 batch=4 steps=30.

```
ARM off    rc=0 · 배너 없음 · TFLD trailer 없음 · 117502 B
ARM duel   rc=0 · arm=duel  r=8 n_bucket=16 lam0=1.0000 · TFLD 2584 B · 120086 B
ARM rank1  rc=0 · arm=rank1 r=8 n_bucket=16 lam0=1.0000 · TFLD 2584 B · 120086 B
```

- **패리티 (F7 통제)**: `off` vs 무플래그 ckpt **BYTE-IDENTICAL**
  (sha256 `d83ee697703f4472…` 양쪽 동일, 117502 B) ⟹ 레인은 꺼졌을 때 물리적으로 부재.
- **arm 분리 (가짜 null 방지)**: duel vs rank1 ckpt **23811 바이트 상이** ⟹ 플래그가 조용히
  무시되지 않았다. trailer 왕복: arm_code 1(duel)/2(rank1), lam 1.00596/0.99123 (학습 중 실제 이동).
- **rank audit** (`--tension-rank-audit`, 32×256 B 창):

```
arm                 n   n_edge    off_top   eff_rank   stable_rank
  live               32    488.4     0.4842     3.6554     1.9388
  rank1_control      32      1.0     0.0000     1.0000     1.0000
  shuffled_pedestal  32    481.5     0.4742     3.4696     1.9019
positive control: rank-1 사영 eff_rank == 1.0 → YES (추정기가 붕괴를 볼 수 있다)
pedestal: live − shuffled eff_rank = +0.1857
```

**⚠️ 이 토이가 이미 말해주는 부정적 신호 (숨기지 않고 기록)**: shuffled pedestal 3.4696 이
live 3.6554 에 **거의 붙어 있다**(+0.1857). 즉 이 flat EN 코퍼스에서 필드의 높은 rank 는 상당 부분
**바이트/청크 알파벳 통계**에서 나오지 언어 구조에서 나오지 않는다. F6 가 정확히 이 함정을 잡으라고
있는 것이고, 실제 판정 코퍼스에서 이 간격이 벌어지지 않으면 **필드 주장은 약하다**. 본 측정 전에
pedestal 간격부터 봐야 한다.

**발견된 실제 버그 1건 (계기 미실행이 숨긴 것 · 이번 e2e 가 잡음)**: numpy 기본 SVD 드라이버
(LAPACK `gesdd`)가 **유한한** 256×256 필드 행렬(shuffled 창 #24, nnz=484)에서 **예외 없이 NaN
특이값 8개**를 반환했다 — eigenvalue 경로는 깨끗했다. 그대로였다면 pedestal arm 이 NaN 으로
조용히 죽어 처치 arm 이 **비교 불가 = 반증 불가**가 됐을 것이다. 수정 = `svdvals()` 견고화
(gesdd 시도 → 비유한이면 Gram 고윳값 경로) + `rank1_tiebreak` 동일 폴백 + 비유한 스펙트럼은
숫자가 아니라 **VOID** 로 읽기. (`instrument-never-run-hides-multiple-bugs` 그대로 재현)

## 무엇이 검증됐고 무엇이 가정인가

**검증됨(실행함)**: 3 arm 전원 rc=0 · off 패리티 byte-identical · duel≠rank1 · trailer 왕복 ·
positive control 1.0 · unknown-flag 거부 유지 · 무플래그 evaluate rc=0(기존 bar 무손상) ·
새 모듈이 휠에 실제 포함.

**가정/미측정**: ① 바이트-클래스 concord 가 의미를 나르는지 ② 303M 에서의 거동 ③ H_004 의
honorific 결과가 이 치환 하에서 재현되는지.

## 🔌 런타임 배선 CLOSED (2026-07-20 · 부모 세션)

착륙 시점엔 `core/decode.py` 가 TFLD 를 읽지 않아 `wired: no` 였다(학습·직렬화·감사만 배선).
이제 닫혔다 — 트레일러 사슬 말단(IFAN 다음)에서 `read_tfld` 로 읽고, `_fwd_trunk` 의 임베딩 직후
`tension_apply` 로 **trunk 이전**에 더한다. `core/model.py` 의 학습시 주입과 같은 자리·같은 식이라
`--tension-field` 로 학습한 ckpt 가 학습 때의 장 그대로 디코드된다. 장의 축약은 정수 버킷 연산이라
host-numpy 로 두고, 레인이 켜질 때만 임베딩이 1회 host 왕복한다 — 장 연산을 한 장치에 몰아
cuBLAS/CPU 누적순서 confound(`decode-py-4`, 2.5e-14)를 원천 차단하기 위함이며 레인-off 디코드는
이 비용을 전혀 내지 않는다.

**3-봉인 실측**(toy.clm d=32, `anima-py evaluate --gen 40`, 경로 줄 제외 sha 비교):

| 조건 | 기대 | 실측 |
|---|---|---|
| 트레일러 無 (변경 전 코드 vs 후) | 바이트 동일 | ✅ sha `9d2a6a79…` 동일 |
| 트레일러 有 · lam=0 | 통과(바이트 동일) | ✅ sha `c91604db…` 원본과 동일 |
| 트레일러 有 · lam=1 | 디코드 변함 | ✅ sha `1b4b797b…` (coherence 5/5→4/5 · fab 0.2308→0.2619) |

lam=1 팔의 하락은 **무작위 phi/W_up 을 붙인 합성 트레일러**여서 정상이다(학습된 장이 아님). 이
표가 증명하는 것은 배선이 실제로 발화하고 off 경로가 무손상이라는 것뿐 — 장의 효용은 여전히 미측정.

## 🔗 전체 사슬 스모크 (2026-07-20 · 부모 세션 · 토이)

배선을 닫은 직후, **학습 → 직렬화 → 디코드 → 측정**이 한 사슬로 이어진 적이 한 번도 없었다
(`instrument-never-run-hides-multiple-bugs`). 지출 전 전제조건으로 3 arm 을 완주시켰다.
`anima-py corpus flat --lang en`(798,570 B) · `train --d 64 --L 2 --steps 300 --seq-len 128
--batch-size 8 --seed 7` · `evaluate --gen 40`(경로 줄 제외 sha):

| arm | ckpt | TFLD 트레일러 | decode sha | kwr | fab |
|---|---|---|---|---|---|
| off | 117,502 B | 없음 | `8002162a` | 4/5 | 0.4286 |
| duel | 127,766 B | 10,264 B (arm=duel rank=32) | `26bab19e` | 2/5 | 0.5526 |
| rank1 | 127,766 B | 10,264 B (arm=rank1 rank=32) | `cb9f1382` | 2/5 | 0.5278 |

셋 다 rc=0, 세 sha 가 서로 다르다 ⟹ 사슬이 살아있고 **arm 이 디코드에 실제로 작용**한다
(off≠duel 은 레인 발화, duel≠rank1 은 arm 코드가 무시되지 않음을 각각 증명).

⚠️ **이 표는 F1 이 아니다.** kwr/fab 은 ρ 게이트지 이 카드의 DV(Δd_acc)가 아니며, 300 step ·
d=64 · 1 seed 는 판정 규모가 아니다. duel/rank1 이 off 보다 나쁜 것은 **토이서 장이 파라미터만
늘리고 학습이 안 됐다**는 읽기가 가장 단순하다 — 어느 쪽도 주장하지 않는다(측정 아님).

## ⛔ 303M 발사 BLOCKED — 비용이 아니라 계기 부재

사슬 스모크 직후 확인된 사실: **F1(Δd_acc ≥ 0.15)을 잴 계기가 프로덕션에 없다.** held-out 결합
패널 빌더도, d_acc 채점기도 이식되지 않았다(`--free-slot-score` 는 H_9808 의 codebook 감사지
패널 채점기가 아니다). 지금 303M 을 태우면 **아무도 채점할 수 없는 ckpt** 가 나온다 — v4 H_007 이
지출 뒤 부적격 판정을 받은 그 실패의 재현이고, `instrument-claim-alignment-before-reading-a-bar`
가 정확히 금지하는 순서다. ⟹ 선결 = 패널+채점기 이식(H_9810), 그 다음이 303M.

## 🚦 사전등록 게이트 실행 결과 (2026-07-20 · H_9808 로 자기 자신을 심사)

발사 순서를 내 의견이 아니라 코드로 정하기 위해, 계획중인 303M 실행을 방금 착륙한 H_9808
게이트에 그대로 걸었다.

**게이트 2 `--falsifier-headroom` (산술 축) — 🟢 PASS**
bar 0.15 · ceiling 1.0 · 요구 헤드룸 2×bar=0.30. 통제 0.6211/0.6198 ⟹ 최대 도달가능
Δ = 0.3789/0.3802 ≥ 0.30. (그 최대치가 v4 가 실제로 낸 Δ 와 일치 — v4 의 효과는 헤드룸을
거의 다 쓴 것.) 음성통제(우연 0.5) REACHABLE 이라 게이트가 산술 자체를 정죄하는 상태가 아님.

**게이트 1 `--trained-control-ceiling` (출처 축) — ⛔ REFUSE**

| 앵커 출처 | 판정 | 사유 |
|---|---|---|
| lab/v4 H_004 (panel=hon-bind, d=384 L=4) | ⛔ REFUSE | PANEL-MISMATCH + SCALE-MISMATCH(L 4→24, d 384→768) |
| 같은 수치를 이 패널·이 규모 실측이라 선언 | 🟢 PASS | — |

숫자는 동일하고 **출처만 다른데 판정이 갈린다** ⟹ 거부 근거는 값이 아니라 provenance(형식
오류를 모두 고친 뒤에도 동일 거부). 또한 게이트가 `--L` 미지정 자체를 먼저 거부했다(추측한
규모로는 인증 불가 · H_007 의 d=64 → d=384 부호역전 선례).

⟹ **발사 전 사전등록 목표가 확정됐다**: 이 패널·303M 규모에서 **control-alone 을 먼저 돌려
rank1 이 (0.5500, 0.7000] 안에 드는지** 확인해야 하고, 그 실측 앵커로만 3-arm 지출이 허가된다.
0.70 초과면 SATURATED(포화), 0.55 미만이면 DEAD(우연 대비 통제 아님) — 둘 다 지출 전 중단.

## 종결 조건

`anima-py train --tension-field {duel,rank1,off}` 3 arm × 2 seed 를 held-out 결합 패널에서 돌리고
`--tension-rank-audit` 로 F4/F6 를 읽어 위 표대로 판정. **303M engine-native 측정만이 TERMINAL 을
얻는다**; 토이는 몇 번을 돌려도 DIRECTIONAL 이다(`a_toy_scale_recheck`).

## Cross-links

- origin(rule-exempt · 인용만): `lab/v4/HYPOTHESES/cards/H_004_parser_duel_tension_rank_drill.md`
- readout-side 사망 계보: H_9356(스칼라 동어반복) · H_9714(rank≈2.66) · H_9576(8벡터→1비트)
- 인접 lane: H_9803(IFAN) · H_9698(MBND) · H_9423(CLMS)
