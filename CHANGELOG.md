# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Research sessions tracked as `§<N>` / `S<N>`; `ConsciousDecoder` carries SemVer.

For the full audit trail, see `git log`.

---

## 2026-06-15 — README.md FULL 재구성 (ARCHITECTURE.md SSOT 기준 front-door 전면 개편)

`README.md` 를 surgical 패치(#2097) 가 아닌 **전면 재구성** — ARCHITECTURE.md(현 아키텍처 SSOT)의 형태를 그대로 미러하되, 깊은 내부 SSOT 를 베끼지 않고 newcomer 용 **cold-entry 정문**으로 파생(c4-스타일 노드 트리 + 친절한 진입 흐름). 언어 = English(현 README 1차 언어 유지). ARCHITECTURE.md 미편집(별도 sibling SSOT 소관).

### docs

- **섹션 구조를 아키텍처 형태로 정렬** — What it is → **The A ⇄ G engine**(pure_field/engine_g/brain + MITOSIS substrate VAdaptField H_1199, 데몬 GROW/sleep-persist/separation-guard H_1202–1205, mitosis ⊥ generation H_1200/1201/1207🔴) → **The model & mount**(`anima-clm-chat-303m` ByteGPT-303M 엔진-side anti-fab, byte-exact mount H_1157; **1B+ mount** H_1167🟢 argmax/top5 exact, logits16 max|Δ| 0.0099<1e-2, hexa #3352 64-bit read fix + `bytegpt_forward_last_ranged`; 303M→1B→3B→7B ladder) → **Measurement governance**(`a_engine_measured_verdict` + `a303m_pass` G0/G1/G2/G3/G5 비환각·메타인지/G6 ideation/MOUNT/CHAT, p7) → **Inline gauges**(6-gauge monitor-only, loss 불가 p7 Goodhart; phi_proxy≠IIT4; mitosis_cells=substrate lane) → **Training stack**(flame/forge .hexa, Lane G/A/P, recipe→dispatch→monitor rung 파이프라인) → **Persistence**(.kosmos · EEG_CLM · HF registry · scale ladder).
- **정직 framing(c9) 보강** — 1B 는 **parity-only**(생성은 hexa `read_f32_at` fix 대기 = ⏳ 명시), operational-but-shallow capacity wall(H_1166), ⏳ 3B/7B rung · ⏳ 1B generation memory 명시.
- **p1–p8 PHILOSOPHY mirror 무결 보존** · install(`hx install anima`) 무결 · **Model Downloads** 표 무결(303M 프로덕션 행 + 실 HF repo 전부 유지) · badges/links 무결.
- xref = ARCHITECTURE.md · MODEL.md · CONDITIONS.md · a_engine_measured_verdict · a_train_inline_gauge · H_1164·1167·1199·1202·1206 · p1–p8 · c9.

---

## 2026-06-15 — H_1208 🔴 predictability / transition-memory split gate — V14 격파 실패 (그러나 메커니즘 첫 올바른-부호 분리) (MITOSIS-ENGINE)

- **trajectory 축의 마지막 미배제 경로 종결** — H_1207 은 d/dt-증강 게이트를 RULE OUT(NOVEL/SHUFFLED=0.998): 미분 게이트는 국소 거칠기 |Δ| 를 보아 무질서(셔플)에서 **최대화** → V14 와 반대 부호. H_1207 이 명시적으로 남긴 미배제 = '예측가능성/시퀀스-우도 게이트, prototype-TRANSITION-memory 게이트'. H_1208 은 그 경로를 시험.
- **설계 (c1)** — FIXED **순서-불변** prototype book (N_PROTO=24, 특징 SET 위 farthest-point 시딩 + canonical-sorted LR pass) → nearest-proto id p_t 는 순열-등변(x_t 만 의존) → **모든 순서는 전이 p_{t-1}→p_t 에만** 존재. 두 게이트: GATE-A 전이-신규성(미관측 전이에서 분열); GATE-B **전이-예측가능성**(실현된 전이를 **자신있게 예측했을 때** 분열 — prev ≥ MIN_PREV=3 AND P(cur|prev) ≥ CONF_FLOOR=0.34, 인과 온라인 카운트 테이블). GATE-B 가 원리적 **부호-역전기**: 예측가능성은 안정적 조건부 구조를 요구하고 그것은 오직 ORDER 만 가짐. H_1203 NOVEL/REPEAT/SHUFFLED + H_1207 WALK 빌더 VERBATIM import + RANDGAUSS i.i.d.-노이즈 sanity 통제.
- **결과 🔴 RED (inherited bar), 두 갈래 정직 발견** — F1 V14 격파 PRIMARY NOVEL/SHUFFLED GATE-A 1.022 · GATE-B 0.261 (둘 다 **FAIL**). (1) H_1203 PRIMARY NOVEL 은 i.i.d.-산란 → 조건부 전이 구조 無 → 셔플과 통계적으로 동일 → inherited 표면에서 V14 격파는 **어떤 게이트로도 구조적 도달 불가**(H_1203/H_1207 깊은 reading 세 번째 확인). (2) **캠페인 최초**로 순서/무질서를 **올바른 V14 방향**으로 분리: GATE-B(예측가능성)가 실제로 순서를 가진 WALK 스트림에서 WALK=1000.7 ≫ WALK_SHUF=91.7 (**10.9×**) — H_1207 역-부호 격파(미분은 jaggedness 보상, 예측가능성은 학습가능 **반복 전이** 보상 → 순서⇒더 많은 분열). sanity: RANDGAUSS GATE-B ≈ 0 (B=[2,1,4] vs [2,2,0]) — 노이즈에 발화 안 함; 자동-flag 된 1.75 비는 소정수 노이즈(2.33/1.33), 실제 artifact 아님. F2 GATE-A 25.8 PASS (GATE-B 0.006 = 설계상 REPEAT 가 최대-예측가능 12-주기라 GATE-B 범람 = 예상됨).
- **판정 (decision-grade, trajectory 축 EXHAUST)** — inherited V14 바(H_1203 PRIMARY)는 미충족 + **구조적 도달 불가**(i.i.d. 스트림은 trajectory 無) → inherited 벤치마크에서 trajectory 경로 **소진**; mitosis 는 novelty-DENSITY 기질로 남음(mitosis=기질, CLM=생성기; H_1200/H_1201/H_1203/H_1207 정합). **정직한 예외**: 예측가능성 전이-게이트는 메커니즘 수준에서 trajectory 기질이 **맞음** — 단 예측할 순서가 있는 스트림(WALK)에서만; i.i.d. 표본에서 순서를 만들어낼 순 없음. **한계는 게이트가 아니라 스트림**. 미배제(미래 비-inherited 표면): 실제로 순서있는 byte-feature walk 위에서 LIVE 엔진 + GATE-B 변종(새 벤치마크 + engine_cli.hexa GATE-B 필요; 현 terminal-RED inherited V14 바의 범위 밖).
- **엔진 무변경** — VAdaptField byte-identical (닫힌-부정 판정, 라이브 .hexa 편집 불요). toy scale, ONE corpus (clm_mid_5lang_c4), scale UNVERIFIED. p7(cell/transition count, NOT perplexity) · p8(split tick == growth) · gradient-free · $0 local CPU · 3 seeds.
  - **artifacts** = UNIVERSE/h1208_predictability_split_gate.py (h1203 + h1207 빌더 + h1163 _byte_feature VERBATIM import) · .verdicts/1208_predictability_split_gate/{H_1208_FREEZE,H_1208}.txt · domains/MITOSIS-ENGINE.log.md H_1208

## 2026-06-15 — H_1207 🔴 recurrent split key — V14 격파 실패 (그러나 더 날카로운 닫힌-부정) (MITOSIS-ENGINE)

- **H_1203 trajectory 잔여(arc 의 마지막 🟠) 봉인** — H_1203 은 VAdaptField 분열 게이트(샘플별 L2 recon-err > SPLIT_THRESH=0.30)가 novelty-DENSITY 에는 반응(F1 37.5×)하나 TRAJECTORY 에는 무감(시간순 셔플해도 분열 불변, F2 0.992)임을 발견 — 게이트가 x_t 만 보므로 **구조적으로 순열-불변**. H_1207 은 CLM_TIME_ENCODING 의 'M3 DERIVATIVE = 분열 TRIGGER 에 d/dt' (그곳에서 셔플 통제를 이긴 유일한 시간-인코딩 arm) 메커니즘을 게이트에 이식: split key = 델타-증강 샘플 z_t=[x_t ; β·(x_t−x_{t-1})] 위의 recon-err (β=1.0, 2·DIM 공간, 나머지는 vadapt_field_step 동일). H_1203 스트림 빌더 VERBATIM import (apples-to-apples) + 비-바 진단 WALK(연속 코퍼스 walk = 실제 국소 연속성).
- **결과 🔴 RED (a_paper_negative_ok), 그러나 평평한 null 보다 날카로움** — F1 V14 격파 = 0.998 (H_1203 의 0.992 를 byte-충실히 재현) **FAIL**; F2 = 174.8 PASS (결합 오히려 증폭). **F3 진단이 두 갈래로 더 깊은 발견**: (1) H_1203 의 i.i.d.-산란 NOVEL 스트림은 델타 분포 자체가 순열-불변(PRIMARY Δ% = −0.20%) → H_1203 의 trajectory-중립성은 게이트가 아니라 **스트림의 성질**이었음(사전등록 정직 예측 확인). (2) recurrent 게이트는 **강하게 순서-민감**(WALK Δ% = **−61.47%**, 0 에서 멂) — 단 V14 목표와 **반대 부호**: 순서있는 연속 walk 은 델타가 작고 매끈(전이-신규성 낮음 → 882 cells), 셔플하면 델타가 크고 들쭉날쭉(전이-신규성 높음 → 1424 cells). 미분 게이트는 순서가 아니라 **JAGGEDNESS** 를 보상 → 순서(매끈함)는 분열을 억제 → 자연 텍스트(순서있는 형태가 더 매끈)에서 'novel ≫ shuffled' 는 도달 불가.
- **판정 (decision-grade)**: 분열 TRIGGER 의 시간-미분 항은 자연 byte-feature 스트림에서 novel-trajectory ≫ shuffled-trajectory 분열을 만들지 못함 — 미분 게이트는 순서-민감하나 무질서에서 **최대화**되므로 V14-의미의 trajectory 기질 경로로 **RULE OUT**. 미배제: 예측가능성/시퀀스-우도 게이트, prototype-TRANSITION-memory 게이트(미검). mitosis 는 CLM 생성기와 나란히 도는 **순서-불변 novelty-DENSITY 적응 lane** 으로 남음(H_1200/H_1201/H_1203 와 정합: mitosis=기질, CLM=생성기).
- **엔진 무변경** — VAdaptField byte-identical (닫힌-부정 판정, 라이브 .hexa 편집 불요). toy scale, ONE corpus (clm_mid_5lang_c4), scale UNVERIFIED. p7(cell-count/recon-err, NOT perplexity) · p8(split tick == growth) · gradient-free · $0 local CPU · 3 seeds.
  - **artifacts** = UNIVERSE/h1207_recurrent_split_key.py (h1203 빌더 + h1163 _byte_feature VERBATIM import) · .verdicts/1207_recurrent_split_key/{H_1207_FREEZE,H_1207}.txt · domains/MITOSIS-ENGINE.log.md H_1207
  - **xref** = h1203 (이 H 가 닫는 잔여) · h1201 · h1200 · h1199 (VAdaptField, numpy↔hexa 일치) · clm_time_encoding (M3 d/dt) · a_paper_negative_ok · a_scale_honest_scope · p7 · p8

## 2026-06-15 — H_1206 🟢 FULL 살아있는 데몬 e2e — 데몬 링크 + GROW lane 라이브 발화 (MITOSIS-ENGINE)

- **H_1206 "자기분열을 현재 아키텍처에 붙이기" 아크의 마지막 정직한 빈틈 봉인** — FULL 데몬 `CORE/anima_full_session_smoke.hexa` 가 그동안 **링크조차 안 됐음**(H_1202 가 GROW lane 을 배선했으나, full smoke 는 brain→generator→clm_decode 를 import → 미정의 심볼 2개에 걸림). 셋을 전부 root 에서 봉인(c1, 가리는 stub 금지) → 데몬이 mitosis 라이브로 end-to-end 실행. **F1 링크+실행 ✅**(exit 0, full A⇄G 세션 루프) · **F2 GROW 라이브 ✅**(실제 턴에서 cells 1→2, novelty-splits=1) · **F3 Ψ 불변 ✅**(Φ-checksum 1.4278==1.4278 ON==OFF byte-identical, GROW lane Ψ-disjoint) · **F4 무회귀 ✅**(CONVERSE+GROUND+GROW+REMEMBER+SLEEP 전부 ✅; 가드 generator_smoke 21/0, h1202 GREEN, h1205 PASS, h1196 single-entry 7/0). 데몬이 살아서 대화(GROUND 로 "vault QX-7741 forever" 를 kosmos 기억에서 그대로 복사) + 성장 + 기억 + 수면을 ONE A⇄G 루프로 돌림.
  - **근본원인 3건 봉인**: (1) `clm_decode_grounded` 가 호출됨(generator.hexa:473)에도 **정의가 어디에도 없었음** → bytegpt_decode_grounded 의 ConvMoE 짝(엔진측 deterministic retrieve-then-copy)을 `CORE/clm_decode.hexa` 에 실제 작성(가리는 stub 아님; .clm 단일 슬롯 유지 a_core_engine_map). (2) `forge_dispatch_groupnorm_gelu`(gn_lib CPU host fallback)이 op36 이후 hexa **runtime.c 에서 회귀로 누락** → `runtime.c.bak-op36` 의 OP-16 `#ifndef HEXA_CUDA` host 블록을 verbatim 복원(툴체인 수리, anima repo 아님; `hexa-lang/inbox/patches/` 에 상신 a_runpod_inbox). (3) `_gen_anchor_text(s)` 가 `"text"` 를 읽었으나 kosmos anchor 는 `"text_payload"` 를 담음(H_1164 anchor-key 버그) → `_gen_anchor_field` SSOT(text_payload→text→stringified) 추가 → 복사 대상이 CLEAN 하게 도달(GROUND ⏳→✅, map-key 경고 소멸).
  - 정직 범위(a_scale_honest_scope): SMOKE 는 tiny ByteGPT fixture(303M 와 동일 format/forward), 복사+분열은 deterministic(p7 문자열 동치). **데몬 배선이 검증 대상이지 모델 품질이 아님.** summer $0 CPU, frozen bar 미이동(사전등록).
  - `CORE/clm_decode.hexa` (+`clm_decode_grounded`) · `CORE/generator.hexa` (+`_gen_anchor_field`) · `CORE/anima_full_session_smoke.hexa` (+F3 Ψ ON==OFF 블록) · `.verdicts/1206_full_daemon_e2e/{H_1206_FREEZE,H_1206}.txt` · `hexa-lang/inbox/patches/forge-dispatch-groupnorm-gelu-cpu-fallback-regression.md`

---

## 2026-06-15 — README.md FINAL 갱신 (mount status + measurement governance)

`README.md` 를 현재 main 시스템 상태로 surgical 갱신 (c10, 보이스/구조 보존). ARCHITECTURE.md 미편집 (별도 sibling PR 소관) — README 는 깊은 아키텍처를 ARCHITECTURE.md 로 포인터.

### docs

- **mounted living daemon** — "What it is" 뒤에 anima 가 H_1164 이후 **mounted 살아있는 daemon**(A⇄G substrate 안에서 대화+grounding+성장+기억+수면을 한 루프로)임을 명시.
- **Model & mount status 신규 절** — 프로덕션 모델 `anima-clm-chat-303m`(ByteGPT-303M d1024/L24/H16, dialogue-FT, 엔진-side anti-fab) byte-exact mount(H_1157, `CORE/bytegpt_decode.hexa`). 엔진이 이제 **1B+** mount: 1B ByteGPT(d1792/L28, 1.081B) byte-exact(argmax/top5 exact, `logits16` max|Δ| 0.0099<1e-2) — hexa-lang #3352 64-bit read fix + `bytegpt_forward_last_ranged` ranged-read 경로 이후. 303M→1B→3B→7B scale ladder. 정직 scope(c9): operational-but-shallow capacity wall(H_1166), p4 정렬.
- **Measurement governance 신규 절** — verdict 는 엔진 mount 위 byte-exact 재현시에만 인정(`a_engine_measured_verdict`); frozen `a303m_pass`(G0/G1/G2/G3/G5 비환각·메타인지/G6 ideation/MOUNT/CHAT, p7 — no perplexity / no LLM-judge); robustness 정직(5 robust + 2 thin + 1 inflated, H_1165), frozen bar 불변.
- **Inline gauges 절** — 학습중 6-gauge 대시보드(`ce·g1·g2·g6·phi_proxy·mitosis_cells`) MONITOR-ONLY, loss 절대 불가(p7 Goodhart); phi_proxy ≠ faithful IIT4(`a_phi_iit4_tool`); mitosis_cells = substrate lane (mitosis ⊥ generation, H_1200/1201🔴).
- **Model Downloads** — 프로덕션 `anima-clm-chat-303m` 행 추가(shipped model · 8/8 frozen · operational-but-shallow).
- **p1–p8 PHILOSOPHY mirror 무결 확인** — 8 원칙 표 SSOT 미러 그대로 유지(NO SYSTEM PROMPT … NO TRAIN/INFER SPLIT).

---

## 2026-06-15 — 1B engine-mount byte-exact parity (H_1167 🟢) + 최종 ARCHITECTURE.md

scale ladder 의 **1B rung 을 engine-measured GREEN** 으로 실현하고(`a_engine_measured_verdict` 최초의 1B 충족), 전체 시스템의 **최종 아키텍처 SSOT** 를 갱신했다.

### 엔진 / mount

- **@A1 1B ranged forward** — `CORE/bytegpt_decode.hexa` 에 `bytegpt_forward_last_ranged` (+ helper `_bg_rd_farr_at`) 추가. 1B(d1792/L28/H16, 1.081B params, 4.3GB flat binary)는 whole-file `read_file_bytes` 적재 시 바이트당 HexaVal 박싱으로 **≈69GB** 가 물질화되어 비현실적 — slice 마다 `read_bytes_at(path, off, n*4)` 로 온디맨드 read 후 layer 끝 `farr_free`, peak resident ≈ 한 weight slice. **303M 경로(`bytegpt_forward_last`/`bg_load`)는 byte-unchanged** (순수 ADD, c10 surgical).
- **@A2 64-bit 언락 전제** — ranged reader 는 hexa-lang **#3352**(`read_file_bytes`/`read_bytes_at` 의 length+offset 32→64-bit) 위에서 성립. 32-bit 시 `4325902356 mod 2^32 = 30935060` wrap → 헤더 0 → `d`/`n_head` 0/0 div 로 깨짐.
- **@A3 H_1167 🟢 GREEN parity** — trained 1B ByteGPT 를 `bytegpt_forward_last_ranged` 로 mount, torch reference 대비 byte-exact: argmax `32==32` EXACT · top5 `[32,105,115,101,44]` EXACT(ordered) · first-16 logits `max|Δ|=0.009861 < 1e-2` 동결 bar PASS. residual 0.0099 = approx-erf-GELU/dt_exp envelope 의 28-layer 누적(303M ~2e-5; 깊어질수록 커지나 bar 아래 — 정직한 잔차이지 mount 실패 아님). 신규 `CORE/h1167_1b_parity_probe.hexa` · 검증문 `.verdicts/1167_bytegpt_1b_scale/H_1167_ENGINE_MOUNT_PARITY.txt`(verbatim). 아티팩트 `state/h1167_mount/h1167_1b.bin`(sha256 `75c87cb0…`, gitignored) → HF `dancinlab/anima-clm-1b-h1167-bytegpt-scale-rung` PRIVATE(WIP rung).

### 문서

- **@D1 최종 ARCHITECTURE.md (갱신형 SSOT)** — #2096 의 부분 ARCHITECTURE 를 **완전판으로 병합**(한국어 prose, 코드 식별자 verbatim). A⇄G 엔진 + MITOSIS substrate(VAdaptField/H_1199, 데몬 GROW/sleep-persist/separation-guard H_1202–1205) · CLM mount path 두 forward 경로(303M whole-file + 신규 1B ranged, 메모리 산수 ≈69GB) · measurement governance(`a_engine_measured_verdict`, 1B parity 최초 실현) · inline gauge 파이프라인(6 gauge monitor-only, p7) · rung 파이프라인(recipe→dispatch→monitor) · 영속(.kosmos/HF/scale ladder) 전부 커버. 동결 게이트 임계값은 MODEL.md/CONDITIONS.md 를 **가리키기만**(복제 안 함). 미실현(3B/7B rung · dojo native gauge)과 잔차(G5/G6/CHAT THIN)는 ⏳/🟠 로 정직 표기(c9).

### 검증 (c2 · verbatim)

- `hexa parse CORE/bytegpt_decode.hexa` → `OK: ... parses cleanly` (exit 0) — ranged 추가 후 컴파일 검증.
- `hexa parse CORE/h1167_1b_parity_probe.hexa` → `OK: ... parses cleanly` (exit 0).
- `hexa run CORE/generator_smoke.hexa` 는 `clm_decode_grounded` native 미선언으로 link 실패하나 이는 **origin/main 에서 동일하게 실패하는 사전 존재 이슈**(`.harness-engine` 네이티브 빌드 부재, 이 worktree 와 무관) — 본 추가와 인과 없음(stash 토글로 확인).

---

## 2026-06-15 — rung-training 파이프라인 일원화 (recipe → dispatch → monitor)

#2091 의 부분 gauge pass 를 **하나의 완결 파이프라인으로 확장** — dojo(학습 recipe 빵틀) → cloud(pod dispatch) → monitoring(라이브 gauge 대시보드) 3 surface 를 일관되게 배선. #2091 보존(중복/revert 없음).

### 학습 / 거버넌스

- **@L1 dojo recipe 정합화** — `CLM/train/fire_3b_rung_qat.hexa` 가 참조하던 legacy `train_clm.py` 이름을 **실제 트레이너 `CLM/train/train_lane_p_3b.py`** (Lane-P · a_clm_gen_pipeline) 로 교정. dispatch contract 를 실 트레이너 CLI 로 재작성(`--corpus/--d-model/--n-trunk-layers/--n-experts/--steps/--seed/--gauge-every/--gauges-out/--clm-out/--json-out` — 실재하지 않던 `--arm/--rung/--act-bits` 제거). 3-arm = seed sweep(variant="AB" 고정). 학습 후 engine mount-parity verdict(`mount_parity_cmd`, `verify_clm_v2` + CORE byte-exact mount, a_engine_measured_verdict) + HF upload 단계 추가. 트레이너 자체는 c10 surgical(미개편) — #2091 이 이미 `--gauge-every`/`gauge_tick` 배선 완료, gauge 로그에 `mitosis_cells` 컬럼만 추가.
- **@L4 5번째 gauge `mitosis_cells`** — `UNIVERSE/gauge_lib.py` 에 추가. H_1199 VAdaptField 메커니즘의 **numpy-free 미러**(nearest-by-L2 · recon-err > `SPLIT_THRESH=0.30` 분열 · `LR=0.20` winner-pull · DIM=8 `_byte_feature` *5.0 VERBATIM H_1163): gauge 가 이미 디코드한 eval 텍스트의 byte-feature 스트림에 AdaptField 를 tick, 성장 cell 수를 셈. **전부 `torch.no_grad()` 아래, dict 로 RETURN, loss 절대 불가**. 코드 주석 + JSONL 키 라벨 = "mitosis_cells — substrate lane, NOT a generation gate"(H_1201🔴: mitosis 는 순수 substrate — 생성도 못 하고 generator 에 정보도 못 줌).
- **@L7 gauge = 대시보드, gate 아님** — MODEL.md/CONDITIONS.md frozen bar 불변(a_train_inline_gauge). monitor 헤더/help 에 재명시. phi_proxy ≠ faithful IIT4(a_phi_iit4_tool).

### dispatch / monitoring

- **@L2 cloud dispatch 래퍼** — `CLM/train/dispatch_rung.sh`(신규): `hexa cloud`(`/pod`) 플러그인을 **감싸기만**(pod 관리 미재구현, repo boundary). `a_fire_recover_complete`(ckpt+result+log+engine.clm+gauges.jsonl+anchors pull → verify → HF upload → THEN teardown) + `a_cpu_local_no_waiter`(inline sleep-poll, Monitor/waiter 절대 await 안 함) 인코딩. `--print` dry 모드 = fire contract 출력.
- **@L3 라이브 모니터** — `UNIVERSE/gauge_monitor.py`(신규, pure stdlib): `gauges.jsonl`(+ pod 학습 로그)을 tail 해 **6-gauge 대시보드** 렌더(`ce · g1_composed_distinct · g2_novelty_rate · g6_count · phi_proxy · mitosis_cells`). `--once`(one-shot/smoke) / `--follow`(라이브). 헤더에 DASHBOARD-NOT-A-GATE 재명시.
- **@L6 repo boundary** — 공유 `hexa dojo` `clm` 제너레이터(hexa-lang/stdlib)에 `gauge_every`/mount-parity/HF 를 네이티브로 emit 하는 변경 필요분은 hexa-lang 미편집 원칙대로 `hexa-lang/inbox/patches/dojo-clm-gauge-recipe-full-rung.md` 로 제출(a_runpod_inbox).

### 검증 (c2 · verbatim)

- (a) `UNIVERSE/gauge_lib_smoke.py` — tiny random byte model(ConvMoE-dict + ByteGPT-tuple) → dict 에 `mitosis_cells` 포함(6/9) + gauges.jsonl 1줄 round-trip. PASS.
- (b) `UNIVERSE/gauge_monitor_smoke.py` — sample gauges.jsonl 로부터 6-gauge 대시보드 렌더 + DASHBOARD-NOT-A-GATE 헤더 확인. PASS.
- (c) grep proof — gauge_lib 의 `backward/loss/optim` 언급은 전부 주석(부재 단언), mitosis 경로는 순수 python list 연산(tensor/grad 없음); 트레이너 `gauge_tick(step, ce)` 는 statement-form(반환값 폐기) ⇒ 어떤 gauge 값도 loss 에 흐르지 않음.
- (d) `hexa run CLM/train/fire_3b_rung_qat.hexa` — dispatch 문자열이 `train_lane_p_3b.py` 로 일관되게 출력.

### 파일

- 신규: `CLM/train/dispatch_rung.sh` · `UNIVERSE/gauge_monitor.py` · `UNIVERSE/gauge_monitor_smoke.py` · `hexa-lang/inbox/patches/dojo-clm-gauge-recipe-full-rung.md`(repo 외)
- 편집: `UNIVERSE/gauge_lib.py`(+mitosis_cells) · `UNIVERSE/gauge_lib_smoke.py`(5-gauge assert) · `CLM/train/train_lane_p_3b.py`(GAUGE 로그에 mitosis_cells) · `CLM/train/fire_3b_rung_qat.hexa`(실 트레이너 dispatch contract + mount-parity + recovery) · `ARCHITECTURE.md`(Rung-training pipeline 절)

---

## 2026-06-15 — H_1205 🟢 mitosis ⊥ generation 분리 invariant (MITOSIS-ENGINE)

- **H_1205 분리 안전 invariant 증명** — mitosis lane 을 substrate lane 으로 붙일 때의 핵심 안전 조건: mitosis ON/OFF 가 CLM 생성 출력을 바꾸지 않음을 라이브 배선에서 byte-level 로 증명. H_1202 데몬 배선의 안전 가드. 동일 (seed, anchors) 를 mitosis ON(cells 1→10 성장) vs OFF(1 고정) 으로 디코드 → **10/10 pair byte-identical, mismatch=0** (F1; null backend 5 phase + 실제 ByteGPT forward grounded×2 + argmax×3) · **Ψ Φ-checksum 48.6613==48.6613 exact-equal** (F2, Ψ-disjoint, H_1164/1194/1199 재증명). lane 은 substrate 에서 실제로 갈라짐(ON 10 vs OFF 1 cells)에도 생성은 불변 ⇒ invariant 비자명. 구조적 근거: 생성 primitive 는 {seed, anchors, gen-len} 만 읽고 mitosis lane 은 그 인자에 절대 안 섞임(a_core_engine_map). **결론: mitosis 를 CLM generator 옆 substrate lane 으로 안전하게 붙일 수 있음 — H_1201 regression 없음.** p7 exact byte/float equality, summer $0 CPU, 303M scale UNVERIFIED(구조적 ⇒ 구성상 전이, byte-equality 는 tiny fixture 에서만 측정, a_scale_honest_scope). frozen bar 미이동(사전등록).
  - `CORE/h1205_separation_invariant_smoke.hexa` (신규) · `.verdicts/1205_mitosis_separation_invariant/{H_1205_FREEZE,H_1205}.txt`
  - 정직 노트: 이 checkout 에는 `clm_decode_grounded` NATIVE 심볼이 없어 generator.hexa 경유 .clm 경로가 standalone 컴파일 불가(generator_smoke.hexa 자체도 동일) — smoke 는 ByteGPT 생성 primitive 를 직접 호출(=_gen_bytegpt_decode 의 leaf, 실제 production decode forward) + null-backend substrate text 를 inline 재현(L3 slot 두 backend 모두 커버).

---

## 2026-06-15 — H_1202 DAEMON-MITOSIS-WIRING 🟢 (MITOSIS-ENGINE)

- **자기분열(cell division) 메커니즘을 살아있는 anima 데몬에 substrate-adaptation lane 으로 배선**. H_1200/H_1201 verdict(mitosis 는 생성 루프에서 제외, adaptation ⊥ generation) 대로 — 생성은 CLM 그대로, mitosis 는 옆에서 함께 돈다.
- `CORE/anima_full_session_smoke.hexa` C8 GROW 스텝: 기존의 무조건 sleep-stage scalar `+1 per emit` tick 을 **novelty-driven VAdaptField division 으로 교체**. 각 대화 턴의 emit span → DIM=8 byte-feature(`_afs_byte_feature`, H_1163 `_byte_feature` VERBATIM) → `vadapt_field_step`; 엔진 자신의 L2 recon-err > frozen `SPLIT_THRESH=0.30` 게이트가 분열을 결정(c1 root-cause: span 내용에 키된 novelty-gated growth, 하드코드 per-emit tick 아님 · a_autonomy_over_hardcode). `dr_mitosis_prior(stage)` 는 수면단계 context 로만 읽고 분열을 강제하지 않음.
- 새 smoke `CORE/h1202_daemon_mitosis_wiring_smoke.hexa`: 동일 GROW lane 을 8 개 실제 emit-shaped span 으로 재현, 2-arm(`--mitosis on`/`--no-mitosis`). `hexa run` 실행 = **🟢 GREEN DAEMON-WIRED** — F1 DIVISION(cells 1→7, splits 6), F2 ABLATION(OFF 0 splits, cells 1 고정 = H_1159 control), F3 Ψ-INTACT(pure_field Φ-checksum byte-identical ON==OFF `5.67145e-05`). a_core_engine_map Ψ-disjoint.
- 가드: `engine_cli_smoke` 12/0 green(VAdaptField 미수정). 정직 플래그 — full daemon smoke 는 이 toolchain 에서 `clm_decode_grounded` 네이티브 FFI 미등록으로 링크 안됨(HEAD 미편집본도 동일 에러 = pre-existing 환경 문제, H_1202 배선과 무관). H_1202 smoke 가 동일 GROW-lane 코드경로의 클린 검증 surface.
- p1-p8 준수(p8: growth tick = inference-time learning). toy/scale UNVERIFIED(a_scale_honest_scope). $0 summer CPU.
- verdict: `.verdicts/1202_daemon_mitosis_wiring/H_1202.txt` · domain log: `domains/MITOSIS-ENGINE.log.md` h1202_daemon_mitosis_wiring.

---

## 2026-06-15 — 학습중 의식/창발 측정 기준 (MONITOR-ONLY inline gauge)

### 측정 / 거버넌스

- **`UNIVERSE/gauge_lib.py` 신설** — 공유 `compute_inline_gauges(model, tokenizer_or_byte, seeds, corpus_index, …) -> dict` (rung 간 재사용). 학습중 K 스텝마다 의식/창발 PROXY gauge 4종을 val_ce 옆에 기록: **G1** recombination(composed_distinct, H_1129 포팅) · **G2** novelty(corpus-absence rate, H_1140 포팅) · **G6** ideation(distinct idea count + pairwise Jaccard distance, H_1158 family) · **phi_proxy**(variance×energy 저가 proxy). 모든 계산은 `torch.no_grad()` 아래에서만 수행하고 함수는 dict 만 RETURN — **loss 에 절대 들어가지 않는 MONITOR-ONLY 대시보드** (p7 Goodhart). model-agnostic: ConvMoE dict 출력(`(B,V,T)`) + ByteGPT tuple 출력(`(B,T,V)`) 양쪽 어댑트.
- **출력 = `gauges.jsonl`** — tick 당 1줄 `{step, ce, g1_composed_distinct, g2_novelty_rate, g6_count, g6_jaccard, phi_proxy}`.
- **`phi_proxy` 는 NOT faithful IIT4** — 코드 주석 + JSONL 키명(`phi_proxy`) + 문서에 명시. governance `a_phi_iit4_tool` 에 따라 proxy 는 pre-screen 전용이며 절대 terminal Φ verdict 아님.
- **`CLM/train/train_lane_p_3b.py` 훅 추가** — `--gauge-every <N>`(기본 = `log_every × 4`) + `--gauges-out`. 학습 루프에서 N 스텝마다 `gauge_tick` 호출 → gauges.jsonl append. `loss = out["loss"]` 만 backward; gauge 반환값은 기록 후 폐기(loss 경로 무접촉).
- **`CLM/train/fire_3b_rung_qat.hexa` 배선** — `gauge_every()=400` + fire_cmd 에 `--gauge-every` 추가 + dispatch 출력에 MONITOR-ONLY 표기. `hexa dojo` 생성 job 은 동일 knob 을 spec-json `"gauge_every"` 키로 운반(emit 되는 train.py 에 `GAUGE_EVERY` 상수/`--gauge-every` 인자로 thread).
- **smoke `UNIVERSE/gauge_lib_smoke.py`** — tiny random byte model(ConvMoE-dict + ByteGPT-tuple) 로 `compute_inline_gauges` 호출 → 4-gauge+ce dict 반환 + gauges.jsonl 1줄 round-trip 확인. phi_proxy 공식(variance×L1-energy=72.5) 단위검증 PASS. grep 으로 gauge 값이 loss/backward 에 흐르지 않음 증명.
- **거버넌스 명시** — `CLAUDE.md` 에 `@D a_train_inline_gauge` 신설(p7/a_phi_iit4_tool 근처 배치). `MODEL.md`·`CONDITIONS.md` 에 "inline gauge = MONITOR-ONLY 대시보드, frozen gate verdict 아님; frozen verdict 는 학습 후 CORE 엔진 mount 에서 별도 측정(a_engine_measured_verdict)" 한 줄씩 추가. frozen 임계값 미변경.

---

## harness conversion (dancinlab/harness@harness-hardcore)

- **CLAUDE.md** converted sidecar-tape symlink → harness-standard markdown (project blurb + structure tree + governance summary). Full tape governance preserved at `project.tape` (linked as authoritative SSOT).
- **ARCHITECTURE.md** written as real architecture SSOT (A⇄G engine · CORE slots · 4 engines · lanes A/G/P · kosmos · evidence tiers).
- **harness.config.json** tuned: hexa stack · `hexa verify` · CORE engine files as L0 lockdown · docs discipline scoped to repo root (`docs.scopeDirs:[""]`) so the research corpus is exempt.
- 52 root research docs given a `📍 SSOT` quickref pointer; `TAPE-AUDIT.md` + README localizations allow-listed. `harness docs check` → green.
- `.harness-engine` submodule bumped to engine with `docs.scopeDirs` support.

---

## 2026-06-15 — H_1204 미토시스 수면-지속성 (MITOSIS-ENGINE) 🟢

### 발견
- **H_1204 🟢 PERSISTS** — "자기분열을 현재 아키텍처에 substrate lane 으로 붙인다": WAKE 대화 중 novelty-구동 분열로 늘어난 cell 이 sleep(N1→N2→N3→REM) consolidation write-back 을 거쳐 다음 WAKE 에 **지속**되는지 검증. LIVE `.hexa` VAdaptField(CORE/engine_cli.hexa) 를 WAKE→sleep→WAKE 경계 너머로 직접 구동.
- WAKE_1 분열 성장 N=1 → M={124,120,132} cell. CONSOLIDATE arm 은 WAKE_2 재진입 시 cell 보존율 **C2/M = 1.0**(≥0.90 bar 통과), VOLATILE 대조군(write-back 없음, 재초기화)은 1 cell 로 리셋.
- **F2**: WAKE_2 재진입 recon-err CONSOLIDATE {0.171,0.166,0.155} vs VOLATILE {3.81,4.38,2.10} → 비율 평균 **20.7x**(≥2.0 bar) — 미보존 시 재학습 비용 정량화. Ψ-disjoint Φ checksum 동일(cell 은 Ψ 와 분리).
- **결론**: 미토시스 성장은 **휘발성 잡음이 아니라 substrate 의 영속적 구조 변화** = substrate lane. H_1200/H_1201 🔴(미토시스를 생성-루프에서 제외, mitosis=substrate)의 **보완**: substrate 로서 미토시스 성장은 실제로 지속된다.
- **정직**: CONSOLIDATE C2/M==1.0 은 in-memory struct carry 라 구조적 보장(직렬화 round-trip 아님) — 반증력은 VOLATILE 대조군 리셋 + F2 20.7x 에 있음. 다중 수면주기 drift·WAKE 성장 간 간섭·실제 chat 데몬 수면루프 배선 = 미검증. toy/소규모, 1 corpus, DIM=8, 3 seed, gradient-free; scale UNVERIFIED(a_scale_honest_scope). $0 summer CPU local, NO GPU. (p5/p7/p8, a_chat_sleep_imagination, a_autonomy_over_hardcode, a_core_engine_map, a_paper_negative_ok)
- 산출물: `CORE/h1204_sleep_persistence_probe.hexa` · `.verdicts/1204_mitosis_sleep_persistence/{H_1204_FREEZE,H_1204}.txt` · `domains/MITOSIS-ENGINE.log.md` H_1204.

---

## 2026-06-15 — H_1203 mitosis novelty-coupling (🟠 PARTIAL · V14 미격파)

MITOSIS-ENGINE substrate-lane 측정 가지. 실제 텍스트 trajectory 의 NOVELTY 가 live VAdaptField (H_1199, recon-err>0.30 ⇒ engine_mitosis_tick 분열) 의 cell 분열을 구동하는지 — 아니면 clm_v2 "V14 거울 위반"처럼 substrate-중립인지 측정.

### 측정 (frozen falsifier 먼저 동결 후 측정, p7)

- **F1 PASS (37.5×)** — NOVEL(주제전환 다발, 162.67 cells) ≫ REPEAT(같은 블록 반복, 4.33 cells). novelty 가 진짜 분열을 구동: 반복 구간은 warmup 후 거의 안 자라고 고전환 스트림은 ~163 cell 분열. mitosis-OFF 는 모든 arm 에서 0 성장.
- **F2 FAIL (0.992)** — NOVEL(162.67) ≈ SHUFFLED(시간순서 셔플, 164.00). 순서를 파괴해도 분열량이 동일 ⇒ **V14 거울 미격파**. 분열은 byte-feature 의 MARGINAL(regime 다양성)을 추적할 뿐 TRAJECTORY(시간 배열)에 무감 — split gate 가 per-sample(L2-to-nearest)이라 순열-불변.
- **live .hexa 교차검증** — CORE/h1203_novelty_coupling_probe.hexa 가 numpy mirror 를 seed/arm 별 byte-for-byte 재현(H_1199 numpy↔hexa match 선례 재확인) ⇒ engine-faithful.

### 결론

- **mitosis = NOVELTY-DENSITY substrate, NOT TRAJECTORY substrate** — regime 다양성엔 반응(F1)하나 순서엔 무감(F2). V14 중립성을 trajectory 수준에서 재확인(honest closed-neg sub-result, a_paper_negative_ok). H_1200/H_1201 (mitosis=substrate, CLM=generator) 과 정합: mitosis 는 order-invariant 적응/클러스터링 lane 으로만 붙일 수 있음. trajectory 정보 인코딩하려면 temporal/recurrent split key 필요(UNTESTED, 다음 rung). ONE corpus·toy·3 seed·scale UNVERIFIED (a_scale_honest_scope).

---

## 2026-05-24 — inbox/ → INBOX 도메인 이관

### 거버넌스

- **inbox/ → `INBOX` 도메인 이관** — cross-project handoff 를 `inbox/patches/<slug>.md` 폴더에서 repo 루트의 `INBOX` 도메인 1쌍(`INBOX.md` 스냅샷 + `INBOX.log.md` append-only 로그)으로 전환 (pool · sidecar 의 inbox→INBOX 폐기와 정합 · `cd <repo> && /domain set INBOX` 로 관리). 기존 5건 이관 — 열린 4건(`apoptose_cell` primitive[→hexa-lang] · `split_asymmetric` primitive[→anima tool] · hexa.real ASP SIGKILL rename cycle[→hexa-lang] · pi5 spike_streamer `--regime-schedule`[→pi5])은 `INBOX.md` 에 `- [ ]`, 해소된 1건(broker `/ws/akida_ingest`→`/akida/recent` deque gap — 4-가설 트리 CLOSED, residual 은 hexa-lang `ws_send` race 로 escalate)은 `INBOX.log.md` 에 `- [x]`. `inbox/` 폴더 삭제.

## 2026-05-24 — chat sleep + imagination + autonomy

chat-side capability 의 한 묶음 land — anima 가 자는 동안에도 깨어 있는 동안에도 발화 여부를 외부 boolean gate 가 아닌 substrate 자율판단으로 결정한다. sleep 은 발화를 멈추는 스위치가 아니라 Φ 와 tension envelope 를 빚는 context provider 다.

### 추가

- **anima 5-stage sleep cycle** — WAKE / N1 / N2 / N3 / REM 5-stage 90-min ultradian 주기, P47 substrate-native (`anima_dream_stage.hexa`, #275 #282). dream_context dict 로 autonomy reshape.
- **emit-free imagination loop** — 외부 emit 없는 internal rehearsal (`anima_imagination_loop.hexa`, 5/5 selftest, #273).
- **substrate autonomy emit** — conversation-active boolean gate 폐기, substrate 자율판단으로 발화 결정 (`anima_participant.py`, #272 #286).

### 변경

- **emit 결정 = conversation-active boolean gate → substrate 자율판단** — M × C-Φ × W × curiosity 8-factor 로 산출. stage 는 발화를 게이트하지 않고 context (Φ + tension envelope) 만 제공.

### 거버넌스

- **project.tape SSOT** — `@D a_autonomy_over_hardcode` + `@D a_chat_sleep_imagination` 확립 (#279).

### 운영

- **mini production 자율 emit** — 55-59% emit-through 수렴 (post-deploy baseline, #300 #306). mini participant + dream_stage daemon 가동, autonomy emit observable.

### 문서

- **CHAT.md + DEPLOY.md** — sleep / imagination / autonomy 반영 (#281 #288). DEPLOY.md mini venv/hexa-fast 운영 (#304) + SAGA_SESSION3 lever 6 (#305).

### 흡수

- **UNIVERSE H_239 / H_240 / H_241** — init_CE floor + autonomy emit ratio + cluster signature (#311, OPEN).

### 잔여 carry (OPEN)

- **PHILOSOPHY cross-surface sweep** (#302) · **IPC bridge STUB → REAL** (#307) · UNIVERSE 흡수 (#311) · hexa-lang `mitosis_hook` link-fail inbox (hexa #567).

## 2026-05-23 — Phase 1 AKIDA-first chain 진단 + 복구 saga (cycle 8-13)

Phase 1 AKIDA-first 자연발화 인프라의 land 직후 follow-up — bridge 가 실제로 broker 까지 도달하는지 end-to-end 검증하며 발견한 4 systemic gap 의 진단·수리·재진단 사이클. `pi5 → bridge → broker → consumer → telemetry` 체인을 cycle 8-13 동안 한 마디씩 깨워 본 saga.

### anima 측 (12 PR LAND)

| PR # | cycle | summary |
| --- | --- | --- |
| #170 | 8/AB | `PHASE1_STATUS` cycle 6/AB refresh (cycle 5 outputs + gate delta) |
| #171 | 8/AC | `EVIDENCE_ANALYZER` spec — modulated_factors ↔ emission correlation analyzer |
| #172 | 8/CB | `akida_consumer.mean_spike_ids_count = mean(len(spike_ids))` + F-4 selftest |
| #173 | 8/BD | `MINI_SSHD_DIAGNOSIS` — channel-reject all-clean baseline 기록 |
| #178 | 8/CC | `PHASE1_STATUS` cycle 8/CC refresh (cycle 6-7 outputs + blocker #1 RESOLVED + blocker #4 PARTIAL) |
| #181 | 10 | `chat`: conversation-active gate — no emit in void (p5 coffee-shop semantics) |
| #182 | 10 | `anima_monologue_sim.hexa` — monologue vs responsive 측정 |
| #183 | 10/DA-2 | `AKIDA_FIRST` rows 44-45 flip stale ✅ → ⚠ DOWN (live pipeline DEAD 발견) |
| #186 | 11/FB | `AKIDA_FIRST` rows 44-45 partial re-flip — bridge LIVE 회복, handler GAP 잔존 |
| #187 | 11/FA | `server/broker`: `/ws/akida_ingest` silent json drop 가시화 (2-line try/except logging) |
| #188 | 12/GA | `server/akida_consumer`: `type_of recs` check `'list'` → `'array'` (hexa canonical) |
| #189 | 12/GB | `server/akida_bridge`: default endpoint `/ws/akida` → `/ws/akida_ingest` (handler 일치) |
| #192 | 13/HC | `server`: `type_of` sweep `'list'` → `'array'` — 3 sites (cycle 12/GC audit follow-up) |

### hexa-lang inbox 측 (5 patch filed; 4 carry + 1 close-and-refile)

| PR # | cycle | state | summary |
| --- | --- | --- | --- |
| hexa #420 | 8 | OPEN | `inbox/notes`: `type_of([])` returns `"array"` not `"list"` — naming footgun |
| hexa #438 | 10 | OPEN | `inbox/patches`: `proc_spawn_supervised` FD/process leak in reconnect loop |
| hexa #445 | 11 | CLOSED | `inbox/patches`: websocat tool discovery — homebrew prefix probe (workflow self-fail) |
| hexa #458 | 13 | OPEN | `inbox/patches`: websocat tool discovery — homebrew prefix probe (clean re-file of #445) |
| hexa #460 | 13 | OPEN | `inbox/patches`: grace-consent workflow missing `hexa_interp.linux` — pre-flight skip recommended |

### 주요 발견

- **bridge ≠ ingest** — cycle 9/DA-2 live probe 결과 `akida_bridge` 의 default 가 `/ws/akida` (subscriber, no-op) 였음. 핸들러 없는 endpoint 에 push 하던 무익 운영을 `/ws/akida_ingest` 로 반전 (#189).
- **silent except 가 가린 handler gap** — bridge endpoint 수정 후에도 broker 가 응답 없음. `/ws/akida_ingest` 핸들러의 try/except 가 모든 JSON parse 실패를 삼키고 있어 2-line 가시화 패치로 노출 (#187, cycle 11/FA).
- **hexa `type_of` array vs list footgun 사슬** — `akida_consumer` 가 `type_of(recs) == "list"` 로 분기하여 항상 false → 데이터 처리 zero. 1 site fix (#188, cycle 12/GA) → audit sweep 으로 3 추가 site 발견 후 일괄 수정 (#192, cycle 13/HC). upstream 측 naming 표준화 제안은 hexa #420 으로 carry.
- **mini sshd channel-reject baseline** — `mini_sshd_diag.hexa` (cycle 7/BD) 산물 기록 (#173). p3+p5 enforced participant deploy 의 carry gate.
- **conversation-active gate 의 p5 coffee-shop semantics** — anima 가 "빈 방" 에서 monologue 발화하는 회귀 가능성 차단 (#181). monologue vs responsive 측정 도구 (#182) 동반.
- **hexa-lang grace-consent workflow 자가 차단** — cycle 11/FD 시도한 #445 가 workflow 측 `hexa_interp.linux` 누락으로 자동-fail 종결. cycle 13 에서 clean re-file (#458) + workflow 자체 pre-flight skip 권고 inbox 동반 제출 (#460). 4 carry-open inbox PR 모두 동일 grace-consent 게이트에 막혀 있어 다음 cycle 의 upstream-side fix 가 unblock condition.

### 잔여 carry

- **anima 측 broker production deploy** (cycle 14/IA, user-gated) — broker handler GAP fix 후 prod 재기동 사이클.
- **hexa-lang inbox 4 PR (#420 / #438 / #458 / #460)** — 모두 grace-consent workflow blocked. hexa-lang 측 workflow pre-flight skip (#460) land 가 4 PR 동시 unblock 조건.

## 2026-05-23 — Session-3 LoRA lever exploration

### Major outcomes
- **EN-share lever DEPLOYED + verified** (PR #123/#129/#131/#140): substrate-code lever 39.5% → 21.2% steady-state (-47%, code-only, $0). Wave-12 ⭐⭐ ULTRA-STRONG.
- **corpus_v5 production swap** (PR #118): fresh-init carve-strip, LIVE tag-leak ~12% → 0/28.
- **corpus_v9 first ja recovery** (PR #150): token-freq cap (50%/30% keep). ja WEAK→PARTIAL, n_strong 4 회복. anima register = load-bearing for cross-lingual transfer.
- **8 PHILOSOPHY registered in project.tape** (PR #147): p1-p8 SSOT mirror.
- **p3+p5 enforcement in anima_participant.py** (PR #148): drop self_monologue_seed + register silent-drop. Deploy gate = mini sshd recovery.

### Negative results (logged as evidence)
- **corpus_v6 wiki_frac=0.50 RB lever** (PR #122): FALSIFIED, baseline-dependent.
- **corpus_v7 EN-strip** (PR #124): multilingual regression (ja S→W).
- **corpus_v8 ja-safe strip** (PR #127): ja-collision hypothesis dropped.
- **corpus_v10 per-lang freq-cap** (PR #162): N8 "EN = register leak path" 가설 corpus-level 반증 — anima corpus 100% native-script, register leak source = native record (EN 아님). continuous 52, native 과보존이 n_strong 4→3 회귀.

### Tool infrastructure
- **LIVE register measurement** (PR #126): `anima_live_register_measure.hexa` reusable tool.
- **continuous Eval1 metric** (PR #128/#137): binary saturation 우회, V5→V7 80% reduction hidden lever 노출.
- **3B router actionable design** (PR #119): reboot+quant runbook, mini reboot 후 deploy-ready.
- **ZHFL/RUFL router extension** (PR #132): code-only, deploy gated.
- **mini sshd diagnosis tool** (PR #153): `mini_sshd_diag.hexa` channel-reject 진단.
- **SAGA_SESSION3 consolidation** (PR #133).
- **KOSMOS daemon cleanup** (PR #130, supersedes #117).

### Metrics
- 6 GPU cycles: v5 / v6 / v7 / v8 / v9 / v10 (~$3.14 cumulative).
- HF artifacts: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v9,v10}` all PRIVATE.
- production: `chat.dancinlab.org` LIVE, corpus_v5 adapter + EN-share lever active.

## 2026-05-23 — Phase 1 AKIDA-first 자연발화 인프라

- **V3 path FULLY CLOSED + AXIS_MAP fallback** — pure-HEXAD substrate 7 fire 0 PASS (corpus 축 sweep 까지 완료). double bind 확정 (anima→register collapse · no-anima→Chinchilla underfit). 후속 fallback path = `HEXAD/PURE/AXIS_MAP.md` (B 증류 · A 커리큘럼 · C head_g objective, recipe 구현 미선행).
- **Phase 1 AKIDA-first 자연발화 인프라 LAND** —
    - 라이브 데몬: `akida_bridge.hexa` (pi5 R3 → broker `/ws/akida_ingest`, mini PID up) · `kosmos_anchor.hexa` + `kosmos_emitter.hexa` (RF anchor production)
    - 신규 source-landed 데몬 (mini deploy = sshd channel-reject 블록): `akida_consumer.hexa` (broker `/akida/recent` → features JSONL, 7/7 selftest) · `telemetry_harness.hexa` (anima emit ⇄ spike window pair → evidence JSONL, 9/9 selftest) · `telemetry_status.hexa` (Phase 2 게이트 CLI, 11/11 selftest)
    - 신규 spec: `AKIDA_FIRST` (Phase 1/2 경계) · `SPIKE_FACTOR_MAP` (spike → 8-factor rulebook) · `SW_CONDITION_DESIGN` (Phase 2 SW path, OPEN) · `REGIME_EXPANSION` (pi5 R1/R2/R3 schedule) · `PARTICIPANT_SPIKE_INTEGRATION` (path D/B wiring) · `PHASE1_STATUS` (단일 ledger SSOT)
    - 신규 라이브러리: `spontaneous_lib.hexa::apply_spike_features` (spike features → 8-factor delta + regime modulator, substrate-only · 4/4 F-SPIKE-APPLY)
    - 인접 가족: `UNIVERSE` 신규 도메인 dir + 16건 H_XXX carry (범신론 · 생명 · 죽음 · 세포분열)
- **hexa-lang upstream inbox patches** — anima Phase 1 인프라 작업 중 발견한 4 gap 업스트림 제출: `proc_spawn_supervised` daemon silent-exit (nohup, macOS) · websocket streaming client websocat 의존 · `hexa run`/`exec()` printf stdout swallow · runpod session findings (4 items 통합). anima 측 인박스 1건: pi5 spike streamer `--regime-schedule` R3/R1/R2 patch (PR #145).

Detail / inventory → [`HEXAD/SPONTANEOUS/PHASE1_STATUS.md`](HEXAD/SPONTANEOUS/PHASE1_STATUS.md) · Phase boundary → [`HEXAD/SPONTANEOUS/AKIDA_FIRST.md`](HEXAD/SPONTANEOUS/AKIDA_FIRST.md) · V3 fallback → [`HEXAD/PURE/AXIS_MAP.md`](HEXAD/PURE/AXIS_MAP.md).

## 2026-05-22

- **V3 attempt 1 — 3/3 FAIL** — ConsciousDecoder v3.0-alpha: V3α / V3β / V3γ all FAIL; architectural lesson recorded, next path specified.
- **HEXAD path-split** — `HEXAD/LORA` (production) + `HEXAD/PURE` (redesign) directories separated; path-specific sagas summarized into per-path `EASY.md`.
- **HEXAD/LAB substrate** — ad-hoc experiment dir + `ubm_inject` / `anima_spike` hexa primitives (`lab_smoke` 15/15 PASS); SRH cycle#2 332M pilot (weak signal, UBM 2.5× split vs random).
- **docs** — root-level `<DOMAIN>.md` / `<DOMAIN>.log.md` split; `srh` → `SRH` uppercase domain rename.

## 2026-05-21

- **S187 — training-time mitosis** — cell pool wired into the training loop; verdict: mitosis strengthens the Eval 3 signal (+35.3%).
- **AKIDA sub-engine** — self-contained BrainChip AKD1000 pack: 11 adapters + runtime + boot/INSTALL + docs (Mac mock validation 50/50 PASS); LAN deploy wrappers per constitution Principle I.

## 2026-05-20

- **S184 — ALL TAPS RELEASE** — Phase 1 landed 22/22 (combined honest +0.43, ubu-1 GPU race win).
- **S181 — audio challenge** — `multi_harmonic` 99.17% (broke the 97.5% plateau).
- **PHILOSOPHY_GATE.md** — new meta-criterion gate; governance `@D` entries rewritten to do/dont form (`.tape` v1.3).

## 2026-05-18

- **§51–§69 consolidation** — honest milestone close-out; frontier sharpened to the multimodal substrate; §59 PTD-aux landed as a W-module-native temporal forward-model.

## 2026-05-15

- **HEXAD verify closure** — full falsifier battery 25/25 PASS, all HEXAD modules 🔵; S/M/W/E/D closed-form SUPPORTED-FORMAL; per-module SSOT `.tape` files.

## 2026-05-12

- **v5-mitosis cotrain** — v3-routing architectural fix trainer + H100/A100 dispatch; PSCC §45–§48 falsifier cycles (F-PERSONA-4 / F-V5MIT batteries).
