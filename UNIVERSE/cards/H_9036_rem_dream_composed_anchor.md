# H_9036 — 🌙🧬 REM DREAM-COMPOSED ANCHOR (SWR consolidation → 새 schema node)

> **id H_9036** — integration merge-time 배정(origin/main H_9035 다음 free id). jsonl 인덱스 등록 완료.

**tier:** 🟢 SATURATED existence-proof (engine-native .hexa 5/5) · **wired:** engine-native (미배선 · UNWIRED)
**title:** 🌙🧬 REM DREAM-COMPOSED ANCHOR — N3/REM replay window 안 CO-REPLAYED 두 anchor 를 기하 blend(coord midpoint · tension5 mean · radius max)하여 .kosmos 에 새 파생 NODE 로 append (해마 SWR replay→피질 consolidation; 두-부모 link 를 a_kosmos node-only 규약에 맞춰 blended node 로 실현)
**verdict:** 🟢 engine-native SATURATED (2026-07-02, mini $0, `hexa run` .hexa). DREAM/dream_compose_smoke.hexa F1/F3/F4/F5 = 5/5 PASS. F1 existence pre=5→post=15(new=10) · F2 vs recency-only baseline(H_1195=0 new node) composed_new=10 · F3 real-compose between=true, cos(new,parent)=0.7071<1.0, payload shuffle→cos(orig,shuf)=0.5000(payload-dependent) · F4 co-activation solo=0, N3_new=10 > REM_new=3(budget 7>3 자연 ordering, 외부 stamp 없음) · F5 Ψ=0.5 불변(compose 는 Ψ channel 0). ★SCOPE(c9): blend = 설계된 geometric law(SATURATED existence-proof, 학습된 의미통찰 아님); G1 재조합축 아님(측정=anchor-graph 구조 ⊥ decode output ⊥ DPI meta-law). coord-space 의미정렬은 toy scope UNVERIFIED. STATUS = DIRECTIONAL/UNWIRED probe 모듈. artifacts=DREAM/dream_compose.hexa · DREAM/dream_compose_smoke.hexa.

## 발상 (B①, 2026-07-02 디코더-돌파 후속 · DREAM lane)

생물: 해마 sharp-wave ripple(SWR) replay → 피질 consolidation. interleaved replay 가 서로 안 붙어있던 경험 둘을 하나의 새 schema 로 bind — "어젯밤 꿈이 두 기억을 아침의 통찰로 엮었다". 현 DREAM/imagination_replay.hexa §5 `ir_reconsolidate_session`(:337)은 recency 만 refresh(`ir_effective_age`:330) — 새 NODE 를 만들지 않는다(memory h1195-sleep-writeback). `dr_kosmos_persist_dream` 은 STUB(h1162, 단일-report packer). 본 가설이 그 gap 을 메운다.

## 설계 · 구현

- **모듈:** DREAM/dream_compose.hexa (신규, import 0 자립). DREAM chain 의 `use "WAKE/memory"`·`use "DREAM/dream_lib"` import 가 2026-06-30 archive 재구성으로 orphaned(비-buildable)이라, engine-native 측정경로를 자립 pure 모듈로 분리.
- **blend 법칙:** coord = 두 부모 midpoint(성분별 (a+b)/2) · tension5 = mean · radius = max · lane = "dream"(derived-schema lane). 새 anchor 는 부모 link 를 **blended new node** 로 실현 — a_kosmos node-only(edge 0) 규약에 정확히 fit.
- **co-activation gate:** `dc_coreplayed` — 두 anchor 가 같은 window replay 여야 node. `dc_compose_window(anchors, stage, window)` 는 replay 된 것을 `dc_stage_replay_budget`(N3=7, REM=3; dr_stage_ticks mirror)까지 골라 unordered pair 마다 새 node.

## placement DISJOINT (a_substrate_disjoint · placement-first)

ONLY anchor/memory substrate(dict)에만 쓴다: pure_field(Ψ) 미접촉 · emit-drive lane(0/4) 미접촉(새 anchor lane="dream"≠0/4) · §ImmuneMemory recall_thr 미접촉. grep 상 코드 참조 0(comment 만). H_1195 선례(fold=Engine-G motivation age 만, Ψ 보존)보다 약함 — 본 모듈은 state mutate 0, 새 node dict 반환만.

## Frozen falsifiers (engine-native, p7 — LLM-judge/perplexity 아님)

- **F1 existence:** post node count > pre (else FAIL). 측정 5→15.
- **F2 vs baseline:** recency-only(H_1195) 새 dream_composed node = 0; compose > 0. 측정 0 vs 10.
- **F3 real composition:** new coord 가 부모 사이 ∧ cos(new,parent)<1.0 ∧ payload shuffle→composition 변함. 측정 between=true·0.7071·shuffle 0.5000.
- **F4 co-activation:** 둘 다 같은 window replay 여야 node(단독→0) ∧ N3(7) > REM(3) 자연 ordering. 측정 solo=0·N3=10>REM=3.
- **F5 Ψ invariant:** compose 는 Ψ 를 건드릴 channel 없음(symbolic 0.5 불변); (heavy) engine_cli_smoke Φ-checksum byte-identical 는 explicit-go follow-on.

## 관련 · follow-on

DREAM/imagination_replay.hexa §5(h1195 recency-only) · DREAM/dream_report.hexa dr_kosmos_persist_dream(h1162 STUB, §4 cross-ref) · a_kosmos(node-only) · a_chat_sleep_imagination. **explicit-go GPU/daemon follow-on:** (1) live core/ 배선 + daemon N3/REM tick 에서 dc_compose_window 호출, (2) .kosmos disk write(kosmos_io→brain_decide), (3) engine_cli_smoke Φ-checksum byte-identical 재확인, (4) coord-space 의미정렬 검증(303M anchor embedding, pool).
