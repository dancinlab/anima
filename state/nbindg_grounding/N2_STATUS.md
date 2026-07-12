# NBIND-G N2 (grounding) — 외부데이터로 UNBLOCK → FIRE-READY (2026-07-12)

N2 = NBIND-G grounding 본체(극성이 자연 분포서만 접지된 P_nat 원자에 grid 학습 XOR 연산자 적용?).

## 이력
1. **NSMC-only pre-fire = INVALID (DATA-scale-blocked)** — 순수인증 자연 감성원자 재고 부족(k=4/pol<10).
2. **외부 감성코퍼스 확보($0 공개 다운로드)** → **UNBLOCK**: naver_shopping 200k(상품·`rating\ttext`) +
   steam 100k(게임·`label\ttext`) + NSMC 150k(영화) = **450k·3도메인**. gen_nbindg_n2 `--corpora`로
   pool 마이닝. ⟹ purity≥0.85 P_nat = **k=15/pol** → pre-fire **PASS**. (owner-gated로 오판했던 데이터획득이
   실제로는 $0 로컬 = anti-punt 정정.)
3. **Fable exposure-matched 레시피**(`FABLE_N2_RECIPE.md`) — STAGE-1 exposure-confound 재발 방어: 노출은
   라인수 아닌 **바이트** 현상. 옛 `NSMC_FILLER_MULT=8`(라인)은 f_grid≈0.059 → 20k step서 grid 노출 1.2k≪
   E*12k = 미리 만들어진 INVALID. 수정: 바이트비율 knob + P_nat 편향채움(atom당 occ floor 30) + **T =
   ⌈1.25×E*/f_grid⌉** + grid재현 게이트 + flip0/flip1 분해.

## 빌드 결과 — 모든 게이트 GREEN (seed 7 · `N2_PREFIRE_AUDIT.json`)
| 게이트 | 값 | 판정 |
|---|---|---|
| P_nat viable (occ floor 30 후) | 29 (좋=authored 충돌 드롭) | ✅ |
| n_eval items | 174 (≥120) | ✅ |
| f_grid (bytes) | 0.1426 | — |
| **T_required** | **105,169 step** (=⌈1.25×12000/0.1426⌉) | exposure OK |
| V_F (P_nat in authored / eval-seed in train) | 0 / 0 | ✅ PASS |
| byte-match base_only vs main | 0.98 | ✅ |
| PREFIRE_PASS | **True** | 🔥 fire-ready |

## 4-arm fire (frozen · Fable §3)
| run | corpus | seed | isolates |
|---|---|---|---|
| main-s7 | grid + filler | 7 | 주장: operator × 자연 grounding |
| main-s11 | grid + filler | 11 | seed robustness (V5) |
| base_only | filler(+pad) | 7 | crux: 자연 LM 단독이 설치하는 것(약 예측) |
| shuffle_grid | coin-grid + filler | 7 | format-without-operator |
전부 `--arm ctrl --objective ce_marginal --canon --bf16`, **T=105,169 step** 동일. eval=`--xbind
n2_eval_manifest.json`.

## frozen validity 게이트 (pre-verdict · Fable §4)
(a) main seen P_grid D-acc ≥0.85(grid 설치·아니면 under-exposed INVALID) · (a′) shuffle coin-seen ≥0.85
(control liveness) · (b) T×f_grid ≥1.25×E*(빌드서 확인✅) · (c) V-F(✅) · (d) 2 seed 동일측 bar.

## frozen verdict grid (Fable §5 · Δ는 max(control,0.50) 대비)
- **NAT-CRACK 🟢(grounded)**: 양 seed Δ(main−base_only)≥0.20 ∧ Δ(main−shuffle)≥0.20 · gates pass ·
  base_only∈[0.40,0.65].
- **FORMAT-🧱**: Δ vs base_only≥0.20 이나 Δ vs shuffle<0.20.
- **MODEL-🧱**: gates pass·grid설치이나 Δ<0.20. flip0(=pol 직접·grounding liveness)/flip1(=operator 적용)
  분해 필수 → flip0 낮음=GROUNDING-🧱, flip0 높음+flip1 낮음=operator-transfer MODEL-🧱.
- **INVALID**: 게이트 실패. ckpt는 항상 PULL(a_fire_recover_complete).

## 상태 = FIRE-READY · wall 실측 → rent=spend owner $go 게이트
corpora summer push 완료(`~/nbindg_n2/`). **calibration(summer RTX5070·345M CLMConvMoE): 500 step=228s
→ 2.19 steps/s → T=105,169 = 13.3h/run**(CE 5.68→0.96 정상학습). Fable §6 규칙 >10h/run → **rent 4-way**.
- **rent**: 총 ~53 GPU-h(4 arm×13.3h) × ~$0.4/hr ≈ **~$21** · wall 13.3h(4 pod) or 26h(2 pod) = **rent=spend
  owner $go 필요**.
- **$0 pool**: aiden 303M heavy OOM 위험(mem) → summer-only 순차 ≈ **53h(2+일)** = 비현실적.
⟹ frozen-first(과학을 예산에 맞춰 재단 안 함·Fable 29atom·occ floor 30·T=105k 유지)이라 합리적 경로=rent이나
**rent=spend=owner $go 게이트**. FIRE 커맨드(각 arm): `anima-py train --arch clm --canon --arm ctrl
--objective ce_marginal --corpus n2_<arm>_train.txt --cell-label en-general --steps 105169 --batch-size 8
--bf16 --seed <7|11> --out natem_n2_<arm>.clm` → PULL ckpt(a_fire_recover_complete) → seen-0.85 게이트 →
`anima-py evaluate <ckpt> --xbind n2_eval_manifest.json`(PYTHONUTF8=1) → flip0/flip1 분해 → verdict.
NEXT: owner $go(rent) 시 4-arm 발사. (별도: summer anima-py stale evaluate-py-11 → eval 전 재설치.)

## 산출
`gen_nbindg_n2.py`(멀티코퍼스+exposure-matched·all-green) · `N2_PREFIRE_AUDIT.json` · `n2_eval_manifest.json` ·
`FABLE_N2_RECIPE.md` · 코퍼스=regenerable(`--corpora`·외부데이터 `~/g1_natem/`). card H_9286.
