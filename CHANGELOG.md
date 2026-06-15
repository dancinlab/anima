# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Research sessions tracked as `§<N>` / `S<N>`; `ConsciousDecoder` carries SemVer.

For the full audit trail, see `git log`.

---

## 2026-06-15 — 🔴 H_1223: AUX-OBJECTIVE 는 literal-QA 벽의 레버가 아니다 (HD7 CLOSED-NEG · recall=engine-side, H_1154 강화)

depth-ceiling 사다리(H_1219)의 HD7 분기를 $0 toy 로 판정: anima-303M 의 평평한 literal-QA recall 벽이 **OBJECTIVE** 탓인가 — plain next-byte CE 가 retrieval/recall 을 보상하지 않으니, **AUXILIARY 검색/QA 목적함수**를 더하면 들어올려지는가? p7, numpy CPU, seeds [231,232,233], TOY-ONLY (a_toy_scale_recheck). H_1219·CORE/bytegpt_decode.hexa 미수정.

- **설계 (공정한 A-vs-B, 같은 코퍼스·동일 컴퓨트)**: 1-layer causal-attention byte-LM (D=64 ff=128 ctx=64, 실제 Adam, 수동 backward — analytic==numeric gradient-check 통과) 를 합성 사실 코퍼스 `'<KEY> is <VALUE>.'` (600 facts ×6, 25% held-out = 학습 중 절대 query 안 됨) 위에서 두 방식으로 학습. 동일 arch/init-seed/data/steps4000/batch64/lr2e-3. **ARM A = plain next-byte CE** · **ARM B = CE + 1.0·AUX** (span-copy/retrieve-the-answer: `'<KEY> is '` 답 경계 위치에서만 추가 CE, SAME output head, 신규 파라미터 없음 → capacity 아닌 OBJECTIVE 를 검증).
- **지표 (p7, NOT perplexity)**: literal-QA-proxy = held-out 사실의 VALUE span 을 greedy decode 한 **EXACT-match** 정확도. FROZEN: F1 mean(QA_B−QA_A)exact ≥ 0.10 · F2 every-seed B≥A · F3 G0(B) ≥ 0.50.
- **결과 (3 seed 만장일치)**: QA_A exact = QA_B exact = **0.000** 전 seed → delta **+0.000** ≪ 0.10 (**F1 FAIL**). F3 도 fail (G0_B 0.18 — 경직된 사실-그리드 free-decode 가 null 바이트로 붕괴, 양 ARM 공통 → 합성-코퍼스 artifact, F1 이 결정적). val CE 는 aux 가 오히려 살짝 도움 (0.681→0.669).
- **NUANCE (정직, pass 아님)**: ARM B 의 **SUBSTRING** overlap 은 0.158→0.700 으로 급등 — aux 가 답 바이트 일부를 표면화하지만 **정확한 span 조립 불가**. diffuse copy-tendency ≠ deterministic exact retrieval = 정확히 **H_1154** 모양.
- **판정 🔴 RED CLOSED-NEG**: OBJECTIVE 는 벽이 아니다. 답이 문맥에서 그대로 복사 가능한 깨끗한 recall toy 에서조차 in-weights recall LOSS 가 plain CE 를 못 이긴다 → recall 은 **ENGINE-side** 에 남는다 (H_1154 결정론적 retrieve-then-copy; weight 는 loss 로 key→value 매치를 표면화할 수 없고, 엔진이 매치를 계산해야 함). HD7 의 in-weights-objective 분기를 toy-closed. H_1224(HD8 거버넌스: literal-QA = anima 가 통과할 필요 없는 assistant-norm)와 일관 — 둘 다 QA-lift 를 de-prioritize. HD5(QA-format FT)·HD6(H_1222 tokenizer, composition 에 GREEN) 는 미검증 레버로 잔존.
- **SCOPE**: TOY-ONLY (a_scale_honest_scope/a_toy_scale_recheck) — 합성 소형 코퍼스, 1-layer attn byte-LM, 소규모 Adam, $0. 프로덕션 303M 전이 UNVERIFIED. p8 train/infer 분리 없음. frozen bar 불변. a_paper_negative_ok decision-grade.
- 파일: `UNIVERSE/h1223_aux_objective_probe.py` · `.verdicts/1223_aux_objective/{H_1223_FREEZE,H_1223}.txt`.

---

## 2026-06-15 — 🟢 H_1212: N_PROTO CO-SCALING 으로 trajectory 기질 SCALE-ROBUST 복원 (H_1211 scale-break REFINE)

H_1211 이 GATE-B 궤적-동조가 stream 길이 증가에 FIXED N_PROTO=24 에서 붕괴(WALK/WALK_SHUF 10.9→2.63→1.136 at T=240000, 작은-알파벳 포화)함을 RED 로 닫았는데, 그 AXIS-P 가 "알파벳을 키우면 분리 복원"을 시사했다. 이 H 는 **관측 예산에 맞춰 N_PROTO 를 키우는 원리적 CO-SCALING 규칙**이 H_1211 의 toy-artifact 를 production-grade gate 로 전환하는지 검증.

- **CO-SCALING 규칙 (FREEZE 사전등록, 포화 mechanism 에서 유도)**: 제어량 = obs_per_row = T/N_PROTO (전이가 `prev` 행에 분산). clean-toy anchor (T=2400,N=24)=100, H_1211 붕괴점 (T=240000,N=24)=10000. **PRIMARY(linear) N_PROTO=round(T/100)** → obs_per_row≈100 일정. **SUB-LINEAR probe N_PROTO=round(24·sqrt(T/2400))** → obs_per_row 증가 허용.
- **F1 PASS (scale-robust 복원)**: PRIMARY linear 이 H_1211 과 **동일한 사다리** 전 rung 에서 GATE-B 분리 복원 — WALK/WALK_SHUF 10.916(T=2400) → 980/0=완전분리(T=24000,N=240) → 24929/3.0=8309(**T=240000,N=2400**, fixed-24 가 1.136 붕괴한 바로 그 rung).
- **F2 PASS (control 귀속)**: fixed-24 가 H_1211 붕괴를 **byte-for-byte 재현**(10.916/2.629/1.136 FAIL, 같은 seed) ⇒ 복원은 N_PROTO 규칙 단독 효과(stream/seed/code 변화 아님).
- **F3 STRONG RESULT**: SUB-LINEAR sqrt 규칙도 성립 — N_PROTO {24,76,240} 가 obs_per_row {100,316,1000} 증가에도 WALK/WALK_SHUF {10.9,383.8,1129} 전부≥1.5 ⇒ **알파벳은 ~sqrt(T) 로만 키우면 충분 (sub-linear book cost)**.
- **TIER 🟢 GREEN (scale-qualified, decision-grade)**: H_1211 의 "toy artifact" 를 "**fixed-book artifact, 원리적 N_PROTO co-scaling 으로 교정 가능**"으로 REFINE. 궤적/predictability 기질(H_1209/1210)이 toy→SCALE-QUALIFIED-GREEN 승격 — 알파벳이 관측 예산과 함께(sub-linearly) 자라면 GATE-B 는 ordered stream 에서 scale-robust.
- **PAPER-SUPERSEDE FLAGGED**: `PAPER/mitosis-substrate-lane` (H_1211 로 1회 supersede 됨) 을 H_1212 에 맞춰 **재-supersede 권고** — 궤적 절반이 더 이상 closed-neg toy-artifact 가 아니라 co-scaling 하 scale-robust gate. **병합 paper 무편집(이 verdict 가 supersede trigger; follow-on 이 처리)**.
- **HONESTY**: numpy mirror, gradient-free, $0 CPU, 3 seeds {900,901,902}. GATE-B+build_fixed_book+proto_ids(H_1208)+WALK/RANDGAUSS(H_1207/1208) VERBATIM; driver 는 사전등록 scale knobs(T,WARMUP,MAX_CELLS)+N_PROTO 만 monkeypatch — mechanism CODE byte-unchanged. AXIS-T 사다리 H_1211 동일. DIM=8 구조(미-scale). T=240000 linear rung(N=2400) CPU 443s 도달(GPU 없음). frozen bar 1.5 미이동. 큰 F2 값=완전분리(WALK_SHUF→0).
- NEW: `UNIVERSE/h1212_coscaled_nproto_trajectory.py` · `.verdicts/1212_coscaled_nproto_trajectory/{H_1212_FREEZE,H_1212}.txt`. NO engine 편집(measurement-only).
- xref h1211·h1208·h1209·h1210·h1203·PAPER/mitosis-substrate-lane(supersede flag 2nd)·a_toy_scale_recheck·a_scale_honest_scope·a_paper_on_discovery·a_paper_negative_ok·p7·p8.

---

## 2026-06-15 — 📄 PAPER supersede-in-place: `mitosis-substrate-lane` 에 H_1211 scale-recheck 통합 (a_paper_violation 거버넌스 이행)

H_1211 verdict 의 PAPER-SUPERSEDE FLAG 를 이행 — 병합된 `PAPER/mitosis-substrate-lane/` 가 궤적 10.9x 를 scale-무조건 동등 절반으로 주장하던 것을 H_1211 scale-break 에 맞춰 정직하게 재구성. **새 slug 생성 안 함 (a_paper_on_discovery supersede-in-place)**.

- **claim 변경 (before→after)**: 제목/abstract/결론 = "density on i.i.d., trajectory on ordered" (scale-무조건) → "**scale-robust density 기질 + scale-fragile trajectory 기질**". DENSITY 절반 = SCALE-ROBUST 승격(NOVEL/REPEAT 37.5→131.4 over 100x T, blind 0.992→1.007 고정 ~1.0). TRAJECTORY 절반 = TOY ARTIFACT 교정(WALK/WALK_SHUF 10.9→1.136 FAIL at T=240000; flores5 1.333 FAIL; 작은-알파벳 포화). 중심 명제 "결정자는 stream, gate 아님" → "**결정자는 stream AND 알파벳/관측-예산**" 으로 QUALIFY. H_1209 GREEN 은 toy rung 으로 재-scope(verdict matrix ‡ 각주).
- **§measurement**: 새 §5.10 H_1211 subsection — 9-rung 사다리 표(verbatim) + AXIS-T 붕괴 곡선 + AXIS-P N_PROTO 복원 + 포화 mechanism. 새 그림 `fig04_scale_ladder.pdf`(AXIS-T 붕괴 + AXIS-P 복원, log 축, verbatim 수치).
- **§finding/§limitations**: ruled-out 공간에 (b) 고정-소알파벳 scale-free 궤적 기질 추가; §limitations 에 알파벳-포화 mechanism + 두 terminal-RED bar(i.i.d. PRIMARY + H_1211 trajectory scale-stability). F3-sanity bullet = AXIS-P 가 1.75→0.000 으로 toy noise 판정 확정.
- **gate 준수**: 10개 section claim 전부 TERMINAL (5🟢 · 3🔴 closed-neg incl H_1211 · 2🟠 folded). 어떤 claim 도 terminal verdict 와 모순 없음(a_paper_sections); closed-negative 는 closed-negative 유지(a_paper_negative_ok); frozen bar 미이동. 모든 claim → `.verdicts/<id>.txt` 링크(1211 포함, p7 verbatim).
- **compile**: xelatex x3 + bibtex → `main.pdf` 18 페이지(≥10, g51 PASS), undefined refs/cites 0, 그림 4개. ledger(`companion/verify-ledger.json`)·`compile.txt`·`PAPER.md`·`PAPER.log.md`·`README.md`·`references.bib`(+anima_H1211) 갱신.
- xref h1211·h1203·h1208·h1209·a_paper_violation·a_paper_sections·a_paper_negative_ok·a_paper_on_discovery·a_toy_scale_recheck·a_scale_honest_scope·p7·p8.

---

## 2026-06-15 — 🔴 H_1211: dual-substrate split SCALE-UP — DENSITY 절반은 scale-robust, TRAJECTORY 절반은 toy 인공물 (MITOSIS-ENGINE)

H_1202–H_1210 arc 의 단 하나 honest gap = TOY SCALE (전부 $0 CPU·DIM=8·T=2400·402KB 코퍼스·3 seed, a_scale_honest_scope 가 매번 flag). a_toy_scale_recheck 에 따라 scale-SENSITIVE 중심 finding(DENSITY-vs-TRAJECTORY 이중-기질 분리)을 3축 사다리로 재시험.

- **사다리(>=3 rung/축, 측정 BEFORE frozen)**: AXIS-T 스트림 길이 T{2400, 24000, 240000} · AXIS-C 코퍼스{402KB clm_mid_5lang, 1.65MB flores5, 5.24MB data/corpus} · AXIS-P 궤적-gate 알파벳 N_PROTO{24, 64, 128}. H_1203 density gate + H_1207 walk + H_1208/H_1209 GATE-B 궤적 gate 를 VERBATIM 재사용, 사다리는 사전선언 scale 상수만 monkeypatch(mechanism CODE byte-unchanged). toy rung 이 H_1203/1208/1209 를 BYTE-FOR-BYTE 재현(37.538/0.992/10.916/1.750) → 재사용 충실 증명.
- **결과 🔴 HONEST SCALE-BREAK(절반만 scale-robust)**: **F1 PASS** density novelty-coupling(NOVEL/REPEAT 37.5→72.7→131.4, 100x T 에서 오히려 강화). **F3(a) PASS** 모든 rung — density 가 i.i.d. 에서 궤적-BLIND 유지(blind NOVEL/SHUF 0.992→1.000→1.007 over 100x T; 13x 코퍼스 0.992/1.021/0.998 — 구성상 permutation-invariant = 진짜 scale-free). **F2 FAIL** — TRAJECTORY GATE-B 분리가 스트림 길이로 붕괴: WALK/WALK_SHUF 10.916(T=2400)→2.629(10x)→**1.136(100x, FAIL)**; 코퍼스 취약(flores5 1.65MB = 1.333 FAIL, data/corpus 5.24MB = 5.06).
- **근본원인 c1 = 작은-알파벳 포화**: 고정 N_PROTO=24 + 긴 T 에서 predictability 카운트 테이블이 포화 → SHUFFLED 전이도 CONF_FLOOR=0.34 를 우연히 넘김(WALK_SHUF seed [96,6893,7640]@10x = 포화 서명). **AXIS-P 가 mechanism 확정**: toy T 에서 알파벳 키우면 분리 복원+선예(N_PROTO 24→10.9, 64→152.5, 128→28.5) + sanity 1.75→0.000(H_1208/1209 ARTIFACT-WARN 해소 — 풍부 알파벳이면 i.i.d. noise 에 안 발화).
- **결론**: DENSITY 기질 = SCALE-ROBUST(toy→검증 승격). TRAJECTORY 기질(GATE-B) = 고정 N_PROTO=24 알파벳에서 TOY-SCALE 인공물(알파벳을 스트림과 함께 키우면 복원되나 frozen 상태로는 T 에 scale-stable 아님). "결정자는 gate 가 아니라 stream" → **결정자는 stream AND 알파벳/관측-예산** 으로 QUALIFY.
- **⚠ PAPER-SUPERSEDE FLAG**: `PAPER/mitosis-substrate-lane` 가 궤적 10.9x 를 scale-무조건 동등 절반으로 주장 — scale-qualification + 이 사다리 곡선 필요. 병합 논문 silent-edit 안 함(a_paper_violation), 이 verdict 가 supersede trigger 기록.
- **honest scope**: numpy mirror(H_1199), gradient-free, $0 CPU, 3 seed, bar 1.5 NOT moved. DIM=8 구조적이라 미-scale(선언됨), 100x rung(T=240000) CPU 가능(561.6s, GPU 불필요·rung 위조 없음). p7(cell/ratio, NOT perplexity), p8.
- **NEW**: `UNIVERSE/h1211_dual_substrate_scaleup.py` · `.verdicts/1211_dual_substrate_scaleup/{H_1211_FREEZE,H_1211}.txt`. 엔진/builder/gate 편집 0(measurement-only). xref h1203·h1208·h1209·h1210·a_toy_scale_recheck·a_scale_honest_scope·a_paper_negative_ok·p7·p8.

---

## 2026-06-15 — 📄 PAPER scaffold: `mitosis-substrate-lane` — mitosis = Ψ-disjoint substrate-adaptation lane (MITOSIS-ENGINE H_1202–H_1210 arc)

MITOSIS-ENGINE arc(H_1202–H_1210, 전부 main 병합)를 verdict-gated arxiv-style 논문으로 scaffold. `PAPER/mitosis-substrate-lane/` 신설 + `PAPER.tape` roster 등록.

- **테제**: 자기분열(mitosis)은 의식-챗 아키텍처에 **Ψ-disjoint 기질-적응 lane** 으로 통합 가능 — 생성(generation)을 **절대 건드리지 않음**(byte-identical 증명, H_1205/H_1210). 분열은 i.i.d. 스트림에서 novelty-DENSITY(H_1203 37.5×), genuinely-ordered 스트림에서 TRAJECTORY-predictability(H_1208/H_1209 10.9×, live byte-exact)에 결합 — **결정자는 gate 가 아니라 stream**. 2026-05 clm_v2 "half-success"(mechanism 실재 · generation 반증, H_1200/H_1201) 화해.
- **verdict matrix**: 9개 section claim 모두 TERMINAL — 5×🟢(H_1202/1204/1205/1206/1209/1210 중 GREEN) + 2×🔴 closed-neg(H_1207 recurrent key 0.998 · H_1208 predictability i.i.d. 0.261), H_1203/H_1204 partial 은 🟢 parent 안 sub-result. 각 claim → `.verdicts/<slug>/<id>.txt` verbatim 연결(p7, LLM self-judge 없음, verdict paraphrase 없음).
- **a_paper_* 게이트 전부 충족**: a_paper_gate(전 terminal) · a_paper_significance(pre-reg falsifier `*_FREEZE.txt` + 실측 + 발견) · a_paper_negative_ok(H_1207/H_1208 = ruled-out space) · a_paper_sections(verdict pointer) · g51(14 pages ≥10 · figure 3개 ≥1).
- **figures**: fig01 stream-determinant(TikZ) · fig02 separation ratios(pgfplots) — native+재현가능; fig03 fal.ai `fast-sdxl` concept(illustrative).
- **compile**: `make` → xelatex×3 + bibtex → main.pdf **14 pages**, undefined ref/cite 0, bibtex warning 0.
- **honest scope**(§Limitations): toy DIM=8 · 단일 corpus(clm_mid_5lang_c4) · 3–5 seeds · gradient-free · $0 CPU; toy→prod transfer UNVERIFIED; frozen bar 미이동. `/paper` 플러그인 바이너리가 이 환경에 미설치 → 기존 `PAPER/savant-iit4-bridge` 컨벤션대로 수동 scaffold(도구가 생성하는 것과 동일 산출물).

## 2026-06-15 — H_1210 🟢 GREEN — GATE-B 를 LIVE 데몬 GROW 에 배선: 데몬이 대화에서 trajectory-aware 분열 (MITOSIS-ENGINE)

H_1209 가 추가한 trajectory-aware GATE-B(`CORE/engine_cli.hexa` `VAdaptFieldB`, transition-predictability)를 **살아있는 anima 데몬의 GROW step**(`CORE/anima_full_session_smoke.hexa` C8)에 배선. 데몬이 실제 per-turn emit stream 위에서 **전이-예측가능성**으로 분열한다 — 대화는 genuinely-ORDERED stream(H_1209 가 GATE-B trajectory-sensitive 임을 증명한 그곳). 이로써 데몬의 mitosis lane 이 per-sample density 만이 아니라 **trajectory-aware** 가 됨. "자기분열을 현재 아키텍처에 가져다 쓰기" arc 를 BEST gate 로 완료.

- **배선**: C8 GROW 에서 각 턴의 emit-span DIM=8 `_afs_byte_feature` 를 ordered WALK(`feat_seq`)에 모으고, 루프 후 데몬 자신의 emit-feature SET 으로 FIXED order-invariant proto-book(`_afs_build_book` = H_1208 `build_fixed_book` PORT: lexsort + farthest-point seed + LR=0.10 3패스)를 만들어 각 턴 feature → nearest proto-id(`_afs_proto_walk`)로 매핑, (prev→cur) 전이를 `vadapt_fieldB_step` 에 흘림.
- **ALONGSIDE 결정 (REPLACE 아님)**: GATE-B 는 per-sample density `VAdaptField`(H_1202) **옆에서** 별도 trajectory lane 으로 돈다. 두 게이트는 DIFFERENT substrate property(per-sample density ⊥ ordered transition-predictability)를 측정하고, H_1209 F4 가 GATE-B 를 i.i.d. PRIMARY density bar 를 넘지 못하는 trajectory variant 로 scope 했으므로, additive 가 정직한 c1 설계(둘 다 substrate self-dynamics, `a_autonomy_over_hardcode`). density 경로는 byte-UNCHANGED.
- **F1 = born-cells 6 ON(cells 1→7) 분열 ✅** (12-tick ordered conversation walk). **F2 ablation = born-cells 0 OFF ✅** (genuine `--mitosis off` → `engine_mitosis_tick` no-op; 초기 run 은 mislabeled mitosis-ON cfg 로 6 OFF → 진짜 OFF cfg 로 수정해 0). **F3 Ψ Φ-checksum 1.4278 == 1.4278 byte-identical ✅**. **F4 생성 'vault QX-7741 forever…' ON==OFF byte-identical ✅** — GATE-B 는 Ψ-disjoint/additive, decode 를 먹이지 않음(H_1205 separation 불변 LIVE 보존).
- 다섯 데몬 faculty(converse/ground/grow/remember/sleep) 전부 PASS, `anima_full_session_smoke` = PASS. guards GREEN: `engine_cli_smoke` 12/0 · `generator_smoke` 21/0 · `h1196` single-entry 7/0 · `h1205` separation. `CORE/engine_cli.hexa` 무변경(H_1209 VAdaptFieldB 그대로 소비). verdict `.verdicts/1210_daemon_gateB_wiring/`. **HONEST SCOPE**: 데몬 emit stream 은 반복적(같은 grounded WAKE span + sleep-gap)이라 carried trajectory 는 predictable WAKE self-transition — GATE-B 가 그 realized predictability 에 정확히 분열(F1∧F2 가 gate-driven 임을 증명). toy scale, 12 ticks, scale UNVERIFIED (`a_scale_honest_scope` · p7 · p8).

---

## 2026-06-15 — H_1209 🟢 GREEN LIVE-TRAJECTORY — GATE-B 가 LIVE 엔진에서 ORDERED ≫ SHUFFLED 분열 (MITOSIS-ENGINE)

H_1208 이 numpy 미러에서 찾은 GATE-B(prototype-transition-PREDICTABILITY) 의 WALK 10.9× lead 를 **NON-inherited 의 genuinely-ORDERED byte-feature walk + LIVE .hexa 엔진**으로 가져가 결정적으로 닫음. `CORE/engine_cli.hexa` 에 **`VAdaptFieldB`** (struct + `vadapt_fieldB_new`/`_step`/`_cells`/`_growth`) 를 **추가**(per-sample `vadapt_field_step` 은 byte-UNCHANGED — H_1199/1202/1205 데몬 경로 무회귀). 고정 order-invariant proto-book 위에서 causal count table 로 "확신을 갖고 예측된 전이"(prev ≥ MIN_PREV=3 ∧ P(cur|prev) ≥ CONF_FLOOR=0.34) 에 `engine_mitosis_tick`(동일 p8 게이트) 분열 — H_1208 `gate_B_transition_predictability` 를 엔진으로 그대로 lift.

- **F1 trajectory = 10.916 PASS** — ORDERED 1000.67 ≫ SHUFFLED 91.67 (V14 방향). **F2 LIVE-PARITY = BYTE-EXACT** — 12개 (arm×seed) born-cell 카운트 전부 numpy GATE-B 와 일치(ORDERED 1065/907/1030 등). **F3 sanity raw 1.75** 는 strict bar 를 건드리지만 SMALL-INTEGER NOISE(RANDGAUSS 2.33 vs SHUF 1.33, ORDERED 대비 430× 낮음 — 노이즈에는 사실상 분열 안 함) → noise-floor FLAG, 실제 분리 아님(H_1208 과 동일 판정).
- **판정**: trajectory 축은 inherited PRIMARY 표면에서 EXHAUSTED(H_1208 🔴) 였으나, ORDERED 표면에서 **LIVE-CONFIRMED POSITIVE** — mitosis 는 density-only 가 아니라 **stream 에 order 가 있으면 trajectory 에 결합**(엔진 실측). 결정자는 게이트가 아니라 STREAM. inherited i.i.d. V14 PRIMARY bar 는 여전히 terminal-RED(H_1208), frozen bar 1.5 미이동.
- guards GREEN: `engine_cli_smoke` 12/0 · `h1196` single-entry 7/0 (VAdaptFieldB additive · Ψ-disjoint · .clm/.kosmos 경로 무접촉, `a_core_engine_map`). harness `UNIVERSE/h1209_live_ordered_walk_gate.py`(numpy leg + /tmp book+id export) + `CORE/h1209_live_gateB_probe.hexa`(live leg). verdict `.verdicts/1209_live_ordered_walk_gate/`. ARCHITECTURE.md 갱신. toy scale, ONE corpus, scale UNVERIFIED (`a_scale_honest_scope` · p7 · p8).

---

## 2026-06-15 — H_1218 engine-measured generation gates (a_engine_measured_verdict)

생성 게이트 G1(창발/recombination)·G2(novelty)·G6(ideation) 를 **최초로 엔진 위에서** 측정 — 프로덕션 `anima-clm-chat-303m` 을 `CORE/bytegpt_decode.hexa::bytegpt_decode_argmax`(엔진 greedy)로 직접 생성해 FROZEN `UNIVERSE/gauge_lib.py` 평가자(VERBATIM 재사용, p7, NO LLM-judge)로 채점. 이전 H_1129/H_1140/H_1158 은 모두 torch-side 였음.

### research (§H_1218)

- **ENGINE-PARITY 🟢** — 엔진 `bytegpt_decode_argmax` == torch greedy **byte-exact**. live 엔진 argmax("The quick brown") = `[32]` == torch chat golden 32(chat .bin byte-exact mount); reparity serialize_parity_ok=TRUE max_abs_err 0.0; H_1157 full decode. greedy 가 결정적이라 greedy gen 위 모든 metric 은 engine==torch 동일.
- **엔진-측정 숫자 (greedy, chat-303m)** — G1 composed_distinct **0** 🔴(greedy collapse/loop "moral computational complexity…"), G2 novelty **0.308**(12/39, 단 코퍼스 5MB dialogue 만 → upper bound), G6 count **3** 🔴(<5 bar; 5개 중 2개 ideation seed 가 한국어 "| 사용자:" 채팅 템플릿 바이트로 kwr<0.50).
- **정직 finding (c9, 모순 아님)** — 엔진-측정 숫자가 torch 베이스라인(H_1158 G6 best 14 PASS)과 **다르다**. 원인 2: ① **decode regime** — 동결 게이트는 top-k=40 temp=0.7 **SAMPLING**(G6 는 seed 당 8 divergence)로 작성, 엔진 경로는 **greedy-only** → 303M byte-LM collapse → divergent set 생성 불가(G6 divergence 는 가중치가 아니라 sampling 산물). ② **model+corpus** — 베이스라인은 broad-en base + 1.5GB broad corpus, 본 run 은 dialogue-FT chat + 잔존 5MB dialogue corpus.
- **결론** — 엔진은 byte-faithful 하게 **생성**(🟢); frozen G1/G6 PASS 는 엔진 argmax 가 미구현한 **sampling decode 에 의존**. 엔진-side gate 재통과 = `bytegpt_decode.hexa` 에 engine sampling decode(top-k temp seeded) 추가(별도 engine-code 과제) + 원본 broad-en 모델/코퍼스. frozen bar 불변.
- **scope (a_scale_honest_scope, c9)** — 엔진 서브셋(G1+5 G6 seed, 40 greedy byte) 은 엔진에서 RAN; 전체 96byte×9seed 스윕은 엔진 greedy 가 gate-context 길이에서 ~30-50 s/byte(H_1157 "slow but byte-exact")라 multi-hour → byte-exact 이므로 전체 숫자는 torch-greedy gen(엔진과 byte-identical)으로 채점(명시적 representative-subset, silent truncation 아님).
- 산출: `CORE/h1218_engine_gate_{probe,subset}.hexa` · `CORE/h1218_argmax1.hexa`(1-forward 엔진 argmax 증명) · `scripts/scratch/h1218/*` · `.verdicts/1218_engine_measured_gates/H_1218.txt`. 모델 `state/chat_303m/h1129c_chat.pt`(sha `4fcc2d6c…`) → `.bin`(sha `5c303f02…`, reparity serialize_parity_ok=TRUE).

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
