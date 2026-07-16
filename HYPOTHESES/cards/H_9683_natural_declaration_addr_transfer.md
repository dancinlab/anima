---
id: H_9683
title: NAT-ADDR — does the addr-loss lever transfer from synthetic nonce to NATURAL declarations?
tier: PROPOSED (R7 · 두 lane 접합 · H_9672 T3 가 스스로 남긴 칸 · DIRECTIONAL design)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9683 (R7) — 자연선언 주소전이

**Origin.** 병렬 세션 [[H_9672]] T3(#3895 · 🟢 303M CRACK-DIRECTIONAL)를
`a_parallel_session_compare` 로 대조하다 나온 접합점. **그 카드가 명시적으로 남긴 칸**:

> "**G1 자연선언 전이는 별도 H**" · scope = **감독-주소 co-train tier(창발-주소 아님)"

**Claim (one line).** `--store-addr-weight`(L_addr = CE(att, target_slot))가 **합성 CVCVC
nonce** 에서 303M 주소벽을 뚫었다(P1-balanced **0.9688** · addr-gap 0.008). 같은 레버가
**자연 teacher 선언**에도 전이되는가 — 아니면 성공이 합성 원자의 **깨끗한 키 분리**에 기생하는가?

## 왜 이게 두 lane 의 접합인가
| lane | 상태 |
|---|---|
| **A · 주소 (H_9672)** | 🟢 합성 nonce·감독-주소서 **벽 돌파 증명**(engine-native 303M) |
| **B · 자연/외생 내용 (R-series)** | 🧱 "주입·공학습은 되는데 **자연 내용은 안 된다**"(H_9267 XBIND 1.000 vs H_9304 자연 TOST 0) |

H_9672 는 **A 를 풀었고 B 를 명시적으로 열어뒀다**. 이 H 가 그 다리.
D0-1 census 가 이미 예고: `_entity_key`(byte-bag) 는 **위치맹** ⟹ anagram 충돌
`[demar, merad]` 키 L2=0.0000. **자연 어휘는 합성 nonce 보다 키 충돌이 훨씬 심하다**
(형태론·굴절·부분어 공유) ⟹ **전이 실패의 사전 예측 기전이 이미 장부에 있다.**

## Minimal decisive experiment (레버 = 이미 배선됨 · origin/main)
자연 선언 원자로 storebind 코퍼스를 만들고 **동일 T3 레시피**를 돌린다:
```bash
anima-py corpus storebind --lang en --atoms natural_decl_atoms.json \
  --balanced-manifest --seen-manifest --out nat_addr_s${S}.txt
anima-py train --init py303_full.clm --corpus nat_addr_s${S}.txt \
  --store-addr-weight 1.0 --store-addr-audit --canon --seed ${S}
anima-py evaluate NAT_s${S}.clm --xbind nat_balanced.json
```
H_9672 의 **사전등록 판정표를 그대로 상속**(재발명 금지): C0-e ORACLE ≥.90(미달=INSTRUMENT-DEAD·P1 미판독) ·
**P1-balanced ≥.75 = CRACK** · [.60,.75) PARTIAL · (.40,.60) KILL-잔존 · addr-gap ≤.20 ·
4-cell 각 ≥.65 · flip-coh ≥.90 · shuffle at balance-floor.

## Frozen falsifier (사전등록 · 제3결과 포함)
- **P1-balanced ≥ .75** ⟹ 레버가 자연선언으로 **전이** = A·B 한 뿌리 + escape 획득.
- **(.40,.60)** ∧ 합성 arm 이 **같은 fire 에서 .95+ 재현**(양성통제 · 필수 동반 팔) ⟹
  **전이 실패가 자연 어휘에 국한** = "합성 원자의 키 분리에 기생" 확정.
- **addr_top1(held) 은 높은데 P1 낮음** ⟹ 주소는 섰으나 **값읽기가 자연 다의성에 익사** = 제3결과.
- **키 충돌 사전-census 가 bar 를 무효화**: D0-1 방식으로 자연 원자 self-nearest 를 먼저 재고,
  충돌 원자를 **유효 n 에서 제외**한 뒤 채점([[H_9672]] D0-1 선례 — 안 하면 BY-CONSTRUCTION 주소불능이 레버 탓으로 오독).

## Controls (≥2)
① **합성 nonce arm 동시 재현**(양성통제 · [[positive-control-before-reading-a-negative]] — 없으면 자연-null 은 INSTRUMENT-DEAD)
② `--store-addr-weight 0` OFF arm(byte-identical 확인 · 벽 재현)
③ shuffle/balance-floor ④ anagram-충돌 제외 vs 미제외 두 채점면.

## ⚠️ 선행조건 — [[H_9678]] PRECONDITION-FAIL 이 여기에도 걸린다
현 study transcript 는 **entity–value 원자가 0개**(`Perhaps…` 23/30 · 숫자 0 · TTR 0.302)
⟹ **자연 선언 원자를 실제 teacher 에게서 얻으려면 사실-선언형 study run 이 선행**.
다만 이 H 는 **teacher 없이도** 실행 가능 — 자연 EN 어휘 선언 원자를 코퍼스로 직접 합성하면
"자연 어휘 × 감독주소" 를 teacher 비용 0 으로 격리한다(**권장 1단**: 자연어휘 전이가 죽으면
사실-선언형 study run 을 태울 이유 자체가 사라진다).

## Cost · kill-list
1단(자연어휘 원자 · teacher 없음) = **pool~GPU(오너 go)** · 레버·판정표·계기 전부 **기존**
(신규 코드 0). Kill-list: **저촉 없음** — H_9672 재발명이 아니라 **그 카드가 스스로 별도 H 로
남긴 전이 질문**이고, "자연 코퍼스 XOR rescue"(H_9304/9316 CLASS-CLOSED)도 아니다
(가법단서를 자연 문장에서 **찾는** 게 아니라, 주소를 **감독으로 선불**하고 자연 **어휘**만 남긴다).
⚠️ 자기표시: P1 이 shortcut 대역(0.637 근처)이면 [[H_9672]] 의 3중 봉쇄(balanced 1차채점 +
random shuffle-Δ + addr audit)를 그대로 적용 — 그거 없이 읽으면 다수-극성 shortcut 오독.
