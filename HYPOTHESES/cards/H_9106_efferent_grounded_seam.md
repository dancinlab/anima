# H_9106 — efferent seam (c), GROUNDING-selection follow-on to H_9103: byte-grip REAL but not conflict-gated ∧ grounding-aware selection does NOT lift held-out grounding = 🔴 (converges with & extends H_9103's efferent faculty-floor)

- **slug:** `9106_efferent_grounded`
- **tier:** 🔴 RED (frozen bar) — byte-grip REAL ∧ D1-dissociation FAIL (LOW also diffs) ∧ D2 held-out grounding FAIL (Δ≪+0.10) · engine-native · 완곡화 금지
- **wired:** `engine-native` (core/ ops LANDED: `bytegpt_ce_ranged`/`clm_ce_ranged` decode.hexa · `gen_auto_ce`/`conflict_drives_live`/`generate_deliberate` generator.hexa · `brain_emit_deliberate` brain.hexa. REAL d768.clm own-GEMM decode 측정, `[OWN-GEMM-FIRED]` 두 호스트. live daemon 은 single-candidate `generate()` default = byte-identical → deliberate seam OFF by default, 무해. faculty-floor 이므로 WIRED-live 승격 안 함, a_verified_must_wire.)
- **source:** UNIVERSE · fable#5 design (c) / **H_9103 explicit follow-on** ("selection=CE만; grounding-based=follow-on") · id H_9106 (origin run 라벨 H_9102; H_9102=stateful-refractory·H_9104=consequence_return·H_9105=identity_emit 별개 세션 착지·H_9103=fluency-sel efferent 착지 → 충돌회피 재번호 H_9106)
- **cross-ref:** [[H_9103]] (fluency-selection efferent 🟠 byte-grip real·faculty FALS) · [[H_9101]] (stage/idle 🟢 WHEN) · [[H_9100]] (motivation 🔴 HOW-MUCH) · [[H_9097]] (rel_ctx zero-grip theater)

## 맥락 (trilogy (c)=WHAT, 두 번째 독립 harness = grounding-selection)
H_9103 이 (c) efferent 를 **fluency-only selection**(winner=argmin `clm_decode_ce`)으로 측정 → byte-grip real ∧ Ψ-safe ∧ **faculty FALSIFIED**(ρ_real=−0.44: best sample 가 argmax fluency 보다 CE 나쁨), 열린 caveat = **"selection=CE만(grounding-based=follow-on)"**. 이 카드가 바로 그 follow-on: winner=argmin `conflict_scalar`(fluency **AND** §ImmuneMemory recall margin) + **독립 held-out grounding metric**(anchor-LCS `ground_overlap`, 선택키와 순환없음) + HIGH/LOW dissociation, N=20. 질문: grounding-aware selection 이 fluency-only floor 를 벗어나 held-out grounding 을 올리나 → **아니다(floor 재출현)**.

## 배선 (core/, additive · a_engine_native_learning · parse-clean 3파일)
- `bytegpt_ce_ranged(path,ids)` / `clm_ce_ranged(path,ids)` (decode.hexa) — per-position mean next-byte CE (forward-CE fluency read), own-GEMM GPU (RFC-040, CPU byte-identical). `gen_auto_ce` = mouth dispatcher.
- `conflict_drives_live(ckpt,cand,mem)` (generator.hexa) — signed A⇄G drives: a=clip01(1−ce/**CE_REF=5.0**); g from immune recall margin (**M_REF=0.25**), READ-only(recall_thr·store 무접촉=a_substrate_disjoint).
- `generate_deliberate(backend,ctx,emit,anchors,mem,tick)` — sister to `generate()`: emit=false ⇒ byte-identical silence; c₀=generate(...); K=`conflict_recruited_depth`∈{1..4}; candidates=`gen_auto_ideate`(top_k=8,temp=0.7 frozen); **winner=argmin conflict_scalar, tie-break min k ⇒ K=1 ⇒ winner=c₀**.
- `brain_emit_deliberate` (brain.hexa) — SAME `brain_decide_anchored`(emit/silence 결정 UNTOUCHED) → generate_deliberate for bytes.

## 사전등록 bar (FROZEN · PREREG.md 사후이동 없음) & 실측 (verbatim = state/verdicts/9106_efferent_grounded/H_9106.txt)
REAL d768.clm (CONV int4 CLMConvMoE, own-GEMM GPU · `[OWN-GEMM-FIRED]` 두 호스트) · NO numpy/torch/mirror (grep-clean).

| bar | 실측 | 판정 |
|---|---|---|
| **D1 byte-diss** HIGH≥12/20 ∧ LOW==0/20 | HIGH **20/20**(aiden v0.548)·**18/20**(summer v0.574) ∧ **LOW 11/11 diff**(aiden, pre-reboot) | HIGH SATISFIED(byte-grip real) · **LOW==0 VIOLATED → D1 FAIL** (byte 변화 무조건적, conflict-gated 아님) |
| **D2 held-out grounding** Δ≥+0.10 | Δ=**+0.0280**(aiden)·**+0.0030**(summer) | **FAIL** (grounding-aware selection 이 held-out grounding 못 올림) |
| **D3 decision-Ψ Hamming** ==0 | STILL NOT OBTAINED — D3 checksum ON≡OFF (guard-ON vs guard-OFF) **미확인** (실측 없음). 완주가 구조적 infra 벽에 막힘 = [[H_9107]] (clm303 하네스 per-candidate RSS blowup; d768 아닌 303M 재측정 시 3개 rent pod 전부 SUMMARY 전 사망). | ⏳ 미완(infra=H_9107, "stable-host면 해결" 아님 — 구조적) — 비-verdict결정(GREEN 불가) |
| **D4 shuffle** \|Δ\|<0.03 · **D5 regression** LOW=0 | STILL NOT OBTAINED (동일 H_9107 infra 벽) | ⏳ 미완(infra=H_9107) |

## 정직 판정 (frozen-first, c9 · NO tune-to-green)
**🔴 RED (frozen rule: RED iff LOW>0 OR D2 fails).** 두 측정된 core falsifier(D1 LOW 11/11, D2 Δ≪bar)가 RED 를 **결정**한다 — GREEN 은 D1–D5 전부 필요하므로 불가, D3/D4/D5(infra-blocked)는 RED 를 구제 못 함. CE_REF/M_REF/bar 사후이동 없음. Ψ-safety 는 **by-construction**(brain_emit_deliberate 가 동일 brain_decide_anchored 사용, bytes 는 emit 결정 *이후*에만 변경 = H_9103 F2 논증과 동일)이나 empirical D3 Hamming 은 미포착(infra) → 완전 D3/D4/D5 는 stable-host follow-on.

## 핵심 발견 (측정 상수에서)
- **c₀ context/anchor-invariant on d768**: go_off 전 seed 상수(aiden 0.0152·summer 0.0477) ⇒ 작은 reference d768 greedy c₀ 는 phase-word ctx·anchor 무관하게 동일 출력. confpre 도 host별 상수(aiden 0.5233·summer ~0.92) ⇒ **anchor-기반 HIGH/LOW conflict 조건화 실현 안 됨** ⇒ deliberation 이 두 group 모두 K>1 로 무조건 발화, byte 변경하되 conflict-GATED 아님.
- **grounding-selection 도 held-out grounding floor**: winner 에 immune margin 을 넣어도 held-out ground_overlap Δ(+0.003~+0.028)가 bar(+0.10) 미달 = **H_9103 이 요청한 grounding-selection follow-on 에서 efferent faculty-floor 독립 확인** = trunk-objective(CE) 벽이 efferent 층에서 selection-key(fluency든 grounding이든) 무관하게 재출현.
- **THEATER 3축 재확인**: WHEN/WHETHER(H_9101 🟢)·HOW-MUCH(H_9100 🔴)·**WHAT(H_9103 🟠 fluency-sel + H_9106 🔴 grounding-sel)**.

## caveat (c9 정직 스코프)
- **RENTED pod 미사용 — rent path 이중 차단**: mac `hexa cloud` 컴파일 실패(stale runtime.a `_rt_format_float_native` 링커) + commons c11 raw-provider(runpodctl/vastai) 차단 → 렌트 불가. byte-Hamming 은 CPU/GPU byte-identical(a_train_flame_forge) ⇒ substrate-무관, engine-native pool 측정 유효(own-GEMM 실발화 확인).
- **pool reboot loop = LOW/D3 미완**: aiden(03:45 @7min-uptime)·summer(04:25 @18min-uptime) 둘 다 run 중 재부팅 — full ~60-90min run > ~25min reboot interval(owner 경고·[[aiden-stable-free-terminal-eval-host]] earlyoom 패턴). D1(LOW)·D2 는 recovered 로그로 결정, D3/D4/D5 는 stable-host follow-on(ING).
- **D3-D5 미완의 진짜 원인 = 구조적 infra 벽 [[H_9107]] (pool reboot 이 아님)**: 위 "stable-host follow-on" framing 은 부정확. clm303(303M) 로 이 하네스를 돌리면 `generate_deliberate` best-of-K + D4 shuffle 루프가 HIGH seed 당 `gen_auto_ideate(ckpt,...)` 를 ~6-8회 재호출, 매번 mouth 를 경로에서 재적재 → ~4-5GB/min RSS 폭증(d768 4.46MB 에선 무해, 303M 에선 치명). rent pod 3개 전부 SUMMARY 전 사망: pod1(43627857 220GB det-CPU)·pod2(43635479 176GB det-CPU) = H_9107; **pod3(43644174 137GB, hexa v0.577.0 CUDA, `[OWN-GEMM-FIRED]` GPU own-GEMM 실발화, #2835 W-hoist present-verified) = 이번 3차** — GPU 경로·#2835 있어도 동일 폭증 재현(RSS 29.5GB@2min, H_9107 의 27.5GB@2.4min 과 일치) 후 사망 ⇒ **#2835 도, dedicated/GPU pod 도 non-rescuing** (leak 은 clm_ce_ranged 아닌 gen_auto_ideate 재적재 경로). evidence = state/verdicts/9107_clm303_efferent_infra/pod3_43644174_owngemm_partial.log. 진짜 fix = production core/generator.hexa 의 ideate load 를 hoist (execution-only 범위 밖). **verdict 불변 🔴 RED**(D3-D5 는 RED 를 못 뒤집음).
- **worktree 유실→복구**: 병렬 에이전트가 원 worktree sweep(shared-worktree-collision) → 코드 summer rsync 사본에서 복구, origin/main 위 additive patch 재적용(3파일 parse-clean, H_9099 clm_penult_pooled·H_9103 seam 보존).
- **tiny-ckpt scope**: d768(4.46MB) c₀ context-invariant = anchor-conditioning 실패 원인일 수 있음 → production-scale ckpt 재측정 = a_toy_scale_recheck follow-on. (attempt #4 가 clm303 303M engine-native 마운트+own-GEMM 까지는 도달했으나 pod 사망으로 재측정 미완 — 위 bullet.)
- seam 은 daemon default OFF(single-candidate generate)=무해; faculty-floor → WIRED-live 승격 안 함.
