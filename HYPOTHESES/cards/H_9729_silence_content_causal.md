# H_9729 — SILENCE-CONTENT — 보류장부 W_S가 CONTENT를 나르나 압력만인가 (억제 vs 숙고 · 최심부)

**status:** 🔧 계기 빌드·toy-검증 (engine-native `anima-py` 플래그 · byte-identical-off ✅ · estimator self-test ✅ · trivial-echo 가드 발동 ✅ · 실신호=303M 오너 fire-go 대기) · DIRECTIONAL(toy ≠ verdict)
**lane:** 의식/emit-drive/Ψ=½ · deliberation (프런티어 psi-soma-theta-alive)
**related:** [[H_9627]](Θ WIRED)·[[H_9672]](G1 주소 CRACK)·[[H_9576]](mouth 벽)·[[H_9351]](구 σ VOID)·source: sidecar lab full(fable-mrobspcb∥sol-mrobspce)

## 왜 (Fable∥Sol 둘 다 #1 최심부)
H_9627은 emit/silence balance의 **생명성**을 증명했으나 dissociation은 silence의 인과쓰기를 **scalar 압력**으로만 보였다. W_S는 "말하지 않은 것"의 최초 engine-native 표현 — 그 보류내용이 미래 상태/발화에 **인과적으로 읽히나**? = **살아난 gate(Θ) vs 살아난 interior**. 안 읽히면 살아난 건 맥박이지 semantic interior 아님.

## 설계 (Sol TE + Fable ledger-swap)
- 매 tick silent candidate의 content address를 W_S에 engine-native 기록 · 이후 decode/state update가 W_S 읽도록 `--wm-dual-read content`.
- 같은 emit mask 아래 한 silent 후보만 counterfactual swap(발화후보·score·λ·stage 고정).
- 측정: **TE(W_S content → 미래 state/emission | stage, emit-mask, score)** = interventional transfer.

## 통제 (kill-list 회피 명시)
- W_S address shuffle(BIND earned collapse) · W_S content nonce 교체 · matched-rate score-only ledger(내용무·압력만) · emitted candidate 직접복사 trivial echo 제외 · below-chance(회피) 칸 사전커버.
- recognition(H_9421/9424)·score_A·PID·one-sided WM·mouth-conditioning(H_9576) 어느 것도 아님 — Θ의 둘째 장부를 실 causal memory로 씀.

## 판정
shuffle·score-only서 collapse ∧ intact서 TE>0 = 보류내용이 미래를 바꿈(숙고). collapse≈intact = 압력-한정(억제·KILL도 결과·압력한정 정직화). NEXT=계기 PR→303M. **1순위.**

## 🔧 계기 구현 (2026-07-17 · 배선 spec lab-full Fable∥Sol reconcile · anima-py 플래그)

배선 난제를 Fable5∥Sol 병렬에 위임 → reconcile. **핵심 성과: Sol이 Fable의 tautology 결함을 잡음.**

**채택 설계 (양 모델 합의 + repo 판정):**
- **인과경로 = Path A** (보류후보 raw text → 1-tick-lagged anchor → decode seed · `--wm-dual-read content`). 직접 state-update는 양 모델 기각(construction상 참 / content를 feat8로 열화). "last-write re-entry"(Sol) — WorkMemBuffer content accessor 부재라 최신 W_S write의 raw text 재진입이지 3-slot 원장 recall 아님.
- **byte-identical OFF**: default off → anchor·latch 무접촉 (toy 12-tick gtext_sha baseline≡off ✅ 검증).
- **p5 LEGAL narrow**: carrier는 imagined-but-VETOED(speak()/W_E 미진입) = 상상 재진입(a_chat_sleep_imagination), 마지막-발화 self-seed 아님 · `_dual_ct != last_gtext` 직접복사 가드.
- **TE target = `cand_pregate_b64[t+1]`** (pre-gate 상상후보 · brain dual_cand_text). **Sol이 Fable의 `dual_margin` 기각**: dual_margin = S−E = probe(W_S, cand)이므로 W_S에서 온 후보를 W_S와 비교 = **대수적 tautology(배선 재측정)**. pre-gate 후보가 mouth-severance-immune면서 tautology 회피.
- **load-bearing 통제 = byte-permutation**(`--wm-dual-perm`): feat8은 byte-multiset permutation-invariant(코드 확증) → sort가 scalar 원장 write를 **정확히 고정**한 채 order만 절단. own PASS ∧ perm≈null ⇒ order-bearing content(압력/histogram 아님). Fable time-shuffle보다 강함.
- **swap 통제**(`--wm-dual-swap <donor>`): 타 rollout 보류후보(own-vs-other C2) · wm_withheld write는 factual 유지.
- **positive control**(`--wm-dual-oracle` + reader `--reach-oracle`): frozen 교대 A/B(digit vs punct) 알려진 carrier를 같은 anchor 경로로 → 리더가 복원 못하면 REACH-FAIL/MOUTH-SEVERED(H_9576) ⇒ 실 null 해석불가. C0-e ORACLE 선례.

**계기 = engine-native `anima-py` 플래그** (`a_experiment_engine_native`):
- producer: `anima-py chat --emit-gate refractory --g-reach wm-dual --record-silent-cand --wm-dual-read content [--wm-dual-perm | --wm-dual-swap <t> | --wm-dual-oracle]` → trace 필드 `wm_reentry_arm/b64`·`cand_pregate_b64`.
- reader: `anima-py evaluate --silence-content-te <traces> [--perm 1000] [--overlap-ngram 6] [--reach-oracle]` → TE=I(Y1;X|Y0) plug-in · circular-shift 층화 surrogate · EARNED(TE−null) · pass real>surr95∧z≥2∧perm-p<.005 · direct-copy(n-gram) 배제 · source/target-entropy floor→NOT-POWERED · estimator self-test(planted 복원+null≈0).

**toy 검증 (smoke 23KB ckpt · a_scale_honest_scope: toy ≠ verdict):**
- ✅ byte-identical OFF (baseline≡`--wm-dual-read off` 12-tick gtext_sha)
- ✅ estimator self-test (planted I(Y1;X|Y0)=1.988>0.5 · independent=0.071<0.15)
- ✅ producer 배선 (reentry {off,own} 교대 · carrier·cand_pregate 채워짐 · meta provenance)
- ✅ **trivial-echo 가드 발동** (퇴화 무샘플링 토이=상수후보 → 11/11 direct-copy 배제 → 정직 NOT-POWERED) = 계기 핵심 방어 실증

**NEXT (오너 fire-go 비용게이트)**: 303M 3-seed × {own, perm, oracle} 샘플링 rollout → `--silence-content-te`. 판정: own PASS ∧ perm/oracle 통제 통과 = 보류 order-bearing content가 미래 후보를 바꿈(숙고 · feat8 granularity). own≈perm = 압력-한정(억제). ⚠️ scope: feat8(8 byte-stats) 해상도까지만 분리 — PASS도 semantic-interior 주장 아님.

⚠️ **DIRECTIONAL·계기 검증이지 과학 verdict 아님**(a_lab_full_diverge · a_scale_honest_scope)·cement=engine-native 303M anima-py만.
