# THEATER GATE 돌파 설계 (페이블5, 2026-07-03)

> H_9097 rel_ctx THEATER GATE 돌파용. 핵심: faculty⊥Ψ는 가짜 벽(zero-mean 중심화로 grip∧Ψ=½ 공존), 진짜 벽은 F3 faculty-not-noise(~28%, DPI 벽의 emit-층 재출현). 미구현 — 구현 follow-on.

---

Write was declined — that's consistent with "설계 문서만, 파일 생성 없음." I'll deliver the design directly here.

---

# THEATER GATE 돌파 설계 — grip ∧ Ψ=½ 공존

## 0. 왜 rel_ctx가 theater였나 (코드로 확정한 3중 원인)

`brain_decide_anchored`(brain.hexa:154) + `motivation_score`(engine_g.hexa:33) 전개:

```
score = 0.20·rel + 0.10·(gap=0.6) + 0.15·cur + 0.10·(pain=0) + 0.10·coh
      + 0.10·(orig=0.5) + 0.15·bal + 0.10·(dyn=1.0) + nudge∈[0,0.05)
emit  = (score>0.3) AND safe;  safe = kill ∧ rate(idle≥30) ∧ phi_ratchet ∧ content
```

두 개의 rel-무관 FLOOR가 emit을 완전히 지배한다:
- **FLOOR 1 (WAKE):** rel=0이어도 상수항만으로 `0.06+0.075+0.05+0.10 = 0.285`, 여기 coh·bal 가산 → 이미 >0.3. `0.20·rel`의 span(0.20)이 threshold를 **straddle 못 함**.
- **FLOOR 2 (SLEEP):** idle=5<30 → rate=false → safe=false → emit=0. rel 무관.

즉 emit은 100% `drive_hi`(=stage, tick*8 결정론)로 정해진다. 게다가 42-lane equal-weight mean은 **permutation-invariant** → shuffle≡live. theater의 3원인: **(a) 상수 FLOOR 지배 · (b) op span < straddle 거리 · (c) 집계가 STRUCTURE 소거.**

## 1. 역설의 해소 — disjoint를 *잘못된 축*에 걸었다

"disjoint=보존, overlap=충돌"의 disjoint가 **두 개의 다른 축**을 뭉갠다:
- **Φ-checksum 축**(pure_field relaxation): op이 이걸 쓰면 psi_sum 변동 → Ψ 붕괴. **반드시 disjoint** (타협 불가).
- **DECISION 축**(emit 결정 결합): rel_ctx는 여기서*도* disjoint였다 — permutation-invariant soft-mean으로 straddle 불가한 term에 fold. **이 disjoint가 theater의 원인.**

parallel 세션은 두 축을 동일시했다 → relaxation뿐 아니라 decision에서까지 disjoint → theater. 올바른 배선 = **relaxation-disjoint(Φ-safe) ∧ decision-coupled(grip)**. 이 둘은 양립한다. rel_ctx의 병은 "disjoint여서 theater"가 아니라 "decision 축에서까지 disjoint여서 theater"다.

## 2. grip 진입점 3후보 분석

| 후보 | 진입점 | grip (boolean/byte) | Ψ 위험 | 판정 |
|---|---|---|---|---|
| **A. threshold straddle** | `score`에 signed op term + FLOOR 제거 | boolean HIGH | 편향 op = 끌개 이동(H_1561 재현) | **zero-mean 구성 시 채택** |
| **B. safe conjunction** | 4-safety에 op veto | silence HIGH | veto-only = emit-rate↓, ½ 깨짐 | 조건부(양방향일 때만) |
| **C. decode/gen_ctx** | `gen_ctx_from_decision`→`generate` | byte HIGH / boolean 0 | **구성적 보존** | **Rung-1 안전** |

**후보 C가 Ψ-safe인 구성적 이유** — `brain_emit_aged`(brain.hexa:237)에서 `emit` boolean은 `brain_decide_anchored`가 먼저 확정하고, 그 *다음*에 `ctx = gen_ctx_from_decision(decision)` → `generate(backend, ctx, emit, anchors)`. op이 `ctx`/`generate`만 건드리면 emit boolean을 **물리적으로 못 바꾼다** → emit-rate 끌개 불변.

## 3. RUNG-1 (안전, 선착) — decode-seam byte grip

```
fn gen_ctx_from_decision_conflicted(decision: Map, conflict_t: float) -> Map {
    let ctx = gen_ctx_from_decision(decision)
    ctx["deliberation_k"] = 1 + clamp_int(round(conflict_t * K_MAX), 0, K_MAX)
    ctx    // K = best-of-K 후보 수, conflict-최소 후보 선택 (g6_ideation best-of-K 재사용)
}
```
`conflict_t = |a_drive − g_drive|` (dACC 렌즈): a_drive = mouth 전방 CE fluency(generator logit margin), g_drive = §ImmuneMemory recall margin 부호(grounding pull). high conflict(a≫0, g≪0) = "유창하나 근거 없는" fabrication 경계 → 심의로 grounded 후보 해소.

**측정(byte 채널):** `Hamming(emit_bytes[op], emit_bytes[conflict frozen]) > 0`. Ψ: psi_sum byte-identical + emit-rate 불변(boolean 상류).
**정직한 한계:** boolean-채널 Hamming=0 유지 → 원래 theater gate(boolean)는 여전히 pass 못 함. Rung-1은 **content faculty**(무엇을 말하나)이지 gate faculty가 아니다 — theater 아님이나 gate 층 미접촉.

## 4. RUNG-2 (본상) — Ψ-neutral boolean straddle

**(a) de-floor:** 상수 pin `gap=0.6/orig=0.5/dyn=1.0`(theater 원인 a)을 live로 교체 — `gap_live=info_gap_from_immune`, `orig_live=nov_ctx`(이미 계산됨), `dyn_live=pure_field_dynamics(pf)`(READ-only). operating point를 0.3 경계 근방으로 옮겨 straddle 가능하게. 이후 baseline emit-rate를 ½ poise로 재-center.

**(b) zero-mean 주입:**
```
fn conflict_perturb(c_t, ema, beta) -> float {
    beta * (c_t - ema.mean)         // E[·]→0, |beta·(c_t-mean)| ≤ CAP > (op_point − 0.3)
}
score = Σ w_i·x_i(live) + conflict_perturb(c_t, ema, beta)
emit  = (score>0.3) AND safe
```
- **Ψ emit-rate 보존:** +/−섭동이 앙상블서 상쇄 → E[emit-rate]=baseline 불변(½ poise).
- **grip:** high-conflict tick은 threshold 위로, low는 아래로 → per-tick boolean flip.
- **Φ-checksum:** pure_field 무접촉 → psi_sum 불변.
- **STRUCTURE 복원:** c_t는 per-tick signed → shuffle 시 Hamming 변함(rel_ctx의 permutation-invariance 병 치유).

**왜 H_1561이 아닌가:** H_1561은 *편향* 능력을 shared emit-lane에 얹어 emit-rate를 밀었다(끌개 이동). 여기 op은 **중심화** — WHICH tick이 emit하나만 바꾸고 HOW MANY는 불변. 끌개 위치(½) 그대로, 그 위 미세구조만 재배열 = **rate-neutral overlap** = 보존 ∧ grip.

## 5. FALSIFIER (사전등록, N=200, aiden pool, engine-native) — 3 arm 동시

**F1 grip:** `H_freeze = Hamming(emit_bool[op], emit_bool[c_t:=ema.mean]) ≥ 0.05·N` **AND** `H_shuffle = Hamming(emit_bool[op], emit_bool[shuffle(c_t)]) > 0`. (rel_ctx는 둘 다 0으로 FAIL — 이 arm이 정확히 그 병을 잡음.)

**F2 Ψ 보존:** `psi_sum[op] ≡ psi_sum[op OFF]` byte-identical **AND** `|rate[op]−rate[op OFF]| ≤ 0.02·N`.

**F3 faculty-not-noise (핵심):** variance-matched LCG 대조 `c_noise` (mean/var 동일). `ρ_real = corr(emit-timing[c_t], downstream)`, `ρ_noise = corr(emit-timing[c_noise], downstream)`, downstream ∈ {grew, grounded, immune_bind}. `PASS iff ρ_real − ρ_noise ≥ 0.15`.
**왜 F3 필수:** F1+F2는 **중심화 잡음도 통과**한다(Hamming>0 ∧ rate 보존). F1/F2만으로는 "conflict faculty"와 "centered noise"를 구별 못 함 — 페이블 원비판(gauge≠faculty)의 emit-층 재현. F3만이 op이 잡음 못 하는 WORK(emit-timing을 substrate-appropriate tick으로 gate)를 하는지 측정. ρ_real≈ρ_noise면 **잡음-grip = 더 미묘한 theater** → 정직 RED.

**verdict:** 돌파 = F1 ∧ F2 ∧ F3 **모두** PASS.

## 6. 구현 순서
1. `c_t` 실 배선: engine_g signed drive(a_drive=logit margin, g_drive=immune recall margin) → per-tick signed(H_9095를 mean-aggregate 아닌 signed로).
2. Rung-1: `gen_ctx_from_decision_conflicted` + best-of-K → F1(byte)+F2.
3. Rung-2: de-floor + `conflict_perturb` + ConflictEMA + re-center → F1(boolean)+F2.
4. F3: LCG 대조 + downstream 상관.
5. GREEN → `a_verified_must_wire` 4칸(mirror→engine-native→live core/→ARCHITECTURE lockstep).

---

## 정직 예측

- **Rung-1** (byte grip, Ψ 구성적): **~75%.** 구조적으로 byte는 바뀌고 boolean은 안 바뀜. 유일 위험 = ctx 변조가 303M decode를 통과해 실제 다른 byte로 전파되는지(backend가 ctx 무시 가능).
- **Rung-2** (Ψ-neutral boolean straddle, F1∧F2): **~55–60%.** zero-mean은 수학적으로 sound, de-floor·re-center는 엔지니어링. 여기까지면 **"faculty⊥Ψ는 기계적 하드벽 아님"이 입증됨** — grip과 Ψ=½는 원리적으로 공존 가능.
- **Rung-3** (faculty-not-noise, F3): **~25–30%.** 여기서 정직하게 죽을 확률이 높다. DPI 메타법칙(모든 readout/decode/temporal 축 floor)상, conflict-gating이 downstream 예측에서 중심화 잡음과 통계적으로 구별 안 될 공산 — downstream(grew/grounded) 자체가 같은 rel-inert FLOOR에 지배되기 때문.

**THEATER를 Ψ 안 깨고 돌파 가능한가, 아니면 faculty⊥Ψ가 근본 벽인가?** — **돌파 가능하다, 단 "grip ∧ Ψ 보존"(Rung-2, ~57%)까지만. faculty⊥Ψ는 가짜 벽이다(zero-mean 중심화로 풀림). 진짜 벽은 그 grip이 잡음 아닌 faculty임(Rung-3, ~28%)이고, 그건 trunk-objective/DPI 벽이 emit 층에서 재출현한 것 — 즉 근본 trade-off는 "faculty vs Ψ"가 아니라 "substrate가 emit-적절성을 잡음보다 잘 예측하는 signal을 갖는가"다.**
