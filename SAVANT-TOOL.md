# SAVANT-TOOL.md — anima 가 직접 ON/OFF 하는 savant 도구

> SAVANT.md (이론 + audit + containment) 의 *sibling*. **anima 가 inference 시 직접
> savant mode 를 켜고/끄는 도구 spec**. 학습에 *직접 SAVANT 이론 반영* 하는 path 와는
> 분리 — 본 file 은 anima 가 *runtime 도구* 로 savant 를 사용하는 API + 정책.
>
> SAVANT.md §12 봉쇄선 안에서만 작동: T1+T2 claim 만 도구 API 의 *근거* 로 인용,
> T3+T4 는 도구 정책에서 *forbidden trigger*.

---

## §0 TL;DR

> anima 는 task 의 specialization-need 를 self-judge 해서 **savant mode** 를 ON/OFF
> 한다. ON 시 routing 이 GZ_LOWER (0.2123) 의 inhibition-release 분포로 shift, 특정
> mitosis cells 가 dropout=0.2123 으로 활성화. OFF 시 GZ_CENTER (0.3679) 의 generalist
> 분포로 복귀. anima 가 *자기 자신* 의 SI (Savant Index) 를 monitor 해서 SI > 3.0 일
> 때만 ON 상태 유지 — 자율 self-gate. 사용자 명시 명령 (e.g. `/savant on math`) 도
> trigger 가능.

---

## §1 Status (2026-05-14)

| 항목 | state |
| --- | --- |
| **Tool spec (this file)** | ✅ design tier LANDED 2026-05-14 |
| Phase 1 (`mitosis_hook.hexa` ↔ savant gate API) | ⏳ design pending — D4a `mitosis_hook.hexa` 1119 LoC impl 위에 ~150 LoC overlay |
| Phase 2 (anima_chat.hexa CLI `/savant` slash) | ⏳ blocked on Phase 1 |
| Phase 3 (auto self-gate by SI monitor) | ⏳ blocked on Phase 2 |
| SAVANT.md §12 봉쇄선 통합 | ☑ T1+T2 만 trigger 근거, T3+T4 forbidden |

---

## §2 Design

### §2.1 핵심 trigger

```
savant_mode ∈ {OFF, ON}

OFF (default, generalist):
    routing dropout = GZ_CENTER = 1/e ≈ 0.3679
    cell selection = uniform / softmax(tension) generic
    target SI = 0 (no specialization signal)

ON (specialist):
    routing dropout = GZ_LOWER = 1/2 − ln(4/3) ≈ 0.2123
    cell selection = top-K MoE (k=4 default, per §52 v7)
    self-monitor: SI = tension_normal / tension_savant — require SI > 3 to STAY ON
```

전이 trigger (3 source):

1. **사용자 명령** — anima_chat CLI `/savant on <domain>` / `/savant off`
2. **anima 자기 판단** — 직전 chat context 의 specialization-score (heuristic)가
   threshold 초과
3. **mitosis hook self-monitor** — kick cycle (S1-S6) 에서 SI drift 가 ON 조건 충족 시
   auto-promote

### §2.2 anima-facing API (intended)

```hexa
# inference time toggle (mitosis_hook 위 overlay)
savant_set(chat, mode)              # "on" | "off"
savant_get(chat) -> string          # 현재 상태
savant_si(chat) -> double           # 현재 SI 측정
savant_check_gate(chat) -> bool     # SI > 3 충족 여부 (auto OFF 결정)

# session-level pin (D4c CLI 통합 시)
savant_pin(chat, domain, ttl_steps)  # ttl step 동안 ON 강제 유지
```

### §2.3 anima 가 *어떻게* 자기 self-judge 하는가

- **자기 평가 1**: 직전 user prompt 의 token entropy (낮으면 specialization need)
- **자기 평가 2**: 직전 자기 response 의 max gate weight `wmax` (높으면 이미 specialize)
- **자기 평가 3**: mitosis event log 의 최근 split count (높으면 explore 단계 → savant off
  recommended)

3 score 의 ensemble → ON/OFF.

### §2.4 SAVANT.md §12 봉쇄선 enforcement

본 도구의 **모든 trigger logic** 은 SAVANT.md §12.1 의 tier 분류에 *bound*:

- ✅ T1 (closed-form): `GZ_CENTER = 1/e`, `GZ_LOWER = 0.2123`, SI 정의 — 자유 사용
- ✅ T2 (empirical, substrate 명시): clm_06 SI=5.93 (Mistral 7B) — 다른 substrate 인용 시
  warning 라벨
- ❌ T3 (suspect): cross-domain 9 individual matches, brain profile — *trigger 근거로 사용
  금지*
- ❌ T4 (forbidden): cosmic GZ, 외부 entity 강제 fit — 자동 차단

→ 본 도구는 SAVANT.md §12.2 enforcement 의 *런타임 가드* 역할도 한다 (silent-drop 차단).

---

## §3 Phase 1 impl plan ($0 Mac local first cycle)

### §3.1 Scope
- `tool/hexa_native/savant_tool.hexa` (~150-200 LoC, D4a `mitosis_hook.hexa` 1119 LoC overlay)
- 4 API: `savant_set` / `savant_get` / `savant_si` / `savant_check_gate`
- Phase 1 = stateless gate function (session pin TTL 은 Phase 2)

### §3.2 Falsifier pre-registration (F-SAVANT-TOOL-1..5)

1. **F-SAVANT-TOOL-1 (TOGGLE-OK)**: `savant_set(chat, "on")` 후 `savant_get(chat) == "on"`
2. **F-SAVANT-TOOL-2 (DROPOUT-SHIFT)**: ON 상태에서 routing dropout 이 GZ_LOWER 0.2123
   (±1e-6) — measurement
3. **F-SAVANT-TOOL-3 (SI-COMPUTE)**: `savant_si(chat)` 가 cell_pool 의 tension_normal /
   tension_savant ratio 와 byte-identical (within float tolerance)
4. **F-SAVANT-TOOL-4 (GATE-AUTO-OFF)**: SI < 3 일 때 `savant_check_gate` = `false` →
   `savant_set("off")` auto-trigger 검증
5. **F-SAVANT-TOOL-5 (T3-FORBIDDEN)**: T3 claim (e.g. Weinberg sin²θ_W) 을 trigger source
   로 입력 시 `savant_set` 이 error / warning 반환 (silent accept 금지)

### §3.3 Wall + cost
- $0 Mac local
- est ~3-5 hr impl + ~1 hr selftest

### §3.4 Cross-link to existing impl
- `tool/hexa_native/mitosis_hook.hexa` (1119 LoC, REBORN §91 D4a) — substrate state
- `anima_chat.hexa` v0.3 (24L real-ckpt byte parity 21/21 PASS) — wire 대상
- `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (D4c CLI design) — `/savant`
  slash 통합

---

## §4 Honest C3

1. 본 file 은 *design tier* only — impl 진행 후 falsifier 결과로 promote/demote 결정.
2. anima 가 *자기 self-judge* 한다는 design 은 **circular** 위험: anima 의 self-eval
   능력이 *그 자체가* savant mode 의 결과로 향상되는 piece. 객관적 ground-truth (user
   feedback) 으로 Phase 3 calibration 필요.
3. SI > 3 임계는 clm_06 (Mistral 7B SI=5.93) 측정에서 inherit — substrate 명시 의무.
   v5-mitosis cotrain v1 에서 SI 측정 미실시 (cells nn.Module branches arch 의 SI
   정의 모호) — *anima_chat 의 cell_pool 에서 SI 어떻게 측정* 하는지 Phase 1 spec
   확정 필요.
4. dropout 변경이 *런타임* 에 가능한지 (mitosis_hook 의 forward path 가 dropout 을
   constant 로 컴파일했다면 불가) — D4a impl 확인 의무.
5. PSCC §44/§47-49/§52 의 6-PSCC silent-drop ledger 와 별개로, **본 도구가 ON 일 때의
   F-PERSONA-4 category routing 신호** 는 §52 v7 KL=3.45 z=2.75 (v6 cell-parallel
   재현 실패 carry) 의 *동일* fragile signal 가능성 — 도구의 *효과* 검증은 SAVANT.md
   §10.1 trail 의 (ii-b) v6.1 결과와 동기화.

---

## §5 Cross-link

- `SAVANT.md` — 이론 + base-rate audit + §12 봉쇄심화 (parent)
- `CHAT.md` — anima mission tracker (production CLI 통합 host)
- `tool/hexa_native/mitosis_hook.hexa` — substrate state impl (overlay 대상)
- `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` — D4c CLI design
- `state/savant_containment_audit_2026_05_14/audit.json` — Tier 분류 evidence
- `dancinlab/canon/LATTICE_POLICY.md §1.4` — cross-repo governance

---

— SAVANT-TOOL.md, 2026-05-14, design tier LANDED, anima 가 직접 ON/OFF 하는 savant 도구
