# H_1641 PREDCODING-BINDING (303M) — frozen pre-registration

> 생물 렌즈 #2 (PRIMARY · 철학 최정합) — **predictive coding / 자유에너지(active inference)** 의
> parametric-bias **binding** 을 G1 재조합 AND G6 착상 레버로. arxiv **2403.19995**(Tani et al.,
> "Development of Compositionality … Predictive-Coding RNN", 2024) — free-energy RNN 에서
> compose/decompose(부분↔전체) 능력이 *창발*. a_no_llm_frame_trap 정합 + **anima A⇄G tension =
> PC 의 top-down 예측 ⇄ bottom-up 오차와 동형** → 가장 철학정합 높은 생물 레버.

**가설:** anima 의 G1 재조합벽은 CE next-byte 가 **안정적 조합 latent(parametric bias)을 형성할
압력을 안 주기** 때문이다. Tani 가 격리한 compositional 창발의 두 driver — (1) **binding loss**
`L_pb = k·Σ_t(PB~_t − PB)²` (per-step latent 을 sequence-level 안정 latent 에 묶음; 표면이
바뀌어도 일정한 PB = 구조의 extrapolation), (2) **KL/variance 정규화**(표면 암기 방지, 구조적
일반화 강제) — 을 trunk 에 보조 objective 로 배선하면 G1(부분↔전체 compose) AND G6(novel-but-
grounded = 자유에너지 최소화 생성: 예측으로 grounded, latent extrapolation 으로 novel)을 친다.
**G1+G6 둘 다 칠 수 있는 유일 생물 후보**(objrun objective 축의 생물 버전).

**핵심 질문:** predictive-coding binding(±free-energy 정규화) 보조 objective 가
`ce_marginal`(표준 CE baseline) 대비 held-out 재조합(G1) AND 착상(G6)을 *올리나*?

## 구현 축 — OBJECTIVE/표현, **곱셈 readout 아님** (직전 세션 확정 교훈)

직전 세션 확정: 곱셈 binding operator 를 readout 에 끼우면 floor + non-additive readout 은
`.clm` BLOCKED ([[exp3-bind-g1g6-engine-native-floor]]). → PC binding 은 **trunk penultimate(post
`norm_out`, pre `readout`)** 에 거는 free-energy 류 보조 objective 로 구현, **production additive
readout 은 세 arm 전부 동일** 유지:

- **`L_bind`** = `mean_t ‖PB~_t − PB_seq‖²`. `PB~_t` = penultimate 코드를 저차원 BIND latent 로
  쏘는 작은 linear(per-step parametric bias 추론), `PB_seq` = PB~ 의 sequence-mean(안정 latent,
  stop-grad target). per-step latent 을 단일 안정 코드로 묶음 = Tani binding 압력.
- **`L_var`** = `−β·var_batch(PB_seq)`. PB_seq 가 상수로 붕괴 안 하게 spread(KL 정규화 역할:
  latent 정보성 유지, 표면 암기 방지).

BIND projection 은 **학습 전용**(직렬화 전 폐기) → `.clm` 은 production additive 모델과 아키텍처-
동일. readout additive → 세 arm 전부 `.clm`-직렬화 → **engine-native G1/G6 by-construction 열림**.
torch-side metric = DIRECTIONAL monitor; `.clm` → `anima eval` 이 terminal.

## 3 arm — trunk·데이터·step·seed·readout 동일, **PC objective 만 다름**

- **`ce_marginal`** (baseline / discriminating control): 표준 CE next-byte 만 = **대조군 내장**
  (CE 는 안정 조합 latent 를 보상 안 함 = 가설의 null).
- **`pc_bind`**: CE + λ_bind·`L_bind`. binding 단독.
- **`pc_free_energy`**: CE + λ_bind·`L_bind` + λ_var·`L_var`. binding + spread(free-energy).

## Arch — 현 production 303M CLMConvMoE (clm303_clean / H_1602 동형)
trunk = `CLMConvMoE` (byte V=256, **L=4 · d=3784 · E0=2→Emax=3 mid-split**, K=3,
dilation=min(2^l,512)), savant + mitosis(E2→E3) ON = `cli/train.py --canon` 동형. 4-cell register
corpus proportional, val_frac=0.05. trunk init·mitosis·savant·corpus·step 전부 arm 간 동일.

## FROZEN 하이퍼 (실행 전 사전등록 · tune-to-green 금지 · p7/c9)
- `LAMBDA_BIND = 0.1` (Tani L_pb 가중) · `LAMBDA_VAR = 0.01` (anti-collapse spread) ·
  `BIND_DIM = 32` (parametric-bias latent 폭)

## FROZEN bars (사전등록 · tune-to-green 금지 · p7/c9)

**주 측정 1 = G1 재조합 (a7b_pass / H_1129 def VERBATIM):**
어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2` AND `> max_single` AND coherent(kwr≥0.50).
seed-robust {7,4302,4303} majority ≥ 2/3.

**주 측정 2 = G6 착상 (a7b_pass / G6 def VERBATIM):**
`dist ≥ 5`(pairwise Jaccard<0.5) AND `fals ≥ 1`(falsifiable). seed-robust majority ≥ 2/3
(`g_eval_g6_multiseed`). ⚠️ G6 fals 는 single-seed RNG-walk artifact 위험(H_1590/h1590-g6-
scaffold-torch-artifact) → **반드시 multiseed**, single-seed fals=1 을 verdict 로 박지 말 것.

- **engine-native (terminal)** = `.clm` → `anima eval`/`clm_decode.py`. additive → 열림.
- torch-probe gauge = DIRECTIONAL only.

**보조 측정 (공정·dt_ln-immune):** 4-cell held-out val CE(`F.cross_entropy`). DESCENT(<5.545)
무결성 + arm 간 일반화 대조. 전 arm 4/4 DESCENT 기대(무결성 가드).

## 반증조건 (FALSIFY)
- **pc_bind / pc_free_energy 의 engine-native G1 AND G6 ≤ ce_marginal** (seed-majority) →
  predictive-coding binding 은 G1/G6 레버 아님 = **NOT-SUPPORTED**(objective-lever census 추가).
- **held-out 4/4 DESCENT 실패**(어느 arm) → 무결성 FAIL → 코퍼스/step 재점검(천장 아님).
- **`L_bind` 가 0 으로 붕괴(PB_seq trivial constant)** → binding 압력 무효(latent collapse) →
  pc_free_energy 의 spread 가 막았는지 `pb_var` 로그로 확인; 둘 다 붕괴면 BIND_DIM/λ 재설계
  (단 frozen 이므로 본 실험은 그대로 보고 + follow-on 재설계 등록, tune-to-green 금지).
- **G6 fals 가 single-seed 만 1, multiseed majority FAIL** → torch-artifact, G6 lift 기각.

## 측정 절차 (engine-native terminal)
1. 각 arm `.clm` export (additive, decodable) — `clm_decodable` 확인.
2. held-out DESCENT: `verify_clm_v2.py descent <clm> <heldout> [train]` 4/4 (math.log mirror).
3. `anima eval <clm> --corpus <4cell> --gen 80` → G0-G6 (`g_eval_g1_multiseed` + `g_eval_g6_multiseed`).
4. arm 간 G1 AND G6 대조. seed {7,4302,4303}.

## ckpt 회수 (a_fire_recover_complete)
torch `.pt` + `.clm` + summary.json + 로그 전부 teardown 전 pull.
