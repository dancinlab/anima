# H_9856 — G6 재발사: 추상 register 확장 + 교정된 FORGET 게이트 (사전등록 · 발사 전 동결)

**status:** 🔒 PRE-REGISTERED (판정표·선결조건 **발사 전** 동결) · 코퍼스 검증 완료
**wired:** yes — `anima-py corpus falsidrill [--falsi-ablate]` (담체 12 · 2-register 어휘 · #4284 착륙)
**source:** [[H_9837]] REAL 팔 실측 2건 — ① 밀도 전이 8.2% ② `ρ·form` 통제 붕괴

## 실측이 지목한 두 병목 (추측 아님)

**① 형식이 주제를 못 건넜다.** [[H_9837]]: 코퍼스 밀도 **0.197 → 모델 0.0162 = 8.2%** 만 전이.
드릴은 `rainfall·salt·voltage`(물리량)인데 평가 프롬프트는 `consciousness arises from cells: `
(추상·정신). **한 번도 보여준 적 없는 register 간극을 건너라고 요구**한 셈이다.
→ 교정: 어휘의 절반을 **정신·추상**(attention·belief·thought·insight·judgement…)으로.
평가 개념 **내용어는 여전히 전부 held out** — 일반화 축은 그대로 두고 register 간극만 닫는다.

**② 경직 담체가 모델을 망가뜨렸다.** `ρ·form` 통제 `self-shuffle 0.0 → 0.4`.
→ 교정은 [[H_9855]] 에서 착륙(담체 3 → 12 · 어순 2방향 · 길이 가변).

## 🔒 교정된 선결 무효조건 (BLOCKING · **값이 아니라 축과 통제로** 건다)

[[H_9837]] 의 무효 원인을 그대로 고친다. convergence
`forget-gate-must-read-the-axis-verdict-not-the-reinforced-value`:

1. `HILLOCK` = **LIVE**
2. **`ρ·form` 축 판정 == PASS** — val 이 아니라 **축**(통제 포함). val 은 드릴이 강화하는 지층이라
   항상 통과하므로 게이트로 쓰면 위조다.
3. `ρ·form` 통제 **`self-shuffle ≤ 0.05`**(그 축의 동결 상한) — 지난번 죽은 바로 그 지층
4. `dist ≥ 5` (TEMPLATE-COLLAPSE 차단)

하나라도 어기면 ⛔ **INVALID** — 팔을 **읽지 않는다**(글자대로 통과 = tune-to-green).

## 🔒 판정표 (동결 · 발사 전 · BASE = fals-rate 0.004149 · sd 0.00414)

| 조건 (선결 4/4 통과 전제) | 판정 |
|---|---|
| `ρ·fan` **PASS** ∧ fals-rate > **0.01657**(=BASE+3sd) | 🔑 **G6 BREAK** — 단, ABL 팔이 특이성을 확인해야 완결 |
| `ρ·fan` PASS ∧ fals-rate ≤ 0.01657 | 🟡 **GATE-PASS-UNDERPOWERED** — 통과가 뽑기 운(지난번 12% 사건 재현) |
| `ρ·fan` FAIL ∧ fals-rate > 0.01657 | 🟡 **RATE-UP / GATE-MISS** — 비율은 올랐으나 8뽑기서 안 나옴 |
| `ρ·fan` FAIL ∧ fals-rate ≤ 0.01657 | 🔴 **NEGATIVE** — 이 용량에서 밀도+register 는 레버가 아니다 |
| fals-rate < BASE − 2sd | ⚠️ **ANTI-LEARN** — 그 팔 INVALID, 별도 조사 |
| 선결 1~4 중 하나라도 실패 | ⛔ **INVALID** (손상) — 과학 판정 없음 |

**추가 스윕 금지**: 이 표 밖 하이퍼 불변. dose 조정은 🔴/🟡 칸에서만, 별도 H 로.

## 코퍼스 검증 (발사 전)

| 팔 | 줄 | 반증가능 | 담체 | held-out 누수 |
|---|---|---|---|---|
| real | 600 | **600 (1.0000)** | 12 | 0 |
| ablation | 600 | **0 (0.0000)** | 12 | 0 |

⚠️ **정직 고지**: 이 드릴 문장들은 **형식 드릴**이지 사실 드릴이 아니다 —
`humidity causes a quantity of recollection that is higher than …` 는 의미상 참이 아니다.
이 개입이 가르치는 것은 **반증가능한 주장의 형태**이며, 내용의 진리성은 이 실험의 대상이 아니다.
그 한계는 판정에 그대로 남는다(**형식 통과 ≠ 좋은 과학적 주장**).

## 재생성 커맨드

```
anima-py corpus falsidrill --out fd_real.txt --n-blocks 24000 --seed 7
anima-py corpus falsidrill --out fd_abl.txt  --n-blocks 24000 --seed 7 --falsi-ablate
anima-py train --init py303_full.clm --d 3784 --L 4 --e0 3 --emax 3 --no-mitosis \
  --corpus mix_real.txt --steps 2000 --ckpt-every 500 --seq-len 512 --batch-size 4 --seed 7
anima-py evaluate <ckpt> --rho-axon --rho-axes fan,form --rho-no-cells --fan-draws 250
```

## Cross-links

[[H_9837]] 두 병목을 실측한 팔 · [[H_9855]] 담체 교정 · [[H_9828]] 밀도 목표수치 · [[H_9829]] 연속 rate
