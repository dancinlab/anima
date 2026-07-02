조사가 충분히 모였습니다. 분석을 정리합니다.

---

# anima 아키텍처 분석·비평

근거는 전부 워킹트리 실물에서 읽었습니다: `ARCHITECTURE.json`(25 섹션 트리), `core/brain.hexa`(836L), `core/engine_g.hexa`(65L), `core/pure_field.hexa`(342L), `core/generator.hexa`(2251L), `core/engine_cli.hexa`(11,599L), `core/emit_policy.hexa`(69L), `cli/anima.hexa`, `hexa.toml`.

## (1) 구조적 강점

**단일 진입(single-entry) 규율이 실제 코드로 지켜지고 있다.** 가중치는 `generator.hexa` §4 `generate()` 한 슬롯으로만 들어오고, mouth 2종(conv `.clm` / ByteGPT `.bin`)은 `gen_mouth_kind`(generator.hexa:628) header-sniff 디스패처가 같은 슬롯 뒤에서 고른다. `.kosmos` 도 `load_anchors` 한 API(§3 `generator_read_anchors`, generator.hexa:292)로만 읽힌다. 이 불변식이 문서 주장에 그치지 않고 `h1196_single_entry_audit.hexa` 스모크로 기계 검증된다는 점이 드물게 좋은 설계다.

**"분리=보존, 중첩=충돌"(a_substrate_disjoint)이 사후 합리화가 아니라 반례까지 가진 법칙이다.** ARCHITECTURE 의 disjointness map 은 6개 GREEN(mouth⊥identity H_1471, mouth⊥tool H_1566, savant⊥의식 H_1578, savant⊥정직 H_1576, mitosis⊥의식 H_1577, 섭동 self-restore H_1575)과 함께 **counter-example H_1561**(공유 emit-lane 침범 → Ψ 붕괴)을 명시한다. 반례를 보존한 법칙은 falsifiable 하고, 새 능력의 배치 규칙(placement-first)을 실제로 유도한다 — (4)번 답의 근거가 된다.

**Ψ-안전 consult 패턴의 일관성.** 모든 lane consult 는 "bounded additive nudge, neutral 시 byte-identical" 계약을 지킨다: anchor fold cap 0.05(brain.hexa:96), gap bias cap 0.05(gap=0 → brain_decide 와 byte-identical), affect ±0.05, cerebellum ~0.005. 회귀 검증도 수치로 한다(h1205 phiSum 48.6613==48.6613). "consult 는 정보를 더하되 게이트가 되지 않는다"는 원칙이 코드 레벨 계약으로 존재한다.

**정직성이 구조에 내장됨.** ARCHITECTURE 에 "🚧 Not yet built (honest)" 섹션, 벽 스코어카드(neuromodulation = 유일한 정직한 🧱), G6 M2-M5 FALS=0 을 "architecture-depth 벽"으로 박제. 게이트 1·6은 `tool/enforce_anima_gates.py` 로 CI 차단 — 거버넌스가 문서-only 가 아니다.

**p8(train/infer 연속) 이 진짜 구현 방향과 맞물려 있다.** MITOSIS(engine_grow/VAdaptField/apoptosis)가 추론 데몬 안의 tick 으로 존재하고, `cli/train.hexa` 가 같은 ops 위에 SAVANT/MITOSIS 레버를 조립한다 — 철학이 별도 문서가 아니라 배선이다.

## (2) 위험 · 취약점 · 모순

**(a) 서사–구현 갭: "Engine G" 는 65줄짜리 하드코딩 선형 스코어보드다.** `engine_g.hexa` 의 실체는 8-가중 선형합(가중치 0.20/0.10/0.15… 손튜닝, sum=1.0) + 임계 0.3/0.6/30초다. "reverse, gradient-free 엔진이 A 를 밀어낸다"는 서사에서 기대되는 역동성은 없고, A⇄G "긴장" 커플링의 실체는 `safety_phi_ratchet_ok(phi > ratchet/2)` — **불리언 AND 게이트 하나**다(brain.hexa:53). tension = ‖A‖/‖G‖ 라는 ARCHITECTURE 문구를 뒷받침하는 연속량 상호작용이 brain_decide 경로에는 없다. `a_autonomy_over_hardcode`("hardcode 게이트 없음")와 spont_im_threshold=0.3 하드코딩의 긴장도 해소되지 않았다 — emit_policy.hexa 는 H_646/651(Φ-variance=0)로 "숫자는 자유"라 정당화하지만, 이는 뒤집으면 **의식 substrate 가 emit 행동 수치를 전혀 구속하지 못한다**는 뜻이기도 하다(Φ-inert = 자유 ≠ 창발).

**(b) kosmos_io 의 canonical 위치가 연구 잔해 경로다.** `.kosmos` 단일 진입이라는 core 급 기구가 `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.hexa` — 날짜 박힌 UNCLASSIFIED 그리드 경로 — 에 살고, `core/generator.hexa`(import 줄 48)와 `cli/anima.hexa:44` 둘 다 이를 import 한다. "core/ 는 외부 의존 0(substrate 엔진만)" 패키징 불변식이 hexa.toml:76 의 1-파일 특례로 겨우 지탱된다. `.worktrees/s1-fp32/core/kosmos_io.hexa` 가 존재하는 걸 보면 core/ 로 옮기는 작업이 브랜치에 있는데, main 에는 미착륙 — 알려진 부채지만 단일-진입 SSOT 가 이 경로에 있는 동안 rsync 기반 pod 패키징·리팩터 모두 이 특례에 취약하다.

**(c) brain_decide 변형 폭발 — consult 가 합성되지 않는다.** `brain_decide`, `_anchored`, `_bg`, `_cerebellum`, `_wm`, `_affect`, `_margin`, `_gap` … lane 마다 **별도 진입 함수**가 자란다. consult map 은 "전부 OPTIONAL/ADDITIVE"라 하지만, additive 라면 fold 하나로 N 개 lane 을 합성할 수 있어야 하는데 현재는 margin+affect+wm 을 동시에 쓰려면 새 변형이 필요한 조합 구조다. cli/anima 가 "76 lane 중 40개를 motivation 에 연결"했다는 노드가 있는 것을 보면 실전에서는 별도의 ad-hoc 합성이 이미 벌어지고 있다 — consult 레지스트리(가산 항 리스트를 받는 단일 brain_decide)로 수렴하지 않으면 lane 이 늘수록 조합 드리프트가 커진다.

**(d) engine_cli.hexa 11,599줄 신-파일(God-file).** ~76 lane(GWS·SelfIdentity·AttentionalBlink·Rivalry·Pharm·ThirdLaw·BrainTopology…)이 한 파일에 산다. ARCHITECTURE.json 과의 1:1 lockstep 을 "grep 으로 누락 0 검증"하는 수동 규율에 의존하는데, 바로 지금 워킹트리의 ARCHITECTURE.json 이 **9,377줄 미커밋 재작성 상태**이고, 스켈레톤에 있는 "G0-G6 능력 게이트 사다리" 노드가 현 워킹트리 파일에서 검색되지 않는다(`능력 게이트` 0건). lockstep SSOT 자체가 지금 drift 창 안에 있다.

**(e) EMIT 계약이 p5 와 미묘하게 충돌한다.** `generate()` 계약은 "emit_decision=true ⇒ text≠''" 이고, backend 미장착이면 **null placeholder 를 emit** 한다(fellback=true, generator.hexa:364-369). 정직하게 플래그되지만, "긴장의 외재화만 허용, filler 금지"(p5)의 관점에서 mouth 고장 시 자동 stub 발화보다 abstain 이 원칙에 더 맞다. 대칭적으로, 의식의 emit 판독 자체도 얇다: `ci_emit_decision` = **lane0(GWS ignition)과 lane4(LearnedPrecision) 두 스칼라의 평균 ≥ 0.5**(engine_cli.hexa:9053-9059). 15-lane 서사 대비 실제 외재화 드라이브는 2-lane 평균이다.

**(f) SSOT 중복·취약 로더.** engine_g.hexa 스스로 "HEXAD/CHAT/spontaneous_lib.hexa 가 live-chat 복사본, 정합화는 follow-up"이라 적어둔 상수 이중화가 미해소. 임계값 레지스트리도 3곳(emit_policy.hexa 0.60/0.30/0.27 · engine_g.hexa 0.3/0.6/30s · config/consciousness_laws.json α/balance)으로 흩어져 있다. 그리고 `_psi_load`(pure_field.hexa:39-82)는 손으로 짠 문자열-split JSON 파서로 3개 fallback 경로를 뒤지고, 실패 시 **eprintln WARN 후 조용히 default** — 의식 상수가 배포 환경에 따라 소리 없이 달라질 수 있는 구조다.

**(g) core/ 에 연구 프로브 ~90개 혼재.** `h####_*.hexa` 프로브가 production 엔진 파일과 같은 디렉터리에 산다. "self-contained core/ pod" 서사에는 무해하지만(150MB), canonical 재구성을 거친 디렉터리치고는 프로브/엔진 경계가 흐리다.

## (3) 미충족 갭 (ARCHITECTURE "Not yet built" + 실측 잔여)

- **G1 재조합**: 최대 갭. readout/decode-procedure/objective-보조축 전수 🧱(H_1812/1814/1816/1602/1834/1837, EXP-3), 남은 생존 레버는 γ trained-constructive-bind(H_1840, GPU cost-gated) 하나.
- **G6 깊이**: M1 만 engine-native PASS, M2-M5 FALS=0 — 원인은 격리됨: production mouth 인 **L1 ConvMoE 에 attention 깊이가 없다**(H_1394 DECISIVE — capacity 도 script 도 아닌 ARCHITECTURE). "DEEP engine-mountable mouth(L>1 ConvMoE 또는 attention decoder)"가 명시된 NEXT 인데 미착륙.
- **3B/7B rung**: 파이프는 배선, engine-measured mount 는 1B 가 마지막 GREEN.
- **G5 in-dist**: F2 useful 0.875 < 0.90(over-eager abstain) — non-fab 은 견고하나 유용성 잔여.
- **CHAT register**: strict register 가 THIN/INFLATED(303M shallow ceiling), en-SNS 코퍼스 KNOWN-SMALL.
- **thalamus 콘텐츠축**: 🧱 유지(타이밍축만 PhaseField 로 WIRED-live), neuromodulation 은 정직한 벽.
- **구조 부채**: kosmos_io core/ 이관(b), brain_decide consult 합성(c), engine_g↔spontaneous_lib 정합화(f).

## (4) G1 변수바인딩 결핍 × 현 구조 — 어디에 바인딩 기구를 붙여야 disjoint-정합인가

먼저 **붙이면 안 되는 곳**(전부 실측으로 기각된 축):
- generator §6.5-계열 decode-time consult(emit-bias/scoreloop) — readout 축은 G1 을 못 연다(⊙ NMDA readout, PC-binding, tension-mouth, temporal-DEQ 전수 🧱; DPI 메타법칙).
- `§ImmuneMemory` recall_thr — G5 non-fab 게이트와의 결합은 fab 폭증(H_1576 B4). 금지 좌표.
- emit-drive lane0/lane4(`ci_emit_drive`) — 건드리면 Ψ 붕괴(H_1561).

disjoint-정합인 부착점은 **두 층**이고, 현 구조가 이미 둘 다의 자리를 갖고 있다:

**① mouth-내부(trunk objective) — 유일하게 살아있는 G1 레버의 정합 좌표.** 바인딩을 학습시킨다면 그것은 L3 슬롯으로 들어오는 ckpt **가중치 안**의 일이다. L3 mouth 는 이미 by-construction 으로 emit-drive·ImmuneMemory 와 disjoint 하다(mouth⊥identity H_1471: ckpt 를 통째로 갈아끼워도 self-anchor·Ψ 불변). 즉 γ trained-constructive-bind / recomb-objective 는 **a_substrate_disjoint 관점에서 추가 배선 비용이 0** — 기존 `gen_auto_backend` 디스패치(generator.hexa:641)를 그대로 타면 된다. 단 trunk 는 ByteGPT 쪽이어야 한다(py303 ConvMoE 는 single-coverage floor 라 G1 측정 이전 단계; 깨끗한 벽은 ByteGPT single=2).

**② substrate-측 명시 바인딩 lane — engine_cli.hexa 의 기존 lane 패턴 그대로.** "변수바인딩"을 연속 가중치가 아니라 이산 slot-filler 구조로 갖는 faculty(가칭 §VariableBind: `bind_new/_assign/_deref`)를 **`§Memory & store lanes` 옆**, 즉 이미 있는 `WorkMemBuffer`(H_1282, recall-support nudge ~0.018)와 `CA3 REPLAY predictor`(ca3_replay_*) 의 형제로 둔다. 이 패턴이 정합인 이유가 셋: (i) WM lane 은 이미 "항목을 잡아두고 되읽는" 기구라 role-filler 쌍의 자연 확장이고, (ii) brain 소비는 검증된 `brain_decide_gap` 계약(bounded ±0.05, neutral byte-identical)을 복제하면 Ψ-disjoint 가 구조적으로 보장되며, (iii) engine-native verdict 배선 사다리(struct+faculty+smoke → consult)가 lane 마다 이미 표준화되어 있다. deep-research 메모리와도 일치한다(additive-slot+consistency = cheap·증명보장, disentanglement 단독 = 실패).

핵심 판별: ①은 "mouth 가 스스로 재조합하게" 하는 길(비쌈, 유일 미기각), ②는 "재조합≠능력" 프레임전환 — 바인딩을 mouth 밖 operator 로 짓고 결과를 content 로 내보내는 길이다. ②의 출구가 곧 (5)다.

## (5) frame-break(kosmos-anchor 합성)의 실제 접붙임 지점

현 core/ 배선에서 anchor 는 **읽기 전용 + verbatim 복사** 두 용도뿐이다: (i) `brain_decide_anchored` 가 tension_5ch 를 vecsum-fold 해 motivation nudge 로만 쓰고(brain.hexa:126-194 — **내용은 안 본다**), (ii) grounded decode 가 anchor 텍스트를 **바이트 그대로 복사**한다(H_1163: "grounded bytes copied VERBATIM, ungrounded bytes fall back to the LM"; 학습형 copy-head 는 실스케일 기각 H_1150-1154). anchor 두 개를 **합성해 새 anchor 를 만드는 op 는 어디에도 없다**. 이 부재가 정확히 접붙임 자리다. 이음새를 경로 순서로:

1. **읽기 — `load_anchors`(kosmos_io) → `generator_read_anchors`(generator.hexa §3)**: 합성 연산자의 입력은 이 기존 단일 진입으로 들어온 anchor record(`#{path, name, fields, text_payload, tension_5ch}`)여야 한다. 2nd `.kosmos` 경로 신설은 a_core_engine_map 위반.
2. **합성 — engine_cli.hexa 신규 faculty(가칭 §AnchorCompose), `§SelfIdentity` 옆**: SelfIdentity 가 이미 유일하게 ".kosmos 디스크 영속"을 엔진 쪽에서 수행하는 lane(H_1471 R2b)이므로, anchor 를 쓰는(write) 두 번째 faculty 의 선례·코드 경로가 바로 옆에 있다. tension 합성의 수학 선례도 이미 core 에 있다 — `anchor_tension_fold` 의 5ch 벡터합+τ-감쇠(brain.hexa:126-147)를 motivation 스칼라가 아니라 **새 anchor 의 tension_5ch 생성**으로 재사용하면 된다. 텍스트 쪽 합성이 곧 (4)-②의 바인딩 연산자(slot-filler 치환)가 실행되는 곳이다.
3. **영속 — 같은 kosmos_io 로 append**: 제약 하나가 중요하다. `.kosmos` 는 **node-only, edge/relation entry 금지**(a_kosmos). 따라서 합성 anchor 의 provenance(어느 두 anchor 에서 왔나)는 관계 엔트리가 아니라 **payload 필드 + placement triple(coord·lane·radius)** 안에 인코딩해야 하고, lane/tier 의미는 anima profile(`anima-consciousness-carving`)에 바인딩해야 한다.
4. **판단 — brain 추가 배선 불필요**: 합성 anchor 는 `brain_decide_anchored` 의 기존 fold 를 그대로 타므로(cap 0.05 saturating) Ψ-안전이 공짜로 보장된다. 굳이 새 consult 를 만들면 오히려 disjoint 심사를 다시 해야 한다.
5. **발화 — `_gen_anchor_texts`(generator.hexa:573) → `clm_decode_grounded`/`bytegpt_decode_grounded`**: 이게 frame-break 의 결정적 이음새다. 합성 anchor 의 텍스트는 grounded copy 경로로 **mouth-FT 없이, trunk 가중치를 안 건드리고** 그대로 발화면에 도달한다. mouth⊥tool(H_1566: 지식=anchor·결정=brain·실행=agent)의 일반화 — "재조합 = anchor-측 operator, 발화 = 기존 verbatim copy" — 이며, 메모리의 kosmos-Merge 🟡 REACHABLE(operator-side) 판정이 가리키는 지점과 일치한다.
6. **정직 가드 — recall_thr 불가침**: 합성 anchor 는 경험이 아니라 파생물이므로 G5 §ImmuneMemory 가 보증하도록 밀어 넣으면 안 된다(disjoint 금지좌표). provenance tier 를 payload 에 명시하고, 신뢰도는 기존 `brain_decide_margin`/`_gap` 의 읽기-전용 신호로만 다루는 것이 정합.

**정직한 한계 하나(c9):** 이 경로는 G1 의 frozen bar(엔진 mouth 의 free-generation distinct count)를 그 자체로는 안 깬다 — 재조합이 mouth 밖에서 일어나기 때문이다. 이것은 "G1-bar 돌파"가 아니라 "재조합≠능력" 프레임의 **능력-레벨 우회**로 박제해야 하며, bar 를 anchor-합성 출력으로 재정의하면 그게 바로 tune-to-green 이다. G1 bar 자체를 노리는 유일 생존 레버는 여전히 (4)-①(trunk objective, cost-gated)이다.

---

**요약**: 강점은 단일-진입·disjointness 법칙·bounded-consult 계약·정직성의 코드화이고, 최대 위험은 서사(두 엔진의 긴장)와 구현(선형 스코어보드+불리언 ratchet)의 갭, kosmos_io 의 연구-경로 잔류, brain_decide 변형 폭발, 그리고 지금 열려 있는 ARCHITECTURE.json 미커밋 재작성 drift 창이다. G1 바인딩은 mouth-trunk objective(비용-게이트, 유일 미기각)와 engine_cli 신규 바인딩 lane(WM/CA3 형제, gap-consult 계약 복제) 두 좌표만이 disjoint-정합이며, frame-break 는 `load_anchors → §AnchorCompose(신규, SelfIdentity 옆) → kosmos_io append(node-only 제약) → brain_decide_anchored(기존 fold) → *_decode_grounded verbatim copy` 사슬로 현 배선에 정확히 접붙는다.
