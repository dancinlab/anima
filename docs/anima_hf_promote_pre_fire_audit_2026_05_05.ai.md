# anima HF promote pre-fire audit (2026-05-05)

**Audit ID**: BG-DB-HF-PROMOTE-PRE-FIRE-AUDIT-2026-05-05
**Audit UTC**: 2026-05-05T18:20:17Z
**Scope**: Verify auto-fire scripts + HF state + confirm-strings before user fires PUBLIC promotes after time-gated review windows.
**Reference baseline**: `state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json` (BG-E, 2026-05-05T13:00:00Z)
**Fire mode**: $0 mac doc-only — actual fire EXCLUDED from this audit.
**Constraints**: raw#9 + raw#10 honest C3 + raw#15 no-promote-script-mutation; HF token redacted.

---

## §1 Time-gate countdown

Reference NOW_UTC = `2026-05-05T18:20:17Z`.

| Window | Eligible after (UTC) | T-minus | Status |
|---|---|---|---|
| clm fire | 2026-05-06T23:26:12Z | T-29.10h | NOT_YET (gated) |
| Pβ fire | 2026-05-07T03:48:00Z | T-33.46h | NOT_YET (gated) |
| clm cleanup (24h grace after PUBLIC) | 2026-05-07T23:26:12Z | T-53.10h | NOT_YET |
| Pβ cleanup (24h grace after PUBLIC) | 2026-05-08T03:48:00Z | T-57.46h | NOT_YET |

Both promote windows currently in DWELL phase. T+0 from BG-E baseline ≈ +5.5h elapsed.

---

## §2 HF state pre-check (sha + private + siblings)

Live curl against HF API at audit time:

| Repo | sha (live) | private | siblings | lastModified | vs BG-E |
|---|---|---|---|---|---|
| `dancinlab/clm-v4-mk2-v1` | `80440a1d38db9addc4445bb959057558a57f4230` | True | 16 | 2026-05-04T23:26:12Z | MATCH |
| `dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1` | `7643e764488f8e11020a7663c50f2e590b70d10f` | True | 6 | 2026-05-05T03:44:35Z | MATCH |

**Verdict §2**: PASS — both repos sha + private + siblings + lastModified identical to BG-E 13:00Z snapshot. No silent HF-side mutation during dwell.

### §2.1 Local script SHA256 (re-shasum vs BG-E baseline)

| Path | sha256 (now) | BG-E baseline | Match |
|---|---|---|---|
| `state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash` | `f1933930c4b671e030fa4323044141c73c5466355ad7dc3ea8c08cd7bd35f5e8` | same | YES |
| `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash` | `c0e83446ddba2438ad3bf411074402c1a507ba89f749f7e77a555aebeb115d66` | same | YES |
| `state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash` | `d6c736e4cb6f9934d23f0509ec9bc55866f7f8dffd69b427cf8894344a362d8d` | same | YES |
| `state/p9_pbeta_hf_upload_2026_05_05/cleanup_pbeta_2026_05_08.bash` | `3e00113df8e1be35bc4bf3e0c620d412e92ef58baaf932d0369b6960dba4dab9` | same | YES |
| `state/anima_hf_promotes_2026_05_06_auto_fire.bash` | `440c85f4a0abbd508fa3561fcd3c18ad87cb809c4c925b7264832979a7755a9b` | same | YES |
| `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` | `9646dc4d7793fef9c2468b9e2c9c4f0663931a393f198c9ce7380f7b568d06e8` | same | YES |

**Verdict §2.1**: PASS — 6/6 local script SHA256s match BG-E baseline. raw#15 no-mutation invariant satisfied during 5.5h dwell.

---

## §3 --check-only dry-run

Command:
```
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --check-only
```

Output (head-40):
```
===============================
  anima HF promote auto-fire
===============================
Now UTC:               2026-05-05T18:20:17Z
clm window ends:       2026-05-06T23:26:12Z
pbeta window ends:     2026-05-07T03:48:00Z
clm fire-able now:     NO
pbeta fire-able now:   NO
===============================

Mode: check-only. NO fire.

=== clm cleanup dry-run (head -10) ===
[promote    ] starting public promote pre-check at 2026-05-05T18:20:17Z
[promote ERR] GATE 1 FAIL: review window not yet elapsed (now 2026-05-05T18:20:17Z < ends 2026-05-06T23:26:12Z)

=== pbeta promote dry-run (head -10) ===
[promote    ] starting public promote pre-check at 2026-05-05T18:20:17Z
[promote ERR] GATE 1 FAIL: review window not yet elapsed (now 2026-05-05T18:20:17Z < ends 2026-05-07T03:48:00Z)
```

**Interpretation**: GATE 1 (review-window elapsed) correctly FAILS; both promotes blocked. `clm_fire_able`/`pbeta_fire_able` evaluated to NO via bash string-compare (`[[ NOW > END ]]` short-circuits). G2 (siblings/sha) + G3 (privacy flip) not exercised because G1 short-circuits — expected behavior.

**Verdict §3**: PASS — gate enforcement working; no premature fire path reachable.

---

## §4 User fire commands (verified)

Confirm-strings extracted by direct grep against `read -rp` lines:

- `state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash:114` → `'PROMOTE-clm-v4-mk2-v1'`
- `state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash:115` → `'PROMOTE-pbeta-50k'`

Both match BG-E sub5 record. **No placeholder remains** — `PROMOTE-pbeta-50k` is the literal confirm-string.

### §4.1 Sequenced fire plan (4 user commands)

```bash
# (1) T+0 after 2026-05-06T23:26:12Z — clm window close
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-clm
# confirm prompt: PROMOTE-clm-v4-mk2-v1

# (2) T+0 after 2026-05-07T03:48:00Z — Pβ window close (must be AFTER step 1 succeeds → PEFT base PUBLIC)
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-pbeta
# confirm prompt: PROMOTE-pbeta-50k

# (3) >= 2026-05-07T23:26:12Z — clm cleanup (24h grace after step 1)
bash /Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash --fire-clm

# (4) >= 2026-05-08T03:48:00Z — Pβ cleanup (24h grace after step 2)
bash /Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash --fire-pbeta
```

Alternative collapsed paths (operator discretion):
- `--fire-all` on promotes script: sequential clm→Pβ with 5s spacer; aborts Pβ if clm fails (script line 95–97).
- `fire-all` on cleanups script: sequential cleanup with 5s spacer.

**Sequencing invariant**: Pβ is PEFT-loaded against clm-v4-mk2-v1 base → step (2) MUST follow successful step (1), else non-auth readers cannot resolve the base.

**Verdict §4**: PASS — 4 commands literal-verified against case statements + read prompts; no escaping/quoting risk.

---

## §5 Honest C3 (5 caveats)

1. **C1 — HF token rotation risk during 29-58h dwell.** The `--fire-*` commands invoke `hf` CLI internally; if the user rotates `huggingface.token` via `secret set` between now and T+58h cleanup, the promote/cleanup will fail at HF API auth. Mitigation: re-verify token freshness `secret get huggingface.token` at fire-time + check HF whoami before typing confirm-string. (No automated re-check inside the bash scripts — this is operator-side discipline.)

2. **C2 — Auto-fire scripts STILL UNTRACKED in git** (?? status carried from BG-E sub4). 5.5h dwell elapsed since BG-E flagged this, no commit yet. SHA256 match in §2.1 confirms no mutation during 5.5h, but git-untracked status means a stray `rm` or filesystem mishap would lose them silently. Mitigation: commit before sleep tonight, or re-run §2.1 SHA256 diff at fire-time.

3. **C3 — Pβ fire-eligibility decoupled from clm public success.** The `--fire-pbeta` mode only checks `pbeta_fire_able` (T-window), NOT whether clm PUBLIC promote actually succeeded. If user runs (2) without running (1) first, Pβ script's GATE-base-public check (inside `public_promote_pbeta_2026_05_08.bash`) is the sole guard. Operator should manually verify clm public state on HF UI between (1) and (2). `--fire-all` mode handles this via line 95 abort, but `--fire-pbeta` standalone does not.

4. **C4 — GATE 2 (HF-side sha + siblings) is fire-time check, not dwell-time.** During the 29-33h remaining dwell, no automated mutation alarm exists. Re-run §2 HF state pre-check + §2.1 local SHA256 at T-1h to T-0h before fire to catch silent mutations. BG-E's recommendation stands: re-shasum + diff at fire-time.

5. **C5 — uchg/chflags formally deprecated 2026-04-22.** No filesystem-level lock on promote scripts during dwell; mutation detection relies entirely on (a) git status + (b) SHA256 baseline diff. Both work, but neither blocks active mutation — they only detect after-the-fact. Acceptable per anima's post-uchg posture, but operator should not assume scripts are immutable.

---

## Overall verdict

**PASS** — auto-fire infrastructure remains intact 5.5h after BG-E baseline. All 6/6 local SHA256 match, both HF repos (sha + private + siblings + lastModified) match, GATE 1 enforcement verified via dry-run, both confirm-strings literal-verified.

**Recommended pre-fire ritual (operator)**:
1. Re-run §2 HF state pre-check curl at T-1h to T-0h.
2. Re-run §2.1 local SHA256 + diff vs this verdict.
3. Verify `secret get huggingface.token` non-empty + `hf whoami` returns expected account.
4. Type confirm-string EXACTLY: `PROMOTE-clm-v4-mk2-v1` then `PROMOTE-pbeta-50k`.
5. After clm PUBLIC, manually verify on HF UI before firing Pβ.
6. Wait 24h before each cleanup (consumer download grace).
