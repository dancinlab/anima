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
| FLUENCY | ⛔ **HF엔 INVALID(측정불가)** — #4540 로 크래시는 고쳤고 재-check 는 rotation-null z=+293.79 를 **정확히 재현**했으나, fluency arm 이 raw byte 를 토큰ID 로 먹임(subword Mistral 엔 무의미) → NLL gate-OFF=13.95(쓰레기)·**FORM PANEL 이 스스로 INVALID 선언**("organ 이 자연문 선호 안 함"). **가드가 가짜 숫자를 거부한 정상 작동**. HF fluency = fluency arm 이 `organ.encode` 토큰화를 써야 유효(follow-up). | — |

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

## 다음
① **fluency arm 을 HF-호환으로 수정**(byte→`organ.encode` 토큰화 · probes 수정과 동종): 현재 fluency 는
   subword organ 에 byte 를 먹여 FORM PANEL 자가무효 → HF 이득영역의 "저비용 vs 비용有"가 **미측정**으로
   남음. 수정 후 재-check 로 dNLL/FORM margin 판독. (303M byte-LM 은 fluency 유효 = H_9943 −6.9%.) ② λ 스윕(0.5=병렬 H_9947 인접 / 0.2 / 0.1)으로 이득영역 경계 +
   교환비 정밀화. ③ 303M(H_9943)서 gate_strength 스윕과 대칭 = 두 축(λ·gs)의 이득영역 지도.
산출: log `graft_mistral_lam03_track1.log`·recheck `graft_mistral_lam03_check2.log` · ckpt `graft_mistral_lam03_s1.pt`.
