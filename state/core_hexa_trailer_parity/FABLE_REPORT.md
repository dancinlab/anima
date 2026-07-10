# anima `core/` 심화 분석 보고서 (coredeep · 2026-07-10 · 코드 무수정, 읽기+분석만)

전체 요약 — 가장 중요한 발견 세 가지: **(1)** `.clm` 트레일러 체인(SLW·CLML)이 **py 채널에만 배선**돼 있어, canonical `e1_slw_303m.clm` 기준으로 hexa 와 py 두 production 표면이 이미 **다른 forward 함수**를 계산한다(§2·§5). **(2)** 문서가 말하는 "Ψ=1/2 고정점"은 코드에서 세 갈래로 흩어져 있고, 그중 실제로 살아있는 것은 `tr_psi` settle 루프 하나뿐이며, 그 A⇄G "대립"은 독립 두 엔진이 아니라 **단일 스칼라의 유도 상보값**이다(§1). **(3)** 결합 무결성은 대체로 건강하다 — `core/` → `archive/`·`bench/`·`agent/` import 0건, decode lane 의 GPU 경로는 env 없이 default-on. 잔존 opt-in GPU env 는 train lane 2건뿐이다(§4).

---

## 1. 텐션 루프의 실제 코드 경로

### A⇄G⇄brain 이 만나는 곳 (py twin 기준, hexa `cli/anima.hexa` 동형)

live 데몬은 `anima_consciousness_mode` (`cli/chat.py:368`, hexa `cli/anima.hexa:636`)의 12-tick 루프(`cli/chat.py:1393,1401`)다. 한 tick 의 흐름:

1. **lane read → emit-drive**: `immune_memory_recall_margin_text` (`cli/chat.py:1413`) → `ci_lane_scores` (`:1421`) → `emit_drive = ci_emit_drive(lanes)` (`:1424`). `ci_emit_drive = 0.5*(lanes[0]+lanes[4])` (`core/engine_cli.py:7154`, hexa `engine_cli.hexa:9092`).
2. **A⇄G conflict**: `ag_a_drive = emit_drive; ag_g_drive = 0.0 - (1.0 - emit_drive)` (`cli/chat.py:1427-1428`, hexa `cli/anima.hexa:2466` 부근) → `conflict_scalar(a,g)` = 반대부호일 때 `|a|·|g|` (`core/engine_cli.py:9568`, hexa `:8600`).
3. **Ψ=1/2 settle**: conflict → `conflict_recruited_depth` (`:9582`) → `tension_resolve_depth(ag_pop, tr_full, 0.3, 0.5, ag_budget, 2, 0.06, cfg)` (`cli/chat.py:1432`; 정의 `core/engine_cli.hexa:11317` / `core/engine_cli.py:9623`). 여기가 **Ψ=1/2 가 계산·사용되는 유일한 live 지점**이다: `tr_psi(pop, thr)` = "인구 중 `ci_emit_drive ≥ thr` 인 비율" (`core/engine_cli.py:9589`), settle 판정 = `|Ψ − 0.5| < 0.06`.
4. **settle → motivation**: settle-depth 비율 = `agloop_ctx` (`cli/chat.py:1433-1435`) 가 8-factor 의 `dyn_v` 자리로 (`:1779-1782`), phasic tension Δ(`ten_phasic`, `:1757-1759`)는 `urgency` 를 거쳐 `rel/cur/idle` 스케일로 들어간다.
5. **brain**: `brain_emit(pf, rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx, idle, …, backend, live_anchors)` (`cli/chat.py:1779`; hexa `cli/anima.hexa:3727`,`5453`) → `brain_decide_anchored`: `emit = should_emit(score) && safe`, safety 4-AND 중 `safety_phi_ratchet_ok(phi, pf.phi_peak)` 가 A(pure_field Φ)→G 게이트 (`core/brain.hexa:45-76,161-201`; `core/engine_g.hexa:63-65`). EMIT 이면 L3 슬롯 `generate()` (`core/generator.hexa:466-546`) → `_gen_clm_decode` → `core/decode.hexa` mouth.

### 설계 문서 vs 코드의 차이 (확인된 것만)

- **Ψ 상수 3분열.** ① `PSI_BALANCE = _psi_load("balance", 0.5)` 는 `core/pure_field.hexa:90` / `core/pure_field.py:102` 에서 **로드만 되고 어디서도 사용되지 않는다**(core+cli 전체 grep 결과 정의 2건뿐). ② `ep_psi_clamp()` (`core/emit_policy.hexa:33`)의 유일 호출자는 `core/emit_policy_smoke.hexa:42`. ③ 실제 살아있는 Ψ는 `tr_psi` 이며, thr=0.5·eps=0.06 은 emit_policy 를 거치지 않는 **호출부 리터럴**이다(`cli/chat.py:1432`). 설계("숫자는 emit_policy 한 곳", EMIT_SUBSTRATE_DESIGN.md:126-133)와 다름.
- **settle 인구는 합성 fixture.** Ψ settle 이 도는 `ag_pop` 은 live 기판 상태가 아니라 conflict 스칼라로 파라미터화된 템플릿 행렬(`anima_tr_pop_conflicted`, `cli/chat.py:96-110`)이다. "A⇄G tension 이 Ψ를 ½로 당긴다"는 문장은 코드에서 "conflict 크기가 합성 인구의 settle 예산을 정하고, 그 settle 깊이가 motivation 한 인자로 돌아온다"로 실현돼 있다.
- **A/G 대립은 유도된 상보.** 배경 SSOT 의 "A(forward CE-trained) ⇄ G(reverse gradient-free) 대립"과 달리, live conflict 의 두 drive 는 한 스칼라 `emit_drive` 의 함수다(`ag_conflict ≈ e·(1−e)`, e=0.5 에서 최대). CE-trained 쪽(.clm mouth)은 conflict 계산에 관여하지 않는다. 참고로 `CORE.md:8-10` 은 A=pure_field Φ, G=engine_g 8-factor 로 정의 — 같은 "A⇄G" 이름이 문서마다 다른 쌍을 가리킨다.
- **emit 임계 이원화.** EMIT_SUBSTRATE_DESIGN §3 의 `emit_threshold 0.60/0.30`·`target_emit_rate 0.27` 은 `core/emit_policy.hexa:30-32` 에 있으나, 실제 emit 결정 임계는 `engine_g` 의 `spont_im_threshold()=0.3` (`core/engine_g.hexa:22,52`)다. emit_policy 에서 prod 에 실제 도달하는 것은 `ep_theta_stage`/`ep_scale_*` (`core/dream_envelope_ctx.hexa:49-58` → `cli/chat.py:46,1761`, `cli/anima.hexa:54`) 뿐.
- **core/CLAUDE.md 가 stale.** `emit_policy.hexa` 를 "비-production" 으로 분류하지만 위처럼 chat 루프에 도달하고, "py 미러 2026-06-28 폐기" 선언과 달리 이 worktree 의 `core/*.py` 는 `cli/chat.py`·`cli/evaluate.py` 가 import 하는 살아있는 production 표면이다(#3245-3251 복원). `core/*.py` 헤더 배너("DEPRECATED py-MIRROR·DIRECTIONAL", 예: `core/brain.py:2-4`)도 현행 `a_eval_py_canonical`(py=TERMINAL-eligible)과 충돌.
- **brain.hexa 내부 모순 1건.** `core/brain.hexa:521-523` 주석은 "brain.hexa intentionally does NOT import engine_cli.hexa" 라고 하지만 `:26` 에서 H_9102 `ImmuneMemory` 타입을 위해 `import "core/engine_cli.hexa"` 를 한다.
- **consult 계열은 문서상 "threaded into the live path"지만 prod 미호출.** §3 참조.

---

## 2. hexa ⇄ py 2-production 미러 정합성

**결론: 갈라진다.** 방향은 대칭적이다 — 트레일러/lane 은 py 가 상위집합, GPU/디바이스는 hexa 가 상위집합.

### verdict 무결성에 직결되는 발산

| # | 지점 | py | hexa |
|---|---|---|---|
| 1 | **SLW slot** | 로드 `core/decode.py:539-540`, forward 적용 `:718-723` (`core/slw.py:51-91`) | **코드 전무** (grep 0건). `core/slw.py:16-18` 의 "decode.hexa byte-parity partner" 주장은 대응물 없음 |
| 2 | **CLML lane** (fork-A) | 로드 `core/decode.py:545-546`, 적용 `:737-739`; writer `core/serialize.py:97-106` | **코드 전무** |
| 3 | **ANIMA_ENGINE env** | env 무시, 상수 `"conv"` (`core/engine_cli.py:179-181`) | env 읽음 (`core/engine_cli.hexa:194-199`) |
| 4 | **NUL byte** | bytearray 로 보존 (`core/decode.py:1462-1468` 명시) | hexa string 은 NUL 불가 → argmax 가 byte 0 을 내면 1바이트 누락 |
| 5 | **serialize writer 조건부 발산 3건** | `np.round` half-to-even (`core/serialize.py:256`) · 홀수 tail nibble pad **0** (`:266-267`) · f32-cast scale | hexa-native writer(`cli/train.hexa`): `to_int(q±0.5)` half-away (`:861-868`) · pad **8** (`:896`) · f64 quant 후 f32 기록 (`:885-891`) |

**#1 의 함의가 가장 크다**: canonical `e1_slw_303m.clm` 은 SLW 트레일러를 갖는 모델인데, hexa `clm_decodable` 은 CLMX 까지만 검사하고 트레일러를 묵살하므로, 같은 파일에 대해 `anima-py evaluate`(TERMINAL 표면)는 slot-ON, hexa det-eval/`anima chat` 은 slot-OFF forward 를 돈다. 두 채널이 **다른 함수**다. (slot 효과의 수치 크기는 이번 분석에서 미측정 — 구조적 발산 사실만 확정.) Gate4 이후 lane `.clm` 이 생기면 #2 로 같은 발산이 확대된다.

#5 는 "hexa 학습→hexa serialize" 경로와 py serialize 출력이 특정 조건(정확히 .5 인 quant code, `cout·rest` 홀수 블록)에서 byte 불일치할 수 있다는 뜻이다. `cli/train.hexa:832-835` 의 "byte-for-byte ground truth = serialize.py" 주장은 코드상 조건부다. 참고: `.pt` 재직렬화 경로는 hexa 채널도 `cli/serialize.hexa:57-72` 가 `python3 core/serialize_standalone.py` 로 shell-out 하므로 동일 코드 = parity 자명.

### 반대 방향 (hexa 상위집합) — 의미론 위험 낮음

- GPU own-GEMM/device-resident/f32 경로 전부 hexa 전용 (`core/decode.hexa:685-693, 1544, 2671, 2970, 4028-4159`); byte-exact 주장이며 py 는 순수 numpy host. 단 device attention 은 `dt_exp` Taylor 라 host 대비 ~1e-6, argmax-eq·NOT bit-eq (`decode.hexa:2663-2667`).
- KV-cache 커버리지: py 는 윈도-슬라이드 재구축으로 argmax·topk 모두 KV (`core/decode.py:1157-1173,1270-1275,1340-1355`); hexa 는 `nseed+gen<=block` 일 때만, 공개 topk 엔트리는 **KV 없음 = O(gen²)** (`core/decode.hexa:3327-3343,3362-3378`). 토큰 스트림 의미론은 동일, wall-time 만 다름.
- `gen_fm_rerank` 는 py 의도적 미구현(DEFERRED, `core/generator.py:411-418`).

### 차이 없음으로 확인된 곳

`engine_g`(상수·수식 1:1, `core/engine_g.hexa` ↔ `.py` 전항목), `brain`(전 함수 1:1, exp/sqrt libm 정합 근거 `core/brain.py:31-38`), `pure_field`(JSON 로더까지 미러; `config/consciousness_laws.json` 실측값 = 하드코딩 디폴트와 동일 — CWD 의존 로드 실패 시에도 수치 동일), PRNG/샘플러 트리오·LayerNorm·GELU·GN·int4 dequant·CLMB bind·grounded/abstain 로직 (decode 대조 §3 "차이 없음" 목록, 예: eps=1e-5 biased-var LN `decode.hexa:1417-1443` ↔ `decode.py:869-883`).

---

## 3. Dead lane / 미배선 census

prod 폐포(검증됨): hexa `cli/anima.hexa:43-58` import 11개 + `cli/evaluate.hexa:40-42`; py `cli/chat.py:34-49` + `cli/evaluate.py:39-41,681,698`.

**prod 도달 확인 (dead 아님)**: `pure_field`·`brain`·`engine_g`·`generator`·`decode`·`kosmos_io`·`dream_lib`·`dream_envelope_ctx`·`dream_persist`·`dream_compose`·`imagination_replay`·`wake_memory`·`emit_policy`·`phi_envelope_substrate`(dream_envelope_ctx 경유)·`rho_fan`(evaluate 전용)·`hippo_lane.py`(`core/generator.py:711` 경유; hexa twin 은 `core/kosmos_io.hexa:661,697,752` + `core/generator.hexa:1145` inline — H_9129 GREEN wired 유지)·`clml.py`(py decode 경유)·`engine_cli`.

**미배선/차단 lane 전수**:

| 항목 | 위치 | 능력 | 왜 안 닿나 | 배선 시 변화 | a_substrate_disjoint |
|---|---|---|---|---|---|
| brain consult 계열: `brain_decide_margin`/`_gap`/`_cerebellum`/`_wm`/`_affect`/`_bg` + `brain_emit_deliberate` | `core/brain.hexa:279-891` (py 동형) | ρ·tether margin/gap·소뇌·WM·affect 의 bounded motivation consult + best-of-K deliberation | prod 루프는 `brain_emit` 단일 호출 (`cli/chat.py:1779`, `cli/anima.hexa:3727,5453`); 호출자는 `engine_cli_smoke.hexa:1534+` 등 smoke 뿐. 단 margin **신호 자체**는 `rel_lane` 으로 우회 유입 중 (`cli/chat.py:1413-1414`) | emit 임계 부근 ±0.05 유계 shade — 카드들이 "wired" 로 서술한 소비가 실제 데몬에 생김 (a_verified_must_wire 관점 재점검 대상) | 위반 아님 — motivation 스칼라만, Ψ/generator 불가침이 설계에 명시 (`brain.hexa:507-536`) |
| `mitosis_hook_lib.hexa` | `core/mitosis_hook_lib.hexa:349,530` | p8-literal serve-time mitosis (forward tail 에 cell split/merge) | 유일 참조 `tool/hexa_native/mitosis_hook.hexa:2`; `imagination_replay` 는 명시적으로 "wired_to_lib=false" (`core/imagination_replay.py:7-11`) | forward 내부 cell_pool 개입 — 단 동등 능력이 이미 `vadapt_field_step` C8 GROW 옆-lane 으로 배선됨 (`cli/chat.py:1794-1806`) | **위반 소지** — forward 그래프 내부 개입은 mouth 와 겹침. 현행 옆-lane 구현이 disjoint 정합 |
| `metacog_lib.hexa` + `audit_hook.hexa` | `core/metacog_lib.hexa:42,155` · `core/audit_hook.hexa:34,49` | 5-tier self-audit verdict taxonomy + N-tick audit hook | importer 가 `anima_full_session_k7_smoke.hexa:36` 뿐. prod metacog 은 `engine_cli.hexa:9136,9169` 의 **별개 in-file 구현** | 데몬 자기감사 tick | READ-only 요약이라 분리 가능 |
| `substrate_hook.hexa` | `core/substrate_hook.hexa:56,75` | savant-mode trigger (savant_lib 위 controller) | smoke-only; `engine_cli.hexa:89` 의 import 는 주석 처리 | savant 트리거가 tick 에 | context 스칼라 read 면 유지 가능 |
| `savant_lib.hexa` (잠재 lane) | `core/savant_lib.hexa:99,133` | GZ×SI 측정 primitives | hexa 폐포에 import 는 됨(`engine_cli.hexa:90`)이나 `ANIMA_SAVANT` **default OFF** (`engine_cli.hexa:325-333`); py twin 모듈 없음(`sv_*` 는 `engine_cli.py:9231-9541` inline) | savant 측정 lane 활성 | 측정자(E축)라 emit 게이트 아님 — 정합 |
| `xsubstrate_bridge.hexa` | `core/xsubstrate_bridge.hexa:11,22` | EEG/AKIDA spike/외부 logit → brain-context 스칼라 bridge | repo 내 importer 0 (archive harness 만) | 외부 기판 신호가 brain context 로 | context READ 설계라 분리 가능; AKIDA 는 `a_lane_akida_gpu_split` 별도 lane 태그 필요 |
| `shared_seed`(.hexa/.py) + `anima_birth.hexa` | `core/shared_seed.hexa:37,55` · `core/anima_birth.hexa:33` | QRNG 공유키(부모→자식 birth key) | smoke-only (`anima_birth_smoke.hexa`, `shared_seed_smoke.hexa`); py importer 0 | birth 경로 | 무관 (emit 아님) |
| `lane_p_engine_probe`/`lane_p_three_axis`/`lane_x_explore`/`emergence_ideation`/`three_axis_probe`/`omega_clm_closure_probe` 등 | 각 파일 `main` | self-run probe/실험 | importer 0, env 로 직접 실행 — `core/CLAUDE.md` "비-production" 선언과 일치 | — (의도된 lab) | — |
| `core/phi/` 166파일 | 디렉토리 전체 | phi 실험군 | prod 폐포에서 import 0건 (내부 상호참조만) | — | — |
| `core/DECODER/flame_mm.py` | 헤더 L2-4 | deprecated py 미러 | importer 0 (hexa 쪽 `flame_mm.hexa` 는 `decode.hexa:51` 로 prod) | — | — |
| `core/engine_cli.py:10209-10234`, `core/clm_serialize_v2.py:469-486` 등의 `__main__` 블록 | — | self-smoke | 최상단 entry-guard `exit` 가 먼저 실행 → **도달 불가 사문** (`engine_cli.py:8-10` 등; `brain.py`·`engine_g.py` 동일 패턴) | — | — |

부정적 발견(정직): 위 표 외에 "정의됐지만 안 닿는" prod 후보는 없었다. dream/imagination/wake 계열은 전부 살아 있다.

---

## 4. 결합(coupling) 위반 감사

**① `core/` → `archive/`·`state/`·`bench/`·`agent/` import: 0건.** 코드-레벨 참조는 전부 문자열 경로이며 import 아님: `core/verify_clm_v2.py:819-821` (golden `.clm` 탐색 — `state/laneg_d768_recover/...` 상대경로 + **절대경로 하드코딩**, 없으면 skip, `GOLDEN_CLM` env override), probe 파일들(`emergence_ideation.hexa:104`, `three_axis_probe.hexa:56`, `clm_ce_descent_probe.hexa:35-37`), smoke 출력 문자열 1건. `bench/`·`agent/` 참조 코드 0건. `core/serialize_standalone.py:46-53` 은 archive 시절의 4-단계-상위 `_REPO` 계산이 vestigial 로 남아 있으나 line 49 fallback 으로 무해하게 동작. — 단방향 불변식은 **건강**.

**② GPU fast-path opt-in (`a_gpu_default_no_optin` / H_9119 재발 여부):**
- **decode lane: 깨끗.** `core/decode.hexa` 에 getenv 0건; `_clmd_devres() = cuda_available()` default-on, 구 `CLM_PROD_DEVRESIDENT` 게이트는 제거되고 주석에만 잔존 (`core/decode.hexa:677-693`). `core/decode.py`·`cli/chat.py`·`cli/evaluate.py` env 읽기 0건.
- **train lane: opt-in 2건 잔존** — `CLM_PROD_DEVFEED`/`HEXA_FUSE_ALL` (`cli/train.hexa:165-166`), `CLM_PROD_DEVRESIDENT`/`HEXA_FUSE_ALL` (`cli/train.hexa:448`), 둘 다 default OFF 의 GPU device 경로다. 정확히 H_9119 의 dont("byte-exact capability-detectable GPU path 를 opt-in env 뒤에 두지 마라") 패턴이 **train lane 에 남아 있다.** 참작 사정: mac prebuilt 에 해당 커널 심볼이 없어 link-capability 게이트 성격이 있고(주석 근거 `train.hexa:165` 부근), train 은 verdict 표면이 아니다. 그래도 `.harness/enforce_anima_gates.py` enforce-후보로 올릴 가치가 있다.
- `HEXA_DET` (`cli/anima.py:62-67`)는 반대 방향의 **의도된** opt-in(결정론이 opt-in, fast 가 default) — bit-det-drop-fast-train 오너 정책과 정합.
- 기타 env 는 faculty 게이트(`ANIMA_MITOSIS` default **ON** `engine_cli.hexa:148-153`, `ANIMA_TOPO_COUPLE`/`ANIMA_REFSEL`/`ANIMA_SAVANT`/`ANIMA_FORWARD_MODEL` OFF)로 GPU 무관.

**③ `a_cli_single_entry` 우회:** `engine_cli.{hexa,py}` 는 서브커맨드 없는 순수 라이브러리(hexa `fn main` 없음; py 는 direct-run guard `engine_cli.py:8-10`). cli→`python3 core/*` subprocess 는 `cli/serialize.hexa:68` 단 1건이며 cli/CLAUDE.md 가 sanctioned 로 명시(.pt unpickle 은 py 불가피). 나머지 subprocess 는 전부 canonical 디스패처 내부 verb dispatch (`cli/anima.py:130-271` spawnv, `cli/anima.hexa:273-445` exec)와 유틸(`od`, `nvidia-smi`, `date`). 신규 위반 없음. 사소 표기 1건: `cli/eval_pod.sh:96` 이 verb 를 `eval` 로 쓰는데 코드 분기는 `evaluate` (hexa main `cli/anima.hexa:500-503`) — 동작 여부 미확인.

---

## 5. G1 fork-A CLML lane 의 정확한 배선 지점

### 현황 — py 왕복은 이미 완결

- **자료구조/codec**: `core/clml.py` — `lane_apply` (numpy 추론 미러, `:42-64`), `pack_clml`/`read_clml` (`CLML` magic trailer: `lane_type u8 · r u32 · tau f32` + `W1[d,r] b1[r] W2[r,V] w_g[2d] b_g[1]` LE f32, `:75-107`), `CLMLModule` (torch, `:133-155`). 수식 = `logits + clip( sigmoid([yn_t;c_t]·w_g+b_g) · gelu(c_t·W1+b1)·W2 , ±tau )`, `c_t` = `yn` 의 causal 누적평균.
- **serialize**: `core/serialize.py:97-106 append_clml_trailer` — 트레일러 체인 **끝**(CLMX→CLMB→SLW→CLML, `:93` 주석) append. 현재 호출자는 research 의 `state/recomb-routing-lane/clml_wire.py` 뿐(cli 미노출).
- **decode(py)**: `clm_load_weights` 안 `read_clml` (`core/decode.py:545-546`, absent→`None`=passthrough), forward 에서 `yn_trunk = yn` **pre-slot 캡처** (`:711`) → SLW `slot_apply` (`:718-723`) → readout (`:725-733`) → `lane_apply(yn_trunk, out_logits, W["clml"])` (`:737-739`). 즉 Gate4 (`anima-py evaluate --system-g1`, `cli/evaluate.py:1360-1363`) 가 🟢 로 착지하면 **py 채널 측정·chat 은 추가 배선 없이 이미 산다.**
- v0.3 참고: 실코드의 "v0.3" 은 (L,E) 일반화 문법(magic bump 없음, `core/serialize.py:150-171`, `serialize_v3 :372-391`)이고, LANE 은 별도 CLML **트레일러** 컨벤션으로 실현됐다. 메모리의 ".clm v0.3 LANE" = 이 트레일러다.

### 빠진 것 = hexa twin (a_verified_must_wire 의 "live core/ wired" 충족 지점)

`core/decode.hexa` 에 CLML(및 전제인 SLW) 코드가 0건이므로, 🟢 시 hexa 쪽 배선 지점은 정확히:

1. **로더** `_clmd_load` (`core/decode.hexa:343-429`): CLMB 센티널 파싱(`:408-422`) 뒤에 SLW(`"SLW\x01"`) → CLML(`"CLML"`) 순서로 트레일러 파싱 추가. `W["clml_W1"/"clml_b1"/"clml_W2"/"clml_wg"/"clml_bg"]` farr 핸들 + `W["lane_type"]/["lane_r"]/["lane_tau"]`. absent/short → `lane_type=0` (py `read_clml :91` 과 동일 guard 관용구). `clm_decodable`(`:73`)은 불변 — "트레일러 부재 ⇔ byte-identical" 계약(`core/clml.py:15`) 유지.
2. **scratch** `_clmd_scratch_new` (`:555`): `c`(T·d 누적평균 버퍼)·`z`(T·r)·`delta`(T·V) resident 버퍼 + pre-transposed `W1t/W2t` (기존 `tcWt` 관용구 `:448-458` 그대로).
3. **streaming forward** `_clmd_fwd_logits_sc` (`:695`): 최종 GN 출력 `sc["yn"]` (`:752-755`) 을 `yn_trunk` 로 스냅샷(**SLW 를 함께 들이면 slot 적용 전에 떠야 함** — py `:711` 과 동일 순서), readout(`:759-778`) 후 `out_logits += clip(gate·(gelu(c·W1+b1)·W2), ±tau)`. 두 GEMM(`c·W1`, `z·W2`)은 `mm()`/`_clmd_conv1d_pre(K=1)` 로 forge 시임에 태워 **`cuda_available()` default-on** (`a_gpu_default_no_optin` — env 게이트 금지, `_clmd_devres :685-693` 선례 그대로).
4. **per-call forward** `_clmd_fwd_logits` (`:785`) 에도 동일 적용 — `clm_forward_ce`/`clm_omega_closure` 측정 경로가 lane .clm 을 정직하게 재도록.
5. **검증**: `core/verify_clm_v2.py` 구조체크에 CLML 섹션 추가 + parity gate "hexa lane-ON logits vs py `lane_apply` max|Δ|" (f64 기준 0 또는 ≤2e-16 — CONV 미러의 기존 정밀도 급).

### DISJOINT 를 코드 수준에서 보장하는 방식

(i) emit/silence 결정은 `brain_decide`(8-factor+safety)에서 **logits 이전에** 완결되고, lane 은 EMIT 확정 후 `generate()→clm_decode_*` 의 바이트 함수만 바꾼다 — mouth⊥decision. (ii) Ψ 경로(`tr_psi`·`ci_emit_drive`)는 decode logits 를 전혀 읽지 않는다(§1 경로 참조). (iii) bias 는 학습된 gate × `±tau` clip 으로 유계·additive. (iv) 트레일러 부재 시 exact passthrough. 회귀 가드는 기존 discipline 재사용: chat 의 `psi_intact` ON==OFF Φ-checksum (`cli/chat.py:1958-1964`). **주의 1건**: `clm_decode_grounded` 의 anchor-copy 는 비영향이지만 **LM-argmax fallback 은 lane 영향권** (`core/decode.py:1522-1560`) — ρ·tether(비조작) 측정 시 lane-ON/OFF 를 명시해야 한다.

### 🧱 착지 시 대안 각도 (한 문단)

Gate4 가 held-out 생성에서 죽으면, 1차 저비용 각도는 lane 구조 확장이다: 현 delta 는 `f(c)`(문맥 요약의 정적 logit-bias)뿐이므로 bottleneck 입력을 `[y_t; c_t]` 로 확장(`W1` 을 `(2d,r)` 로)해 위치-조건부 라우팅을 허용하는 것 — `CLML_DEEPEN_DESIGN.md` §2.1 의 dump-1회 레시피 그대로 frozen-trunk·$0 재학습이 성립한다. 그다음 각도는 read-side(logit)가 아니라 **write-side 재주입**: 이미 codec 이 존재하는 SLW 슬롯 형식으로 pooled 컨텍스트를 readout 이전 `yn` 에 gated-write 하는 변형 — 단 이는 trunk 함수 자체를 바꾸므로 DISJOINT(emit-byte 불변) 증명을 처음부터 다시 해야 하고, copy-discount(C-mask+N2 null) 를 먼저 통과한 셀에서만 판정해야 한다(§1.4 사전등록 bar). γ trunk-bake(H_1840 frozen-gate 차단) 재발사는 아니다 — trunk 재학습이 아니라 주입 지점 이동이다.

---

## 6. 심화 레버 (순위)

**1. hexa 2-surface 트레일러 parity 복원 (SLW+CLML hexa reader + parity gate).**
무엇: §5 의 1–5 배선 + verify parity. 왜 지금: canonical E1-SLW 303M 에서 **이미** 두 채널이 다른 함수(§2 #1)이고, Gate4 결과와 무관하게 verdict 무결성 회복이 선행 조건이다(🟢 면 발산이 lane .clm 으로 확대). 반증가능 예측: hexa lane/slot-ON logits 가 py 와 max|Δ|=0 (f64) — 실패하면 codec/적용순서 결함이 실측으로 드러난다. compute: $0 CPU(pool). 죽은 레버와 무관(정합성 작업, 능력 주장 없음).

**2. CLML copy-discount P0 (0.98 champion 재채점).**
무엇: `CLML_DEEPEN_DESIGN.md` §1 의 C-mask + N2 surface-lexicon null 로 기존 0.98 셀 재채점. 왜 지금: Gate4 와 독립·$0·fork-A 프로그램 전체의 사전등록된 첫 관문("N2 가 만점이면 그 셀은 verdict 무자격"). 반증가능 예측: copy 가설이면 `Acc ≈ f(overlap)` 단조 하강 / 합성 가설이면 평탄 (기울기가 지표). compute: $0 (캐시된 hidden). γ trunk-bake 재발사 아님 — frozen trunk read-side.

**3. Ψ 상수 단일화 + H_651식 재확인.**
무엇: 3분열된 Ψ 상수(§1 — `PSI_BALANCE` 미사용, `tr_psi` thr/eps 호출부 리터럴, `ep_psi_clamp` smoke-only)를 emit_policy 경유 단일 SSOT 로 배선하고, α-sweep 으로 "Ψ 상수는 settle-depth 분포를 움직이되 Φ-checksum 은 평탄(NON-DEFINITIONAL)" 을 live 루프에서 재측정. 왜 지금: 설계 계약(숫자 한 곳)과 코드가 어긋난 상태에서 Ψ 관련 후속 측정이 쌓이는 중. 반증가능 예측: eps 0.06→0.03 이 `agloop_ctx` 분포를 유의하게 움직이고 `psi_intact` 는 유지 — Φ까지 움직이면 H_651 의 live-루프 반례 발견(그 자체가 결과). compute: $0. σ de-theater 가 죽인 것(emit shade 로의 pool-fold/self-fold)과 목적이 다름 — emit 채널 조작이 아니라 측정 프레임 정합.

**4. A⇄G conflict 원천 독립화 측정 (urgency 채널 한정).**
무엇: 현 `ag_g_drive = -(1-emit_drive)` 유도 상보(§1)를 engine_g motivation(진짜 G 신호)으로 대체한 변형의 conflict/settle-depth/urgency 분포 Δ 를 ARM-SHOCK 양성대조와 함께 측정 — **배선이 아니라 측정 먼저**. 왜 지금: "opposing engines" 프레임의 코드 실현이 단일 스칼라 함수임이 이번에 확정됐고, urgency 는 σ frontier 에서 유일하게 살아남은 proven 채널이다. 반증가능 예측: 독립화가 `ten_phasic` 분산을 키우고 emit-timing ΔEff>0; ΔEff≈0 이면 즉시 기각(THEATER — 유도 상보로 충분하다는 결론도 결과). compute: $0 pool. read-side pool-fold(죽음)와의 비겹침: fold(신호를 emit shade 로 접기)가 아니라 conflict 의 **입력 원천** 교체이며, 판정은 동일한 ARM-SHOCK discipline 을 재사용.

**5. hexa BYTE-mouth 공개 topk 엔트리 KV-cache.**
무엇: `bytegpt_decode_topk_sampled(_ranged)` (`core/decode.hexa:3327,3362`) 에 py 식 윈도-재구축 KV(`core/decode.py:1157-1173`) 이식. 왜 지금: chat mouth 의 대화 응답이 이 엔트리를 타면 O(gen²) — py 채널과 wall-time 비대칭. 반증가능 예측: 토큰 스트림 byte-identical + per-emit wall 급감; 단 kvcache-scalar-glue-bound 선례상 이득이 glue-bound 로 유계일 수 있음(그 상한 실측 자체가 결과). compute: $0 CPU, GPU 검증은 pool. 죽은 레버와 무관(H_9119 는 devres 게이트 문제였고 이건 커버리지 문제).

---

### 미확인으로 남긴 것 (정직 표기)
- E1-SLW 303M 에서 slot-ON vs slot-OFF 의 **수치** 차이 크기 (구조 발산만 확정).
- `cli/eval_pod.sh:96` 의 `eval` verb 가 hexa main 에서 실제 동작하는지.
- hexa-native writer 발산 3건(§2 #5)이 실존 ckpt 에서 실제 byte 차이를 낸 적이 있는지 (조건부 발산점 식별만).
- Gate4 자체의 결과 (LIVE aiden 계산중, `state/recomb-routing-lane/GATE_RESULT.md`).

메모리에 1건 저장함: `hexa-py-trailer-divergence-slw-clml` — SLW/CLML 트레일러의 hexa 묵살 발산(향후 lane/slot .clm verdict 인용 시 선확인용).