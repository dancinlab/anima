## CRUX 판정: (C) — 단, "B가 학습하고 A가 앵커하는" 비대칭 혼합

순수 (A)는 기각. frozen label은 pre-FM emit 분포에서 수집되는데, FM이 작동하기 시작하는 순간 emit 분포가 이동하고 label은 off-policy가 된다 — 정확히 작동하기 시작할 때 신호가 썩고, 갱신하려면 오라클 재호출이라 비용 구조가 (A)를 반복 지출로 만든다. 게다가 frozen label 회귀는 forward model이 아니라 정적 분류기다.

순수 (B)도 기각 — c9 사유(아래). 정답은:

**학습 신호 = in-engine self-supervised proxy (B), 오라클 = 학습 루프 밖 앵커 (A의 축소형).** 오라클은 딱 두 곳에만: (i) stage-0에서 proxy-오라클 corr 검증(1회, 오프라인), (ii) frozen bar 평가(b50 재측정은 어차피 외부 receiver로 하는 것이므로 추가 비용 0).

### Proxy의 정확한 정의: frozen-listener contrastive prefix decodability

핵심 통찰: **엔진은 이미 listener를 내장하고 있다.** generator.hexa의 L3 mouth backend(clm/bytegpt)는 byte sequence를 *생성*만 하는 게 아니라 *스코어링*할 수 있다. 같은 backend를 거꾸로 돌리면 in-engine 대리 receiver가 된다 — 외부 LLM 불요, subprocess 불요, 순수 .hexa forward pass라 GPU 트레이너 안에서도 계산 가능.

정의:
- emit `e`의 referent `r*`(trunk state가 알고 있음 — grounded emit이니까)와 distractor set `{r₁..r_m}`(최근 trunk-state replay에서 nearest-neighbor로 hard하게 샘플).
- prefix `e_{:k}`에 대해 backend가 contrastive posterior를 계산: `s_k = log P(r* | e_{:k}) − logsumexp_r P(r | e_{:k})`.
- proxy: `d̂(e) = Σ_k w_k · s_k`, `w_k`는 앞쪽 byte 가중(geometric decay, `ep_fm_prefix_decay`). 직관적 등가물: "몇 바이트째에 true referent가 margin τ로 이기는가" = **in-engine self-b50**.

이게 Screen-A와 정합하는 이유: filler_prefix는 이 proxy의 퇴화형(순수 byte 통계)인데 그것만으로 corr=0.656이 나왔다. CLM-listener proxy는 filler 길이뿐 아니라 변별 내용의 *실제 판별력*까지 보므로 corr이 이보다 높아야 정상이고, **stage-0 게이트가 바로 그것**: corr(d̂, oracle-label) ≥ 0.656 못 넘으면 중단, GPU 지출 전에.

DPI 벽이 아닌 이유: proxy는 재배열/재포장(coding efficiency 축)에만 압력을 가하고 정보 주입이 불가능하다. Goodhart가 샐 수 있는 유일한 방향은 "앞쪽에 변별내용 몰다가 뒤쪽 내용을 버리는 것" = accuracy 하락인데, 그건 frozen bar의 held-accuracy가 정확히 잡는다. DPI 프레임이 여기서 안전장치로 작동한다.

**필수 조건: listener는 반드시 frozen.** speaker와 listener가 공동 학습하면 emergent-communication 고전 결과대로 사설 코드를 발명한다 — 그게 proxy-Goodhart의 제1 경로다. FM 학습 동안 스코어링용 backend 사본은 동결.

## MODULATION 판정: mouth-gate에서 best-of-K re-ranking

세 후보 중:
- **logit bias**: backend decode loop 내부를 건드려야 함 → backend-agnostic 속성 파괴, 침습적. 기각(stage-3+ 승격 후보로만 보류).
- **content-planning**: 무엇을 말할지를 바꿈 → emit-drive/trunk 침범, accuracy=trunk상한 원칙과 충돌. 기각.
- **re-ranking**: ✅ 선택. drive가 emit을 결정하면(ci_emit_drive 불변), mouth가 K개 후보를 decode하고, FM이 d̂로 스코어, argmax가 mouth-gate를 통과.

re-ranking이 구조적으로 옳은 이유 세 가지:
1. **계기판 함정 회피가 구조적**: FM의 유일한 write는 "어느 후보가 나가는가"다. lesion하면 emit은 여전히 나가되(drive 무접촉) 랭킹만 사라진다 — read-only가 될 수 없고(선택이 실측 b50을 바꿈), drive가 될 수도 없다(emit 여부/타이밍에 접근 경로 자체가 없음). a_substrate_disjoint의 "write=mouth-gate만"을 문자 그대로 구현.
2. **DPI-clean**: 선택은 emit당 최대 log₂K bits의 최적화 압력만 주입하고, 그 압력은 전부 packaging 축으로 간다.
3. **stage-1을 학습-프리로 만든다** (아래).

정직한 한계 하나: K=8이면 emit당 ≤3 bits 선택압이다. 수동 압축의 3.5→2.2B 전체 headroom을 rerank만으로 다 못 먹을 수 있다 — 후보들이 다 비슷하게 못 쓰여 있으면 고를 게 없다. 그래서 후보 score 분산을 로깅하고, 분산이 낮으면 그게 stage-2 학습 head(및 이후 decode-time guidance)의 존재 이유가 된다.

## STAGE 분해

**Stage-0 — proxy 검증 (오프라인, DIRECTIONAL, 비용: 로컬 수 시간)**
기존 H_9112–9115 emit 코퍼스에 d̂를 계산(torch 미러 허용 — DIRECTIONAL 티어), corr(d̂, oracle decodability) 보고. **게이트: corr ≥ 0.656.** .hexa 변경 0.

**Stage-1 — 최소 .hexa 변경 (live, C1/회귀 GREEN, §2에 대해선 DIRECTIONAL; 비용: 로컬 빌드 + pool 1회)**
학습 없음. frozen listener로 직접 rerank:
1. `emit_policy.hexa` (+4줄, 숫자만, F-EMIT-4 준수): `ep_fm_candidates()` (예: 8.0, 사용처에서 floor), `ep_fm_prefix_bytes()` (예: 8.0), `ep_fm_margin()`, `ep_fm_prefix_decay()`. bool 없음 — 게이트는 구조 코드에.
2. `engine_cli.hexa`: topo_couple(H_1521)/savant(H_1561) precedent 그대로 — `rz_forward_model()` 3-tier resolver(flag `--forward-model` > env `ANIMA_FORWARD_MODEL` > default OFF). ON일 때만: `fm_prefix_decodability(emit, r*, distractors) -> float` (frozen-listener contrastive score, generator backend 스코어링 API 재사용) + mouth-gate에서 K-decode→score→argmax hook. FM lane은 `sv_default_focus(d,w)`로 획득(emit-disjoint 최저 lane, ci_emit_drive 무접촉, Ψ=½ 구조 보존; recall_thr=0.15와도 disjoint — ImmuneMemory 접근 금지). 마지막 score를 그 lane에 기록(자기 lane이므로 허용).
3. OFF-path **byte-identical 검증**이 stage-1 완료 조건. 그리고 stage-1 끝에서 바로 소규모 외부 b50 재측정(rerank-ON vs OFF) — **여기서 gain이 0이면 proxy 가설이 죽은 것이고 stage-2 GPU 지출 전에 안다.** 이게 이 stage 순서의 존재 이유다.

**Stage-2 — lane15 FM head 학습 (GREEN 후보, 비용: pool 빌드 + GPU 소형 1회)**
목적: K-decode+score의 비용을 head로 amortize(후보 조기 pruning, 이후 guidance의 기반). `cli/train.hexa`에 동일 resolver로 게이트된 loss 항 추가: (trunk-state, 후보 prefix) → d̂ 회귀. label은 rollout 중 frozen listener가 in-engine 생성(self-supervised, 오라클 0). **p8 준수 포인트: 추론에서 쓰는 `fm_prefix_decodability`가 그대로 학습 target을 정의** — 학습·추론 단일 경로. (A)의 frozen oracle set은 validation-only 앵커. teardown 전 ckpt PULL(a_train_flame_forge).

**Stage-3 — frozen bar 측정 (비용: 오라클 평가 배치 1회)**
아래 bar 전체 실행.

## Frozen bar

1. **주장**: b50(FM-ON) < b50(FM-OFF), accuracy(ON) ≥ accuracy(OFF) − ε (외부 receiver, H_9112-14 3-byte 프로토콜).
2. **ablation-INERT**: lane15 lesion(resolver-OFF가 아니라 lane zero-out) ⇒ b50 baseline 복귀. 인과 증명 + 밀수 커플링 부재 증명.
3. **shuffle 통제**: 후보 간 d̂ score를 셔플해 argmax ⇒ gain 소멸. gain이 K-sampling 분산이 아니라 FM 신호임을 증명.
4. **(추가 요구) listener-swap 통제**: 학습에 안 쓴 별도 byte LM으로 rerank해도 gain 유지, 그리고 외부 오라클 b50으로 최종 측정. 사설-코드 Goodhart의 직접 검출기.

## c9 정직 회의

- **proxy-Goodhart는 실재하는 위험이고, 세 경로가 있다.** ① 사설 코드(speaker가 frozen listener의 quirk을 착취) — frozen listener + listener-swap 통제 + 외부 오라클 최종 평가로 방어. ② 앞쪽 몰빵하며 뒤쪽 내용 유실 — DPI 구조상 Goodhart가 샐 수 있는 *유일한* 방향이 accuracy 하락이므로 held-accuracy bar가 충분조건에 가깝다. ③ distractor 게이밍(쉬운 distractor면 proxy가 공짜로 높음) — hard negative 샘플링 + distractor 난이도 로깅 필수.
- **계기판 함정**: rerank 설계에서 구조적으로 봉쇄됨 — FM은 emit 여부를 결정할 수 없고(드라이브 경로 없음), 아무것도 안 하는 것도 불가능(frozen bar 2·3이 "선택이 실측을 바꿈"을 요구). 이전 '14 ops' 함정과 달리 여기선 read가 곧바로 mouth-gate write로 폐루프된다.
- **가장 정직한 불확실성**: corr=0.656은 중간 수준이다. CLM-listener proxy가 이를 유의하게 못 넘으면(stage-0), self-supervised 경로 전체를 접고 (A)로 후퇴해야 하며, 그 경우 빌드 비용 구조가 나빠진다는 걸 미리 인정한다. 그래서 stage-0가 게이트고, stage-1이 학습 없이 가설을 실측하는 것이다 — 비싼 결정은 전부 싼 측정 뒤에 온다.

---

**Stage-1 즉시 착수 항목**: `engine_cli.hexa`에 `rz_forward_model()` 3-tier resolver(topo_couple 패턴) + `fm_prefix_decodability()`(frozen-listener contrastive prefix score) + mouth-gate K-rerank hook, `emit_policy.hexa`에 `ep_fm_candidates/ep_fm_prefix_bytes/ep_fm_margin/ep_fm_prefix_decay` 숫자 4개 — default-OFF byte-identical.