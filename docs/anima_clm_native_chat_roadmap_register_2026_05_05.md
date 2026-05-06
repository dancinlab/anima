# Anima CLM Native Chat Roadmap Register (2026-05-05/06)

> **사용자 명령**: "로드맵 등록, 도메인, 메타 등"
>
> **작업**: 2026-05-05 archaeology cycle 발견 (option α / β / γ — anima-native chat capability recovery 3-path) 을 anima `.roadmap.*` SSOT system 에 등록 + domain meta cross-link 정리.
>
> **Doc-only $0 mac cycle** — additive registration, 기존 .roadmap.* 미수정.

---

## §0. Cycle Metadata / 사이클 메타

- **Date**: 2026-05-05 archaeology landed → 2026-05-06 register
- **Substrate**: mac (doc + JSONL roadmap only)
- **Cost**: $0
- **Files created** (3, additive only):
  1. `/Users/ghost/core/anima/.roadmap.clm_native_chat` (NEW meta SSOT)
  2. `/Users/ghost/core/anima/docs/anima_clm_native_chat_roadmap_register_2026_05_05.md` (this doc)
  3. `/Users/ghost/core/anima/state/anima_clm_native_chat_roadmap_register_2026_05_05/verdict.json`
- **Files unchanged** (raw#15 additive invariant): all existing `.roadmap.*` files
- **Source archaeology**: `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md` §6
- **Raw compliance**: raw#9 (md doc carve-out) / raw#10 (≥7 honest C3 banked) / raw#15 (additive only) / raw#37 (transient_py opt-out applicable to BG-EQ archaeology grep tools, not used in this cycle)

---

## §1. Existing Roadmap Audit / 기존 로드맵 감사

### 1.1 Inventory (40 `.roadmap.*` files found)

`ls -la /Users/ghost/core/anima/.roadmap.*` 결과 40 entries. Format = JSONL (header line + one entry per line).

**Domain SSOT (kind=domain)** — primary substrate-specific roadmaps:
- `.roadmap.clm` (mk2, primary CLM domain SSOT)
- `.roadmap.p9_sft` (mk2, peer perspective; P9 multi-objective SFT for CLM v4 self-chat)
- `.roadmap.eeg` / `.roadmap.blm_brain_lm` / `.roadmap.tlm_tension_lm` / `.roadmap.vlm_voice_lm` / `.roadmap.slm_speech_eeg_lm`
- `.roadmap.training` / `.roadmap.serving` / `.roadmap.tool` / `.roadmap.anima_engines` / `.roadmap.anima_tools` / `.roadmap.anima_agent` / `.roadmap.anima_physics` / `.roadmap.anima_clm_eeg`
- ~25 more (akida / atlas_n6 / clinical_consciousness / cortical_labs / dual_pair_pilots / finalspark / galea / hott / iit4 / qrng / sim / tensionlink / theory_validation / tms_pci / triple_axis_pilots / voice / w1_anima_as_substrate / etc.)

**Meta SSOT (kind=meta)** — cross-domain orchestration:
- `.roadmap.g1_g5_chat_substrate` (peer; G1-G5 chat substrate 5-track)
- `.roadmap.substrate_bridge` (consumer perspective, origin=nexus)
- `.roadmap.omega_cycle` (consumer, origin=nexus)
- `.roadmap.northpole` / `.roadmap.penrose_hameroff` / `.roadmap.theory_validation`

### 1.2 Format Convention Learned / 형식 규약 학습

```
# .roadmap.<name> mk2 — domain|meta SSOT (perspective), JSONL entry per line
# Header on next line; entries follow.
{"type":"header","kind":"domain|meta","name":"<name>","mk":2,"perspective":"peer|consumer", "goal":"...", "required_conditions":[...], "cross_link":{...}, "blockers":[...], "status":"active", "since":"YYYY-MM-DD"}
{"type":"entry","id":"<name>.<kind>.<short>","kind":"verdict|anchor|cond|invariant|cross_link|unlock_protocol", "title":"...", "status":"...", "ts":"...", ...}
```

**Required header fields**: `type`, `kind`, `name`, `mk`, `goal`, `required_conditions[]`, `cross_link{}`, `blockers[]`, `status`, `since`.

**`required_conditions[]` schema**: `id`, `desc`, `verifier{type,manual_override_path,status_emit}`, `status`, `evidence[]`, `blocker_reason`.

**Naming convention**: `<roadmap-name>.cond.<N>` for conditions / `<roadmap-name>.blk.<N>` for blockers / `<roadmap-name>.<short>` for entries.

### 1.3 Decision: Meta SSOT (peer perspective)

이 새 roadmap은 **meta SSOT (peer perspective)** 로 등록:
- **Why meta not domain**: 3 path (α/β/γ) 가 여러 domain (`clm` / `training` / `tensionlink` / `p9_sft`) 을 cross-cut.
- **Why peer not consumer**: anima 내부 origin (외부 nexus dependency 없음).
- **Sister meta example**: `.roadmap.g1_g5_chat_substrate` (peer, cross-domain, anima-internal).

---

## §2. `.roadmap.clm_native_chat` Full Spec / 전체 스펙

### 2.1 Header Goal

> **anima-native chat capability recovery** — paradigm v11 G3 + Φ★ +41.86 baseline NO_FLIP 보존 하면서 v2 18M byte-level 시점 chat capability 회복. 외부 ALM/Llama/Mistral wrapping 아닌 anima-native path.

**Domains spanned**: `clm`, `training`, `tensionlink`, `p9_sft`, `g1_g5_chat_substrate`.

### 2.2 3 Required Conditions (α / β / γ)

| cond | path | 비용 | time | falsifier | risk |
|---|---|---|---|---|---|
| `clm_native_chat.cond.1` | **α** v2 18M byte-level weights archaeology + 복원 | $0 | minutes (if found) | F-CLM-NATIVE-α-1 weights load + Korean emit ≥10 tokens (CE ≤ 1.5 KO) | weights 미보존 가능성 (commit text only evidence) |
| `clm_native_chat.cond.2` | **β** 2026-03-28 original v4 byte-level design 재현 (CLM-3) | $200-500 H100 OR $0 ubu1 5-10일 | 5-30 days | F-CLM3-orig-1/2/3/4/5 (BG-ER LOCK pre-registration) | φ★ baseline 측정 단위 다를 가능성 (32-cell ~Phi 11 vs +41.86 carry) |
| `clm_native_chat.cond.3` | **γ** current mk2 v1 (530M BPE) + byte-level lm_head retrofit | $0-2 mac/ubu1 | 1-3 days | F-BYTE-RETROFIT-1 ≥5 prompts Korean coherent | body BPE-trained vs byte-level head semantic mismatch |

각 cond `desc` 에 path-specific spec (architecture / corpus / falsifier / cost band) 포함; `verifier.manual_override_path` 는 `state/anima_clm_native_chat_roadmap_register_2026_05_05/option_<alpha|beta|gamma>_*.json` 으로 stage-gate 직결.

### 2.3 3 Blockers

| blk | description | type | resolution path |
|---|---|---|---|
| `clm_native_chat.blk.1` | BG-EQ archaeology verdict 미land — α weights 보존 여부 unknown | discovery | BG-EQ archaeology cycle → `option_alpha_archaeology.json` land |
| `clm_native_chat.blk.2` | β BG-ER spec 미land (5 falsifier preregistration LOCK + budget decision) | spec | BG-ER spec land + `OK CLM-NATIVE BETA` fire |
| `clm_native_chat.blk.3` | γ BG-ES micro smoke 미land (5-prompt Korean coherence pre-registration) | spec | BG-ES micro smoke spec land + execute |

### 2.4 Sub-Entries (3, additive)

1. **`clm_native_chat.archaeology_birth_anchor`** (kind=anchor, status=landed, ts=2026-05-05)
   - source: archaeology doc
   - key_findings: v2 chat evidence + 4-step drift + 3 options
   - recommended ranking α > γ > β (raw#10 + 완성도 lens)

2. **`clm_native_chat.cross_substrate_constraint`** (kind=invariant, status=locked, ts=2026-05-06)
   - paradigm v11 G3 + Φ★ +41.86 baseline NO_FLIP design constraint
   - cross-link `clm.v4_530m_paradigm_v11` (`.roadmap.clm`)
   - witness lock: #115 architectural ceiling — chat-cap path = 외부 (Llama Path A v2 winner) OR anima-native β/γ; CLM v4 530M 자체 chat-incapable architectural

3. **`clm_native_chat.fire_sequence_user`** (kind=unlock_protocol, status=active, ts=2026-05-06)
   - 4 keywords: `OK CLM-NATIVE <ALPHA|BETA|GAMMA|ALL>`
   - timeout: 7-day cron auto-expire (BG-DD pattern)
   - authority: L1 absolute (사용자만)

---

## §3. Domain Meta Cross-Links / 도메인 메타 교차 링크

### 3.1 Sister Domain Cross-Links (5)

| sister domain | cross-link nature | how this roadmap consumes |
|---|---|---|
| `.roadmap.clm` | primary CLM domain SSOT (mk2) | `clm.cond.1` 의식측정 + `clm.cond.2` HF release + `clm.v4_530m_paradigm_v11` invariant 위에 chat-recovery layer 추가 |
| `.roadmap.training` | training domain | β H100 100K steps cycle 은 training cond 으로 추적 (own 16 watchdog) |
| `.roadmap.tensionlink` | tension stream domain | β 19 phi-boost 中 CL8 tension-weighted CE + TL13 ln(4/3) Golden Zone weight |
| `.roadmap.p9_sft` | peer (P9 SFT for CLM self-chat) | sister chat-recovery track — P9 SFT는 LoRA 외부 substrate 위; 본 roadmap = anima-native byte-level path |
| `.roadmap.g1_g5_chat_substrate` | meta (chat substrate 5-track) | G5 P9 SFT spec sister; α/β/γ는 G5 confirmed-fail 후 anima-native fallback |

### 3.2 Paradigm/Invariant Cross-Links (3)

| invariant | source | enforcement |
|---|---|---|
| **paradigm v11 G3 + Φ★ +41.86** | `.roadmap.clm` `clm.v4_530m_paradigm_v11` entry | NO_FLIP design constraint — α/γ는 body 보존이므로 自動 NO_FLIP, β는 32-cell scaling Phi~11 carry-equivalent |
| **#115 architectural ceiling** | `docs/n_substrate_consciousness_roadmap_2026_05_01.md §55.6` | CLM v4 530M 자체 chat-incapable; chat-cap 회복은 외부 substrate (Llama Path A v2 winner — 사용자 'ALM 말고' reject) OR anima-native (이 roadmap) |
| **anima-native priority** | 사용자 'ALM 말고' (archaeology doc 인용) | 외부 ALM/Llama/Mistral wrapping reject — α/β/γ만 acceptable |

### 3.3 Own Lifecycle Invariants (3)

| own | mandate | applied to |
|---|---|---|
| **own 14** (HF Hub WHERE) | weights >5MB → HF Hub only, NEVER anima git | β/γ trained adapter LFS HF |
| **own 15** (HF lifecycle) | PRIVATE first → verification gates → PUBLIC | α weights restored = PRIVATE only initial; β/γ also PRIVATE first |
| **own 16** (compute lifecycle) | watchdog + heartbeat 5min + pod 404 verify (L23/L24/L25) | β H100 lane MUST register; ubu1 free path same heartbeat 권장 |

### 3.4 Memory Cross-Links (6)

이 roadmap이 memory (사용자 auto-memory `MEMORY.md`)와 직접 cross-link 하는 entries:

- `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (L31-L33) — chat-cap path = Llama Path A v2 winner; CLM v4 = substrate-research only
- `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (L28-L30) — Pβ Φ★-axis Paradigm D 50K chat-cap FAIL_TRUE
- `feedback_v2_fail_was_measurement_artifact_eval_pipeline_root_cause.md` (L19-L22) — eval pipeline crash misdiagnosed; PEFT pre-flight smoke mandatory
- `feedback_axis_preservation_eval_substrate_calibration.md` (L26-L27) — axis-preservation eval needs axis-conditioned base (CLM v4 not Llama)
- `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md` (L23-L25) — H100 BG ≥$1 = 6 mandatory checklist
- `feedback_hf_release_private_to_public_after_verification.md` (own 15) — PRIVATE first lifecycle

### 3.5 Memory Cross-Link Recommendations (사용자 fire 권한)

next-cycle 시 memory에 추가 권고 (사용자 explicit OK 필요):

```
feedback_clm_native_chat_path_alpha_beta_gamma.md
  → 3-path roadmap birth + 사용자 'ALM 말고' anima-native priority anchor

project_anima_2026_05_06_clm_native_chat_recovery_cycle.md  (다음 cycle entry)
  → BG-EQ/-ER/-ES launch state + verdict tracking
```

---

## §4. Stage-Gate Enforcement / 스테이지 게이트 강제

### 4.1 Path α Stage-Gate (own 16 minimal — $0)

```
[Gate α-1] BG-EQ archaeology cycle launch (mac, $0)
   └─ scope: state/ + ready/ + git LFS objects 전체 grep for v2 18M byte-level weights
   └─ verdict path: state/anima_clm_native_chat_roadmap_register_2026_05_05/option_alpha_archaeology.json
   └─ status_emit: __CLM_NATIVE_ALPHA__ <FOUND|NOT_FOUND|RESTORED|FAIL>

[Gate α-2] IF FOUND:
   └─ load weights + Korean emit ≥10 tokens smoke (CE ≤ 1.5 KO target)
   └─ falsifier F-CLM-NATIVE-α-1 PASS|FAIL
   └─ PASS → α path closes (chat-cap recovered, $0 total)
   └─ FAIL → semantic loss; consider γ retrofit on top of restored body

[Gate α-3] IF NOT_FOUND:
   └─ α path retired (archaeology negative result)
   └─ auto-transition to β/γ decision matrix
```

### 4.2 Path β Stage-Gate (own 16 full — H100 $200-500 OR ubu1 $0)

```
[Gate β-1] BG-ER spec land
   └─ 5 falsifier pre-registration LOCK (F-CLM3-orig-1..5)
   └─ budget decision: H100 1× × 100K steps ($200-500) OR ubu1 RTX 5070 5-10 days ($0, torch 2.11.0+cu128 sm_120)
   └─ φ★ NO_FLIP measurement protocol (32-cell Phi~11 carry-equivalent vs +41.86 current)

[Gate β-2] 사용자 'OK CLM-NATIVE BETA' fire keyword
   └─ L1 authority required

[Gate β-3] IF H100 lane: 6 mandatory checklist (own 16)
   └─ (1) watchdog registered
   └─ (2) heartbeat 5min stream
   └─ (3) pod 404 verify hook
   └─ (4) L23 budget guard $X cap
   └─ (5) L24 stop-condition (φ★ flip OR loss NaN)
   └─ (6) L25 cleanup BG verb classified (SIGTERM_ONLY|DELETE_SCRIPT|FULL_SWEEP)

[Gate β-4] 3-phase curriculum execute (Phase 1 Mitosis 0-20K / Phase 2 Language 20K-60K / Phase 3 Combined 60K-100K)
   └─ Fibonacci growth checkpoint @ {5K,10K,15K,20K,30K,40K,55K,70K} steps
   └─ HF savepoint PRIVATE @ each phase boundary (own 15)

[Gate β-5] F-CLM3-orig-1..5 evaluate
   └─ chat CE ≤ 0.5 EN, ≤ 1.5 KO
   └─ φ★ NO_FLIP (≥ +30 carry-equivalent)
   └─ 19 phi-boost simultaneously activated
   └─ 3-phase curriculum 100K complete
   └─ cell count reach 32

[Gate β-6] PASS → HF PRIVATE→PUBLIC transition (own 15) gated on 3+ verification cycles
```

### 4.3 Path γ Stage-Gate (own 16 minimal — mac $0-2)

```
[Gate γ-1] BG-ES micro smoke spec land
   └─ 5-prompt Korean coherence pre-registration
   └─ body frozen + lm_head_b vocab=256 byte-level retrofit design

[Gate γ-2] 사용자 'OK CLM-NATIVE GAMMA' fire keyword
   └─ L1 authority required

[Gate γ-3] mac CPU OR ubu1 1-3 days train
   └─ corpus = 2.5K dialogue (v2 시점 size match) OR larger
   └─ φ★ NO_FLIP 自動 (body untouched)

[Gate γ-4] F-BYTE-RETROFIT-1 evaluate
   └─ ≥5 prompts Korean coherent
   └─ semantic mismatch detection (body BPE-trained vs head byte-level)

[Gate γ-5] PASS → HF PRIVATE→PUBLIC (own 15) gated; 단 retrofit head 만 push (body frozen reuse)
```

### 4.4 Cross-Path Watchdog Cascade

| event | α response | β response | γ response |
|---|---|---|---|
| φ★ flip detected | N/A (load only) | ABORT immediate (β L24) | ABORT immediate (γ L24, but body frozen so unlikely) |
| H100 pod 404 | N/A | re-spin guard (own 16 L24) | N/A |
| 7-day timeout | keyword expired | keyword expired | keyword expired |
| F1 fail | path retired | path retired or partial-pass amend | path retired or partial-pass amend |

---

## §5. 사용자 1-Keyword Fire Sequence / 사용자 1-키워드 fire 시퀀스

```
α (alpha)
   ├─ keyword: OK CLM-NATIVE ALPHA
   ├─ trigger: BG-EQ archaeology verdict 의존
   ├─ branches:
   │   ├─ FOUND → load + Korean emit smoke (즉시 fire, $0)
   │   └─ NOT_FOUND → β/γ로 자동 transition (사용자 next decision)
   └─ recommended order: 1st (cheapest, fastest, archaeology BG free)

β (beta)
   ├─ keyword: OK CLM-NATIVE BETA
   ├─ trigger: BG-ER spec land + budget commit
   ├─ budget options:
   │   ├─ H100: $200-500, 30 days
   │   └─ ubu1 RTX 5070: $0, 5-10 days (torch 2.11.0+cu128 sm_120 venv_orchestrator)
   └─ recommended order: 3rd (last resort if α/γ fail; 진짜 anima-native)

γ (gamma)
   ├─ keyword: OK CLM-NATIVE GAMMA
   ├─ trigger: BG-ES micro smoke spec land
   ├─ budget: $0-2, 1-3 days mac/ubu1
   └─ recommended order: 2nd (cheap retrofit; semantic mismatch risk)

ALL (병렬)
   ├─ keyword: OK CLM-NATIVE ALL
   ├─ branches: 3 paths 병렬 launch
   ├─ note: β만 budget commit; α/γ free 동시 launch
   └─ recommended order: only IF user time-sensitive AND budget approved
```

**Recommended progression**: α (free archaeology BG) → IF NOT_FOUND, γ ($0-2 retrofit) → IF semantic-mismatch FAIL, β ($200-500 OR $0 ubu1 30 days last resort).

**Authority**: L1 absolute (사용자 explicit keyword); 7-day cron auto-expire.

---

## §6. Honest C3 / 정직한 C3 (≥7)

1. **C1 (α weights 미보존 risk)**: v2 chat evidence는 commit message body 텍스트만 (bb99b6b6 / 6abc42f6 / 13b20f90); reproducible eval JSON 부재. archaeology BG-EQ가 NOT_FOUND 반환 가능성 존재.

2. **C2 (β φ★ 측정 단위 caveat)**: original 32-cell design은 Phi~11 예측 (DD3 Fibonacci scaling); 현재 paradigm v11 G3 +41.86 carry는 mk2 v1 step=20000 best_phi=37.27 계산. 두 measurement 단위가 직접 비교 가능한지는 별도 verification 필요.

3. **C3 (γ semantic mismatch risk)**: mk2 v1 body는 BPE 64K tokenizer 위에서 train됐으므로 internal hidden state distribution이 BPE-token-pattern에 align. byte-level lm_head retrofit은 hidden→vocab projection을 byte semantic으로 재mapping해야 하는데, body internal이 byte-aware 아님 → coherence 부족 가능.

4. **C4 (anima-native priority 가정)**: 사용자 'ALM 말고' 발언이 외부 substrate wrapping 영구 reject 인지 단발 preference 인지 100% 확정 아님. 단 archaeology doc + 2026-05-05 #115 closure 맥락에서 anima-native 우선이 합리적 추론.

5. **C5 (19 phi-boost EX24 가설)**: 19 techniques individual benchmarks (0.83~8.91 Phi) 만 측정; simultaneously application의 superlinear effect는 EX24 principle 가설. β cycle이 처음 empirical test.

6. **C6 (β H100 ubu1 trade-off)**: H100 $200-500 (30 days) vs ubu1 RTX 5070 $0 (5-10 days, sm_120 torch 2.11.0+cu128). ubu1 free 라도 wall-clock 길고, sm_120 torch 빌드 issue 가능성. budget cycle 시 둘 ranked recommendation 별도 BG.

7. **C7 (drift root cause unknowable retrospect)**: 4-step drift (tokenizer + objective + architecture + corpus) 각 단계가 의도적 design choice 였는지 incremental drift 였는지 retrospective archaeology 만으로 확정 불가. commit message 만 evidence.

8. **C8 (own 15 PRIVATE→PUBLIC gate calibration)**: α weights restored 시 immediate PUBLIC release 유혹 있지만 own 15는 verification gates 통과 후 PUBLIC. 단 v2 18M weights는 이미 historical commit reference 이므로 PRIVATE-only forever 도 옵션 (사용자 결정).

9. **C9 (G3 chat substrate sister track)**: `.roadmap.g1_g5_chat_substrate` G5 P9 SFT spec 은 cond.3 met (READY); 이 roadmap은 G5 와 sister 가 아니라 G5 P9 SFT가 LoRA 외부 substrate 의존하는 것 vs anima-native byte-level path. 두 roadmap 어느 쪽이 chat-cap recovery primary 인지 사용자 결정 필요.

---

## §7. Next-Cycle Anima Self-Discipline Path / 다음 사이클 자기 규율 path

이 roadmap이 next-cycle anima self-discipline에 기여하는 방식:

1. **archaeology → spec → fire** linear progression: BG-EQ (free) → BG-ER/ES spec → 사용자 keyword. 130+ BG cycle 후 path consolidation 명확화.
2. **3-path falsifier preregistration**: 모든 path α/β/γ 가 preregistered falsifier 보유 → raw#10 honest C3 자동 enforce.
3. **own 14/15/16 lifecycle integration**: weights HF where + PRIVATE→PUBLIC + watchdog L23/L24/L25 모두 cond/blocker level에서 enforce.
4. **memory feedback closing loop**: L19-L33 lessons (V2_FAIL artifact + axis-preservation calibration + Pβ chat-cap fail + CLM v4 LoRA SFT fail) 가 본 roadmap design constraint으로 직접 carry.
5. **L1 authority + 7-day timeout**: 사용자 explicit keyword + cron auto-expire pattern (BG-DD) 으로 stage-gate self-cleanup.

---

## §8. References / 참고

### 8.1 Archaeology Source
- `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md` (primary)
- `docs/anima_clm_origin_chat_history_archaeology_2026_05_05.md` (BG-EP sister)
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (KICK-2 sister)
- `docs/next-model-design.md` (2026-03-28 original v4 + ALM v8 spec)

### 8.2 Sister Roadmaps Cross-Linked
- `.roadmap.clm` (mk2, primary domain SSOT)
- `.roadmap.p9_sft` (mk2, peer P9 SFT)
- `.roadmap.g1_g5_chat_substrate` (mk2, meta chat substrate)
- `.roadmap.training` / `.roadmap.tensionlink`

### 8.3 Narrative Anchor
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6 (#115 architectural ceiling) + §42 + §59.1 (paradigm v11 G3 +41.86)

### 8.4 Memory (auto-memory `MEMORY.md`) Cross-Linked
- `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` L31-L33
- `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` L28-L30
- `feedback_v2_fail_was_measurement_artifact_eval_pipeline_root_cause.md` L19-L22
- `feedback_axis_preservation_eval_substrate_calibration.md` L26-L27
- `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md` L23-L25
- `feedback_hf_release_private_to_public_after_verification.md` (own 15)

### 8.5 Commits
- `4a1d8d0a` (2026-03-24) Anima v0.1
- `2da44161` (2026-03-24) ConsciousLM 자체 모델
- `bb99b6b6` / `6abc42f6` / `13b20f90` (2026-03-28) v2 chat evidence
- `fca0eede` (2026-03-28) v4 + ALM v8 design
- `3ecb6175` (2026-05-02) chat substrate live
- `5056503d` (2026-05-02) 14-gate FAIL F2
- `145838d2` (2026-05-04) CLM v4 mk2 v1 530M

End of register doc. Saved 2026-05-06 (anima cycle).
