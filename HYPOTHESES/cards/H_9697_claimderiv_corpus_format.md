# H_9697 — R5 claim-derivation 코퍼스 포맷 + 대조 목적함수 (derivtrace 의 G6 유사체)

**status:** ⚫ LEDGER-WITHDRAWN (발사 전 필수 게이트가 두 기둥 다 이미-음성으로 판정 · $0 kill · 2026-07-17) · 선행 [[H_9693]]
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

## 🔒 발사 전 ledger 조회 결과 — 등록취소 (2026-07-17 · $0 · GPU 미소비)

카드의 `⚠️ 발사 전 필수` 게이트(`check-ledger-before-lever-fire`)를 실행 → **두 기둥이 모두 이미 음성**:

**① objective 축 (`composed_nce`/`constructive_bind`) = G6-KILLED 중복.**
- **H_1602**: objective 3변종 {ce_marginal·infonce·contrastive_equilibrium} × 3seed → **9/9 전부 G1 composed_distinct=0 · closure 0/9**. `composed_nce` = contrastive-objective 족과 동형.
- **H_1640** (arm×objective 매트릭스 · 이 카드가 지목한 대조군): **G6 fals=0** 로 측정 완료.
- **H_9131**: "G1 재조합 = G6 반증 = 하나의 **trunk-objective 벽** 수렴(H_9129) · 레버는 readout 아닌 target(비교환 상호작용항)". objective 축은 G6 로 이미 스윕·판정됨.

**② 데이터포맷 축 (`claimderiv`, [[H_9124]] DERIV 의 G6 유사체) = G1 근거 붕괴.**
- **H_9124 레버1 derivation-trace**: 최초 G1 lift(bd=2>ms=1) 처럼 보였으나 **+robustness 반증(leave-one-pair-out 4쌍 {0,1}{0,4}{1,3}{2,3} 전부 g1_pass=FALSE·flat 보다 낮음)** ⟹ 원 단일쌍은 **threshold artifact**, "derivation-trace G1 robust lift 실패". G6 유사체는 미측정이나 그것을 동기화한 **G1 선례 자체가 무너졌다**.

⟹ 카드 falsify 절 `⚠️ ledger 서 이미 판정됐으면 중복(등록취소)` 발동. objective 축 G6-dead + 포맷축 G1-근거-붕괴 = R5 는 두 기둥 다 이미-음성 위에 서 있어 **발사가 GPU 낭비**. 게이트가 정확히 그걸 막았다(이게 결과 · `power-before-negative-verdict` 상 음성이 아니라 **선행연구 중복**이라 TOST 불요).

**남은 미탐(등록취소 후 잔여)**: 데이터포맷 G6 유사체를 **H_9124 가 무너진 그 robustness 축(leave-one-pair-out)까지 통과**하도록 재설계하면 별개 각도 — 단 그건 R5 원안이 아니라 새 카드여야 한다.

## source
lab full Fable A3 · 선행 [[H_9693]].
