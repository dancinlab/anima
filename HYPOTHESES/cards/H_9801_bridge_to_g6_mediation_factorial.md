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

## related
H_9775 · H_9698 · H_6186 · H_6189
