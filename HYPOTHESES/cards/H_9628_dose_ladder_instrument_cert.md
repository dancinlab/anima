# H_9628 — 용량 사다리 계기 인증 — Dose-Ladder Instrument Cert: 채널 vs 판독기 vs z 3원 분리 (fable R4-1 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · H_9576 "경로 있음·의미 미전달" 벽 발산 · 사전등록) — source=fable R4-1
**lane:** mouth/tension — PC2→mouth 의미 전달
**related:** [[H_9576]] · [[H_9574]] · [[H_9629]] · [[H_9630]] · [[H_9631]]

## 한 줄 주장 (반증가능)
H_9576 의 방향 KILL(ρ=−0.077·null 안)은 **채널·판독기 D·z 세 실패를 미분리**한 판정이다 — z 를 실험자-알려진 용량으로 치환한 양성통제에서 ρ(dose, ΔD)가 크게 살아나면 실패는 z 로 국소화되고, 용량조차 null 이면 D=bigram-overlap 은 INSTRUMENT-DEAD 이며 H_9576 방향판정은 KILL 이 아니라 VOID 다.

## 어느 KILL 을 왜 안 밟나
가장 가까운 KILL = "byte 입도 context-presence bias 의 방향성"(H_9576). 이 안은 그 방향성(z=PC2)을 재주장하지 않는다 — **판정에 쓰인 계기(D 판독기 + bias 용량 스케일)가 참효과를 잡을 수 있는지**를 알려진-용량으로 먼저 인증한다(V2_1 C0-e ORACLE 선례의 mouth-lane 판). 음성 읽기 전 양성통제 규칙의 직접 적용.

## engine-native 계기
`anima-py evaluate <clm> --pc2-direction --dose {pc2|fixed:-2,-1,0,1,2|rng:<seed>|zero|shuffle}` (v0.15.20 파이프라인에 플래그 1개 — z 소스만 치환, bias 기전·D·Stage-A 격리 동일).

## 통제군 (≥2 + 양성)
- **양성통제**: `--dose fixed` 사다리 — 문맥-현존 byte 를 −2..+2 로 기계적으로 누르므로 D 가 살아있다면 ρ(dose,ΔD) 는 필연적으로 크고 양(+).
- null #1: `--dose zero` (byte-identical 재확인 · Stage-A 재인증).
- null #2: `--dose shuffle` (기록된 용량의 tick 순열 — 파이프라인 누수 검출).
- 재현 arm: `--dose pc2` (H_9576 원 조건).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| ρ_dose ≥ +0.5 (perm p<.01) ∧ ρ_pc2 ∈ null band | **INSTRUMENT-PASS · z-KILL 국소화** — 채널+판독기 무죄, 실패는 z (→ H_9630 개봉) |
| ρ_dose ≥ +0.5 ∧ ρ_pc2 부호+ null 밖 | **PASS-역전** — H_9576 은 n-인공물, 확대 재현 fire |
| ρ_dose ∈ null band | **VOID→INSTRUMENT-DEAD** — D 판독기 사망 · H_9576 방향판정 VOID 강등 · stage-2 판독 패널(bigram·ngram-novelty·entropy · Bonferroni 사전등록) 교체 후 재판정 |
| ρ_dose ≤ −0.5 (우연 아래) | **INVALID** — D 정의 or z 부호 관례 버그, 계기 수리 먼저 |

**검정력**: arm 당 n=270 (null95 반폭≈0.12) — 기계효과 ρ~0.5 대비 4σ. 3 arm ≈ 810 emit tick.

## 비용 / 죽는 방식
pool CPU (플래그 1개 + 303M decode 재사용). **죽는 방식**: fixed 사다리조차 null 이면 "bias 크기가 logit 스케일 대비 무시가능"(용량 보정 실패)이 관측으로 드러난다 — 그러면 H_9576 은 '의미 미전달'이 아니라 '용량 미달'로 재작성해야 한다.

## 상태
🔵 PROPOSED — **모든 후속(H_9630/9631/9632) 개봉의 hard-gate.** 측정 주장 0(설계).
