# RESULTS — g1_coverage_bytes (2026-07-02, summer pool RTX5070, torch 2.11 DIRECTIONAL)

## 수치 (strict = pair-특이 " attrA attrB" 시작-일치, n=60 held / 60·40 seen)

| arch | arm | seen-true strict | held strict | held loose | 비고 |
|---|---|---|---|---|---|
| attn | HIGH 72% | **1.000** | **0.950** | 0.950 | |
| attn | LOW 7% | **1.000** | **0.033** | 0.067 | 템플릿 모양은 완벽, 속성 결합만 오답 |
| attn | SHUFFLE | 0.000 (true) | **0.000** | 0.000 | 자기(오답)타깃 암기 0.75 → 학습능력 有 |
| convd | HIGH 72% | 1.000 | **0.850** | 0.850 | dilation 1/2/4/8, RF≈61B (RF-벽 수리) |
| convd | LOW 7% | 1.000 | **0.000** | 0.000 | |
| convd | SHUFFLE | 0.000 (true) | **0.000** | 0.000 | 자기타깃 암기 0.93 |

## cheap-gate 3종 판정
- (a) seen-sanity: HIGH/LOW 전 arm strict 1.000 → harness 유효.
- (b) pair-특이성: LOW arm 이 완벽한 템플릿 모양(" X Y .")을 내면서 strict 0.03 → v2 함정 회피 실증.
  SHUFFLE seen-true 0.00 → 지표가 진짜 조합 정답만 잡음.
- (c) control: SHUFFLE held 0.000 (요구대로 실패) — 조합 규칙 파괴 시 커버리지·크기 동일해도 0.

## VERDICT: 🟢 LEVER (DIRECTIONAL)
조합-커버리지 밀도가 자연어 byte 에서도 pair-특이 재조합을 켠다:
held 0.95 vs 0.03 (attn), 0.85 vs 0.00 (conv-dilated) — **arch-무관 재현** (toy 상전이의 NL-byte 브리지).
conv 는 dilation 으로 RF-벽만 수리하면 동일 레버 작동 → RF-벽은 측정벽이지 과학벽 아님 재확인.

질적 관찰: LOW arm 은 부품(fact)·템플릿은 전부 학습했고 held 에서 슬롯당 한쪽 속성은 자주
맞히나(예: clock+mirror → "quiet misty") pair-특이 *바인딩*이 안 됨 — 커버리지가 가르치는 것은
템플릿이 아니라 **결합 연산의 일반화**라는 toy 해석과 일치.

## 정직 스코프
- torch 미러 = DIRECTIONAL (engine-native 아님, a_engine_native_learning). 3.3M/2.5M param toy→NL 브리지,
  단일 seed, 24개념 어휘. 303M trunk 로의 transfer 는 미검증 (a_toy_scale_recheck).
- 산출물: summer:~/g1full/ (corpus 3종·meta.json·bt.py·log 6·results 6) + 본 디렉토리 사본.
