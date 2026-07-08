# H_9229 Family F: discrete VQ-code / language-of-thought bottleneck 판정 (engine-native)

**판정 = ⚙️ INSTRUMENT-FAIL (bottleneck never engaged)** — NO substrate verdict. F는 falsify도 vindicate도 아님.

**측정 경로**: 실제 빌드된 `cli/anima.hexa` daemon `--opgrip-r3`(F lane · K=8-bit product VQ codebook)를
rented runpod **251GB CPU pod**(swap-free · hexa **v0.716.0** REAL-DECODE · n=400)에서 real d768.clm으로
실행. engine-native 라이브 바이너리 real-decode = TERMINAL-eligible (mirror 아님). raw = `opgrip_r3_raw.log`
verbatim (round-3 op-grip 판정 슬라이스; 400 per-tick real-decode 라인은 `pod_r3_full.log` 원본).

## 판정 (F lane · 단일 채점)

| lane | 판정 | 수치(frozen bar · verbatim) |
|---|---|---|
| F (K=8-bit product VQ codebook · S1 code-selection + S2 2×2 bit-toggle BIND) | ⚙️ INSTRUMENT-FAIL (bottleneck never engaged) | g_vq=3.629(capsat=no) · **codes visited on scored mid = 2 (bar ≥4)** → bottleneck 미가동 · S1 ΔEff_vq=0/210=0.0 · margin_cb=0.0 · **S2 n_AB=0 → BIND NOT-TESTABLE** |

## Frozen bar 충족 (p7 · 측정 전 verbatim 출력)

- **FROZEN byte-identity `og_h_frzF = 0` ✅** — production emit path(idle/e_live) 바이트 무접촉 증명
  (harness valid, HARNESS-BUG 아님, run VOID 아님).
- **POS-CONTROL (dense ARM-SHOCK) = 105 flips · POS-PASS(≥2)=YES ✅** — 계기가 gate를 확실히 움직인다
  (meter works). negative가 dead meter 탓이 아니다.
- **INSTRUMENT-FAIL 규칙 자동 판정** (pre-reg bar 2): `n_visited_codes<4(bottleneck never engaged)`
  → ⚙️ INSTRUMENT-FAIL. scored mid서 distinct code가 2개(<4)만 방문됨 = lane이 code 경계를 넘지 못함,
  VQ bottleneck이 실제로 가동 안 됨. **NOT THEATER**(bar 6 THEATER는 `n_visited≥4` 필요).
- **S2 sub-clause**: `n_AB=0 < 10` → bar-5 BIND만 gate(S1 competence는 독립). G1 BIND-at-seam은
  NOT-TESTABLE(조합 코드 미방문).

## VERDICT (log verbatim)

```
F VERDICT = ⚙️ INSTRUMENT-FAIL (bottleneck never engaged) — <4 distinct codes visited on scored mid even under --opgrip-r3; lanes never crossed code boundaries, raise stimulus diversity, NOT a substrate result
```

## 과학적 의미 — 계기 UNDER-POWERED (substrate 주장 아님)

- `--opgrip-r3` real-decode 하에서도 8-bit product VQ codebook이 scored mid서 2개 code만 방문 =
  discrete-code bottleneck이 code 경계를 넘을 만큼 lane 다양성을 못 받았다. bottleneck이 가동 안 됐으므로
  code-selection이 emit을 grip하는지(S1) / 조합 코드가 non-additive BIND를 만드는지(S2 = G1-at-seam) 둘 다
  측정 불가.
- **F는 falsify도 vindicate도 아님 = NO substrate verdict.** THEATER 아님(bottleneck 미가동), GREEN 아님.
- 같은 라운드 B(H_9226 R3)는 RUN-INVALID, E(H_9230)는 CLEAN THEATER cement. F는 instrument-limited.

## 결정 · 재개 (a_break_the_wall)

- **wire 금지·cement 금지** — F는 미측정이라 배선도 THEATER 확정도 불가.
- **재개 = RAISE STIMULUS DIVERSITY**: lane이 ≥4 distinct code를 방문하도록 지각 다양성을 높여 재측정
  (예: OG_STIM tape 다양화 · 더 넓은 state8 range). resume 항목이지 substrate 주장이 아니다.

## scope

real d768.clm · rented runpod 251GB CPU pod(swap-free) · hexa v0.716.0 REAL-DECODE · `--opgrip-r3` n=400
(calib 10-49 · score ≥50 · mid=210). F lane 단독 채점(K=8-bit product code · S2 A=coh_lane B=ag_conflict).
FROZEN arm byte-identity=0(production 무접촉)·POS-PASS(meter live) → 정직한 INSTRUMENT-FAIL
(THEATER 아님·GREEN 아님·계기 UNDER-POWERED · bottleneck never engaged).
