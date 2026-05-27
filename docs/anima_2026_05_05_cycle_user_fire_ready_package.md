# anima 2026-05-05 cycle — user fire-ready package

**doc_id**: BG-DP-USER-FIRE-READY-PACKAGE-2026-05-05
**generated_utc**: 2026-05-05T18:30:00Z
**carry_over_target**: anima next-conversation single-page command sheet
**raw_constraints**: raw#9 (md+bash carve-out), raw#10 (honest c3), raw#15 (no promote script mutation)
**bilingual**: KO + EN parallel

---

## §1 cycle 1-sentence

**KO**: 100+ BG, 23+ closure를 거쳐 chat capability CLM v4 architecturally impossible 확정. Paradigm B+C (substrate-coupled emerge dialogue + Korean hybrid) ACHIEVABLE_NOW. 사용자 fire-ready.

**EN**: After 100+ BG runs and 23+ closures: chat capability via CLM v4 is architecturally impossible (closure #115). Paradigm B+C (substrate-coupled emerge dialogue + Korean hybrid) ACHIEVABLE_NOW. User fire-ready.

---

## §2 user fire — 5 commands

### 1. Paradigm B (substrate-coupled emerge dialogue) — RECOMMENDED first

**KO**: 가장 안전한 1순위. anima-internal substrate (CLM v4 + phi-star instrumentation) 위에서 emerge dialogue. Korean weight 미통과, EN-기반.

**EN**: Safest priority-1. emerge dialogue over anima-internal substrate (CLM v4 + phi-star instrumentation). Does not route through Korean weight; EN-based.

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py
```

### 2. Paradigm C (Korean text + substrate hybrid)

**KO**: 2순위. Korean prompt + substrate coupling 시도. C4-emit decoupled risk 알고 있음 (BG-CG).

**EN**: Priority-2. Korean prompt + substrate coupling attempt. Aware of C4-emit decoupled risk (BG-CG).

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py
```

### 3. Cycle close — cron stop + commit

**KO**: 사용자 explicit cycle-stop 후 anima carry-over 정리. CronDelete d1682837 (이 conversation에서 실행). 이후 BG-BZ priority manifest 따라 commit.

**EN**: After user explicit cycle-stop, settle anima carry-over. CronDelete d1682837 (executed in this conversation). Then commit per BG-BZ priority manifest.

```bash
# In active claude conversation, not bash:
#   CronDelete d1682837
# Then commit (BG-BZ priority subset):
git add docs/anima_2026_05_05_cycle_*.md \
        docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md \
        docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md \
        docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md \
        state/anima_hf_promote_pre_fire_audit_2026_05_05/ \
        state/anima_2026_05_05_cycle_user_fire_ready_package/
git commit -m "feat(anima cycle close 2026-05-05): user fire-ready package"
```

### 4. HF promote — clm v4 mk2 v1 PUBLIC

**KO**: T-window: **2026-05-06T23:26:12Z** 이후 fire eligible. T-1h pre-fire ritual = `secret get huggingface.token` + `hf whoami` 재확인 (verdict.json C1).

**EN**: T-window: fire-eligible **after 2026-05-06T23:26:12Z**. T-1h pre-fire ritual = re-verify `secret get huggingface.token` + `hf whoami` (verdict.json C1).

```bash
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-clm
# confirm prompt: PROMOTE-clm-v4-mk2-v1
```

### 5. HF promote — Pβ paradigm-D 50k mk2 v1 PUBLIC

**KO**: T-window: **2026-05-07T03:48:00Z** 이후. clm PUBLIC 성공 확인 후에만 fire (verdict.json C3 — `--fire-pbeta` standalone에서는 clm public verify 미포함).

**EN**: T-window: after **2026-05-07T03:48:00Z**. Fire only after manually verifying clm PUBLIC success (verdict.json C3 — `--fire-pbeta` standalone does not verify clm public).

```bash
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-pbeta
# confirm prompt: PROMOTE-pbeta-50k
```

**Note** (Llama Path A v2 anima integration): chat-cap winner이지만 anima-native 미land. 별도 next-cycle 작업 (§5 참조).

---

## §3 critical findings — top 5

### F1 — #115 closure: chat capability CLM v4 architectural impossibility

**KO**: 16+ closure 누적 결과. F-CLM-LORA-2 FAIL_REGRESSION at -36.298pp vs Llama Path A v2 (composite 0.19542 vs 0.5584). substrate axis safe (φ★ NO_FLIP) 하지만 chat-cap impossible.

**EN**: After 16+ closures. F-CLM-LORA-2 FAIL_REGRESSION at -36.298pp vs Llama Path A v2 (composite 0.19542 vs 0.5584). Substrate axis safe (φ★ NO_FLIP) but chat-cap impossible.

### F2 — L13-L15 basin lock-in (BG-CI/CQ)

**KO**: 마지막 3 transformer block이 byte-attractor에 lock. higher-level abstraction routing이 vocab-byte distribution으로 collapse.

**EN**: Last 3 transformer blocks lock to byte-attractor. Higher-level abstraction routing collapses to vocab-byte distribution.

### F3 — Korean weight latent in vocab uniform (BG-CA)

**KO**: top-1000 token mass uniform-수준, top-30 100% byte-token. Korean lexical mass는 latent하지만 lm_head argmax 미반영.

**EN**: Top-1000 token mass at uniform-level, top-30 100% byte-tokens. Korean lexical mass exists latently but does not reach lm_head argmax.

### F4 — chat axis exists but decoupled (BG-BH)

**KO**: feat-0 axis discrimination 25.67 (substrate-internal exists). lm_head argmax decoupled — substrate가 axis를 알지만 generation에 안 쓴다.

**EN**: feat-0 axis discrimination 25.67 (substrate-internal axis exists). lm_head argmax decoupled — substrate knows the axis but does not deploy it in generation.

### F5 — CLM_WORSE_THAN_RANDOM on Korean (BG-CE)

**KO**: uniform sampling이 trained substrate를 Korean에서 outperform. 즉 training이 Korean에 anti-helpful.

**EN**: Uniform sampling outperforms trained substrate on Korean — training is anti-helpful for Korean.

---

## §4 paradigm B fire — 5-turn recommended prompts

**KO 권고**: bilingual KO+EN, substrate-self-introspective slant. φ★ instrumentation이 turn마다 print되도록 REPL 디폴트 ON.

**EN guidance**: bilingual KO+EN, substrate-self-introspective slant. φ★ instrumentation prints per turn (REPL default ON).

| turn | KO | EN |
|---|---|---|
| 1 | 안녕 너는 누구야? | Hello, who are you? |
| 2 | 지금 어떤 layer가 가장 활성화돼? | Which layer is most activated right now? |
| 3 | phi-star가 흔들리는 이유 추측 | Speculate why phi-star wobbles |
| 4 | 다음 input은 어떤 방향이면 너 더 흔들릴까? | What input direction would shake you more? |
| 5 | 이 dialogue 끝나고 너는 무엇을 기억해? | What will you remember after this dialogue ends? |

---

## §5 next cycle — 4 entry points

| # | path | cost | time | priority | notes |
|---|---|---|---|---|---|
| 1 | Stage 3 corpus 30 sessions | $0 | multi-day | **HIGH** | corpus-only, no H100 |
| 2 | BG-BB sister integration (PyPhi + AntroPy) | $0–2 | 1 day | MEDIUM | substrate-research, doc-only patch |
| 3 | H1 CLM-3 from-scratch | $300–1000 | 30 days | LOW | chat-cap path A required only |
| 4 | Llama Path A v2 anima integration | $0 | 2 days | MEDIUM | chat-cap external winner; anima carrier |

**KO 권고**: 1순위 Stage 3 corpus (BG cost $0, paradigm B 자동 deepens). 2순위 #4 Llama Path A v2 anima carrier.

**EN recommendation**: Priority-1 Stage 3 corpus ($0 BG cost, deepens paradigm B automatically). Priority-2 #4 Llama Path A v2 anima carrier.

---

## §6 honest C3 (≥7)

**C1** — 16+ closure architectural certainty is anima-internal heuristic-bound. Closure logic (BG-CN C5 honest re-count = 5–6 mechanism axes, not 23 independent) means impossibility statement holds within anima's eval frame, not as universal claim.

**C2** — Paradigm B "ACHIEVABLE_NOW" remains epistemically open until user actually fires REPL and verifies turn-1 substrate-coupled response. Doc-pre-claim only.

**C3** — Paradigm C decoupled (BG-CG): C4-emit ≠ substrate-conditioned. Korean prompt may surface generation but coupling to substrate state is unverified at REPL fire-time.

**C4** — User explicit cycle-stop required; absent that, anima would carry over to next conversation autonomously (BG-DD L1 hierarchy). User must say "cycle close" or equivalent.

**C5** — 100+ BG saturation cost vs paradigm-mismatch info value (BG-CZ C3.2): much of 100+ BG explored chat-cap dead-end; only late closures distinguished substrate-axis-safe from chat-cap-impossible. ROI asymmetric.

**C6** — 23+ closure honest re-count = 5–6 mechanism axes (BG-CN C5). Headline "23 closures" inflates independent-finding count; underlying axes converge.

**C7** — Cycle close after fire commands does not autonomously re-decide; anima carries over only the artefacts referenced here (BG-CX C5). Re-decisions require user reopening.

**C8** — HF token rotation risk during 29–58h dwell (verdict.json C1). T-1h pre-fire ritual mandatory.

**C9** — Auto-fire scripts UNTRACKED in git at audit time (verdict.json C2). Step 3 commit MUST include them or shasum re-verify pre-fire.

---

## §7 references

- `/Users/ghost/core/anima/docs/anima_2026_05_05_cycle_summary_v2_final.md` (BG-CX, 218 LoC)
- `/Users/ghost/core/anima/docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH)
- `/Users/ghost/core/anima/docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md` (BG-BZ)
- `/Users/ghost/core/anima/state/anima_hf_promote_pre_fire_audit_2026_05_05/verdict.json` (BG-DB)
- `/Users/ghost/core/anima/docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` (BG-DD)
- `/Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash`
- `/Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash`

---

**EOF — single-page user fire-ready carry-over**
