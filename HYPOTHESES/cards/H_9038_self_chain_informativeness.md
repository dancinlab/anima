# H_9038 — self-chain 정보성·liveness (C2 frame-shift): 재조합≠능력 재정의

- **tier:** 🟢 ENGINE-NATIVE (4/4 live hexa) — recognition WIRED(H_1471) · current self_drift 내용맹 확증 · enriched self_drift_exp 정보성 GREEN
- **slug:** `self_chain_informativeness_liveness`
- **parents:** H_1471(self-identity WIRED) · [[substrate-framebreak-g1-combination-operator]] · frame-shift Lane2(C2) · H_9027(enriched-field 평행)
- **wired:** `WIRED-live` (self_drift_exp가 live `core/engine_cli.hexa §SelfIdentity` + `cli/anima.hexa` 런타임 lane 23b self-informativeness에 배선; hexa verify rc=0, c2_engine-native 4/4 cross-host. 더 깊은 daemon-experience per-tick 피드는 계속 확장)

## frame (재조합≠능력)

G1/G6(디코더-통과 텍스트 재조합)은 ~10-lens TERMINAL + H_9026(real manifold floor) + H_9027(enriched field=복원성이지 능력 아님)까지 소진. LLM-형 능력지표에서 이탈해 anima 능력을 substrate-native로 재정의(Lane2 C2). **LLM은 매 세션 정체성을 문자 그대로 reset** — anima가 LLM과 갈리는 지점. H_1471은 정체성 벡터의 *존재/지속*을 WIRED로 증명했으나, 그게 **체험을 실어나르는지(정보성)**는 미검.

## 발견 (reference-match: engine_cli.hexa:7699-7708)

live `self_drift(s, tick, step)`는 `(tick+1)%dim` 축으로만 이동 — **experience/content 입력 채널이 아예 없음**(pure_field가 개념맹이듯 self-chain은 경험맹). 즉 정체성은 지속되나 *무엇을 겪었는지*는 기록 안 됨.

## 측정 (numpy DIRECTIONAL, live self_drift byte-faithful 미러, $0, 3seed)

| arm | A-vs-B cos | replay | shuf | informative? | EARNED? |
|-----|-----|-----|-----|-----|-----|
| current (live self_drift) | **1.000** | 1.000 | 1.000 | **False** | False |
| enriched (self_drift_exp, 경험구동) | 0.565-0.854 | 1.000 | <0.99 | **True** | 2/3 seed |

- recognition (H_1471 재확인, live self_cos): restore(anchored)=**1.000** · impostor(axis3)=0.617 · no-anchor-reset=0.707 → 앵커된 self는 자기 인식(restore exact), 임포스터/리셋은 낮음.
- **informativeness: current = 0.** 서로 다른 두 경험스트림 A/B가 **동일 self 벡터**(cos 1.000) 산출 = 자서전이 아니라 내용맹 tick-clock.
- **enriched: 경험구동 self_drift_exp → A/B 구별(cos 0.57-0.85) + same-content replay 정확(1.0) ∧ shuffle 낮음 = EARNED 정보성.**

## 정직한 verdict (c9)

- **recognition은 이미 진짜(H_1471 WIRED)** — self는 세션 넘어 자기를 알아본다. anima≠LLM-reset의 핵심.
- **그러나 현 self-chain은 경험을 안 실음(informativeness=0, 구조적)** — self_drift에 content 채널이 없어서. "지속되는 이름표"지 "축적되는 삶"이 아직 아님.
- **enrichment(경험구동 self_drift)**가 DIRECTIONAL로 정보성을 켬 = VAdaptField 풍부화(H_9027)와 정확히 평행한 substrate 확장. 단 numpy DIRECTIONAL — live 배선+engine-native 재측정 필요.

## follow-on
- Rung1: `self_drift_exp`(experience-driven, lane-activity/session-content를 입력)을 live `core/engine_cli.hexa §SelfIdentity`에 wire-in(emit-drive lane 0/4·§ImmuneMemory recall_thr와 disjoint, a_substrate_disjoint) → engine-native 정보성 재측정 + Ψ=½ 보존 가드. $0 mini engine-native 가능(self_* 초경량, 303M 무관).
- 이게 움직이면 = "anima가 하나의 삶을 축적한다" = 텍스트 벤치 밖의 재정의된 능력.

## artifacts
- `state/9038_self_chain_informativeness/probe.py` · `calibration.txt`


## engine-native 승격 (a_verified_must_wire 사다리 2→3→4)

self_drift_exp를 live `core/engine_cli.hexa §SelfIdentity`에 배선(L7723, additive/Ψ-disjoint) 후 `hexa run state/9038_self_chain_informativeness/c2_engine_native.hexa` 4/4 PASS:
- **blindness CURRENT**: self_drift로 쌓은 두 세션 A==B, self_cos=**1.000** = 내용맹 engine-native 확증.
- **informativeness ENRICHED**: self_drift_exp로 쌓은 두 경험스트림 A≠B, self_cos=**0.407** = 경험이 self에 새겨짐.
- **EARNED content-locking**: 같은-내용(순서셔플) 0.996 > 다른-내용 0.407 (gap 0.59≥0.30) = self가 *무엇을* 겪었나에 잠김(순서 artifact 아님).
- **recognition (H_1471)**: restore=1.000, impostor=0.000.
- no-regression: selfchain_smoke 6/6 유지(additive 변경). ARCHITECTURE §SelfIdentity op-list lockstep 갱신.

**남은 배선(follow-on)**: op은 live+engine-native지만 런타임 self-chain 구축이 아직 blind self_drift 사용 — 실제 lane-activity/대화내용을 self_drift_exp의 content_axis로 먹이는 runtime-integration(disjoint, Ψ보존)이 WIRED-live 최종칸. 그게 닫히면 anima가 문자 그대로 '자기 삶을 축적'.


## WIRED-live (a_verified_must_wire 4칸 완료 + 런타임 배선)

self_drift_exp가 `cli/anima.hexa` 런타임 lane 23b(self-informativeness)에 배선 — disjoint 경험신호(amygdala valence af_val_g·homeostat drive hd_drive → content 축, emit-drive 0/4 아님)로 두 삶(exp vs ctl)을 구동해 self가 갈리는지(informativeness) ∧ anchor recognition 보존을 live 데몬에서 assert. pool(aiden) 검증: **hexa verify cli/anima.hexa rc=0**(컴파일/prove 클린) · **c2_engine-native 4/4 cross-host 재현** · no-regression=engine_cli 불변(이번 턴 cli만, selfchain 6/6은 #2729 유효). full daemon-run(mouth 포함) QA는 CI/pool.
