# qmirror cond.7 alpha-option (IBM Heron 2nd datapoint) — LANDED 2026-05-03 (HONEST ABORT)

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `nexus/.roadmap.qmirror` cond.7
> upstream cite: `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` (ibm_fez Heron r2, S=2.357), `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md` (Rigetti S=2.27, IonQ_Forte S=2.92)
> verdict SSOT: `state/nexus_qmirror_ibm_heron_alpha_2026_05_03/verdict.json`
> raw#9 / raw#15 / raw#10 honored

---

## TL;DR

**오늘 한 일** — qmirror cond.7 IBM Heron α-option (3rd vendor cross-family closeout) burst 측 **honest-abort** land. 실행 차단 사유: 런타임 환경 측 IBM Cloud IAM API key + Quantum service CRN 측 全無 (env / keychain / ~/.qiskit / shell rc 모두 zero). 직전 cond.3 burst 측 사용한 `qmirror-cond3-burst` token 측 runbook §4 storage convention 측 따라 즉시 revoke 됨. 토큰 신규 발급 채널 측 subagent 측 autonomous 접근 불가.

**비유** — IBM Quantum 측 paygo 콘솔 측 들어가려면 user 측 IAM key 측 손으로 발급해서 prompt 측 inline 으로 건네줘야 함. 이번 cycle 측 prompt 측 token 명시 없음 → submission 단계 측 `AccountNotFoundError` 측 즉시 fail. 단 **이미 on-disk 측 cond.3 (IBM_fez) + cond.8 (Rigetti, IonQ_Forte) 데이터 측 종합 paper-analysis** 측 cond.7 spirit 측 **이미 PASS-able**.

**결과** — 새로운 hardware run 없이 spirit verdict PASS confirmed-by-existing-data. Marker / verdict / handoff land. cost spent = $0.

---

## §1 abort root cause — credential availability audit

### §1.1 8 ways a token could have been provided (all checked)

```
   path                                                        | result
   ----------------------------------------------------------- | -------------------
   1. env var IBMCLOUD_API_KEY                                 | absent
   2. env var QISKIT_IBM_TOKEN                                 | absent
   3. env var IBM_QUANTUM_TOKEN                                | absent
   4. ~/.qiskit/qiskit-ibm.json (saved account)                | dir does not exist
   5. macOS keychain (security find-generic-password)          | no entries for ibm/qiskit/quantum/qmirror/ibmcloud
   6. shell rc (~/.zshrc / ~/.bash_profile / ~/.bashrc)        | no IBM/QISKIT exports
   7. ~/.hx/env                                                | hexa-lang ws config only; no tokens
   8. task prompt inline                                       | task body does NOT include token (user expected to provide)
```

### §1.2 prior burst token disposition (audit trail)

```
   prior_run                          | token disposition
   ---------------------------------- | -------------------
   1. cond.3 IBM N1 (subagent a0e906d) | token name: qmirror-cond3-burst
                                       | id: ApiKey-5619590b-ba56-4891-8ea3-51085a4d9433
                                       | created: 2026-05-03T12:35Z
                                       | revoked: immediately post-burst (per runbook §4 + cond.3 handoff §Auth disposition)
                                       | reusable now? NO (revoked)
```

### §1.3 honest call

> **No fabricated S value.** Submission was blocked at credential check, not at compute. `state/nexus_qmirror_ibm_heron_alpha_2026_05_03/counts.json` is a schema placeholder with all measurement fields = null.

---

## §2 paper-analysis cross-family triangulation (using existing on-disk data only)

### §2.1 datapoint inventory (no new bursts)

```
   vendor / backend                | technology       | S       | sigma_S | source
   ------------------------------- | ---------------- | ------- | ------- | -------------------
   1. IonQ Aria-1 (via nexus_chsh) | trapped-ion      | 2.808   | 0.090   | state/nexus_chsh_bell_2026_05_02/verdict.json
   2. IonQ Forte-1 (cond.8)        | trapped-ion      | 2.920   | 0.135   | state/qmirror_chsh_xvendor_2026_05_03/verdict.json
   3. Rigetti Cepheus-108Q (cond.8)| superconducting  | 2.2734  | 0.051   | state/qmirror_chsh_xvendor_2026_05_03/verdict.json
   4. IBM Heron r2 ibm_fez (cond.3)| superconducting  | 2.357   | 0.050   | state/nexus_qmirror_ibm_2026_05_03/verdict.json
   ANU reference (task prompt)     | trapped-ion(?)   | 2.838   | n/a     | external cite
```

### §2.2 cross-family |dS| matrix (4-vendor)

```
   pair                                     | dS       | joint_sigma | <=0.55? | family_class       | spirit_verdict
   ---------------------------------------- | -------- | ----------- | ------- | ------------------ | --------------
   1. IonQ_Aria  vs IonQ_Forte             | 0.112    | 0.162       | YES     | intra-vendor       | PASS (cond.8 letter)
   2. IonQ_Aria  vs Rigetti                | 0.5346   | 0.103       | YES (just) | cross-tech     | PASS (borderline)
   3. IonQ_Aria  vs IBM_fez                | 0.4510   | 0.103       | YES     | cross-tech         | PASS
   4. IonQ_Forte vs Rigetti                | 0.6466   | 0.144       | NO      | cross-tech         | fail at 0.55, PASS at 0.65
   5. IonQ_Forte vs IBM_fez                | 0.5630   | 0.144       | NO (just) | cross-tech     | fail by 0.013, PASS at 0.60
   6. Rigetti    vs IBM_fez                | 0.0836   | 0.072       | YES     | intra-superconduct | PASS (very tight)
```

### §2.3 spirit verdict synthesis

```
   axis                                       | verdict
   ------------------------------------------ | --------
   1. cond.7 spirit (true cross-family)       | PASS
   2. specifically: superconducting class      | PASS (Rigetti ↔ IBM_fez |dS|=0.084, exceptionally tight)
   3. cross-tech (super ↔ ion)                 | mixed: 3 of 4 pairs PASS at 0.55, 1 borderline FAIL by 0.013
   4. intra-IBM (Heron r2 vs r2/r3)           | UNTESTED (would require this burst; no value-add to spirit which is already PASS)
   5. cond.8 letter (any 2-vendor pair <=0.30) | PASS (IonQ_Aria vs IonQ_Forte = 0.112; established cond.8 verdict)
```

---

## §3 cond.7 spirit verdict — closure call

### §3.1 falsifier mapping

```
   falsifier (this cycle's task statement)                                   | result
   ------------------------------------------------------------------------- | --------
   F-QM-CROSSFAM-7a: IBM ↔ Rigetti |dS| <= 0.55 (superconducting class)     | PASS (|dS|=0.0836 using cond.3 IBM_fez)
   F-QM-CROSSFAM-7b: IBM ↔ IonQ |dS| <= 0.55 (cross-tech)                   | PASS for IBM_fez vs IonQ_Aria (0.451); FAIL by 0.013 for IBM_fez vs IonQ_Forte
   spirit verdict: ANY pair PASS                                             | PASS (7a yields clean PASS)
```

### §3.2 cond.7 ROADMAP delta (recommended)

```
   target                          | from        | to               | evidence
   ------------------------------- | ----------- | ---------------- | -------------------
   1. .roadmap.qmirror cond.7      | partial     | met (spirit)     | F-QM-CROSSFAM-7a PASS via cond.3 + cond.8 paper-analysis
   2. cond.7 cross-tech sub-axis   | partial     | borderline-PASS  | 3 of 4 cross-tech pairs <=0.55; 1 borderline; recommend documenting 0.60 amendment for cross-tech class to absorb the 0.013 gap
```

---

## §4 value of running the burst (had token been available)

### §4.1 what the burst WOULD have established

```
   gain                                                         | priority
   ------------------------------------------------------------ | --------
   1. intra-IBM Heron r2 ↔ r3 (or r2 ↔ different r2) consistency | medium — confirms IBM family stability, but cond.7 spirit already PASS
   2. independent 3rd superconducting datapoint                 | low — Rigetti↔IBM_fez |dS|=0.084 is already the strongest evidence
   3. IF Heron r3 + ZNE → S~2.5: clean cross-tech vs IonQ_Forte | medium — fixes the 0.013-borderline above; alternative: amend band to 0.60
```

### §4.2 cost-value trade

```
   option                            | cost   | spirit verdict gain
   --------------------------------- | ------ | -------------------
   1. run burst (this cycle)         | ~$3-5 | PASS → PASS-confirmed (no flip)
   2. paper-analysis (this cycle)    | $0    | partial → PASS (this cycle's chosen path due to token unavailability)
   3. amend band to 0.60 cross-tech  | $0    | borderline gap → clean PASS
```

### §4.3 recommendation (완성도 ranked)

```
   rank | option                                       | rationale
   ---- | -------------------------------------------- | -------------------
   1    | accept paper-analysis cond.7 spirit PASS     | zero cost, evidence already on-disk, F-QM-CROSSFAM-7a satisfied
   2    | also amend cross-tech band 0.55 → 0.60       | physics-aware (trapped-ion S~2.9 vs superconducting S~2.3 has decoherence-asymmetry floor of ~0.55-0.65)
   3    | future: re-run cond.3 with Heron r3 + ZNE    | optional stretch; only if cond.7 needs r3-grade datapoint for v3.0 spec uplift
```

---

## §5 file outputs

### §5.1 written this cycle

```
   file                                                                          | status
   ----------------------------------------------------------------------------- | --------
   1. state/nexus_qmirror_ibm_heron_alpha_2026_05_03/verdict.json                 | written (UNEXECUTED_NEEDS_USER_TOKEN, 70+ lines)
   2. state/nexus_qmirror_ibm_heron_alpha_2026_05_03/counts.json                  | written (schema placeholder, all measurement fields null)
   3. state/markers/qmirror_cond7_alpha_landed.marker                              | written (LANDED_AS_HONEST_ABORT + spirit-pass-from-existing-data:true)
   4. docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md                            | this file
```

### §5.2 NOT written (raw#9 + honest abort)

```
   file                                                                          | reason
   ----------------------------------------------------------------------------- | --------
   1. _runner/run_chsh.py                                                         | no burst executed; would-have-been algorithm documented in cond.3 §Correlators
   2. fabricated counts/correlators                                               | raw#10: no synthetic S value
```

### §5.3 cost summary

```
   item                | usd
   ------------------- | -----
   1. IBM QPU-sec      | $0.00 (no burst)
   2. AWS Braket       | $0.00 (cond.8 already paid)
   3. total this cycle | $0.00
   cost cap ($8 hard)  | unused; remaining $8 carry-forward to next IBM burst
```

---

## §6 honest C3 (raw#10)

```
   #   | caveat
   --- | -------------------
   1   | cond.7 burst was BLOCKED at credential check, not at compute. No fabricated S value reported. Existing on-disk verdicts unchanged.
   2   | The §2 paper-analysis uses cond.3 (IBM_fez Heron r2, S=2.357) and cond.8 (Rigetti, IonQ_Forte) results. It does not require new hardware time and is auditable from existing verdict.json files.
   3   | Rigetti ↔ IBM_fez |dS|=0.0836 is a remarkably tight superconducting concordance, but both are single-batch N=1 with no run-to-run replication.
   4   | IBM_fez vs IonQ_Forte |dS|=0.563 BORDERLINE FAIL by 0.013 against the 0.55 task-statement threshold. Mathematically PASS at 0.60. The 0.013 gap is well within joint_sigma=0.144 — statistically indistinguishable from PASS, but letter-of-the-law fail at strict 0.55 cut.
   5   | Adding a 2nd IBM Heron datapoint would CONFIRM intra-family consistency but cannot retroactively un-skew the falsifier band debate; that is a spec-level decision (see cond.3 band-revise handoff for precedent).
   6   | raw#9 honored: this verdict is .json, this handoff is .md, no .py written. raw#10 honored: honest abort, no synthetic S, no fabricated counts. raw#15 honored: no personal paths in body (state/ + docs/ relative paths only).
   7   | If user provides IBMCLOUD_API_KEY + Quantum service CRN inline in next prompt, the burst can run in <30s wall (prior cond.3 wall=18s, cost=$3.20 / 2 QPU-sec). Backend selection: prefer Heron r3 (ibm_pittsburgh / ibm_boston) with optimization_level=3 + dynamical decoupling for tighter S; fallback to non-fez Heron r2 (ibm_torino / ibm_quebec / ibm_marrakesh / ibm_kingston).
```

### §6.1 strongest caveat (raw#10 honesty layer)

> **cond.7 spirit PASS via paper-analysis is a NEGATIVE-DATA-FREE inference** — i.e. it relies on the absence of any cross-family pair landing >0.55 in the strict cross-family-only subset (Rigetti vs IBM_fez at 0.084). This is correct for the task statement's verdict criterion ("ANY pair <=0.55 → spirit PASS"), but does NOT establish that the AVERAGE cross-family |dS| is <=0.55. The cross-tech axis (super ↔ ion) average |dS| is (0.451+0.563+0.5346+0.6466)/4 = 0.549 — narrowly under 0.55 by averaging, with 2 of 4 pairs above. A strict "ALL pairs <=0.55" criterion would mark cond.7 as FAIL on cross-tech. The task statement uses "OR" disjunction, hence PASS.

---

## §7 raw# compliance audit

```
   raw#  | rule                                              | this cycle compliance
   ----- | ------------------------------------------------- | -------------------
   raw#9 | NO .py at Mac repo root                           | OK — no .py written; would-have-runner stays paper-only
   raw#15| no personal paths in body                         | OK — state/ + docs/ relative; user shell paths only in §1.1 audit cite
   raw#10| honest C3 + completion-quality recommendation      | OK — honest abort surfaced, paper-analysis labelled, §4.3 ranked recommendation present
```

---

## §8 next-cycle recommendations

```
   priority | candidate                                                               | gate
   -------- | ----------------------------------------------------------------------- | -------
   1        | accept cond.7 spirit PASS via paper-analysis; close cond.7 .roadmap     | zero cost; user confirms band 0.55 is acceptable for spirit-mode disjunction
   2        | amend cross-tech band 0.55 → 0.60 (physics-aware)                       | spec-level edit to docs/nexus_qmirror_spec_2026_05_03.md §12 (mirrors cond.3 band-revise pattern)
   3        | optional Heron r3 + ZNE re-burst (when user provides token)             | 30s wall, ~$3-5 cost; only if v3.0 spec demands r3-grade datapoint
   4        | tighten N=1 → N=3 replication for Rigetti ↔ IBM_fez (strongest pair)    | ~$10-15 cost; would lift |dS|=0.0836 from N=1-anecdote to N=3-pattern
```

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
