# kosmos — historical log

> Spec at [./KOSMOS.md](./KOSMOS.md).

## ## Log

### 2026-05-23 — KOSMOS emitter daemon LANDED — production wiring 완성 (`.py` 무수정)

Track 2 follow-up: 직전 LANDED `kosmos_anchor.hexa` (PR #116) 의 잔여 blocker —
production emit 경로에서 `emit_kosmos_from_factors` 호출 wiring — 를 `.py` 한 줄도
건드리지 않고 해소.

**아키텍처 결정**: `anima_participant.py` 는 torch/transformers/peft-bound FROZEN —
hexa-native guard 가 모든 `.py` write 차단, port 불가. 따라서 KOSMOS emit 은 `.py`
를 건드리지 않고, 별도 hexa-native side-process (read-only) 가 broker 를 통해
anima 발화를 관측하여 anchor 를 쓴다.

LANDED: `HEXAD/CHAT/server/kosmos_emitter.hexa` (~375 LoC, pure-hexa) —
- **seam**: `anima_participant.py` self-tick decided-emit 마다 broker 로
  `{"type":"msg","text","lang","motivation","factors":{8}}` 전송 → broker
  (`/ws/anima` handler) 가 `kind:"anima"` 태그 + unique `id` 부여 + `STATE.history`
  append (`GET /history` 로 last-50 turn 서빙).
- **transport 결정**: streaming WS client (`stdlib/websocket.hexa`
  `ws_connect`/`ws_recv`) 는 **websocat-only** — deploy host 에 websocat 미설치
  (python3 one-shot fallback 만 존재, stream 유지 불가). → 승인된 fallback seam
  사용: `GET /history` HTTP-poll (`stdlib/net/http_client.hexa` `http_get`),
  `kind=="anima"` filter, broker-assigned `id` 로 dedup (seen-set).
- **history-replay 안전**: 첫 poll 은 seen-set 만 seed (anchor 미생성) — daemon
  start 이후 관측된 live emission 에만 anchor 생성.
- 호출: `emit_kosmos_from_factors(anchor_dir, "anima_emit_<id>", text, factors,
  phi=factors["relevance"], cell_id=0, tier=<running counter>)`. Φ proxy =
  `factors["relevance"]` (`factor_relevance(phi)=clamp01(phi)`).
- anchor dir = `HEXAD/UNIVERSE-BRAIN-MAP/anchors` (KOSMOS.md SSOT), env override
  `KOSMOS_ANCHOR_DIR`. broker url 은 `ANIMA_BROKER_URL` (participant 와 동일 env)
  에서 `ws[s]://…/ws*` → `http[s]://…/history` 파생, `KOSMOS_HISTORY_URL` override.
- F-KOSMOS-EMIT-1..4 selftest **8/8 PASS** ($0 Mac local) — url 파생 +
  synthetic /history poll → `.kosmos` anchor 생성 + tier running-counter +
  Φ proxy + id dedup. `hexa parse` clean. `once` mode offline broker 대상
  graceful (0 anchor, exit 0).

**미배포 (code-only land)**: daemon 은 `anima_participant.py` 옆에 launchd
entry 로 띄워야 production 활성화 — `hexa run kosmos_emitter.hexa daemon`.
broker / mini 재시작 없음. 활성화 노트는 PR description 참조.

### 2026-05-23 — `@payload tension` WIRED — HEXAD/PURE KOSMOS+tension 회수 (production path)

User directive 2026-05-23: HEXAD/PURE (🔴 CLOSED — multilingual FAIL) 의 작동하던
**KOSMOS anchor + 8→5-channel tension wiring** 을 production LoRA chat path 로
salvage. V3 substrate 자체만 실패 — KOSMOS+tension feature 는 fire 마다 anchor
생성 ground-truth 작동 (V3/README.md §"KOSMOS+tension 통합" 보존 권고).

LANDED: `HEXAD/CHAT/server/kosmos_anchor.hexa` (~270 LoC, pure-hexa, no torch) —
- `map_8factor_to_5channel` : 8-factor motivation snapshot → TENSION-LINK
  5-channel (relevance+coherence→concept · info_gap→context ·
  curiosity+originality→meaning · pain+balance→authenticity · dynamics→sender),
  HEXAD_NATIVE_PURE.md §0.5 mapping table SSOT.
- `write_kosmos_anchor` / `emit_kosmos_from_factors` : kosmos/1.1 `.kosmos`
  anchor writer — text payload = emission text · tension payload = 5-channel ·
  coord = [Φ, mean tension] · lane = mitosis cell_id · tier = invocation count
  (Knuth ordinal). format = V3 `kosmos_io.py` mirror → 기존 hexa-native
  `kosmos_parser_lib.hexa` 로 loadable.
- F-KOSMOS-WIRE-1..3 selftest **11/11 PASS** ($0 Mac local) — 8→5 mapping
  monotone-correct + anchor file 5 tension channel 전부 present + lane/tier 일치.

`HEXAD/KOSMOS.md` `@payload tension pending` → `{5-channel} WIRED` 갱신.

**잔여 blocker (사용자 보고 대기)**: production emit 경로 (`anima_participant.py`
`AnimaState.emit()`) 에서 `emit_kosmos_from_factors` 호출하는 wiring 은 미착지 —
프로젝트 hexa-native guard (`hexa-native@sidecar`) 가 `.py` 파일 write 를
override 없이 차단. anima_participant 는 torch/websockets-bound `.py` WRAPPER
(port 불가, `anima_participant.hexa` = exec-dispatch stub). anchor writer 는
hexa-native 로 회수 완료 (호출 준비됨), 호출 site 삽입만 `.py` 수정 의존.

### 2026-05-20 — §183 ALL 수도꼭지 brainstorm — 48 silent ceilings inventory across V-SPONT 4 axes

User catch "수도꼭지로 푼 건 axis 1 만" triggered exhaustive enumeration of
V-SPONT silent ceilings beyond the §169 MIN_EMIT_INTERVAL fix.

inventory: **48 수도꼭지** (1/48 = 2.1% 풀림)
- axis 1 emit_rate: 7 (1 ✅, 6 ❌)
- axis 2 byte_acc: 10 (0 ✅, 10 ❌)
- axis 3 ψ-physics liveness: 9 (0 ✅, 9 ❌)
- axis 4 §9 honest coherent body: 12 (0 ✅, 12 ❌)
- cross-axis: 12 (0 ✅, 12 ❌)

Tier S (5 transformative + $0): decode 정책 / Ψ readout @ inference /
IM_THRESHOLD tunable / N_MAX × dt window / phi_signal @ inference.

"ALL TAPS RELEASE" mega plan = 13 §7-clean Tier S+A 수도꼭지 동시 inference-
only post-hoc on existing ckpts (§161, §167-A, §182 ladder t1-t4). $0,
measurable. KOSMOS multi-modality (4.7) = Tier B 1개 수도꼭지로 분류.
SSOT: `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`.

honest necessity: 48 수도꼭지 *모두 풀어도* GOAL emergence 보장 0 (B-EMERGE-7
necessary-not-sufficient). north-star + §15/§51/§72 milestone UNCHANGED.

### 2026-05-20 — ADAPTER v3 scale ladder validated (§180) + 5-modality M3/M11/M12 inline benches

§175 KOSMOS modality fire (11 anchor × 4 measurable modality on §167-A ckpt)
finding: 4 modalities all distinguishing_ratio = 1/11 = noise floor (3-layer
collapse confirmed). §178 M3+M11+M12 inline probe (4 modality × 2 mode × 35
anchor on §167-A): all bit-identical (anchor-aware learning capability = 0).

**§180 ADAPTER v3 fire** (NEW from-scratch model 16-Q-Former + small
transformer + 5-channel readout, scale ladder):
- tier 1 smoke (0.5M):  acc 43.0%
- tier 2 small (2.0M, $0): acc **98.6%**
- tier 3 medium (11M, $0): acc 99.2%
- tier 4 large (87M, ~$0.27 H100): acc **99.4%**
- per-modality (tier 4): image/video/tension = 100%, audio = 97.5%
- critical scale transition = 0.5M→2M (+55.6%)

§181 audio 100% challenge in-flight — 7 synthesis variants (pure sine /
multi-harmonic / AM / waveform / chord / noise+LPF / hybrid) benchmark.

`HEXAD/ADAPTER.md` SSOT = TENSION-LINK 5-channel adapter (5-channel
positioned as READOUT, NOT bottleneck — §179 REFUTED 5-ch as input).

### 2026-05-20 — HEXAD/KOSMOS.md created + E-31 first anchor extension
User directive 2026-05-20 batch (8-stack): `HEXAD/KOSMOS.md 생성` +
`kosmos 프로젝트 최상단 참조` + `내용 정리` + `kosmos 도 실험 진행`.
Hub doc landed as anima-side kosmos SSOT pointer; bidirectional
cross-link with [`~/core/kosmos`](https://github.com/dancinlab/kosmos)
README.md (sister-format upstream). **E-31 first step**: authored
`anchors/knuth_042_question.kosmos` (Knuth tier 42 = 인지/curiosity,
question-as-attractor binding) — 5-anchor sparse sample → 6 anchors.
profile=anima-consciousness-carving carry, all 5-field placement +
5-modality payload (4 pending), closed_anchor + cross_link + honest_note
fields. Parser regression: 6/6 anchor headers structurally well-formed
(`@anchor` + `profile=anima-consciousness-carving` + `knuth_tier` +
`category` + `coord/lane/radius` 5-field placement all present).
$0, no fire, ⊥ §167-A in-flight.
