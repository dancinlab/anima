# H_9801 — BRIDGE→G6 MEDIATION 2×2 — G6 착상이 G1 하류인가 독립 faculty 인가를 eval-only 로 판별

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-g6-identity
**source:** lab full 2026-07-19 — Fable A4 ≡ Sol #2 독립수렴
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
G6(착상)가 '온도 걸린 재조합'인지 별개의 다양성 생성 faculty 인지 미결. 동일 ckpt·canonical mouth-agnostic `rho_fan::rho_fan_score_arm_auto` 로 store-fuse{pairodd,none} × seed-class{composed,atomic} 2×2 를 돌리면 한 번에 갈린다.

## instrument
`anima-py evaluate --rho-fan --store-fuse {pairodd|none} --seed-class {composed|atomic}` + `--fan-store-charge frame`(각 frame 의 두 concept 만 store 에 charge, 생성할 claim·measurable word 는 미주입). 판별량 3종: canonical DIST≥5∧FALS≥1 · `--fan-bind` paired bind-Δ · fals_bound(주장이 실제 두 topic 에 묶였나).

## controls (사전등록)
계기 양성통제=온도 사다리 arm(고온서 비정합이어도 Jaccard<0.5 5개 산출 ⟹ 계기가 다양성을 잴 수 있음 증명·실패시 INSTRUMENT-DEAD 무판독) · B0=동일 slot/value/token multiset 의 address derangement · SHUF 통제(H_6186: FORM-only detector 는 SHUF 가 6/6 통과 실측 ⟹ bind-gate 없이 FALS 원값 읽지 말 것) · 우연은 realized 분할서 재유도

## falsify
bridge×composed 에서만 lift ⟹ G6 = G1 하류(다리가 조합 원자 공급). 어디도 lift 없고 온도통제 통과 ⟹ G6 = 독자 벽. 양 seed-class 동등 lift ⟹ 다리는 일반 엔트로피원(둘 다 아님). bridge arm 이 fuse-off 미만 ⟹ 간섭(H_9798 자료).

## cost
eval-only $0–5 (H_9804 와 동일 세션 재사용)

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## 🔬 실측 판정 (2026-07-20 · summer pool · `anima-py evaluate` · gen=40 canonical)

**tier: 🟠 G6 = 독자 벽 (G1 하류 아님) · 결함 위치 = 반증가능성이지 다양성 아님 · n=1 seed/셀 DIRECTIONAL**

2 mouth × 2 seed-class, 전 arm rc=0.

| mouth | seed-class | dist (bar ≥5) | fals (bar ≥1) | temp-ladder |
|---|---|---|---|---|
| ByteGPT h1129 | composed | 6 ✅ | **0** ❌ | ALIVE (6) |
| ByteGPT h1129 | atomic | 6 ✅ | **0** ❌ | ALIVE (6) |
| CLM clm303_clean | composed | 5 ✅ | **0** ❌ | ALIVE (6) |
| CLM clm303_clean | atomic | 6 ✅ | **0** ❌ | ALIVE (6) |

### ① 계기 양성통제 4/4 통과 — 그래서 이 음성은 읽을 수 있다
온도사다리(T=1.3)가 4/4 셀에서 `dist=6 ≥ 5` = **이 계기는 다양성을 잴 능력이 있다**.
사전등록대로 이게 실패했으면 전 arm 판독금지였다(`positive-control-before-reading-a-negative`).

### ② 결함 위치가 갈렸다 — 다양성이 아니라 **반증가능성**
동결 bar = `dist≥5 ∧ fals≥1`. `dist` 는 **4/4 셀 전부 통과**(5~6)하고 `fals` 만 **4/4 전부 0**.
⟹ G6 실패는 "생각이 다양하지 않다" 가 아니라 **"반증가능한 주장을 만들지 못한다"** 이다.
`_g6_is_falsifiable` 은 comparator ∧ measurable ∧ ≥2 content ∧ 비질문 ∧ 비-stance 를 요구하는데,
모델이 그 형식을 **아예 안 낸다**. (H_6186 이 지적한 'FALS 는 FORM-only 라 게임가능' 함정의 반대편 —
여기선 0 이라 게임당한 게 아니라 형식 자체가 부재다.)

### ③ H_9801 의 핵심 물음 답: **G6 는 G1 하류가 아니다**
`composed` vs `atomic` 가 **두 mouth 모두에서 무차이**(ByteGPT 6=6 · CLM 5 vs 6 으로 atomic 이 오히려
높음). 사전등록 판독표의 "양 seed-class 동등 ⟹ G6 독자 벽" 분기가 성립.
⟹ 착상 결함은 재조합 결함의 그림자가 아니라 **별도 faculty 결함**이다. 두 mouth 독립 재현.

### 정직한 한계
**셀당 seed 1개**다. H_9804 에서 방금 배운 교훈(단일 draw 위에 판정을 세우지 마라)이 그대로 적용된다 —
`--seed-offset` 으로 seed 반복하는 것이 이 판정의 다음 관문이다. 다만 ①`fals=0` 이 4/4 로 완전 일치하고
②`composed≈atomic` 이 두 mouth 에서 독립 재현됐다는 점에서, 구조적 결론(독자 벽 · 반증가능성 결함)은
단일-draw 잡음으로 뒤집히기 어렵다. 등급은 **DIRECTIONAL**, seed 반복 후 승급 판단.

### 재개(사전등록)
① `--seed-offset` ×8 로 4셀 전부 반복 → `fals=0` 과 `composed≈atomic` 이 유지되는지
② 유지되면 G6 프런티어를 **"반증가능 주장 생성"** 으로 재정의(다양성 레버는 이미 통과이므로 무의미)
③ H_9803 branch-latent 는 다양성 레버인데 `dist` 는 이미 bar 통과 ⟹ **우선순위 하향** 재검토 필요.

## related
H_9775 · H_9698 · H_6186 · H_6189
