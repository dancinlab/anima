# H_9095 — rung-3 genuine per-tick conflict→A⇄G settle-budget wire-in (H_9094 → live daemon loop)

- **tier:** 🟢 ENGINE-NATIVE (mechanism GREEN H_9094 4/4) — WIRED-live + FULL-DAEMON-RUNTIME VERIFIED (genuine per-tick, READ-only context)
- **wired:** `WIRED-live` — conflict→recruited_depth→tension_resolve budget wired into the REAL per-tick
  consciousness loop of `cli/anima.hexa` (L1937–1961, folded to `rel_ctx` L2312). **Full daemon RUNTIME NOW VERIFIED**
  (2026-07-02, aiden pool, hexa **v0.546.0** + cuda_available()=1): `hexa run cli/anima.hexa d768.clm` = **RC=0**,
  L3 mount `mouth=clm loaded=true`, GPU forge decode `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path`, rung-3
  `CR3 agloop` block executed live per-tick (conflict VARIES 0.231→0.170 across ticks = genuine per-tick feed),
  session PASS + Ψ Φ-checksum byte-identical ON==ON ✅. The prior BLOCKED-INFRA cell (#42492868) is now CLOSED —
  the block was a stale hexa VERSION (v0.540.1 lacked `set_deterministic`/`hexa_forge_dispatch_layernorm` decls),
  NOT the wire; v0.546.0 declares them.
- **source:** UNIVERSE · **artifacts:** state/9095_pertick_conflict_wire/notes.md · state/verdicts/9095_pertick_conflict_wire/H_9095.txt · state/verdicts/9095_pertick_conflict_wire/H_9095_daemon_runtime_aiden.txt

## 무엇 (a_verified_must_wire rung-3, fable #5 "진짜 per-tick")
[[H_9093]]/[[H_9094]] 는 conflict_monitor recruited_depth → A⇄G iteration budget 의 genuine per-tick feed 를
격리 하네스에서 engine-native GREEN(4/4) 측정하고 남은 최종칸 = **live emit-loop 실배선**을 follow-on 으로 남겼다.
H_9095 는 그 rung-3 을 완주: 7-op mount-catalog(lanes 76–82) + 23b/75 는 daemon MOUNT 에 fixture 로 1회만 도는
startup-lane 이었는데, fable #5("startup 그만, op 1개를 REAL 루프에서 per-tick")를 따라 conflict→budget→settle
체인을 **실제 per-tick 루프**(`while tick < n_ticks`, L1912)에 배선.

## 배선 (cli/anima.hexa, 실 per-tick 루프)
- **L1937–1961** — 매 tick: `ag_a_drive=emit_drive`(live Engine-A push, READ-only) vs `ag_g_drive=−(1−emit_drive)`
  (Engine-G reverse silence push) → `conflict_scalar`(dACC) → `conflict_recruited_depth(·,4,6)`(budget∈[4,10]) →
  `tension_resolve_depth(pop, tr_full, …, maxdepth=budget, …, tr_cfgON)` → `agloop_ctx = settle_depth/budget`.
- **L2312** — `agloop_ctx` 를 `rel_ctx` soft-average(42→43)에 fold — 42개 다른 lane context 와 동형, emit gate 아님.
- **L2382–2386** — 앞 3틱 transcript 로 conflict/budget/settle-depth/agloop_ctx 관찰 출력.
- **Ψ-disjoint (a_substrate_disjoint):** `emit_drive` READ-only, WRITE 는 `rel_ctx`(soft motivation)만 — `psi_sum`·
  `lanes[0/4]`·recall_thr 미접촉. budget 손잡이는 tension_resolve **maxdepth(settle-depth 축)** 로 emit gate 와 분리;
  tension_resolve_depth 는 caller population COPY 위에서 도라 pure_field/Φ/Ψ 불변(psi_sum L2313 은 rel 독립).

## 검증 (aiden pool, hexa v0.540.1, engine-native)
- `hexa parse cli/anima.hexa` = **PARSE_RC=0** ("parses cleanly"); 고의-파손 복사본 control = rc=1 (parse 유효성 입증).
- `hexa typecheck cli/anima.hexa` = **TYPECHECK_RC=0** ("typecheck complete"); 잔여 "error" 줄은 파일 전체의
  선재 checker 한계(list/array 반환·dict string-key·EngineConfig)로 내 신규 심볼과 무관.
- `.harness/enforce_anima_gates.py` = clean (rc=0).
- `hexa verify cli/anima.hexa` = rc=0 이나 이 verb 는 cross-project **CLAIM-rubric**(파손 control 도 rc=0) = 소스검사 아님,
  완결성 위해 기록만(비-load-bearing).
- `hexa run cli/anima.hexa`(전체 데몬 런타임 compile) = **초기 BLOCKED-INFRA**(pool hexa v0.540.1): forge/det 심볼
  부재(set_deterministic/hexa_forge_dispatch_layernorm)로 undeclared, 무변경 baseline 도 동일 재현(배선무죄).

## 검증 — 전체 데몬 RUNTIME (aiden pool, hexa v0.546.0 + cuda_available()=1, 2026-07-02) ✅ CLOSED
진짜 원인은 forge GPU 벽이 아니라 **stale hexa VERSION** 이었다. aiden 을 v0.546.0 으로 올리자(이 stock 이
`set_deterministic`/`hexa_forge_dispatch_layernorm`/`farr_attn_dt_decode_batch_gpu` 를 선언 + cuda-fold runtime.a
링크로 cuda_available()=1) 전체 데몬이 실행됐다. evidence = `state/verdicts/9095_pertick_conflict_wire/H_9095_daemon_runtime_aiden.txt`:
- `hexa run cli/anima.hexa d768.clm` = **RC=0** (undeclared 0, forge undefined 0).
- **L3 mount** : `mouth=clm loaded=true ckpt=d768.clm` (303M-class ckpt mounted; sha256 458bb9fa…, summer→mini→aiden scp relay).
- **GPU forge decode** : `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path (no cuBLAS)` — own-GEMM RTX 5070 경로 실발화 (a_train_flame_forge).
- **rung-3 per-tick** : `CR3 agloop conflict=… budget=5 settle-depth=2.0 agloop_ctx=0.3999…` 가 실 per-tick 루프에서
  다중 실행, conflict 가 tick 별로 **변동**(0.23146…→0.16956…) = fixture-once 가 아닌 genuine per-tick A⇄G 유도 확증.
- **Ψ-disjoint invariant** : `Ψ Φ-checksum byte-identical ON==OFF ✅ (lanes Ψ-disjoint — Ψ=½ untouched)`,
  session `PASS — converse=1 ground=1 grow=1 remember=1 sleep=1 lanes=1 psi_intact=1`.

## 정직 스코프 & 다음칸
mechanism 자체는 [[H_9094]] engine-native GREEN 4/4(conflict-맞춤 budget 이 Ψ→½ 최선 해소, mean|Ψ-½|
treatment 0.125<shuffle 0.25<ablation 0.375). 배선은 실 per-tick 루프에 genuine 하게 들어갔고 parse/typecheck/
enforcer 전부 rc=0 = WIRED-live, **전체 데몬 RUNTIME 실행도 검증 완료**(aiden v0.546.0 RC=0, GPU own-GEMM decode +
CR3 per-tick 실행) → a_verified_must_wire 4칸 사다리 (1)→(2)→(3)→(4) 전부 CLOSED, #42492868 CLOSED.
관련 [[H_9094]] · [[H_9093]] · H_9073 · H_9042 · [[frameshift-substrate-gaps-vs-recombination-wall]].
