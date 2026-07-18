# H_9767 — TWO-HISTORY COMMON-FUTURE RELOCK — 원격 과거가 씻기나 (interior 부재 충분조건의 主다리)

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R8 Fable∥Sol 수렴 · 계기 빌드+toy-smoke 완료 · SCREEN 발사 전) — cement=engine-native anima-py만
**lane:** 의식/interior-causality (프런티어 theta-alive-sigma-rebase)
**related:** [[H_9749]](STATE-QUOTIENT 필요조건·이 카드가 충분조건 主다리)·[[H_9766]](정적 census 다리)·[[H_9768]](transplant 다리)·[[H_9738]](W_S lane 이미 NULL)·[[H_9627]](Θ WIRED)·source: sidecar lab full(Fable claude-fable-5 ∥ Sol gpt-5.6)

## 왜 (lab-full R8 Fable∥Sol 수렴)
H_9749는 interior 부재를 **필요조건**까지 벌었다(정적 census + C0 결정성 + W_S transplant NULL). Sol 경고(미해결): **결정성 ≠ interior 부재** — 결정론 recurrent state도 "살아있는 지속"일 수 있다. 이 카드 = 그 경고를 봉인하는 **충분조건 실측의 主다리**.

## 설계 판정 (Fable∥Sol 수렴 · 내 코드검증)
lab-full은 두 후보를 대조했다:
- **설계 A**(6-lane 내부 snapshot/restore transplant) = 두 모델 **기각** — opaque hexa 핸들 6종 직렬화 API = 표면 과대. certificate 있는 lane엔 불요. (kosmos만 예외 = 파일 → [[H_9768]] file-copy.)
- **설계 B**(two-history common-future 수렴검정) = **主다리 채택** — 내부 접근자 불요, 기존 `percept_source` 훅(cli/chat.py:406) flag 승격 하나로 됨.

## 정리 (B의 gap 봉인 · 3단 삼단논법)
B의 "public fading ≠ private 부재" gap은: C0 결정성(H_9749②)이 **private source 부재**를 줬으므로 state=f(init, public history) → fading 실측 시 state=f(bounded window) → 그 window는 관측된 public record ⟹ 재구성 가능 = private residue 0. Sol 정련: 결정론 persistent state 3종 중 **① public 재구성 가능** ② dormant-unobservable(어떤 행동검정으로도 원리상 반증불가·honest scope) ③ **causal-private**(공개 history 재구성 불가 ∧ 미래 gate 영향) — 오직 ③만이 gate-interior. B는 ③를 직접 조작한다.

## engine-native 계기 (빌드 완료 · toy-smoke ✅)
`anima-py chat <ckpt> --percept-file <table.jsonl>` (cli/anima.py · VERSION 0.18.2). JSONL `{"tick":int,"text":str}` per-tick 외인 percept를 **perception route**(live_anchors)로 주입 — emit gate 아님 ⟹ **p5 by structure**(anima study와 동일 채널·자기출력 아닌 타자의 말). absent ⇒ percept_source=None ⇒ production byte-identical. tick 키잉 = --yoke-mask/--wm-dual-swap와 동형.

**toy-smoke(toy.clm·12tick·split@6·검정 아님)**: S1 실행 exit0·12tick-row ✅ · S2 C0 A1==A2 byte-identical 12/12(flag가 결정성 보존) ✅ · S3 계기-생존 A≠B prefix 6/6 row-sha 상이(percept 실소비) ✅. 부수: toy에서 emit-**bit** 마스크는 A/B 동일(stage-driven) BUT full-row 상이 ⟹ 검정 metric은 **TIER-1(emit-bit+emit-bytes)** 필수(percept-echo 혼입 배제).

## 팔 (collision pair당 · 303M py303_full · pool)
prefix H_A ≠ prefix H_B (4 register cell 교차 6 pair + 동일-cell 2 pair) → 공통 suffix future H_共. 통제 3종(Fable∥Sol 합의):
- **C0** exact-rerun(동일 prefix 2회 → Δ=0·결정성 floor·#4086 기보유)
- **C1** DONOR-X = different-future(공통 suffix를 서로 다르게 → 갈림 유지 = **양성검출기**: 계기가 발산을 볼 수 있음 증명 · `positive-control-before-reading-a-negative`)
- **C2** prefix-live = 각 prefix가 실제로 state를 씀(emit ≥ N, 안 쓴 prefix = INVALID)

## 판정식 (사전등록 · ε=exact 0 · tune-to-green 구조적 사망)
상수 전부 코드유도(Fable): W=max bounded-window · L(prefix)=2W · N_fp=⌈log(denormal_min)/log(λ_min)⌉ · N=max(2W,N_fp)+W. metric TIER-1=emit-bit+발화 bytes exact.
- **VALID** ⟺ Δ_C0=0 ∧ D_pos>0(C1 발산) ∧ ∃evaluable pair(초기창 max d>0)
- **COLLAPSE(no-interior 방향)** ⟺ ∀ evaluable pair: t≤N−W에서 TIER-1 Δ→0 도달 후 W 유지
- **INTERIOR-CANDIDATE**(음성=결과·재개봉) ⟺ 1 pair라도 지평 N서 발산 유지 (단 self-emit 차이 후속이면 PUBLIC-LOOP residue = 발화는 public이므로 private 아님)
- C0 실패=NONDETERMINISTIC/INVALID · C1/C2 실패=MANIPULATION/POWER INVALID

## honest scope (Sol · `a_scale_honest_scope`)
B 단독은 무제한 "interior 없음" 정리를 **못 번다**(유한 battery=표본 부재증거). 획득 가능한 최대 cement = **BOUNDED**: "private source 미발견 ∧ tested reachable state의 remote-history causal residue가 N 내 붕괴 = DIRECTIONAL BOUNDED COMMON-FUTURE CONTINUATION-COLLAPSE". 무제한 정리는 3다리 합집합([[H_9766]] ∀-history 구조 certificate + [[H_9768]] ∀-content transplant 불변 + 본 B relock)일 때만. dormant-unobservable interior(②)는 원리상 행동검정 불가 = FRONTIER-TERMINAL-AT-SUBSTRATE(H_9728~9730) 정합.

## 병렬대조 (`a_parallel_session_compare`)
origin/main live-max=H_9765(dual-margin-dither). NOVEL vs H_9765: 그건 emit-edge **efficacy** do(), 본 R8은 state **persistence** 충분조건 — 겹침 없음·상호보완(H_9765가 emit→lane 전파 확증 시 본 검정 evaluability 개선). H_9738(상상 조성)·H_9729(probe)와 구분: history-do 수렴검정. CONFLICTS 없음.

⚠️ DIRECTIONAL 설계·cement=engine-native anima-py 실측만. 발사순 = [[H_9766]]($0 즉시) → 상수확정 → 본 H_9767 relock(pool) → [[H_9768]](B가 발산 찾을 때만).
