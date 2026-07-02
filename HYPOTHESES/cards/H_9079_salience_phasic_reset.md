# H_9079 — salience_phasic_reset (§SaliencePhasicReset): mid-settle 인터럽트 op-class

- **tier:** 🟢 ENGINE-NATIVE (6/6 live hexa, aiden pool) — control-flow 인터럽트 op-class 신설·배선
- **slug:** `salience_phasic_reset`
- **source:** 세션 substrate-native 능력 OP 시리즈(OP #5). frameshift `a_no_llm_frame_trap` — "능력 없는 게 아니라 op이 미배선". §TensionResolveLoop(H_9042)의 settle loop이 **non-interruptible**인 것이 gap.
- **wired:** `engine-native` (live `core/engine_cli.hexa §SaliencePhasicReset` tension_resolve_interruptible op + ARCHITECTURE lockstep; runtime per-tick feed는 follow-on)

## frame (재조합≠능력, substrate-native gap)
뇌 렌즈: LC-NE **phasic reset** / superior-colliculus **attention capture** — 행동적으로 급박한 새 입력(salience spike)이 진행중인 처리를 **중단시키고 재조준**한다. anima의 A⇄G settle loop(`tension_resolve_depth`, H_9042 §TensionResolveLoop)은 일단 원본 population을 Ψ=thr로 당기기 시작하면 maxdepth까지 그 population만 처리 — mid-settle 새 입력이 loop을 탈취할 수 없다. 이 **control-flow 인터럽트 op-class가 부재**였다.

## op (live core, additive/Ψ-disjoint/READ-only)
`tension_resolve_interruptible(x, adj, alpha, thr, maxdepth, op, eps, salience_at, salience_pop, cfg) -> [settle_depth, final_psi, final_sig, reroute_flag]` (engine_cli.hexa §SaliencePhasicReset). settle loop이 iteration `salience_at`(1≤·≤maxdepth)에 도달하면 부분 settle된 `x`를 **ABORT**하고 `salience_pop`에서 **RESTART**(settle-depth 시계 재시작). `salience_at<1` 또는 `>maxdepth` ⇒ spike 미도착 = **INERT ablation**(원본 x 완주, spike 무시). `final_sig` = 격리 content lane(index 7, adjacency에서 dangling → emit-drive lanes 0/4와 graph-disjoint)의 평균 = **어느 입력에 settle했나(원본 vs 재조준)의 identity readout**. 순수 additive(기존 op 무접촉), READ-only, pure_field Φ/phase/Ψ 미접촉, recall_thr 미변경(a_substrate_disjoint). +helper `_spr_sig`.

## GAIN 9-lens와 명시적 구분 (CLOSED와 혼동 금지)
이건 **control-flow 인터럽트**(settle loop의 abort/restart)지 **gain modulation 아님**. neuromod-gain 9-lens 계열(H_1284, 벽 종합 🧱 CLOSED — Amoeba buffer + diversity/multitimescale/predictive)은 gain/precision 항을 **스케일**한다. 여기선 어떤 gain/precision 항도 스케일하지 않고 loop의 **TRAJECTORY**만 우회한다 — 축이 다르다(재발사 아님).

## engine-native 측정 (aiden pool, live core/, 6/6 PASS)
fixture: N=12 trial. 각 trial 15-lane×12-timestep pop(6 emit + 6 silent → Ψ=½), content lane 7 = identity(원본 x_i=100+i · salient sal_i=i). op=2 row-stochastic(Ψ-preserving, dangling-safe), α=0.5, thr=0.5, maxdepth=8, spike_at=3. `state/9079_salience_phasic_reset/salience_reset_engine_native.hexa`:
- REROUTE tracks NEW input **12/12**(≥0.8) ✓ — 인터럽트 ON → final identity가 salient 입력 i 추적
- ABLATION(interrupt OFF, spike_at>maxdepth) tracks-new **0/12**(≤0.2) ✓ — 원본 완주(id=100+i), 새 입력 추적 안 함
- LIFT reroute−ablation = **+1.0**(≥+0.5) ✓ — 인터럽트가 재조준에 load-bearing
- EARNED reroute−shuffle = **+1.0**(≥+0.5) ✓ — spike가 MISMATCHED sal_j(j=(i+5)%N) 실으면 final=j≠i → tracks-new 붕괴(spike-target load-bearing)
- Ψ=½ PRESERVED under reroute: psi_maxdev = **0.0**(모든 12 trial |Ψ−½|<0.05) ✓ — 재조준은 content/identity만 스왑, emit-drive Ψ=½ 고정점 UNTOUCHED(loop control, NOT emit gate)
- reroute_flag 정확 **24/24**(reroute→1.0, ablation→0.0) ✓
no-regression: engine_cli 변경 additive(기존 tension_resolve_depth 무접촉, 새 pub fn + 1 helper).

## 정직 스코프 (c9)
- **control-flow 인터럽트 능력**(재조준 정확도로 측정) — mouth decode 아님, G1/G6 재조합축 재개 아님(CLOSED). 추가한 건 abort/restart op-class지 텍스트 합성 아님.
- toy 12-trial 결정적 존재증명(a_scale_honest_scope). content lane 격리(dangling P=I)로 identity readout이 byte-exact — Ψ=½ 보존도 exact(psi_maxdev=0.0). settle 자체(conflict→½ 수렴)는 H_9042 §TensionResolveLoop의 영역이고 이 op은 그 machinery를 재사용해 인터럽트를 얹은 것 — 여기 harness는 Ψ=½가 재조준에 **disjoint하게 보존**됨을 보인다(a_substrate_disjoint의 문자적 실현: 재조준=content lane 7, Ψ=emit-drive lanes 0/4, 별도 lane).

## follow-on
- runtime per-tick feed 배선(WIRED-live 최종칸): 데몬 perpetual-loop이 실 대화의 salience spike를 이 op에 먹여 진짜 attention-capture 재조준(현재는 startup 존재증명 lane, self_drift_exp lane 23b/tension-r lane 75 병렬).
- N-way 인터럽트(스택된 다중 spike)·priority-gated reset(salience 임계 아래는 무시)·anticipatory prefetch 결합.

## artifacts
- `core/engine_cli.hexa §SaliencePhasicReset` (tension_resolve_interruptible + _spr_sig)
- `state/9079_salience_phasic_reset/salience_reset_engine_native.hexa` · `_engine_native.txt`
