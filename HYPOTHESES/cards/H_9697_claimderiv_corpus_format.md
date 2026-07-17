# H_9697 — R5 claim-derivation 코퍼스 포맷 + 대조 목적함수 (derivtrace 의 G6 유사체)

**status:** 🔵 PRE-REG (lab full · Fable A3 · 데이터축) · not-terminal · 선행 [[H_9693]]
**lane:** G6/ρ·fan · 데이터 포맷축 **related:** [[H_9124]] (DERIV G1 선례) · [[H_9693]]

## 물음

ρ·weave 최초 엔진네이티브 리프트는 objective 도 readout 도 아니고 **데이터 포맷**이었다([[H_9124]] DEF/RULE/OUT — echo=composition 으로 메타법칙 자체 우회). G6 유사체: **"premise-A + premise-B → 정량비교 주장"의 유도 포맷** — OUT 의 내용어가 **두 전제의 함수**가 되도록 생성. `--objective composed_nce`/`constructive_bind` 로 학습하면 **negative 예가 곧 SHUF 쌍** ⟹ 통제군을 목적함수가 내면화 → FORM-only 해로는 loss 를 못 내림(**구조적 #6 회피**).

## 조작

`anima-py corpus claimderiv --out c.txt --lang en --arm {deriv,flat,shuf}` → `anima-py train --objective composed_nce …` → `--fan-bind`.

## 게이트
[[H_9694]] 골격(bind Δ vs SHUF-trained·permutation null·G0 게이트) + **flat 팔**(동일내용 비유도 포맷 — 포맷효과 격리 · [[H_9124]] 2-arm 패턴).

## ⚠️ 발사 전 필수 (Fable)
`check-ledger-before-lever-fire`: **H_1640 arm×objective 매트릭스가 G6 표면으로 이미 스윕·판정됐는지 발사 전 ledger 조회** — G1 표면으로만 측정됐다면 미탐. composed_nce/constructive_bind 가 G6 로 안 돌았으면 NOVEL.

## kill-list 회피
#6 = SHUF 를 loss 의 negative 로 내장 + 판정 bind Δ. #8 = FORM 아니라 전제→주장 함수성(BIND)을 데이터가 강제.

## 최대위험
유도 포맷이 방출표면에 "if…then" 골격을 심어 **frame-echo 로 bind Δ 계기 오염**(계기의 mismatched-pairing null 이 잡아야 함 · [[H_9693]]). + CPT 가 코퍼스 밖 능력 죽이는 전례.

## falsify
🟢 deriv bind Δ > flat ∧ > shuf ∧ null 95% 밖. | 🧱 deriv==flat = 포맷 무효. | ⚠️ ledger 서 이미 판정됐으면 중복(등록취소).

## source
lab full Fable A3 · 선행 [[H_9693]].
