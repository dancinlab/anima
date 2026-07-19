# H_9810 — held-out binding PANEL + d_acc SCORER: H_9805 의 F1 에 계기를 달다

- **id**: H_9810
- **status**: 🔵 INSTRUMENT LANDED · toy e2e PASS · **과학 판정 없음** (303M 미발사)
- **series**: R11 (v4 salvage port · H_9805 의 계기 보완)
- **origin**: lab/v4 H_004 (panel + d_acc 정의) · lab/v4 H_008 + lab/v5 G3/G4 (free-slot 규율)
- **surfaces**: 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)
- **date**: 2026-07-20

## 왜 존재하는가 — F1 에 계기가 없었다

H_9805 는 `--tension-field {duel,rank1,off}` 학습과 `--tension-rank-audit` 를 착륙시켰지만,
사전등록 반증 **F1 = Δd_acc(duel − rank1) ≥ 0.15** 를 읽을 **패널도 채점기도 없었다**. 그 상태로
303M 을 태우면 **아무도 채점할 수 없는 ckpt 3개**가 남는다. 이 카드는 그 두 계기만 만든다.

- `anima-py corpus bindpanel` — held-out 결합 PANEL + 그 drill 코퍼스 + codebook + F2 liveness 면
- `anima-py evaluate <clm> --bind-panel <panel.json> [--vs <clm2>]` — arm 별 d_acc, **FIELD-BLIND
  천장 먼저**, `--vs` 가 F1 의 Δ 를 직접 계산

**이 카드는 장이 도움이 되는지에 대해 아무 주장도 하지 않는다.** 그건 미측정이다.

## 🔑 설계를 결정한 코드 사실 — 장은 공백 마스크만 본다

`core/tension_field.py` 를 읽으면 나오는 사실(추정 아님):

| 요소 | 무엇이 결정하는가 |
|---|---|
| `chunk_heads` (head_A · head_G) | 공백 바이트 위치 = **청크 경계** |
| `chi` = `byte_class(i)==byte_class(j)` | head j 는 항상 문자(class 2) ⟹ **i 가 공백인지 여부**만 |

⟹ **T 는 창의 WHITESPACE MASK 의 함수이며, 어떤 글자가 있는지에 대해 완전히 blind 하다.**
T 가 보는 것은 **단어 길이 수열**뿐이다.

이 사실의 귀결이 결정적이다: **답이 어휘 정체성에 걸린 패널에서는 production 장이 답에 대해
0 비트를 나르고, duel 과 rank1 은 답과 무관한 텐서를 각각 압축할 뿐이며, F1 은 원리적으로
측정 불가**(Δ≈0 이 나오지만 rank 와 아무 상관 없는 이유로). H_004 의 한국어 경어 패널을
그대로 번역했다면 정확히 이 함정에 빠졌을 것이다 — H_9805 가 concord χ 를 바이트클래스로
치환한 순간부터 언어학적 내용은 이미 이식되지 않았기 때문이다.

그래서 이 패널은 **의도적으로 길이-부호화**되어 있다:

```
동사   합치표지 "walks"  = 어간(4)+s   = 5 B      vs  분사 "walking" = 어간+ing = 7 B
명사   단수     "doctor"                = 6 B      vs  복수 "doctors"           = 7 B
```

두 결합 특징이 **청크 길이**로 실린다 = 장이 가진 유일한 채널. 이것은 편의가 아니라
**F1 을 측정 가능하게 만드는 최소 조건**이며, 동시에 이 패널의 scope 한계다(아래 정직한 한계).

## 패널 (`anima-py corpus bindpanel --lang en`)

EN-FIRST 지시 준수. H_004 의 XOR 구성을 경어 일치 → **수 일치(number concord)** 로 옮겼다.

```
conjunct_k = "{V-form} {N1} of {N2} and"        (K 개를 한 문장에 적층)
hp_k  = 동사에 합치표지 -s 가 있는가            pos_k = 단수 명사가 근접(N1) 위치인가
gold_k = hp_k XOR pos_k                          answer ∈ {up, dn}  (둘 다 2 B · 길이 패리티)
```

- **K 적층이 필수**: 단일 contested edge 는 장을 rank 1 로 붕괴시킨다(H_004 가 단일-bind 에서
  off-top 0.000 을 측정하고 F4-DEAD 선언). K 슬롯 = K 개 독립 contested edge.
- **codebook = 완전 2^K factorial** ⟹ GF(2) full rank, prefix-determined 열 0개.
  H_004 는 rank-4 K=6 codebook 을 썼고 teacher-forcing 이 parity 슬롯 2개를 공짜로 채워
  **필드-BLIND 천장 0.667** 이 held-out 까지 도달, 전 arm 이 균등 부풀려져 F1 이 해석불능이 됐다.
  그 결함은 이 codebook 에서 **구조적으로 불가능**하고, 가정하지 않고 **검증**한다:
  `anima-py evaluate --free-slot-score <codebook.json>` (H_9808 재사용 · GF(2) rank 재구현 안 함).
- **휴리스틱 감사 = 정확히 0.500000** (근사 아님): presence · position · locality · verb_lexeme ·
  verb_form · n1_lexeme · n2_lexeme · slot balance 전부. 슬롯쌍 독립도 정확히 0.

### 빌드 게이트가 실제로 잡은 결함 1건 (설계 초안의 conjunction leak)

초안은 어휘를 `(hp-블록, 슬롯)`으로 배정했다. hp 는 블록 안에서 상수이므로 **어휘가 hp 를
식별**하고, 명사의 단/복수 형태가 pos 를 주므로 **N1 단어형에 대한 단순 lookup 테이블이 모든
슬롯을 풀었다** — `n1_lexeme = 1.000`. 그런데 `presence` 와 `position` 은 각각 **결백한 0.5**
를 유지했다. 단항 지표 2개만 봤으면 못 봤을 conjunction 누수이고, 빌드 게이트가 exit 2 로
거부했다. 교정: 어휘 배정에서 블록을 제거(슬롯+rotation 만) ⟹ 모든 어휘군이 4 hp 블록과
2^K gold 패턴을 모두 걸쳐 정확히 50/50.

### 산출물

| 파일 | 무엇 |
|---|---|
| `<out>` | DRILL 코퍼스 (SEEN 어휘 · 8 rotation 전수 ⟹ seen 동사 8 · 명사 8 전부 노출) |
| `<out>.panel.json` | **held-out** 판정 패널 (schema `anima-bindpanel/v1`) |
| `<out>.seen_panel.json` | **F2 liveness** 면 — DRILLED 어휘 (일반화 주장 아님) |
| `<out>.codebook.json` | `--free-slot-score` 입력 |
| `<out>.meta.json` | regen_cmd + "이건 from-scratch drill 이지 CPT 믹스가 아니다" 경고 |

0-SHOT 은 **단어경계 분할**로 검사(부분문자열 금지 · `corpus-py-1 (G)`), 위반 시 exit 2.

## 채점기 (`anima-py evaluate <clm> --bind-panel`)

한 ckpt 에서 **같은 trunk 가중치**로 3 arm:

| arm | 무엇 | 왜 |
|---|---|---|
| `as-trained` | TFLD 트레일러 그대로 | 처치 |
| **`field-blind`** | 트레일러 제거(pre-trunk 잔차 ≡ 0) | **천장 통제 — 제일 먼저 읽는다** |
| `field-rank1` | 같은 가중치, arm_code 를 rank1 로 강제 | ckpt-내 rank 진단 (F1 아님) |

`--vs <clm2>` = **F1 그 자체**: Δd_acc(ckpt1 − ckpt2).

d_acc = **자유 슬롯**에서의 teacher-forced 2AFC (앞선 슬롯은 참값으로 강제 ⟹ 슬롯 k 는 모델
자신의 앞선 오류가 아니라 자기 자신으로 채점). free-slot 집합은 **이 패널의 codebook 에서
재계산**하며 절대 상속하지 않는다(v5 G3). chance 는 실현된 분할에서 재유도.

### 계기가 스스로 검사하는 것 (전부 e2e 에서 발화 확인)

1. **ORACLE preflight** — gold 가 구조 필드(hp,pos)에서 재구성되는가 · 두 답 토큰 바이트길이
   동일한가 · 최대 채점 시퀀스가 `--win` 에 들어가는가(짧으면 우측정렬 창이 앞 conjunct 를
   조용히 잘라 **다른 질문**을 채점한다) ⟹ 위반 시 INSTRUMENT-DEAD, 숫자 읽기 금지.
2. **FREE-SLOT 재계산 + 천장** — determined 슬롯이 하나라도 있으면 INSTRUMENT-DEAD.
3. **CEILING 경고** — field-blind 위 여유가 F1 bar(0.15)의 2배 미만이면 **F1 INADMISSIBLE**
   을 크게 찍는다(v4 H_007 의 실패 양식 · 303M 전에 $0 로 잡는다).
4. **ARM SEPARATION** — 통제 arm 의 per-item 벡터가 처치와 **동일**하면 Δ 는 측정이 아니라
   배관 null 이다. 원인 2가지(레인 미발화 / readout 포화)를 `top_ans` 로 가른다.
5. **DEGENERATE READOUT** — 한 답 토큰을 ≥75% 방출하면 그 d_acc 는 패널의 gold 균형을 되비친
   것이지 판독이 아니다. 어떤 처치 효과도 표현 불가.
6. 동점은 0.5 로 세고 **카운트해서 출력**(조용히 gold 쪽으로 반올림 금지).

## 토이 e2e 실측 ($0 · CPU · 격리 venv 비편집 설치 · **과학 주장 아님**)

```
빌드   anima-py corpus bindpanel --out bp.txt --lang en --bind-k 6 --n-blocks 4000 --seed 7
       K=6 panel=256 items drill=4000 lines bytes=788030
       휴리스틱 감사 전 항목 0.5 정확 · 슬롯쌍 최악편차 0.0 · 0-SHOT 누수 0
게이트 anima-py evaluate --free-slot-score bp.txt.codebook.json --pregate-bar 0.15
       free=[0,1,2,3,4,5] · GF(2) rank=6 · prefix-determined 없음 · GF(2)-dependent 없음
       FIELD-BLIND ceiling 0.5000 = chance 0.5000  → 🟢 GATE PASS
학습   anima-py train --corpus bp.txt --tension-field {duel,rank1} --d 64 --L 2 --steps 3000
       --seq-len 256 --batch-size 8 --seed 7      (rc=0 · TFLD 10264 B · clm_decodable=True)
```

**held-out 패널** (`--vs` = F1 경로, n=48 items × 6 free slot):

```
ckpt         arm            d_acc      sd   top_ans  margin_sd
t_duel       as-trained    0.5139  0.1979    0.9306     0.2576
t_duel       field-blind   0.5347  0.1983    0.9097     0.2480   ← CEILING
t_duel       field-rank1   0.5139  0.1979    0.7639     0.2325
t_rank1      as-trained    0.5278  0.1993    0.7083     0.1595
t_rank1      field-blind   0.5312  0.1944    0.5243     0.1910
[chance] 0.5000 (실현 분할서 유도)
[CEILING] field-blind 0.5347 · 여유 0.4653 → ✅ 헤드룸축 F1 ADMISSIBLE
[F1] Δd_acc(t_duel − t_rank1) = -0.0139
```

**F2 liveness (DRILLED 어휘)** — 이게 이 e2e 의 진짜 결과다:

```
t_duel  as-trained 0.5139 · field-blind 0.5139 · field-rank1 0.5139   (전부 동일)
⚠️ DEGENERATE READOUT — 한 답 토큰 93.1% 방출
⛔ ARM SEPARATION FAILED — field-blind per-item 벡터가 as-trained 와 동일
```

### 이 토이가 말해주는 것 (숨기지 않고 기록)

**위 F1 −0.0139 는 판정이 아니라 계기 시연이다. 그 토이 arm 은 F2 를 통과 못 한다.**
val_CE 0.070 까지 내려간 3000-step 토이가 drilled 셀에서 **정확히 chance** 이고 답 토큰을
93% 한쪽으로 방출한다 = **상수 예측기**. 원인은 v4 가 이미 실측하고 A1 수정으로 대응한 그것:
**답 바이트 12 B 가 시퀀스 ~190 B 의 6%** 라 평범한 next-byte CE 는 표면을 최적화하고 결합
비트를 chance 에 방치한다(H_004 A1: drill d_acc 0.83/0.64 → 두-항 목적함수 `ce_surf + 5·ce_ans`
로 1.0/1.0). **production `anima-py train` 에는 그 답-가중 항이 없다.**

**"덜 학습해서" 가설은 실측으로 배제했다** (예산·용량 통제 · `power-before-negative-verdict`
의 반대 방향 — 음성을 읽기 전에 그 음성이 예산 탓인지부터 봤다):

```
arm                              params    steps   val_CE    F2 d_acc   top_ans
d=64  L=2   3000 step            (기준)     3000    0.0703    0.5139     0.9306
d=128 L=4  20000 step         5.9× 파라미터  6.7×    0.0544    0.5556     1.0000  ← 더 나빠짐
```

**6.7배 학습하고 5.9배 키우니 readout 이 더 축퇴했다**(93.1% → **100.0%** 단일 토큰).
CE 는 계속 내려가는데 결합 비트는 chance 에 남는다 — 예산 부족이 아니라 **목적함수가 답
바이트를 보지 않는 것**이다. ⟹ **다음에 필요한 것은 더 큰 spend 가 아니라 목적함수 항이다.**
이 사실을 $0 에 알아낸 것이 이 카드가 303M 앞에서 하는 일의 전부다.

## 정직한 한계 (scope · 이게 제일 중요하다)

1. **패널은 길이-부호화 결합이지 어휘-의미 결합이 아니다.** production 장이 공백 마스크만
   보기 때문에 그렇게 만들 수밖에 없었다. 여기서 나올 어떤 positive 도 "장이 청크-길이 골격을
   자기 rank-1 요약보다 잘 나른다"는 주장이지 "언어적 결합"이 아니다.
2. **장은 표면의 결정론적 함수다** — T = f(bytes). 정보이론적으로 장이 표면 위에 더하는
   비트는 **0**. 이 lane 이 물을 수 있는 것은 정보가 아니라 **접근성(accessibility)** 뿐이고,
   그건 field-blind 천장이 chance 근처에 있을 때만 읽을 수 있다.
3. **held-out 축은 LEXEME 이다.** 길이 골격은 seen/held 가 공유하므로 이 패널은 어휘 암기를
   막을 뿐 길이-일반화를 시험하지 않는다. 다른 축의 일반화로 읽으면 `corpus-py-1 (F)` 위반.
4. **토이는 몇 번을 돌려도 DIRECTIONAL**(`a_toy_scale_recheck`). 303M 만이 TERMINAL 자격.
5. 이 카드는 어떤 F 도 판정하지 않는다. F1/F2/F3/F4/F5/F7 은 여전히 H_9805 소관이다.

## 재생성 (seed 포함 · corpus-py-1 (J))

```
anima-py corpus bindpanel --out bp.txt --lang en --bind-k 6 --n-blocks 4000 --seed 7
anima-py evaluate --free-slot-score bp.txt.codebook.json --pregate-bar 0.15
anima-py train    --corpus bp.txt --tension-field duel  --d 64 --L 2 --steps 3000 \
                  --seq-len 256 --batch-size 8 --seed 7 --out t_duel.clm
anima-py evaluate t_duel.clm --bind-panel bp.txt.seen_panel.json          # F2 먼저
anima-py evaluate t_duel.clm --bind-panel bp.txt.panel.json --vs t_rank1.clm --out f1.json
```

## Cross-links

- 계기가 채우는 반증표: `HYPOTHESES/cards/H_9805_write_side_tension_field_rank_escape.md`
- 재사용한 $0 심판: `HYPOTHESES/cards/H_9808_pregistration_gates_refuse_before_spend.md`
  (`core/pregates.py::free_slot_audit` — GF(2) rank 재구현하지 않았다)
- origin(rule-exempt · 인용만): `lab/v4` H_004(panel+d_acc+A1/A2 수정) · H_008(free-slot 규율)
