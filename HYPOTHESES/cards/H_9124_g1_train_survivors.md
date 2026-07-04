# H_9124 — G1 학습축 break-walls survivors (derivation-trace + STaR 사전등록)

> **tier:** 🟢 **DIRECTIONAL-POSITIVE** (레버1 derivation-trace = 최초 engine-native G1 lift · robustness 미확인) · 레버2 STaR = 🔴 **FALSIFIED-AT-FLOOR**(engine-native STEP-0 STARVE, |V0_true|=0/80) · 레버3 γ(trained-constructive-bind [[H_1840]])는 미발사 — G1 재조합벽 학습방법 축 workflow(w8yk7akft, 25 agent, fable 위임 없음)가 14 레버 중 census-refute 실패한 survivor. · **wired:** N/A
>
> **핵심:** objective-basin(CE=echo) 메타법칙을 진짜 우회하는 2 학습레버가 census 밖 생존. deep ConvMoE L8은 이미 CLOSED-by-H6188(측정됨, ING standing-go "OPEN"은 착각 — [[H_6185]]/[[H_6188]] 정합).
>
> **★ 레버1 결과(summer 발사, 2026-07-04):** 🟢 **DIRECTIONAL-POSITIVE** — warm-FT h1129 303M 2-arm 통제, engine-native `anima evaluate --py` gen40: **DERIV G1 PASS(bd=2>ms=1) ∧ FLAT G1 FAIL(bd=2,ms=3)** on held-out {c0,c1}(both orderings 미노출=memorization-free). data-format이 격리된 lever = 20+ decode family+전 학습 family 못 뚫은 G1 첫 lift. 정직 caveat: bd=2 marginal(margin=DERIV ms=1 낮아서)·held-out 1쌍·G2 corpus 미로드 novelty 미확인·CLOSURE 미달. robustness follow-on=multi held-out 쌍+G2 corpus+paraphrase. 상세 state/g1_train_wallbreak/derivtrace/RESULT.md.
>
> **레버1 사전등록(발사됨): derivation-trace 절차 코퍼스 (data축·최우선·summer ~1 GPU-hr):** target 시퀀스를 derivation 자체로 재작성("jump thrice : DEF X=JUMP; RULE thrice: X X X; OUT..."). CE=echo 메타법칙 **미적용**(target이 곧 derivation→echo=composition). toy directional lift FLAT 3/7 vs DERIV 13/18. FROZEN bar: warm-FT h1129 + DERIV vs FLAT baseline arm(동일 fixture) → anima evaluate --py engine-native gen=40 G1 best_distinct≥2 ∧ >max_single. FLAT arm이 floor 유지 ∧ DERIV arm만 상승 = data-format 레버 실증. 잔여 위험=H_1822 copy-head 벽.
>
> **레버2 STaR/verifier-filtered self-distillation (CE 유지):** best-of-K→composition-TRUE verifier(surface G1 detector 아님, kosmos-grounded)→verified HIT hard CE relabel+mix→반복. STEP-0 $0 early-kill: base h1129c best-of-K decode |V0|/(K·n)<0.02면 STARVES=FALSIFIED-AT-FLOOR. MANDATORY fab-control(verifier=surface-detector arm은 fab 팽창해야, a_substrate_disjoint savant+honesty).
>
> **★ 레버2 결과(vast 렌트 pod, 2026-07-04):** 🔴 **FALSIFIED-AT-FLOOR (STARVE-at-STEP0)** — engine-native(numpy `core/decode.py` bytegpt mouth, torch-free → terminal, DIRECTIONAL 아님). base h1129.bin(ByteGPT 303M, sha 5cf07a36) best-of-K=8·gen40·10 held-out distant pair(C(5,2))·denom=80: **|V0_true|=0/80(rate 0.0)** < kill_gate 0.02 → STARVE=TRUE. **fab-control(사전등록): |V0_surface|=2/80(rate 0.025) INFLATES vs true(2>0) = verifier 무결 확인**(surface-detector가 non-composition 2개 통과 = 예측대로 fab). coherent=80/80(fluency 정상 = undertrain/garble 아님, 진짜 composition floor). STaR/RFT-KD은 non-empty verified set V0 필요한데 frozen gate surface-form서 base의 V0=空 → 부트스트랩할 것 없음. EM 미렌트(설계대로). [[H_9120]] coverage-floor + ByteGPT single=2/composed-lift-0 정합. **wired:** n/a(ckpt 미생성). 비용 ≈$0.25-0.30(r1 43794031 preempt-GONE 후 r2 43795355 재렌트, 둘 다 teardown 확인). 상세 state/g1_train_wallbreak/star/VERDICT.txt.
> **함의:** STaR은 base best-of-K가 이미 non-empty composition-TRUE V0 내는 G0🟢 trunk 위에서만 성립 — 즉 recomb-OBJECTIVE lever(γ trained-constructive-bind [[H_1840]])가 G1을 먼저 열어야 함. STaR은 스스로 필요한 floor를 못 만든다.
>
> **정직 스코프(c9):** 둘 다 toy-DIRECTIONAL(a_toy_scale_recheck: 303M floor면 STaR verified set 空·derivation은 copy-head 벽 위험). terminal=303M pool warm-FT→engine-native --py 채점. tier=DIRECTIONAL until engine-native.
> **slug:** `g1_train_wallbreak` · **date:** 2026-07-04

## artifacts
- `state/g1_train_wallbreak/SYNTHESIS.md` (14 레버 census + deep-L8 CLOSED 증거 + survivor prereg)
- `state/g1_train_wallbreak/star/` (레버2 STaR STEP-0 early-kill: VERDICT.txt · step0_result.json · step0.log · step0_earlykill.py)
- 상위: [[H_9120]](objective-floor terminal) · [[H_6185]]/[[H_6188]](coverage+RF·deep-L8 FALSIFIED) · [[H_1840]](γ trained-constructive-bind 미발사)
