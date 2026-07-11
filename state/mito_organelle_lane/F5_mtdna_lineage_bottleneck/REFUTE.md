# REFUTE — H_9277 / F5 (mtDNA 독자 계보) 적대적 검증

- **판정: 반박 실패 (refuted = false) · 원 verdict 🔴 THEATER 유지**
- 검증자: 적대적 재현 + 원 실험에 **없던 더 강한 통제 3종 추가 발사**
- 재현 아티팩트: `scratchpad/refute/{f5.py,probe.py}` (원 `run.py` 무변경 복사본 + counter-control)

## 0. 요약

원 결론을 깨려고 6개 공격축(예산 불공정 · tunable FORM · 누출 · seed 분산 · p5 · tune-to-green)을 전부
걸었다. **어느 축도 결론을 뒤집지 못했다.** 오히려 내가 새로 만든 *더 강한* lineage-only 통제
(분포-정확 채널셔플)에서도 Δ가 그대로 0으로 붕괴했다. 다만 문구 하나("정확히 노이즈")는 과대이고,
사소한 구현 결함 1개(분산매칭 off-by-one)를 찾았는데 **둘 다 null에 보수적(=결론을 강화)** 방향이다.

## 1. 재현 (determinism)

- `run.py`를 `PYTHONHASHSEED=0` / `=12345`로 재실행 → `result.json`이 **wall_sec 제외 완전 동일**,
  그리고 **레포에 실린 result.json과도 완전 일치**. 보고된 모든 수치(EXP 0.5593 · C1 0.8010 ·
  C2 0.8222 · C3 0.5505 · ORACLE 0.8051 · UNIFORM 0.5414 · diag 0.6239, 전 paired Δ)가 그대로 나옴.
- 수치 위조·선별보고 없음. RESULT.md ↔ result.json 표 대조 100% 일치.

## 2. 체크리스트별 반박 시도

### ① control 예산 공정성 → **불공정 아님 (오히려 EXP에 불리하게 세팅됨)**
전 arm이 동일 cell(16)·동일 gen(14)·동일 host GD step(60/gen = 840)·동일 파라미터 d(w)+d(g)·
동일 task·**동일 채널노이즈 실현(paired)**·동일 held-out(3 draw)을 쓴다(코드 확인: `train_gen`이 arm
무관하게 같은 step 수, `rng_eta`가 arm 간 공유).
C1/C2는 게놈에 *추가 최적화 신호*(host `|w|` 복사 / CE gradient)를 받으므로 **실험 arm에 보수적**이다.
여기서 중요한 논리 방향: 통제가 과대예산이면 **양성 주장**이 무효화될 뿐이고, **음성 판정은 통제가
강할수록 더 위태로워야 정상**이다. 그런데 EXP는 *분산·cadence까지 동률로 맞춘* C3(추가정보 0)에게도
못 이긴다 ⇒ "통제가 세서 졌다"로 음성을 설명할 수 없다. INVALID 사유 아님.

### ② 양성이 tunable FORM인가 → **역방향으로 정확히 그 이야기다 (THEATER의 교과서적 형태)**
EXP는 σ·thread **FORM 만점**(herit 0.769 · host_indep 0.872 · gdiv 10.0 · uniparental 합착 발생)을
받고도 reach Δ = 0. FORM(계보의 '값')은 σ_mut로 조율 가능하고, BIND(reach)는 earned되지 않았다.
`self-fold THEATER`와 동형. **THEATER 딱지가 붙은 쪽이 실험 arm**이므로 이 축은 원 결론을 지지한다.

### ③ held-out 누출 → **없음**
`make_task`가 Xtr/Xhe를 독립 draw, 라벨노이즈 독립. 학습은 `Xtr`+train-eta로만, 평가는 `Xhe`+별도
eval rng로만. 게놈 갱신도 held-out을 절대 읽지 않는다(`bottleneck_divide`/`uniparental_fuse`가 w·CE·acc를
인자로 받지 않음, EXP는 `ce=None`). 누출 0.
(nit: eval rng seed `555+seed+t`는 (seed,t) 쌍에서 충돌하지만 **arm 간에는 동일** = paired 유지 →
Δ에 편향 없음.)

### ④ Δ가 seed 분산 안인가 → **그렇다. 그리고 이게 결론이다**
EXP−C3 = +0.0088 ± 0.0334, wins 3/6, per-seed 부호 뒤집힘. σ_mut 0.10/0.35/1.00 전부 ΔEff≈0.
동시에 EXP−C1/C2 = −0.24/−0.26, **0/6** — 사전등록 PASS는 분산 문제조차 아닌 완패.

### ⑤ p5 위반 → **없음 (구성적으로 불가)**
`run.py` 전체에 emit/speak/silence 함수가 **아예 존재하지 않는다**(grep 확인 — 주석의 'emit' 언급뿐).
ATP는 표현형성(gate) upstream에만 배선. `if ATP<k: silence` 류 하드코딩 게이트 0.
예산 고갈이 강제하는 건 silence가 아니라 **용량 축소**(eff_ch EXP 16.8 vs C2 2.0). p5_clean 확인.

### ⑥ tune-to-green 흔적 → **없음 (애초에 green이 없다)**
사전등록 카드가 `FAIL(예상 유력)`·THEATER 위험 5위를 **미리 적어뒀고**, 실측이 그 null과 일치.
σ_mut 3점 전량 보고(은폐 0), primary(0.35)는 카드에 사전지정. RESULT.md가 이전 rng 버전(hash(arm))의
결과(EXP−C3=−0.001)까지 자진 공개 — 결론 동일. 하이퍼를 흔들어 얻은 양성이 존재하지 않는다.

## 3. 내가 추가로 발사한 counter-control (원 실험에 없던 것)

원 C3(iid 재추첨)는 "EXP의 g-std만" 맞춘 약한 매칭이므로, **더 강한 lineage-only 통제**를 새로 만들었다.

- **C3-PERM (분포-정확 계보파괴)**: EXP의 *실제* 게놈 g_t를 그대로 쓰되 **채널만 per-cell 셔플**.
  ⇒ 값 분포·per-cell 다중집합·세대별 std·세대간 값 자기상관 전부 EXP와 **정확히 동일**, 오직
  "어느 채널이 ATP를 물려받는가"의 계보 연속성만 파괴. 가능한 가장 공정한 lineage-only 통제.
- **C3-EXACT**: 원 C3의 분산매칭 **off-by-one 수정**(아래 §4)판.
- **장기 드리프트 gens=40**: "14세대는 파워 부족" 반박 시도.

| (6 seed · σ_mut=0.35 · paired) | EXP | C3-EXACT | C3-PERM | UNIFORM |
|---|---|---|---|---|
| gens=14 (primary) | 0.5593±0.0327 | 0.5458±0.0101 | **0.5540±0.0224** | 0.5414±0.0086 |
| gens=40 (장기) | 0.5829±0.0451 | 0.5357±0.0133 | 0.5431±0.0125 | 0.5377±0.0104 |

- **EXP − C3-PERM (primary) = +0.0053 ± 0.0260, wins 4/6** ⇒ 가장 강한 통제에서도 **ΔEff≈0 재확인**.
  원 보고(+0.0088±0.0334, 3/6)와 같은 결론. **계보가 나르는 task 정보량 = 0** 확정.
- **best-of-K readout**(다양성 뒷문): EXP 0.6541 vs C3-PERM 0.6592, Δ=**−0.005**, 3/6 ⇒ 계보 다양성
  이득도 없음. 원 보고가 acc_best를 판정에서 뺀 게 결과를 숨긴 것도 아님(넣어도 음성).
- **장기(40세대)**: EXP−C3-PERM = +0.040 ± 0.057 (wins 4/6) — **여전히 seed 분산 안**, 신호 아님.
  그리고 C1/C2(0.80/0.82)와는 여전히 −0.22. 파워 부족으로 음성이 나온 게 아니다.

## 4. 찾아낸 결함 2건 — 둘 다 **null에 보수적** (결론 강화)

1. **C3 분산매칭 off-by-one**: `std_sched[t]`는 EXP의 gen-t **갱신 전** g-std라서 C3는 항상 **한 세대
   뒤진(=더 작은) 분산**을 쓴다(예: 최종세대 1.087 vs 참값 1.154). 즉 C3가 살짝 **약하게** 세팅됨.
   고쳐서 재측정 → EXP−C3-EXACT = **+0.0135±0.0289 (3/6)** — Δ가 오히려 *커지지만* 여전히 ΔEff≈0.
   ⇒ 이 버그는 **거짓 음성을 만들 수 없다**(EXP에 유리한 방향). 결론 불변.
2. **문구 과대**: "정확히 노이즈(exactly noise)"는 강하다. 장기 horizon에서 EXP가 UNIFORM/C3 대비
   +0.04 언저리로 뜨는데, 이는 계보가 task 정보를 나른 게 아니라 **지속하는 gate에 host w가 세대를
   누적해 co-adapt**하는 부수효과(+ 랜덤 집중 게이트의 chance-floor 볼록성)로 보인다. 신호 기준(Δ vs
   ≥2 control, 부호 안정)엔 못 미치므로 판정은 안 바뀌지만, 정직한 문구는
   **"선택압 없는 계보는 어떤 통제 대비로도 reach 신호를 만들지 못한다(ΔEff≈0)"**여야 한다.

## 5. 구조적 관찰 (판정 불변, 기록용)

EXP arm의 게놈 갱신 경로(`bottleneck_divide` / `uniparental_fuse(ce=None)`)는 **w·CE·acc를 인자로 아예
받지 않는다** ⇒ 성능→게놈 정보채널이 **구성적으로 0**. 즉 F5의 null은 사실상 *선험적으로 보장*된
것에 가깝고, 이 실험의 값어치는 "증명"보다 **(a) 계측기 유효성 확립(dynamic range 0.28 · 양성대조
3개 PASS) + (b) FORM 만점/BIND 0의 THEATER 표본 확보 + (c) F11 사전제약**에 있다.
RESULT.md의 "기계론적 확증"은 엄밀히는 **구성적 확증**이다. (과대주장 아님 — 카드가 이미 "F5 단독은
bite 못한다"고 사전 플래그.)

F11 인계 제약도 타당: diag drift+선택(0.624)조차 C1(0.801)·C2(0.822)에 한참 못 미치므로 **F11의 PASS
바는 "drift보다 낫다"가 아니라 "C1/C2를 넘는다"**여야 한다. 이 제약은 유지되어야 한다.

## 6. 최종

| 축 | 결과 |
|---|---|
| controls_fair | ✅ (동일 예산 · paired 노이즈 · 통제가 오히려 강함) |
| held-out | ✅ 누출 0 |
| Δ vs ≥2 control | ✅ 음성 (−0.27, 0/6) · lineage-only 통제 3종 전부 ΔEff≈0 |
| p5_clean | ✅ emit 코드 부재 |
| tune-to-green | ✅ 흔적 없음 (사전등록 null 적중 · σ 전량보고) |
| 재현성 | ✅ byte-identical |

**refuted = false · final_verdict = 🔴 THEATER (유지).**
권고: RESULT.md의 "정확히 노이즈" → "선택압 없는 계보 = reach 신호 0(ΔEff≈0)"으로 문구 조정,
그리고 §4-1 off-by-one은 F11 재사용 전에 수정할 것(F11에서는 방향이 보수적이지 않을 수 있음).
