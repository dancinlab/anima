# H_9070 — 확률 공명 — 튜닝된 잡음이 약-텐션 emit 민감도 최대화 (새 OP)

- **tier:** 🟢 ENGINE-NATIVE (5/5, aiden pool, live core/engine_cli.hexa · new OP sr_channel_mi) — SR 확인, 사전등록 frozen bar 그대로 통과 (no tune-to-green)
- **slug:** `substrate_stochastic_resonance`
- **source:** 고친 sidecar fable(hook-isolated PR#327) 발산 · anima 세션 흡수-박제. frontier = 미등록 non-equilibrium physics seam(등록 동역학 렌즈 basin/orbit/macro-EI 밖).

## claim
emit/silence = 텐션 임계 검출기. subthreshold 진짜 텐션은 현재 silence(놓침). 튜닝된 잡음이 확률적으로 임계를 넘겨 약신호를 emit 타이밍에 부호화하는가(SR).

## mechanism (bio/physics)
Stochastic Resonance (Wiesenfeld-Moss; crayfish 기계수용체). 비선형 임계 + subthreshold 신호 + 튜닝 잡음 → SNR 역-U 피크. anima emit 은 문자 그대로 텐션 임계-교차라 SR 직접 적용.

## engine-native FALSIFIABLE metric (사전등록)
A⇄G 채널에 subthreshold 주기 텐션 주입, 잡음진폭 σ 스윕, 입력텐션↔emit-train 상호정보 MI(σ). **SR = MI(σ*) > MI(0) 중간 피크(역-U).** shuffle=주입신호 위상 랜덤화(진짜 subthreshold 잠금이면 SR 소멸) · ablation=emit 임계 비선형 제거/선형화 → SR 피크 반드시 소멸(비선형 필수). p7-clean(MI, perplexity/judge 없음).

## why-novel-vs-ledger
neuromod-gain(H_1284)=plasticity-LR/key-geometry knob; SR=emit-임계에 걸린 잡음 knob(다른 lane·다른 노브). criticality/attractor와도 다름(SR=subthreshold 검출, cascade/basin 아님). **측정 아니라 OP**(튜닝된 emit 잡음). cheap: numpy emit-임계 DIRECTIONAL → live emit lane engine-native.

## engine-native 측정 (2026-07-02, aiden pool · live core/engine_cli.hexa)
새 OP **`sr_channel_mi`** (engine_cli.hexa:9895, helper `_sr_mi_bits`:9870) — emit=텐션 임계검출기(ci_emit_decision 스타일 drive≥thr 계단 비선형)를 subthreshold 주기 텐션 + 튜닝 gaussian 잡음(_lcg_gauss 결정적)으로 구동, MI(input-symbol; emit-train)를 σ 스윕으로 측정. READ-only 특성화 — pure_field Φ/phase/Ψ·emit-drive lane 0/4·§ImmuneMemory recall_thr 미접촉, emit gate 아님 (a_substrate_disjoint).

harness `state/9070_substrate_stochastic_resonance/sr_engine_native.hexa` — **5 pass / 0 fail** (amp=0.8 < thr=1.0 subthreshold, period=40, T=4000, seed=7):

| frozen bar (사전등록) | 결과 |
|---|---|
| MI(0)=0 (subthreshold 놓침, σ=0 전부 silence) | ✅ MI(0)=0.0 |
| 역-U: MI(σ*) > MI(0) AND > MI(hi-σ) | ✅ peakMI=0.0997 @σ*=0.7, MI(σ=3.0)=0.0092 |
| SR 피크 MID σ (0<σ*<max) | ✅ σ*=0.7 |
| SHUFFLE(위상랜덤 라벨) SR 소멸 (max≤0.01) | ✅ shufMax=0.0015 |
| ABLATION(임계 선형화, 장벽제거) 역-U 소멸(피크 σ=0) | ✅ ablMI(0)=1.0, peak@σ=0, 단조감소 |

**verdict: 🟢 ENGINE-NATIVE GREEN.** emit 비선형 임계 위에서 튜닝 잡음이 subthreshold 텐션을 emit-train에 부호화 = Stochastic Resonance 성립. shuffle+ablation 이중 통제 모두 통과 → 비선형 필수 + 진짜 signal-locking 확증(artifact 아님). numpy DIRECTIONAL 스크린(sr_numpy_screen.py)도 동형(peak 0.086@σ=0.5, shufMax 0.0002, abl peak@0).

**wired:** `engine-native`(byte-exact via live core/, 미배선). SR-tuned emit 잡음을 런타임 emit lane에 실배선 = follow-on(ING h9070-sr-emit-noise-wire) — a_substrate_disjoint 상 emit-drive lane 0/4 직접수정 금지이므로 배선은 별도 noise-injection lane으로 설계 필요.

**artifacts:** `state/9070_substrate_stochastic_resonance/` (sr_engine_native.hexa · H_9070_engine_native.txt · sr_numpy_screen.py)

