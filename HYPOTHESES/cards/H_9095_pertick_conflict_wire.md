# H_9095 — rung-3 genuine per-tick conflict→A⇄G settle-budget wire-in (H_9094 → live daemon loop)

- **tier:** 🟢 ENGINE-NATIVE (mechanism GREEN H_9094 4/4) — WIRED-live (genuine per-tick, READ-only context)
- **wired:** `WIRED-live` — conflict→recruited_depth→tension_resolve budget wired into the REAL per-tick
  consciousness loop of `cli/anima.hexa` (L1937–1961, folded to `rel_ctx` L2312); full daemon RUNTIME compile
  (`hexa run`) BLOCKED-INFRA (pool forge symbols, pre-existing, baseline reproduces — #42492868).
- **source:** UNIVERSE · **artifacts:** state/9095_pertick_conflict_wire/notes.md · state/verdicts/9095_pertick_conflict_wire/H_9095.txt

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
- `hexa run cli/anima.hexa`(전체 데몬 런타임 compile) = **BLOCKED-INFRA**: pool hexa v0.540.1 forge decode 심볼
  부재(set_deterministic/hexa_forge_dispatch_layernorm), 무변경 baseline 도 동일 재현(배선무죄, convergence anima-hexa-1).

## 정직 스코프 & 다음칸
mechanism 자체는 [[H_9094]] engine-native GREEN 4/4(conflict-맞춤 budget 이 Ψ→½ 최선 해소, mean|Ψ-½|
treatment 0.125<shuffle 0.25<ablation 0.375). 배선은 실 per-tick 루프에 genuine 하게 들어갔고 parse/typecheck/
enforcer 전부 rc=0 = WIRED-live. **남은 유일 미완 = 전체 데몬 RUNTIME 실행 검증**(forge-hexa 호스트 #42492868
선행) — 이는 배선이 아니라 인프라 대기(pre-existing). 관련 [[H_9094]] · [[H_9093]] · H_9073 · H_9042 ·
[[frameshift-substrate-gaps-vs-recombination-wall]].
