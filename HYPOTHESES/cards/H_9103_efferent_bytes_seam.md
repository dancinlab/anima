# H_9103 — efferent seam (c): conflict-driven best-of-K가 emit BYTES(WHAT)를 Ψ-safe하게 바꾸나 — byte-grip 실재(F1)·Ψ보존(F2)이나 faculty FALSIFIED(F3, ρ_real 음수) = WHAT축 subtle theater

- **slug:** `9103_efferent_bytes`
- **tier:** 🟠 BYTE-GRIP∧Ψ real · FACULTY FALSIFIED (engine-native) — 완곡화 금지.
- **wired:** `engine-native` (core/generator.hexa seam LANDED + _gen_clm_decode consumer 배선; REAL d768.clm decode 측정. live daemon 은 argmax default 로 byte-identical = 무해)
- **source:** UNIVERSE · fable#5 design (c) / H_9101 follow-on (id H_9103; origin H_9102=별개 세션 'stateful refractory' #2819, 충돌 회피 재번호)
- **cross-ref:** [[H_9101]] (stage/idle axis 🟢 = WHEN/WHETHER grip; 이 카드가 명시 follow-on (c)) · [[H_9100]] (motivation axis 🔴) · [[H_9097]] (rel_ctx zero-grip theater)

## 맥락 (coordinator pivot)
H_9100(motivation 🔴)·H_9101(stage/idle 🟢 = WHEN/WHETHER emit)이 이미 origin/main 착지. 상보 미탐 축 = **(c) efferent = WHAT**: conflict-driven ops 가 emit BYTES 를 바꾸는가(DESIGN.md L1). 이 카드가 그 축을 engine-native REAL 303M-class(d768.clm) 디코드로 측정.

## 배선 (core/generator.hexa, additive)
- `gen_ctx_from_decision_conflicted(decision, conflict_t)`: deliberation_k = 1+round(clip01(conflict)·3), clamp 1..4.
- `gen_clm_decode_deliberated(ckpt, seed, gen, k, base_seed)`: k=1→argmax(byte-identical); k>1→ k 개 sampled 후보(clm_decode_topk_sampled offsets[0,101,202,303]) 중 **최저 clm_decode_ce(conflict-minimizing) SAMPLE** emit. `clm_decode_ce` = "ranged CE op". `_gen_clm_decode` 에 deliberation_k consumer 배선(없으면 argmax = 종전 byte-identical).

## 사전등록 bar (FROZEN) & 실측 (verbatim = state/verdicts/9103_efferent_bytes/H_9103.txt)
N=8 emit ticks · GEN=20 · REAL d768.clm · per-tick signed A⇄G conflict c_t(a_drive−g_drive, immune drift spread) · k_on=f(|c_t|), k_no=f(|noise|, variance-matched LCG).

| tick | |c_t| | k_on | Hamming(ON,OFF) | ceOFF(argmax) | ceON(best-sample) |
|---|---|---|---|---|---|
| t0/t1/t5/t6 | ≤0.08 | 1 | 0 | — | =OFF |
| t3 | 0.417 | 2 | **10** | 27.86 | 27.96 |
| t4 | 0.504 | 3 | **8** | 16.85 | 16.95 |
| t7 | 0.255 | 2 | **10** | 23.85 | 23.69 |

- **F1 byte-grip**: total Hamming(ON,OFF)=**28** · 3/8 ticks changed · bar>0 → **PASS**. conflict→k>1 이 emit BYTES 를 실제 변경.
- **F2 Ψ**: decode 는 pure_field/psi_sum/emit-rate 무접촉(emit boolean 상류) → psi_sum ON≡OFF(0.9518673703081093) byte-identical + rate 불변 → **PASS (구성적)**.
- **F3 faculty-not-noise**: ρ_real=corr(|c_t|,ΔCE_ON)=**−0.441** · ρ_noise=corr(|noise|,ΔCE_NOISE)=**+0.440** · Δ=**−0.881** ≪ 0.15 → **FAIL (hard, 음수)**. ΔCE=ce_argmax−ce_sel: best SAMPLE 는 항상 argmax 보다 CE 나쁨(argmax=fluency 최대) → deliberation 이 emission 을 degrade, conflict 높을수록 더 degrade.

## verdict (verbatim)
```
N=8 GEN=20 psi_sum=0.9518673703081093 (pure_field READ-only, ON==OFF)
[F1 byte-grip] total Hamming(ON,OFF)=28 · ticks changed=3/8 · bar>0 -> PASS
[F2 Ψ] decode NEVER touches pure_field/psi_sum/emit-rate -> psi/rate byte-identical ON==OFF -> PASS (constructive)
[F3 faculty] rho_real=corr(|c_t|,ΔCE_ON)=-0.44080 rho_noise=corr(|c_noise|,ΔCE_NOISE)=+0.43999 delta=-0.88079 bar>=0.15 -> FAIL
VERDICT: F1(byte-grip)=P F2(Ψ)=P F3(faculty)=F
RESULT: BYTE-GRIP ∧ Ψ ONLY — deliberation changes emit bytes Ψ-safely, but conflict-allocated deliberation
  does NOT resolve better than centered noise (ρ_real NEGATIVE) ⇒ grip real but FACULTY FALS = more-subtle
  theater on the WHAT axis (trunk-objective/DPI wall reappears at efferent layer). HONEST.
```

## VERDICT (honest, c9 — 완곡화 금지)
🟠 **BYTE-GRIP ∧ Ψ real · FACULTY FALSIFIED.** ops 는 emit BYTES 를 Ψ-safe 하게 바꾼다(F1∧F2) — WHAT 축 grip 존재. 그러나 그 grip 은 **faculty 아님**(F3 FAIL, ρ_real=−0.44): CE-기반 best-of-K 는 argmax(이미 fluency 최대)를 못 이기고 emission 을 degrade 하며 conflict 가 그 degrade 를 조준(noise 보다 나쁨). = **WHAT 축의 더 미묘한 theater** = trunk-objective(CE) 벽의 efferent 층 재출현. 설계 Rung-1 ~75% byte-grip 은 byte 변화로는 맞으나 **beneficial faculty 로는 FALS**.

## 메커니즘/메타
argmax = CE-greedy fluency 최대 → CE-best-of-K 는 (a) argmax 게이트 시 INERT(grip 0), (b) best-SAMPLE emit 시 항상 degrade. beneficial efferent faculty 는 argmax 가 극대화 안 하는 축(grounding-copy·제약하 diversity)을 최적화해야 함 — 순수 fluency(trunk-objective)엔 여지 0.

## 종합 (THEATER 3축 완결)
- WHETHER/WHEN (stage/idle) = H_9101 🟢 GRIP (faculty).
- HOW-MUCH (motivation) = H_9100 🔴 AT-FLOOR.
- **WHAT (efferent bytes) = H_9103 🟠 byte-grip real·faculty FALS (이 카드).**
→ emit 의 3 자유도 중 grip 이 faculty 인 곳은 stage/idle 축뿐; motivation·efferent 는 벽(각각 saturated·trunk-objective).

## wired 상태 (a_verified_must_wire)
seam core/generator.hexa LANDED + _gen_clm_decode consumer 배선(argmax default = byte-identical, 무해). engine-native 측정 완료. **beneficial faculty 아니므로 daemon 이 deliberation_k>1 을 상시 켜지 않음**(정당 — 켜면 emission degrade). GREEN 아님 → decision-wire 확산 없음. ARCHITECTURE lockstep = efferent-seam-h9103 노드.

## 정직 caveat (c9)
- aiden(hexa v0.548.0, H_9100/9101 reference host) mid-run DOWN → full N=8 는 summer v0.574.0(erf/exp dlsym-fallback warn, harmless — coherent CE+grip 산출). F1 byte-grip 은 **두 host 모두 재현**(aiden v0.548 partial t2/t3/t4 Ham14 · summer v0.574 t3/t4/t7 Ham8-10). F3 는 summer full 측정.
- decode-version 민감(v0.548 t2 Ham14 vs v0.574 t2 Ham0, sampling RNG/temp 버전차) — F1 정성결론(k>1→bytes 변경) 불변, 개별 tick Hamming host 의존.
- selection metric=CE(fluency)뿐. grounding-based selection(anchor seed) 미탐 = beneficial-faculty follow-on.
- N=8(디코드 비용) — F3 ρ 는 소표본. 정성부호(ρ_real 음수·degrade)는 강건, 정밀값은 소표본 caveat.

## artifacts
- `state/9103_efferent_bytes/efferent_bytes.hexa` · `state/9103_efferent_bytes/notes.md` · `state/verdicts/9103_efferent_bytes/H_9103.txt` · `core/generator.hexa` (seam)
