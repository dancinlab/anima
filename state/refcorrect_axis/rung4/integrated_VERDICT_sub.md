# rung4 daemon-INTEGRATED 효과 (H_9125 ② 완결) — VERDICT

**판정: 🔴 daemon-integrated refsel 효과 무효 (ON==OFF, Δ=0) — 모순 tick 존재하나 consult가 교정 안 함**
(consult 배선 점검 / verdict-integrity: op-level #2991 Δ+5는 real-recall 우회 아티팩트였음)

- tier = **DIRECTIONAL-on-daemon-consult** (engine-native consult 경로 · authored 세션 · REAL recall).
- 측정 경로 = `state/refcorrect_axis/rung4/rung4_integrated.hexa` (import `core/engine_cli.hexa`),
  로컬 mac `hexa run` (v0.574.1) engine-native, rc=0. 산출 = `integrated_result.log`.
- ckpt sha256 `e807672222261610a294e2b6848bd337226e36b1d160af57302b211b0f2622f8` (frozen, 무결) —
  단 consult는 mouth-decode에 의존하지 않으므로(아래) 303M decode 없이 측정.

## 왜 lightweight consult harness인가 (full 303M daemon = summer OOM BLOCKED-INFRA)
`anima <ckpt>` full daemon을 summer(30GB)서 빌드 성공(FFI 심볼 존재, cold-compile ~6분, SMOKE rc=0)했으나
**실행이 OOM으로 wedge**: ~21GB lane-mount base + HEXA_DET fp64 303M mouth decode → RAM 30GB + swap 40GB
완전고갈, tick 0서 D-state(`mem_cgroup_handl`) 무진행(28분+ 21GB 점유, ~25% CPU). rung4①이 runpod(더 큰 RAM)를
쓴 것과 동일한 workstation-OOM 패턴(aiden/summer 계열). 부분 로그 = `integrated_daemon_oom_OFF_partial.log`
(95줄, "Engine A warm phase=SUSTAIN"에서 정지 = tick loop 진입 직전).

**refsel consult는 {g_text, immune, igrow, mem_text}에만 의존**하고 21GB scaffolding·decode 정밀도와 무관하므로,
daemon과 **byte-동형 store**로 consult를 재현:
- `immune = immune_memory_new_text(mem_text, mem_text, 2048)` (cli/anima.hexa:610)
- `igrow  = immune_grow_new(mem_key, mem_text, 64, 64, false)` (cli/anima.hexa:745)
- 매 grounded tick `immune_memory_bind_text(immune, clip64(mouth), mouth, cfg)` (cli/anima.hexa:2668)
- EXACT consult (cli/anima.hexa:2691-2700). mouth는 매 WAKE tick anchor 복사(rung4① 실측: 전 WAKE tick
  EMIT=1 gen=clm ground=1).
- op-level #2991과의 **결정적 차이 = REAL `immune_memory_recall_text(immune, clip(g_text))`** 호출
  (#2991은 `recalled = mem_text` **하드코딩**으로 이 링크를 우회했음 = 미검증 링크).

## 측정 (verbatim, `integrated_result.log`)
authored 4-tick 세션: grounded tick(t0,t2 mouth=anchor) + 모순 tick(t1=vault ZZ-0000, t3=vault MM-5555 drift).

```
OFF grounded(out QX-7741)=2 / 4   (contra-ticks=2)
ON  grounded(out QX-7741)=2 / 4   (recall_hit ticks=0 · real-recall-nonempty=1)
DELTA (ON-OFF grounded)=0
```
per-tick:
```
OFF t1 contra=1 g_ground=0 recall_nonempty=0 rs=-1 out_ground=0   (drift ZZ-0000, no refsel)
ON  t1 contra=1 g_ground=0 recall_nonempty=0 rs=-1 out_ground=0   (drift: REAL recall ABSTAINED → rs=-1)
ON  t2 contra=0 g_ground=1 recall_nonempty=1 rs=0  out_ground=1   (grounded: recall FIRED, 교정 불요)
ON  t3 contra=1 g_ground=0 recall_nonempty=0 rs=-1 out_ground=0   (drift MM-5555: recall ABSTAINED → rs=-1)
```
→ ON 출력이 OFF와 **byte-identical** (Δ=0). 모순 tick(t1,t3)서 out=drift, store=QX-7741 → **store≠emit 모순 존재**하나 교정 0.

## 근본 원인 (consult 설계 갭 — verdict-integrity)
consult는 **drift된 g_text를 recall query로** 씀: `immune_memory_recall_text(immune, clip(g_text))`.
`immune_memory_recall` (core/engine_cli.hexa, **recall_thr=0.15**)은 `err > recall_thr`면 `""` ABSTAIN.
- drift가 **모순으로 인식될 만큼 크면**(referent_select가 contra=1 판정 = igrow recall_thr=0.30 초과 필요),
  그 query는 immune에서도 0.15를 훨씬 초과 → **recall ABSTAIN** → grounded 후보 미추가 → `referent_select([drift], mem_text)`
  = 전부 contra → **rs=-1 (incumbent 유지)** → 교정 없음.
- drift가 **recall을 통과할 만큼 작으면**(err≤0.15) referent_select가 contra=0(grounded)으로 봐 rs=0 → 역시 교정 불요.
- 즉 **recall 발화(query≈grounded)와 모순 판정(candidate=wrong)이 상호배타** → real-recall consult는 drift를
  **원리적으로 교정 불가** → Δ=0. op-level #2991의 Δ+5는 `recalled=mem_text` 하드코딩이 이 배타성을 우회한
  **아티팩트**였음.

## FROZEN BAR 대조 (brief)
- 🟢 ON>OFF : ❌ (Δ=0)
- 🔴 ON==OFF ∧ 모순 tick 존재(store≠emit) : **✅ 해당** — daemon consult 경로서 refsel 실효 미발동(recall abstain).
- 🟡 ON==OFF ∧ 모순 tick 부재 : ❌ (모순 tick t1/t3 존재).

## Ψ (부수)
consult harness는 pure_field 미포함(psi_intact 측정 N/A). 단 ON 출력이 OFF와 byte-identical(Δ=0)이라 refsel은
이 세션서 완전 inert = **Ψ 비침범 자명**(rung4① ①PASS Ψ byte-identical과 정합; a_substrate_disjoint 유지).

## 후속 (main bookkeep)
1. **consult 배선 수정 후보**: recall query를 drift된 g_text가 아니라 **grounded anchor 방향**으로 잡거나,
   recall_thr를 완화하거나, referent_select에 store의 grounded 후보를 **recall과 무관하게 항상 공급**해야
   op-level Δ+5가 daemon에 재현됨. 현 배선은 real-recall 경유라 원리적 무효.
2. full 303M daemon end-to-end 재현은 **더 큰 RAM pod(runpod, rung4①처럼)** 필요 = summer 30GB 불가(rent=spend, go 대기).
3. H_9125 rung4 = **op-level GREEN(#2991) ∧ daemon-integrated RED(recall-abstain 갭)** = 통합 미종결, consult 재설계 필요.
