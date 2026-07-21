# H_9831 — 꿈이 **선언규칙 위에서만** 재조합하면 비가법 정보를 제조하는가 (R11-2)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님)
**source:** fable `DREAM-XBIND` ∩ sol `prediction-error-tagged dream replay` — 두 모델 교집합.
**wired:** no — 미구현.

## Question

G1 의 한 얼굴은 **데이터 벽**이다(H_9304: 비가법 정보 +0.0023 nats = TOST 0 등가). 그런데 이 면은
이미 균열이 났다 — H_9267 합성 XBIND corpus 가 held-out D-acc 1.000, H_9287 이 "재조합 대수는
물리 정보를 **더한다**" 를 측정. 즉 **맞는 데이터 클래스가 있으면 뚫린다**. 수면/꿈 단계는 그
데이터 클래스를 엔진이 스스로 만드는 생성기가 될 수 있고, 깨어있을 때와 같은 기질을 쓰므로
p8-정합이다.

**단, 현재 dream 노드는 `text=""` 인 기하 중점**(sol 이 `core/dream_compose.py` 로 확인)이라
스스로 비가법 타깃을 만들지 못한다. 그래서 가설은 "꿈이 통찰을 만든다"가 **아니라**:
꿈 생성을 **store 주소 위의 대수적 재조합 / 선언된 `CompositionRule` 파생**으로 **구속**했을 때만
레버가 산다.

## Intervention (flag 형태 · 미구현)

```
anima-py train --dream-mix 0.10 --dream-source {store,free,shuffled} \
               --brain-loop dream-replay --brain-dream-policy {error,uniform,priority-shuffle} \
               --brain-runtime required --lang en
```

workspace 가 실패한 rule-bearing episode 만 anchor 로 태그해 REM/N3 에서 co-replay.
타깃은 기하 중점이 아니라 **선언된 규칙이 만든 파생**.

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | `--dream-source store` + `--brain-dream-policy error` | ρ·weave collapse-Δ |
| **free** | 자유 샘플링 꿈 | **사전등록된 실패 팔**. free 와 동률이면 프로그램 전체가 "데이터 증강이었다"로 붕괴 |
| **shuffled** | 토큰 셔플 꿈 — 주변분포 동일, 합성 없음 | 붕괴해야 함 |
| **uniform** | 균등 replay | 핵심 인과 비교. 못 이기면 "뇌 수면"은 장식 |
| **priority-shuffle** | 우선순위만 치환 | 이득 소멸해야 함 |
| **크기-맞춘 실제 corpus** | 계산·바이트 맞춘 추가 실데이터 | "재조합 구조" vs "데이터가 늘었다" 분리 |

## kill-list 비중복

kill #10(소코퍼스 CPT 가 코퍼스에 없는 능력을 죽임)은 **전량 CPT** 를 죽인 것 — 여기는 **혼합비**이며
broad interleave + G0/validation 가드로 차단한다. kill #3 은 **목적함수**를 죽였고 여기는 **데이터**다.

## $0 스크리너

H_9815 토이 store 에서 토이 dream-mix 생성. 3 seed·동일 4kB·동일 업데이트 수에서
error replay 가 uniform 대비 **xor AUC ≥0.15 상승 또는 0.80 도달 스텝 ≥20% 감소**.
priority shuffle / parent permute 에서 이득 소멸. hp 또는 broad validation CE 회귀 시 kill.

## 판독가능성

- 토이 sample-efficiency DV = **오늘 (b)**.
- 실제 G1 주장 = **(a) H_9827 수리 선행**. G6 주장까지 걸면 H_9828/H_9829 수리도 선행.

## 자기반론

모델은 **갖고 있지 않은 비트를 꿈꿀 수 없다** — H_9304 는 비가법 정보를 애초에 흡수 못 했다고
말하고, 자기생성 데이터는 자기 주변분포 증류 = 새 비트 0 인 닫힌 루프다. 레버를 살리는 반론은
하나뿐: 재조합은 **세계에 대한 새 비트**가 아니라 이미 학습된 원자들의 **새 공기(共起)** 만
필요하고, 그것이 정확히 H_9287 이 물리적으로 유익하다고 측정한 것이다. 따라서 이 레버는
**꿈 생성이 store 주소 위 대수적 재조합으로 구속될 때만** 생존한다.

**related:** H_9304 · H_9267 · H_9287 · H_9830 · H_9832 · H_9827
