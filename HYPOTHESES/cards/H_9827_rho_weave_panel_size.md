# H_9827 — G1 을 재는 자가 12항목이다 (ρ·weave 패널 크기 · 303M 예산사다리의 선행조건)

**status:** 🟢 계기 착륙 (토이 e2e PASS · 정답 대조 · 감사가 실제 결함 1건 적발) · 과학 판정 없음
**wired:** yes — `anima-py corpus weavepanel --out panel.json [--weave-families …] [--weave-max N] [--seed S]`
+ `anima-py evaluate <clm> --rho-axon --weave-panel panel.json`
(플래그 부재 = 동결 `_WEAVE` 경로 그대로 = byte-identical 기본값)
**source:** [[H_9820]] 임계 DV 가 계기의 가장 눈먼 지점에 잡음을 전량 집중시킨다는 진단 ·
[[H_9817]] 303M 예산사다리 설계(fable+sol 병렬 위임 합의) · [[H_9327]] ko lane BINDING 벽

## 발견 — 발사 전에 잡아야 했던 것

fable·sol 두 프런티어 모델이 독립적으로 같은 결정실험을 냈다: **303M 을 조작변수 1개(steps)로
log-사다리 재학습하고 매 rung 의 `.clm` 을 engine-native `--rho-axon` 으로 읽는다.**
그 설계를 실행하려고 판정 지표 ρ·weave 의 패널을 열어보니:

```
cli/rho_axon.py:218  _WEAVE = [ ... ]   →  총 12 항목 (ko 6 + en 6)
```

**G1 을 재는 프로덕션 계기 전체가 12항목이다.** 그리고:

- 항목 **1개 = 보고값의 0.083**. 통과 바 `thr=0.30` · 통제 상한 `ctrl_cap=0.15` ⟹
  **결정 구간 전체가 2항목 거리**. [[H_9820]] 이 n=32 에서 "임계 DV 는 잡음을 평균내지 않고
  계기가 가장 눈먼 지점에 전량 집중시킨다" 로 진단한 병이 **n=12 에서 더 심하게** 있다.
- 12 중 **6 이 ko lane** — [[H_9327]] 이 🧱 BINDING 으로 측정하고 모든 탈출이 죽은 레인.
  즉 계기의 절반이 **구성상 죽은 축** 위에 있다.
- 이 패널로 다일치 303M 사다리를 읽으면 [[H_9820]] 의 실수를 **100배 비용으로 반복**한다.

## 계기 (신규 조작 = 기존 커맨드의 플래그 · 규칙 준수)

`anima-py corpus weavepanel` 이 **동결된 항목 모양 그대로**(cue · target · swap_cue · bind_cue · lang)
를 파라메트릭 계열에서 생성한다. **바·통제·채점기는 전부 불변** — 표본크기만 움직인다.

| | n | 계열 | 담체 | 바 0.30 에서 binomial sd | 항목 1개의 영향 |
|---|---|---|---|---|---|
| 동결 `_WEAVE` | **12** | 3 (혼합·산술·이중부정) | 계열당 1 | **0.1323** | **0.083** |
| `weavepanel` 기본 | **212** | 4 | **계열당 2** | **0.0315** | **0.0047** |

⟹ 검정력 **4.2배**. 계열별 내역: arith-add 162 · arith-mul 30 · color-mix 12 · direction 8.

**담체 2종은 선택이 아니라 요건**이다 — convergence `corpus-py-1` (E): 담체가 하나뿐이면
'조성을 배웠나' 와 '이 템플릿 하나를 배웠나' 가 **완전 공선**이라 어떤 팔도 둘을 못 가른다.
빌더는 계열당 담체 < 2 이면 **패널을 거부**한다(exit 2).

## 🔑 감사가 실제 결함을 잡았다 — 동결 배터리의 복사-통과 항목

빌더의 누수 감사가 `double-neg`(이중부정) 계열 **전량을 거부**했다:

> `the opposite of the opposite of hot is` → 정답 `hot`

정답이 **단서 안에 그대로 들어있다**. 즉 **단서에서 단어 하나를 복사만 해도 reach 가 올라간다.**
그리고 atom-swap 통제가 이것을 **못 잡는다** — 복사기는 swap 단서에서 `cold` 를 복사하므로
`hot` 이 안 나오고, 통제는 깨끗한 채로 reach 만 부풀려진다.

**⚠️ 동결 `_WEAVE` 12항목 중 2개(ko 1 + en 1)가 정확히 이 형태다** = 프로덕션 G1 계기의 **1/6 이
복사-통과 가능**. 이 카드는 그것을 **기록하되 동결 배터리를 고치지 않는다**
(`burned-gate-no-refreeze` — 이미 읽힌 게이트의 재동결은 구조적 tune-to-green). 빌더는 다만
그 결함을 **재생산하지 않는다**: `double-neg` 는 기본 계열에서 제외됐다.

## 착륙 검증 (토이 e2e)

- 패널 생성 exit 0 · n=212 · 계열/담체 인구조사 출력 · sd 실계산.
- 감사 4종 전부 발화 확인: swap 이 정답을 유지 / 정답이 단서 누수 / 정답이 bind-strip 누수 /
  같은 단서 두 정답 / 계열당 담체 < 2.
- 감사 위반 시 **패널을 쓰지 않고 exit 2** (doomed panel 이 조용히 실려나가지 않음).
- `--weave-panel` 부재 시 `panel=None` ⟹ 동결 `_WEAVE` 경로 그대로 = **기본 byte-identical**.
- 재생성 결정성: `random` 미사용 · seed 하나로 재현되는 LCG 셔플(`corpus-py-1` (J)).

## 이 카드가 판정하지 않는 것

계기다. **과학 판정 0.** 확장된 패널로 잰 어떤 수치도 아직 없다. 다음 H 가 이 패널로
`py303_full.clm` 기준선을 잡고, 그 다음이 예산사다리다.

⚠️ 남은 선결 과제 (다음 H 가 반드시 먼저 할 것): 확장 항목들이 **원자 노출 축에서 학습됐는지**
코퍼스에서 직접 세야 한다(`corpus-py-1` (F)). 모델이 `seventeen` 을 본 적 없다면 그 항목은
조성 실패가 아니라 원자 부재를 재는 것이다 — 이 빌더는 아직 그 노출 감사를 **하지 않는다**.

## 재생성 커맨드

```
anima-py corpus weavepanel --out weave.json --seed 7
anima-py evaluate <ckpt.clm> --rho-axon --weave-panel weave.json
```

## Cross-links

[[H_9820]] 임계 DV 취약성 진단(동기) · [[H_9817]] 예산사다리가 이 계기를 요구 ·
[[H_9327]] ko lane BINDING(패널 절반이 죽은 축인 이유) · [[H_9826]] 같은 캠페인의 G6 코퍼스 census
