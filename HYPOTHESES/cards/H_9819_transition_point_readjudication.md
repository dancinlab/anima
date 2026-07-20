# H_9819 — 상전이점을 지표로 삼아 3600-step 음성들을 재심한다 (사전등록)

**status:** 🔒 PRE-REGISTERED (판정표 동결 · 실행 전 커밋) · **DIRECTIONAL-SCREEN 상한** (토이·torch)
**wired:** yes — 신규 코드 0줄. `anima-py train --steps N --tension-field … --tension-concord …`
· 채점 = `--serialize-parity` torch 2AFC 팔
**source:** [[H_9817]] GROKKING BREAK — 이 토이의 합성 학습은 **7200~14400 사이에서 상전이**하며,
[[H_9816]]·[[H_9814]]·[[H_9811]] 이 판정을 낸 3600 step 은 **그 아래**다.

## 왜 지표를 바꿔야 하는가 (설계상 강제된 변경)

재심의 자연스러운 형태는 "같은 팔을 상전이 위(≥28800)에서 다시 재기" 지만, 그 예산에서
**기준선(場 없음)이 이미 1.0000**([[H_9817]] seed 7)이라 **천장에 막혀 어떤 상승도 측정 불가**다.
같은 자를 그대로 쓰면 모든 팔이 1.0000 로 붙어 "차이 없음" 이 나오는데, 그건 **레버가 무력해서가
아니라 지표가 포화**해서다 — 그렇게 낸 음성은 3600 음성과 똑같은 종류의 판독 불가다.

⟹ **DV 를 바꾼다: 고정 예산의 d_acc → 우연을 탈출하는 step(전이점).**
천장이 사라지고, "場이 합성을 연다" 는 주장이 **"場이 전이를 앞당긴다"** 라는 측정 가능한 형태가
된다. 이 자는 이 계보의 **모든** 레버에 동일하게 적용된다([[H_9818]] 커리큘럼 포함).

## 개입 — step 사다리 × 팔 × seed

**고정 조건**([[H_9816]] 과 동일 · 한 변수만 다름): K=2 길이-매칭 xor 패널 · `--answer-ce-weight 0`
· `--trunk-norm global` · d=64 · L=6 · seq 96 · batch 8 · `--n-blocks 4000` · corpus seed 7.

- **사다리**: steps ∈ {3600, 7200, 10800, 14400, 21600, 28800}
- **팔**: `baseline`(場 없음) · `duel × morph`([[H_9816]] 의 최고 팔 0.5312) · `rank1 × morph`(**특이성 통제** — 場을 rank-1 요약으로 대체)
- **seed**: {7, 11} — [[H_9817]] 에서 크기가 seed-가변임이 실측됐으므로 단일 seed 금지

**전이점 정의(사전 고정)**: 사다리에서 **d_acc ≥ 0.75 를 처음 만족하는 step**. 끝까지 미달이면
`>28800`. (0.75 = 우연 0.5 에서 약 2.8σ, n=32·sd 0.0884 — [[H_9817]] 의 정정된 검정력 기준.)

## 🔒 판정표 (데이터 보기 전 동결 · DV = 전이점 step · 낮을수록 빠름)

**선결 무효 조건**: `baseline` 이 seed 2개 **모두**에서 사다리 안에 전이점을 갖지 못하면
⛔ **LADDER-TOO-SHORT** — 사다리가 현상을 못 담은 것이므로 **팔을 읽지 않는다**.

| 조건 (선결 통과 전제) | 판정 |
|---|---|
| `duel` 전이점이 `baseline` 보다 **2 칸 이상 빠름**(2/2 seed) ∧ `rank1` 은 그렇지 않음 | 🟢 **場-특이 가속** — 場이 합성을 앞당긴다, 그것도 場이라서. [[H_9816]] 🔴 뒤집힘 · 303M 이식 정당화 |
| `duel` 이 2 칸 이상 빠르나 `rank1` 도 동일하게 빠름 | 🟡 **비특이 가속** — 상승 실재하나 場-특이 아님(기존 스칼라 이음매로 충분) |
| `duel` 전이점이 `baseline` 과 **같거나 느림**(2/2 seed) | 🔴 **RE-ADJUDICATED NEGATIVE** — [[H_9816]] 의 🔴 가 **올바른 예산에서 재확인**됨. 이제야 구조적 주장으로 판독 가능해진다 |
| seed 2개가 서로 다른 칸을 가리킴 | 🟡 **seed-불일치** — 별도 사전등록 없이 연장 금지 |

**추가 스윕 금지**: 이 표 밖 하이퍼 불변. 결과가 무엇이든 **토이 스크린이며 verdict 가 아니다**.

## 이 H 가 동시에 고치는 방법론 결함

[[H_9816]] 의 배관 통제는 `hp × duel × class = 1.0000` 이었다. hp 는 **3600 에서도 학습되는 쉬운
과제**([[H_9815]])이므로 그 통제는 **파이프가 살아있음**은 증명했지만 **이 예산에서 xor 질문이
답해질 수 있음**은 증명하지 못했다. ⟹ **양성 통제는 측정 대상과 난이도가 맞아야 한다**
(convergence `positive-control-must-match-task-difficulty`). 이 사다리는 `baseline` 자신의
전이점을 선결 조건으로 두어 그 결함을 **구조적으로** 막는다.

## 재생성 커맨드 (seed 포함 · 재감사용)

```
anima-py corpus bindpanel --lang en --out bp.txt --bind-k 2 --n-blocks 4000 --seed 7 --bind-task xor
anima-py train --arch clm --corpus bp.txt --d 64 --L 6 --seq-len 96 --batch-size 8 \
  --answer-ce-weight 0 --trunk-norm global --steps <N> --seed <S> \
  [--tension-field {duel,rank1} --tension-concord morph] \
  --serialize-parity bp.txt.seen_panel.json --out <cell>.clm
```

## Cross-links

[[H_9817]] 상전이 실측(동기·DV 변경 근거) · [[H_9816]] 재심 대상 · [[H_9815]] hp 가 쉬운 과제임의 출처
· [[H_9818]] 같은 자를 쓰는 커리큘럼 H
