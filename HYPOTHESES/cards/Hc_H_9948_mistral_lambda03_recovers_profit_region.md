# H_9948 · λ=0.3 이 7B Mistral 의 이득영역을 회복한다 — priced-out 채널이 값을 낮추자 강하게 살아난다 (z=+26→+294)

**한 줄:** H_9947 이 "Mistral organ 결합은 실재하나 λ=1 에서 priced out(부재 아님)"으로 남긴 것을,
`--lam-common 0.3`(7B 교환비 0.68 아래)로 재학습하니 **채널이 강하게 회복**: rotation-null
**z=+293.79**(H_9940 λ=1 의 z=+18.59, H_9947 의 z=+26 대비 급등), MI lift vs pedestal **+0.4234 nats**
(λ=1 의 +0.0048 대비 **~88배**), fit MI 가 붕괴 없이 **0.29~0.62 유지**(λ=1 은 floor 0.004 로 붕괴).
= near-floor 는 organ 무능이 아니라 **λ 세금**이었다는 fable Q1(c)·H_9940/H_9947 을, **값을 제거하니
채널이 살아난다**로 인과 확증.

- 계기: `anima-py graft fit --hf-model mistralai/Mistral-7B-Instruct-v0.2 --carrier-corpus
  en_general.txt --out graft_mistral_lam03_s1.pt --lam-common 0.3 --steps 1000 --n-states 8
  --state-gap 13 --ctx 128 --cont-len 64 --carrier-k 4 --gate-strength 0.1 --seed 1` → `graft check
  ... --rotation-null 64 --k 8 --cont-len 32 --probes 2 --fluency-corpus en_general.txt`
  (summer RTX 5070 · 4bit · seed 1). regime `no-corpus` · DIRECTIONAL (Mistral ≠ 303M terminal).

## 결과 — 이득영역 회복, 강한 통제 통과 (fluency 제외)
| arm | 값 | vs λ=1 |
|---|---|---|
| MI lift vs pedestal | **+0.4234 nats** | +0.0048 → **~88×** |
| **ROTATION-NULL** | MI_trained=0.1233 vs null(n=64) mean 0.0021 q99 0.0031 · **z=+293.79** PASS(>q99) | z=+18.59 → **~16×** |
| SWAP | acc **0.750**(chance 0.125) · MI_swap 2.329/3.0 · perm_p 0.0010 | — |
| ABLATION | KL(ON‖OFF)=0.7133 vs noise q95=0.0581 · **12.28×** (gate≠noise) | — |
| fit MI 궤적 | step200 0.35 / 400 0.49 / 600 **0.62** / 1000 0.52 · L_common 0.7~2.0 유지 | λ=1 은 step75 이후 floor 0.004 |
| FLUENCY | ⚠️ **측정됨(#4546 후 · 이득이지만 비싸다)**: NLL gate-OFF **2.234**(정상 · 이전 byte-fed 13.95 쓰레기 아님) → ON **3.426**(dNLL **+1.192**) · noise-matched dNLL +0.0015 → **price 794×**(gate가 noise보다 훨씬 큰 유창성 비용). FORM panel 이제 VALID(organ 자연문 선호) · dMargin +0.63(**form −19%** · 303M H_9943 −6.9%보다 나쁨). ⟹ **profitable-but-costly** — 회복된 채널(z+294)이 언어를 크게 흔든다. | — |

## 판정 — 🟢 이득영역 존재: λ<교환비면 priced-out 채널이 강하게 회복 (DIRECTIONAL · fluency 미완)
- **H_9947 AGREES + EXTENDS(직접 다음 단계)**: H_9947 = "λ=1 서 real-but-priced-out(z=+26)". 이 카드 =
  "값(λ)을 0.3 으로 낮추니 그 priced-out 채널이 z=+294 로 살아나고 fit 이 MI 를 유지" ⟹ H_9947 의
  "부재 아님, 벌점당함"을 **벌점 제거 실험으로 인과 확증**. fable primary(λ<0.68 refit)·H_9940 next-①.
- **교환비 프레임 정합**: λ=0.3 < 7B 교환비 0.68 이므로 H_9939 가 계산한 그 방향이 net-profitable 이 되어
  optimizer 가 붙잡는다 — 예측대로.

## 정직 경계 (no tune-to-green · verdict-ssot-1)
1. **DV 는 MI↑ 단독이 아니다**: λ 는 MI 를 기계적으로 산다. 이 카드의 verdict 하중은 **rotation-null 지배
   (z=+294, λ 가 못 사는 방향-특이 통제)** 에 있다 — 그건 통과. **단 fluency 미완**(gate 언어비용 ≤ noise?)
   이라 "저비용 이득"인지 "이득이지만 비용有"(303M H_9943 는 −6.9%)인지 **아직 미판정**. 완주 시 갱신.
2. L_common 0.7~2.0 은 높다 — gate-ON 이 유창성을 크게 흔들 수 있다(fluency 가 판정). MI/L_common ≈ 0.3~0.4
   (λ=0.3 문턱 근처) 라 이득이 얇다.
3. DIRECTIONAL: 4bit · 1 seed · Mistral ≠ 303M(terminal 은 H_9943 의 303M).

## 측정된 fluency 결론 (#4546 후 · 병렬 H_9950 AGREES)
λ=0.3 이득영역은 **profitable-but-costly**: rotation-null z=+294 로 방향은 실재하나, gate-ON 이 organ 언어를
NLL +1.192 nats(noise 는 +0.0015 → price 794×) 흔들고 FORM margin 을 19% 깎는다. 병렬 세션 **H_9950**("λ 는
fluency 가격표 · rotation-null 은 이득영역 전체에서 통과")과 정합 — 값(λ)을 낮춰 채널을 켤수록 유창성 대금이
커진다. 303M(H_9943 −6.9%)보다 7B 가 더 비싸다(form −19%) = frozen-substrate channel contraction 의 비용 축.

## 다음
① **fluency arm HF-호환 완료(#4546)** — byte→`organ.encode`, FORM PANEL 이제 VALID. ② λ 스윕(0.5/0.2/0.1)으로
   이득영역-비용 곡선(H_9950 와 합류) · ③ 303M gate_strength 스윕과 대칭 = (λ·gs) 2축 이득-비용 지도. ② λ 스윕(0.5=병렬 H_9947 인접 / 0.2 / 0.1)으로 이득영역 경계 +
   교환비 정밀화. ③ 303M(H_9943)서 gate_strength 스윕과 대칭 = 두 축(λ·gs)의 이득영역 지도.
산출: log `graft_mistral_lam03_track1.log`·recheck `graft_mistral_lam03_check2.log` · ckpt `graft_mistral_lam03_s1.pt`.
