# H_9814 — 비인과 GN 버스를 닫으면 결합이 학습되는가 (per-position norm 대조 · 사전등록)

**status:** 🔒 PRE-REGISTERED (판정표 동결 · 실행 전 커밋) · **DIRECTIONAL-SCREEN 상한**
**wired:** yes(계기) — `anima-py train --trunk-norm {global,position}` · 채점은
`--serialize-parity` 의 torch 팔 (⚠️ `.clm` 디코드는 GLOBAL 의미론이라 position ckpt 의
engine-native 채점은 디코드 레인이 서기 전까지 의미상 오류 — torch 수치는 영구 SCREEN)
**source:** [[H_9813]] — forward 비인과 0.5964 nat 실측. 남은 물음: 그 채널을 **닫으면**
결합(gold = hp XOR pos)이 학습되는가, 아니면 벽은 딴 데 있는가.

## 개입 — 한 변수

`PerPositionGroupNorm` (core/model.py): 같은 affine 파라미터·같은 state_dict 배치, 정규화
통계만 **위치별**로 계산 ⟹ 미래 바이트가 과거 위치로 흐를 채널이 **구성적으로 없음**.

**고정 조건**: K=2 길이-매칭 패널(누수 0 인증) · `--answer-ce-weight 0` (오염 항 미사용) ·
d=64 · L=6(RF 127B≥74B) · 3600 step · seq 96 · batch 8 · seed 7. **한 변수 = `--trunk-norm`.**

## 🔒 판정표 (데이터 보기 전 동결)

**기전 검사 (선행)**: position 팔의 GN 누출 Δ ≤ **0.05** nat 여야 한다(global 팔 실측 0.5964).
미달이면 스왑이 채널을 못 닫은 것 = ⛔ INSTRUMENT-INVALID, 아래 행 판독 금지.

**스크린 DV** = seen 패널 torch 2AFC d_acc (parity 팔 · 우연 0.5):

| 관측 (position 팔) | 판정 |
|---|---|
| d_acc ≥ **0.65** | 🟢 SCREEN-POSITIVE — 비인과 채널이 결합 학습을 막고/굶기고 있었다. 디코드 레인 구축이 정당화됨 |
| d_acc < **0.55** ∧ 기전 검사 통과 | 🔴 SCREEN-NEGATIVE — 채널을 닫아도 안 배운다. 벽은 다른 곳(구조/데이터) |
| 0.55 ≤ d_acc < 0.65 | 🟡 부분신호 — 별도 사전등록 없이 연장 금지 |

global 팔(같은 예산)은 대조군: 기대 ≈ 0.53 ([[H_9813]] 실측).

**추가 스윕 금지**: 이 표 밖의 하이퍼는 건드리지 않는다. 스크린이 무엇이든 **판정(verdict)이
아니다** — 🟢 여도 engine-native 는 디코드 레인 + `anima-py evaluate` 를 거쳐야 한다.

## 실행 결과

(사전등록 커밋 후 기입)

## Cross-links

[[H_9813]] 비인과 실측(이 카드의 동기) · [[H_9810]] 패널 · [[H_9811]] 오염 항 계보
