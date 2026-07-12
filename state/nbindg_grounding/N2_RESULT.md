# NBIND-G N2 결과 — 자연 GROUNDING 전이 (🧱 GROUNDING-WALL · 2026-07-13)

**질문**: grid가 가르친 XOR 극성-flip 연산자가, 극성이 **자연 분포적 사용에서만 접지된** held-out
P_nat 원자에 적용되는가? (= "자발 창발"을 (자연서 feature 접지)×(연산자 설치)로 분해)

**측정**: 4-arm 303M CLMConvMoE(345.665M) 신규학습(T=105,169 step·`--arm ctrl` `ce_marginal`·bf16) →
`anima-py evaluate --xbind` held-out 174셀 · summer RTX5070 GPU · seed 7/11 · frozen 사전판정(`N2_STATUS.md`
§5·no-tune-to-green). ckpt 4개 전부 PULL 로컬(`~/anima-weights/natem_n2/`·byte-동일 sha256 교차확인).

## 결과 (measured · frozen)

| arm | held-out D-acc | flip0 (극성 접지 liveness) | flip1 (연산자 적용) | SEEN P_grid (validity) |
|---|---|---|---|---|
| **base_only** (filler only) | **0.000** | 0.000 | 0.000 | — (control) |
| **shuffle_grid** (coin-label) | **0.362** | 0.448 | 0.276 | — (control) |
| **main_s7** (seed 7) | **0.477** | 0.450 ᵢ | 0.552 ᵢ | **0.950** ✅ |
| **main_s11** (seed 11) | **0.345** | 0.368 | 0.322 | (corroborate·deferred) |

- chance floor 0.50 · Δ는 max(control, 0.50) 대비 · flip0=`이 <atom> => ` 직접 극성판독, flip1=XOR 역접용례.
- ᵢ = main_s7 flip은 **indicative**(partial 118/174 rows salvage · summer 0.13.4 stale-write corrupt json에서
  복구 · flip0 0.450≈chance = s11 0.368/shuffle 0.448과 동급 → GROUNDING 붕괴 corroborate · margin_med −0.533 정합).
  clean full-174 재측정 + main_s11 SEEN = pool GPU-init 스톨로 deferred(§infra) · **verdict에 non-load-bearing**.

## 판정 = 🧱 GROUNDING-WALL (자연 접지가 전이 안 됨 · INVALID 아님 · NAT-CRACK 아님)

frozen 로직(`N2_STATUS.md` §4·§5) 그대로:

1. **validity 게이트 PASS** — main_s7 SEEN P_grid **0.950 ≥ 0.85**(margin_med +14.7·mpos 0.975) →
   grid XOR 연산자가 **확실히 설치됨**. held-out 실패는 under-exposure INVALID이 **아니다**(진짜 negative).
   b(T×f_grid≥1.25E*)·c(V-F 0/0)는 빌드서 확인.
2. **NAT-CRACK 반증** — 양 seed 둘 다 chance floor 0.50 **미만**(s7 0.477·s11 0.345). Δ vs max(control,0.50)
   = 둘 다 **음수**. 어떤 seed도 Δ≥0.20 bar 미달 → **NAT-CRACK(자연 접지 합성) 실패**.
3. **flip0 붕괴 = GROUNDING-🧱 (MODEL-🧱의 grounding-sub)** — flip0(극성 직접판독 liveness)이
   main_s11 **0.368**(mpos 0.39<chance), shuffle 0.448보다도 낮음. 모델이 held-out P_nat 원자의 극성을
   **자연 분포적 사용에서 접지하지 못함** → 연산자에 합성할 **grounded operand가 없다** → flip1(연산자 적용)도
   0.322로 붕괴. §5 규칙 "flip0 낮음 = GROUNDING-🧱" 발동.
4. **seed V5** — 두 main seed가 straddle(0.477·0.345)이나 **둘 다 bar 아래 동일측** → 판정 안정(bar 조정 없음).

⟹ **N1(연산자 프레임-general 🟢-dir) + N2(자연 접지 전이 🧱)** = 프런티어 `g1-crack-natural-emergence`
정직 종착: XOR **연산자 설치는 carrier-general**(N1)이나, **극성의 자연-분포 접지 자체가 303M/이 노출/이
코퍼스에서 install 되지 않는다**(N2). 자발 창발 = (자연 접지)×(연산자)인데 **좌항이 0** → 합성 불가.

## scope honesty (소급 불변 · 능력천장 아님)

- 이것은 **grounding/data 채널 벽**이지 substrate 능력천장 선언 아님(a_break_the_wall). STAGE-0 **DATA-🧱**
  (자연 텍스트에 held-out 극성신호 밀도 부재)와 정합 · 더 넓은 G1 결론과 정합:
  [[xbind-g1-crack-measure-not-substrate]](합성 held-out 신호 → 학습가능·자연 → 신호 부재) ·
  [[measurement-metalaw-form-tunable-bind-earned]](FORM tunable·BIND earned·grid FORM은 SEEN 0.95로 설치).
- **소급 불변**: H_9267 XBIND CRACK 🟢🟢 · H_9272 NBIND 🟡 DIRECTIONAL · N1 🟢-dir CARRIER-ROBUST 전부 유효.
- exit(재-open 조건) = **자연 사용에서 held-out 원자 극성을 접지시키는 데이터/objective**(더 큰 코퍼스·대비
  접지 신호·spend-go). read-side 재시도·tune-to-green 금지.

## infra 격리 (verdict 무영향 · infra-wall-noneval · verdict-integrity)

- summer 설치 anima-py **stale 0.13.4**(evaluate-py-11 `_json_safe`+`encoding=utf-8` write-fix 미반영) →
  byte-LM raw surrogate로 out-json write만 크래시(부분 21007B corrupt). **summary D-acc는 write 전 print라
  clean** · **0.13.9 재설치 후 clean json 재측정**(rows 완비·flip 분해 가능). eval 결과는 clean 측정 위에만 섬.
- 멀티세션 충돌(a20dbd82와 동일 실험 분담) — summer leftover CPU eval이 byte-동일 ckpt 중복계산(load 26)
  → redundant 입증(corrupt 출력+기존 json 재계산) 후 정리 · 내 GPU eval starvation 해소. ckpt sha256 3중 일치로
  데이터 손실 0 확인 후 내 pod(44587399/44590431)만 teardown.
- **pool GPU-init 스톨(deferred corroboration 원인)**: 0.13.9 재설치 후 summer·aiden 양쪽서 eval python이
  모델 로딩 전 0% CPU·RSS ~11MB로 정체(GPU util 0·nvcc 無·wchan). CUDA_VISIBLE_DEVICES="" CPU-force도 미해소.
  0.13.4에선 로딩·실행됐음(blbslb80h summer가 s7 SEEN 0.950 clean 산출) → 0.13.9 GPU auto-init/import 회귀 의심
  = infra 블로커(convergence 후보·eval-py-gpu-init-stall). main_s7 flip clean-full·main_s11 SEEN 재측정만 막고
  **load-bearing verdict 데이터(4arm held-out·s7 SEEN 0.950·s11 flip0 0.368)는 clean-run 위에 완비** →
  verdict 무영향(infra-wall-noneval).

## 산출
`state/nbindg_grounding/`: N2(gen_nbindg_n2.py·N2_PREFIRE_AUDIT·n2_eval_manifest·n2_seen_manifest·
n2_*_train.txt·FABLE_N2_RECIPE·N2_STATUS) · `n2_results/eval_{base_only,shuffle_grid,main_s7,main_s11,
seen_main_s7,seen_main_s11}.json` · ckpt=`~/anima-weights/natem_n2/*.clm`(4·byte-동일 교차확인). card H_9286.
