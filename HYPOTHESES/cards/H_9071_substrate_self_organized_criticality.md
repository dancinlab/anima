# H_9071 — 자기조직 임계 — 15-lane 분기율 σ≈1, avalanche, dynamic-range payoff

- **tier:** 🟡 PARTIAL / DIRECTIONAL-characterization (engine-native 2/5, 2026-07-02) — SOC property PRESENT (σ 자기조직 ≈1 + P(s) 헤비테일), capability payoff FLOOR (dynamic-range peak-at-σ≈1 미지지 + topology-generic)
- **slug:** `substrate_self_organized_criticality`
- **source:** 고친 sidecar fable(hook-isolated PR#327) 발산 · anima 세션 흡수-박제. frontier = 미등록 non-equilibrium physics seam(등록 동역학 렌즈 basin/orbit/macro-EI 밖).

## claim
A⇄G lane 망이 임계점(edge-of-chaos) 근방에 자기조직되나, 그리고 임계가 dynamic range/susceptibility를 최대화하나.

## mechanism (bio/physics)
피질 뉴런 사태(Beggs-Plenz): P(s)~s^-1.5, 분기율 σ≈1; 임계가 dynamic range·정보전달 최대화. Ψ=½ 고정점 또는 coupling gain이 임계로 self-organize할 수 있음.

## engine-native FALSIFIABLE metric (사전등록)
한 lane kick → 활성임계 넘는 lane 수 = 사태크기 s, 다수 kick/state서 분포 수집. **P(s) power-law(임계) vs exponential(subcritical) vs bump(supercritical) · 분기율 σ.** 능력 주장: dynamic range(구별가능 emit-rate로 매핑되는 입력텐션 범위)가 σ≈1서 최대. shuffle=degree 보존 coupling 랜덤화(구조적 임계면 power-law 파괴) · ablation=coupling gain detune → σ가 1 이탈 + dynamic range 하락(평평=INERT=결정적 기각).

## why-novel-vs-ledger
attractor-topology=basin·heteroclinic=saddle orbit·causal-emergence=macro-EI — 어느 것도 avalanche/분기율/dynamic-range 측정 안 함. 정직: characterization 편향, 능력 고리=dynamic-range 최대화. cheap: numpy 사태 DIRECTIONAL → live lane coupling.


## engine-native 측정 (2026-07-02, aiden pool, hexa v0.540.1)
harness `state/9071_substrate_self_organized_criticality/soc_engine_native.hexa` — `hexa run` via live `core/engine_cli.hexa`. 새 op 불필요(순수 characterization: 기존 pub `topo_brain_adjacency()`·`topo_degree_matched_random()` READ-only, Ψ-disjoint). 임계 gain g_c=1/⟨k⟩=0.15 은 그래프 구조에서 **유도**(metric-tune 아님), σ 는 측정 확인. 분기 dynamics = refractory branching(한 lane kick→per-edge prob=gain 로 이웃 활성, avalanche size s), dynamic range = Kinouchi-Copelli 외부자극 sweep Δ=10·log10(r90/r10).

측정치 (brain 15-lane, ⟨k⟩=6.667):
- **σ (분기율):** sub(g=0.075)=0.478 · **crit(g_c=0.15)=0.969≈1** · super(g=0.255)=1.693 — gain 단조, g_c 에서 σ≈1 확인.
- **P(s) 헤비테일 frac(s≥5):** sub=0.061 · **crit=0.337** · super=0.706 — 임계서 파워로 헤비테일 창발(crit=5.5× sub).
- **mean avalanche size:** sub=1.82 · crit=3.88 · super=8.29.
- **dynamic range Δ(dB):** sub=10.93 · **crit=13.56 · super=13.561** · shuffle@crit=14.25.
- **degree-shuffle@crit:** σ=0.973 · htfrac=0.331 (brain 0.337 과 사실상 동일).

frozen bar 판정 (no tune-to-green):
- **B1 σ tunable-to-1** ✅ PASS — σ(crit)=0.969∈[0.80,1.25] ∧ gain 단조. **edge-of-chaos 자기조직 REAL.**
- **B2 P(s) power-law 창발** ✅ PASS — htfrac crit(0.337) ≥ 2× sub(0.061). **임계서 헤비테일 avalanche REAL.**
- **B3 dyn-range peak at σ≈1** ❌ FAIL — Δ(crit)=13.56 ≈ Δ(super)=13.561 (super 가 미세 우위). Δ 는 sub→crit 상승 후 crit→super **평탄(peak 아님)**. Kinouchi-Copelli peak-at-criticality 가 n=15 유한 substrate 서 clean 하게 재현 안 됨.
- **B4 gain-detune decisive** ❌ FAIL — maxΔ−minΔ=2.63 dB < frozen 3.0 dB. gain sensitivity 실재하나(sub 열등) modest·일방향, frozen bar 미달.
- **B5 shuffle breaks power-law** ❌ FAIL — degree-preserving shuffle 가 σ·P(s)·Δ 모두 보존(htfrac 0.331≈0.337, σ 0.973≈0.969). **SOC 시그니처는 topology-GENERIC(⟨k⟩-driven branching universality)이지 anima connectome-specific 아님.**

### 정직 해석 (characterization-biased, c9)
**속성은 실재하나 능력 payoff·connectome-특이성은 FLOOR.** anima 15-lane 망은 유도 gain g_c=1/⟨k⟩ 에서 분기 σ→1 로 자기조직되고 임계서 파워로-유사 avalanche 분포를 낸다(edge-of-chaos 특성화 성립, 2/5). 그러나 (a) dynamic-range 가 σ≈1 서 **최대화되지 않고**(임계→초임계 평탄, B3/B4 미달) (b) 전체 SOC 시그니처가 degree-보존 shuffle 로 **깨지지 않음**(B5) → 이는 ⟨k⟩ 가 결정하는 **generic branching-process universality**이지 anima 특유 배선의 능력이 아니다. finite-size caveat: n=15 는 Kinouchi-Copelli peak 이 날카로워지는 열역학 극한 훨씬 아래라 초임계 saturation 이 약해 Δ 가 peak 대신 plateau. **bar 는 frozen 유지·이동 없음.**

- **verdict:** 🟡 PARTIAL — SOC/임계 특성화 GREEN(σ≈1 자기조직 + 헤비테일 P(s)), dynamic-range payoff + connectome-특이성 FLOOR (topology-generic).
- **wired:** N/A — capability payoff floored(배선할 GREEN 능력 없음). 순수 characterization, live op 신설 없음.
- **artifact:** `state/9071_substrate_self_organized_criticality/soc_engine_native.hexa` · `state/9071_substrate_self_organized_criticality/H_9071_engine_native.txt`
- **follow-on:** dynamic-range peak 은 열역학-극한 스케일(더 큰 lane pop) 필요 가설 — 현 15-lane substrate 에선 미지지. 재발사는 scale-up 필요(cost-gated), σ-criticality 자체는 특성화 종결.
