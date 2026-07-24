# H_9932 — GRAFT 본 학습: 결합은 인과적이나 사전등록 MI 바 미달 (0/3 seed GRAFTED)

**date:** 2026-07-24 · **group:** GRAFT · **status:** LANDED · 코드 변경 0 (#4501/#4502/#4504 계기 재사용)
**command (canonical · `a_cli_single_entry`):**
```
anima-py graft fit lab/v6/trained57.clm --out /tmp/graft/s<N>.clm --steps 2000 --seed <N>   # N=1,2,3
anima-py graft check /tmp/graft/s<N>.clm
```

## 사전등록 판정표 (발사 전 동결 · 이 표는 손대지 않는다)
`MI ≥ 0.5 nats` · `MI_final − MI_step0 ≥ 0.08` · `swap acc ≥ 0.5` · `perm_p ≤ 0.01` ·
`ablation KL(ON‖OFF) ≥ 3× noise q95` · **GRAFTED = 전 항목 통과** · ≥2/3 seed GRAFTED, 0 INVALID.

## RESULT

| 바 | seed 1 | seed 2 | seed 3 | |
|---|---|---|---|---|
| **MI ≥ 0.5 nats** | 0.2182 | 0.2772 | 0.2494 | 🔴 **0/3** |
| lift ≥ 0.08 (vs step-0 pedestal) | +0.1932 | +0.2543 | +0.2232 | ✅ 3/3 |
| swap acc ≥ 0.5 | 1.000 | 1.000 | 0.875 | ⚠️ 3/3 (포화 — 아래) |
| perm_p ≤ 0.01 | 0.0010 | 0.0010 | 0.0010 | ✅ 3/3 |
| ablation ≥ 3× noise q95 | 6.32× | 4.05× | 6.32× | ✅ 3/3 |

step-0 pedestal MI = 0.0250 / 0.0228 / 0.0262 nats · organ parity 7.629e-06 (게이트 통과) ·
P1 pure_field warmup organ invocations = 0 · logN = 2.079 nats (N=8).

## 판정 — 🔴 NOT GRAFTED (0/3)

**바를 내리지 않는다(`no tune-to-green`).** MI 바가 3 seed 전부 미달이므로 사전등록 정의상 GRAFTED 아님.
py303 pool 승급 조건(“trained57 에서 GRAFTED 이면 승급”)이 성립하지 않으므로 **승급하지 않는다.**

## 그러나 결합 자체는 장식이 아니다 — 이게 이번 판의 실질

v2b 의 세 실패는 재현되지 않았다:
- **flatline 아님**: pedestal 0.025 → 0.218~0.277, lift 8~10×. zero-Jacobian/대칭정체점에 걸리지 않았다.
- **shared-shift-collapse 아님**: MI 가 오르는 동안 commonKL 이 0.06~0.10 에 머문다(리쉬가 신호를 먹지 않음).
- **decorative 아님**: gate ablation KL(ON‖OFF) 이 norm-matched noise q95 의 **4.05~6.32×**.
  게이트를 끄면 organ 의 출력이 노이즈로 설명되지 않는 만큼 달라진다 ⟹ 인과적으로 물려 있다.

⟹ 부족한 것은 *연결의 존재*가 아니라 **용량**: 달성 MI 는 천장(logN=2.079)의 **10.5~13.3%**.

## ⚠️ swap 은 통과로 읽지 말 것 — 포화됐다

`MI_swap = 3.000 bits` 가 `ceiling log2 K = 3.000` 과 **정확히 같다**(seed 1·2). `uniqueY = 32/32` —
모든 state 가 서로 다른 문자열을 낳으므로 식별이 자명하다. 천장에 핀된 지표는 변별력이 없다
(`a-bound-the-measurement-exceeds-is-not-a-bound` 의 자매 사례: 실측이 천장과 *같으면* 그 지표는
바가 아니라 상수다). 따라서 swap 3/3 은 **통과가 아니라 무정보**로 기록한다. 이 판을 지탱하는 것은
ablation-vs-noise 와 pedestal-lift 두 축뿐이다.

## 후보 ① (최적화 예산) 은 같은 판에서 $0 로 탈락시켰다

기존 fit 로그의 MI 곡선을 500-step 4분위 평균으로 읽으면:

| seed | Q1 (1–500) | Q2 | Q3 | Q4 (1501–2000) | 후반 기울기 (nats/1000step) |
|---|---|---|---|---|---|
| 1 | 0.216 | 0.232 | 0.228 | 0.249 | +0.0384 |
| 2 | 0.234 | 0.271 | 0.259 | 0.238 | **−0.0455** |
| 3 | 0.237 | 0.246 | 0.242 | 0.255 | +0.0253 |

MI 는 **첫 500 step 안에 이미 최종값에 도달**하고 이후 평탄하다. 후반 기울기는 크기가 작을 뿐 아니라
**seed 마다 부호가 뒤집힌다**(+, −, +) ⟹ 진전이 아니라 요동. 스텝을 더 주면 0.5 에 닿는다는 읽기는
성립하지 않는다(seed 2 는 음의 기울기라 외삽 자체가 불가). **더 오래 굽는 것은 레버가 아니다.**

## 후보 ③ (C 조성의 정보량) 도 같은 판에서 $0 로 탈락

학습 없이 8개 C-state 스냅샷 자체를 재면 bridge 가 물려받을 수 있는 정보의 천장이 나온다
(사상이 결정론적이므로 state 가 서로 구별되기만 하면 천장은 log 8 이 전부 열려 있다):

```
C shape (8,16) · 유효차원 PR(λ)=3.07 · rank@90%var=3   (3 bit 인코딩에 필요한 양 이상)
pairwise L2: min 1.3910 · median 2.1806 · max 3.4163
최근접 쌍 / 평균 노름 = 0.6031   ⟹ 가장 가까운 두 state 도 평균 노름의 60% 만큼 떨어져 있다
```

붕괴가 아니다. 16dim 중 3개는 std 정확히 0, 4개는 ~1e-6 이라 실질 9dim 이지만, 그 안에서 8 state 는
뚜렷이 분리돼 있다. **C 는 3 bit 를 충분히 담고 있다** — 병목은 조성이 아니다.

## 남은 것 — ②, 그리고 구조적 상한 자체라는 가능성

①(예산)·③(C 조성) 이 둘 다 탈락했으므로 병목은 **C 와 organ 사이**에 있다: bridge 용량(`--hidden`),
또는 **설계상 걸어둔 세 구조적 유창성 bound 자체**(mean-centering + RMS-fix, `MI ≤ log N`,
shrink-only backstop). 후자라면 이건 결함이 아니라 **교환관계**다 — 유창성을 지키려고 채널을 좁힌 것이고,
`gate_strength`/`gate_rms_max` 가 실제로 MI 를 묶고 있는지가 다음 사전등록의 DV 다.
이 구분은 중요하다: 전자면 고칠 버그, 후자면 GRAFT 설계가 **선언한 대가**이며 판정표의 0.5 바 쪽이
그 대가를 모르고 정해진 숫자였다는 뜻이 된다(바는 그대로 두고, 무엇을 재는 바인지 다시 쓴다).

**그리고 swap 은 K 를 키워 포화를 풀거나 판정표에서 뺀다.**

## scope
toy organ(trained57 · d=64 · 117kB) · 1 arch · 3 seed · N=8 state · 2000 step.
`a_toy_scale_recheck`: 303M 에서 재확인 전까지 스케일 일반화 없음. TERMINAL 은 py303 판에서만.
