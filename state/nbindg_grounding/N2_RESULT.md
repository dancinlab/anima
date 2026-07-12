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
| **main_s7** (seed 7) | **0.477** | **0.402** | 0.552 | **0.950** ✅ |
| **main_s11** (seed 11) | **0.345** | **0.368** | 0.322 | 0.7375 △ |

- chance floor 0.50 · Δ는 max(control, 0.50) 대비 · flip0=`이 <atom> => ` 직접 극성판독, flip1=XOR 역접용례.
- 전 수치 clean full-174/80 (aiden 단발 순차 eval·0.13.9). **flip0(극성 접지 liveness) 양 seed 모두 chance
  미만**: s7 **0.402**·s11 **0.368** (둘 다 shuffle 0.448 이하) → 2-seed **grounding 붕괴 확증**.
- △ = main_s11 SEEN D-acc 0.7375은 frozen 0.85 bar **미달**이나 **margin_med +16.0·mpos 0.975 = grid 강하게
  설치됨**(D-acc<0.85는 greedy-first-token vs margin 괴리 아티팩트). ⟹ validity는 **main_s7 SEEN 0.950이
  clean-carry**, s11은 margin-strong이나 D-acc bar로는 marginal(정직 표기) · verdict는 valid arm s7이 담지.

## 판정 = 🧱 GROUNDING-WALL (자연 접지가 전이 안 됨 · INVALID 아님 · NAT-CRACK 아님)

frozen 로직(`N2_STATUS.md` §4·§5) 그대로:

1. **validity 게이트 — main_s7 clean-carry** — main_s7 SEEN P_grid **0.950 ≥ 0.85**(margin_med +14.7·
   mpos 0.975) → grid XOR 연산자 **확실히 설치**. held-out 실패는 under-exposure INVALID이 **아니다**(진짜
   negative). main_s11 SEEN D-acc 0.7375은 0.85 bar 미달이나 **margin_med +16.0·mpos 0.975 = grid 강설치**
   (D-acc<0.85는 greedy vs margin 괴리) → s11도 grid는 들어감·D-acc bar로는 marginal(정직). b·c는 빌드서 확인.
2. **NAT-CRACK 반증** — 양 seed 둘 다 chance floor 0.50 **미만**(s7 0.477·s11 0.345). Δ vs max(control,0.50)
   = 둘 다 **음수**. 어떤 seed도 Δ≥0.20 bar 미달 → **NAT-CRACK(자연 접지 합성) 실패**.
3. **flip0 붕괴 = GROUNDING-🧱 (2-seed 확증)** — flip0(극성 직접판독 liveness)이 s7 **0.402**·s11 **0.368**
   (둘 다 shuffle 0.448 이하·mpos<0.5)로 **양 seed 모두 chance 미만**. 모델이 held-out P_nat 원자의 극성을
   **자연 분포적 사용에서 접지하지 못함** → 연산자에 합성할 **grounded operand가 없다** → flip1(s7 0.552·
   s11 0.322)은 ungrounded 원자 위 noise-level. §5 규칙 "flip0 낮음 = GROUNDING-🧱" 발동.
4. **seed V5** — 두 main seed held-out straddle(0.477·0.345)이나 **둘 다 chance floor 아래 동일측 + flip0
   양 seed chance 미만** → 판정 안정(bar 조정 없음).

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
- **⚠️ '0.13.9 GPU-init 스톨'은 오진 정정(convergence remote-poll-pgrep-1 재발)**: 처음엔 eval python이
  0% CPU·RSS ~11MB로 정체 = 0.13.9 GPU auto-init 회귀로 의심했으나 **오진**. 진짜 원인 = 내가 같은 eval을
  반복 launch해 **~7개 evaluate.py를 한 호스트에 중첩**시킨 상호 CPU-starvation을, pgrep이 console-script
  **wrapper 셸(RSS 3.7MB·0%CPU)**을 잡아 실 python worker(RSS 3GB+·CPU 수백~1000%)를 놓치고 '스톨'로 오독한
  것(hexa-decode-wrapper-stall 재발). **0.13.9 코드 무죄** — 잔여 procs 전량 kill 후 **단발 순차 eval**은
  RSS 3.2GB·CPU 1087%로 즉시 정상 grinding. 교훈=pool eval은 호스트당 단발(pod-dedicated-host)·`ps --sort=-rss`로
  실 worker 확인·kill은 full module-path. main_s7 flip clean-full·main_s11 SEEN corroboration은 단발 재측정으로
  확보(indicative 0.450/0.552가 이미 GROUNDING 붕괴 corroborate·**load-bearing verdict는 clean-run 위 완비**).

## 산출
`state/nbindg_grounding/`: N2(gen_nbindg_n2.py·N2_PREFIRE_AUDIT·n2_eval_manifest·n2_seen_manifest·
n2_*_train.txt·FABLE_N2_RECIPE·N2_STATUS) · `n2_results/eval_{base_only,shuffle_grid,main_s7,main_s11,
seen_main_s7,seen_main_s11}.json` · ckpt=`~/anima-weights/natem_n2/*.clm`(4·byte-동일 교차확인). card H_9286.
