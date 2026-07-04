# H_9129 STEP-0 — 재조합=뇌 조합-substrate 3부품 (numpy toy, DIRECTIONAL)

## 프레임
재조합(G1)은 mouth/Broca 속성이 아니다 — PFC 변수-binding(role↔filler) → 기저핵 gate(어느 결합
선택) → 해마 pattern-completion(저장관계로 novel 완성) → mouth 는 조합-lane 을 READOUT(읽기만).
과제 = 2-hop 관계합성: 해마 M 은 triple(item⊛rel⊛next)만 저장(color⊛size 직접 저장 0).
R1: color→material, R2: material→size. reachable = color→mat→size 두 edge 를 CHAIN 해야 도달
(novel pair, 저장 안됨) = 재조합. unreachable = R1 은 있으나 material 에 R2 없음(dangling) —
표면형태 동일(color→2hop→size)이나 그래프에 완성경로 없음. decoy D1/D2 = gate 가 골라야 하는 딴 edge.

## 결과 (12 seeds, D=2048, chance=0.042)
| | reachable | unreachable |
|---|---|---|
| FULL | **0.972** | 0.049 (≈chance) |
gap = 0.924 → **fooled_by_form = FALSE** (form 이면 reachable≈unreachable 이어야 함)

### Ablation (부품 OFF → reachable)
| 부품 OFF | reachable | drop | verdict |
|---|---|---|---|
| bind OFF (role 미결합, c 단독) | 0.035 (≈chance) | 0.937 | **CAUSAL** |
| gate OFF (R1+D1+R2+D2 중첩) | 0.278 | 0.694 | **CAUSAL** |
| completion OFF (cleanup 제거) | 0.083 (≈chance) | 0.889 | **CAUSAL** |

3부품 전부 인과. bind/completion OFF 는 chance 로 붕괴, gate OFF 는 0.97→0.28 대붕괴(INERT 아님).

## D-sweep (0.36 은 메커니즘 천장 아님 = VSA crosstalk 용량 artifact)
| D | full_reach | full_unreach |
|---|---|---|
| 512 | 0.361 | 0.035 |
| 1024 | 0.701 | 0.056 |
| 2048 | 0.972 | 0.049 |
| 4096 | 1.000 | 0.062 |
용량↑ → reachable→1.000, unreachable 는 항상 chance 고정. 벽이 아니라 중첩 crosstalk.

## Verdict
**BIND** — reachable >> unreachable(gap 0.92) ∧ 3부품 모두 causal. 진짜 관계-조합 신호,
form-priming 아님.

## binding-family(H_1816/1823 mouth-readout NOT-SUP)와 구별 3근거
1. **별개 lane**: 조합은 PFC-bind/BG-gate/해마 M 의 별도 관계메모리에서 발생, mouth 아님.
2. **disjoint objective**: mouth 는 조합-lane 상태를 cleanup readout 만 — 재조합이 mouth-target 아님.
3. **mouth 읽기만**: completion OFF 시 mouth 는 같은 raw 벡터를 받아도 못 읽음 → 재조합은
   상류 3부품 산물이지 readout 학습이 아님. (H_1816/1823 은 재조합을 mouth-readout 에 훈련 = 브로카에
   관계추론 강요 → additive floor. 여기선 재조합을 관계-substrate 에 두고 mouth 는 명명만.)

## 정직 스코프
numpy toy = **DIRECTIONAL**(303M engine-native 아님). tune-to-green 없음(bar=gap>0.10 & drop>0.15
사전고정). 다음: 이 3부품 조합-lane 을 engine-native(clm303/ByteGPT) 옆 lane 으로 배선 후 재측정
(a_engine_native_learning). 특히 reachable/unreachable held-out 을 실 코퍼스 관계그래프로.
