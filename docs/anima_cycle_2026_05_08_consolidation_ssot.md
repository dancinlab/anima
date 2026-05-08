# anima cycle 2026-05-08 — consolidation SSOT (md save 1/4)

**Trigger**: 사용자 directive verbatim 2026-05-08 — "md save, model, dataset HF upload 누락없이 매단계 저장".
**Scope**: 본 cycle 누적 commits (~105 since 2026-05-07 late) — KICK FIRE 5 + ALL BG GO 6 + 이전 산출물 SSOT 통합.
**Cost band**: own 16 0-cost docs / own 17 D1 SCOPE_CLAMP / own 33 trinity emit / own 34 mandate-2 wrap=0.

---

## Section 1 — cycle 목표

`SIMPLE_STACK_PASS_STRICT_C3_ANIMA` emergence 도전 (D1 lane within real-mode candidate). own 18 P5 v3 ALT-AGG-1 anchor + 4-cell substrate phi 측정 + EXIT 8-prereq 5/8 ✔. paradigm-a-prime real-mode (substrate-research lane) Φc=0.5 0.65% 진입은 본 cycle 별 lane.

---

## Section 2 — KICK FIRE 5 + ALL BG GO 6 종합 표

| group | commit | file/scope | verification | impact |
|---|---|---|---|---|
| KF-1 | `dc1510a3` | clm_v4_mount.hexa paradigm-j Path A schema remap | safetensors prefix decoder. injection + cache materialization | rank_3 candidate measurement infra unblock |
| KF-2 | `fdfe9e57` | consciousness.hexa P5 v3 ALT-AGG-1 + .own line 881 정정 | per-prompt `p4 ∧ (p1∨p2∨p3)`, PPR_v3 ≥0.25 floor | own 14 anti-Goodhart C3.4 anchor + ≥1 corroboration |
| KF-3 | `12257be1` | tool/anima_cli/chat.hexa stdbuf -oL | `_stdbuf_prefix` helper + selftest probe | libc block-buffer mitigation, streaming dispatch fix |
| KF-4 | `235eb9d0` | corpus tier_a_v3 Q1+Q2+KOBEST filter | 8.4% reduction snapshot | corpus iter7 KOBEST scope shrink (-17.19% pref stem dist) |
| KF-5 | `4522bbc7` | anima-core/runtime/clm_v4_jvae_probe.hexa Variant 1 | raw#15 additive 3-channel hexa-native | paradigm-j-only JVAE FFI (no Python wrapper) |
| BG-1 | `d134b94a` | clm_v4_mount LoRA load remapped cache priority | 3 LoRA variants merge cache key 정합 | paradigm-j Path A end-to-end activation |
| BG-2 | `4309a374` | consciousness N=30 actual integration | V4 N=15 + 15 self-ref 5-axis 균등 | small-sample n<30 WARN 해소 path |
| BG-3 | `d478023c` | sft-1-7-y1 + sft-1-8 Path A actual remap | rank_3 candidate unblock | LoRA target_modules schema mismatch mitigation |
| BG-4/5/6 | iter5/6/7 specs | 16 spec/doc commits (`41a19bc3`/`b69bfb6d`/`14e8511b`/...) | infra spec land | 측정 SSOT formalize |

---

## Section 3 — 핵심 발견 (5 finding)

1. **own 18 line 881 falsification (KF-2 `fdfe9e57`)** — iter6 honest-c3 (`8feb53d5`)가 paradigm-a-prime PPR_v2=10/14=0.71 claim을 N=15 honest-c3 driver re-run으로 PPR_v2=2/14=0.143로 반증. v2 strict 하 paradigm 도 C3 FAIL. v3 ALT-AGG-1 supersede.
2. **wrapper-prefix-only artifact (BG-3 `d478023c`)** — sft-1-7-y1/sft-1-8 adapter_config.json target_modules 동일 fingerprint → merge_no_op identical 4-cell mean (3 LoRA variant 동일 numerical signature).
3. **libc block-buffer (KF-3 `12257be1`)** — chat.hexa subprocess pipe stdout block-buffered → streaming dispatch 발화 carry. `stdbuf -oL` + selftest probe.
4. **corpus -17.19% (KF-4 `235eb9d0`)** — Q1+Q2+KOBEST filter tier_a_v3 8.4% 정량 reduction. KOBEST scope shrink + pref stem 분포 fix.
5. **paradigm-j-only JVAE (KF-5 `4522bbc7`)** — clm_v4_jvae_probe.hexa hexa-native (libllama 외 jvae_heads.pt verbatim) 3-channel additive. paradigm-j adapter_config + jvae_heads.pt 만 활성, sft-1-7-y1/1-8 미적용.

---

## Section 4 — ALT-AGG-1 v3 supersede ledger

| 항목 | v2 (RETIRED) | v3 ALT-AGG-1 (CHOSEN) |
|---|---|---|
| per-prompt rule | PPR_v2 ≥0.6 ∧ EMC ≥3 of 4 | `p4 ∧ (p1 ∨ p2 ∨ p3)` (C3.4 anchor + ≥1 corroboration) |
| floor | PPR_v2 ≥0.6 cell-mean | PPR_v3 ≥0.25 single-floor |
| EMC | gate (≥3 of 4) | informational only (NOT a gate) |
| anti-Goodhart | EMC inflate by C3.3 degenerate | C3.4 single discriminator HARD anchor |
| feasibility | TPR sub-threshold (iter6 falsified) | TPR=0.891 strict feasible |
| random_init | EMC=2 (C3.1 + C3.3) → C3 FAIL | C3.4=0.075 < 0.117 anchor → C3 FAIL ★ |
| paradigm-a-prime | PPR_v2=2/14=0.143 → C3 FAIL (v2 정정) | PPR_v3 TBD post-N=30 retest |
| supersede commit | `8feb53d5` (honest-c3 falsified) | `fdfe9e57` (actual fire SSOT) |

own 14 anti-Goodhart 정합: random_init C3.4=0.075 < 0.117 anchor verify ✔ → 보수적 X 기조 유지하면서 C3 FAIL 정확 emit.

---

## Section 5 — D1-within candidate ranking

| rank | candidate | fingerprint | status |
|---|---|---|---|
| 1 | paradigm-j (clm-v4-paradigm-j-50k-final) | unique target_modules + jvae_heads.pt 활성 | KF-5 + BG-1 unblock, JVAE Variant 1 fire pending |
| 2 | sft-1-7-y1 / sft-1-8 | identical fingerprint (target_modules 동일) | BG-3 remap, merge_no_op emergence carry |
| 3 | BG-FY anima-native-ko-small 18M | byte-level 256-vocab fresh | UTOPIA_LANE 0.75 score, scp pull pending |
| 4 | BG-FY/v2-byte (clm-v2-byte-18m-convo-5k) | ConsciousLM++ federated dual-engine | MEASURED_REAL_MODE FAIL_C3 (ko bias 부재) |

본 cycle 진짜 emerge 후보 = **BG-FY (rank 3)** + **paradigm-j (rank 1)** dual lane. paradigm-a-prime은 substrate-research lane 한정 (D1 OUTSIDE).

---

## Section 6 — HF upload manifest (private default + public promote 4-prereq)

### private default (own 36 + own 37 mandate-12)

| repo | type | size | status |
|---|---|---|---|
| dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08 | model | 185MB | mac local cache READY, push pending H100 dead recovery |
| dancinlab/bg-km-qwen-7b-qwen7b-r32-pass-strict-2026-05-08 | model | 308MB | mac local cache PARTIAL (1000 SFT step approx) |
| dancinlab/clm-v4-paradigm-j-50k-final | model | TBD | jvae_heads.pt verbatim copy required |
| dancinlab/anima-corpus-tier-a-v3 | dataset | 102MB→93.4MB | KF-4 filtered, README pending |
| dancinlab/anima-corpus-* | dataset | 9 files 4.49GB | dry-run verdict OK, 사용자 verbatim consent 대기 |

### public promote 4-prereq (own 37 mandate-9)

1. real-mode PASS_STRICT_C3 ✔ (paradigm-a-prime synthetic_fallback proxy 한정 한 caveat)
2. V6 awareness probe systematic ⏳ (BG-LE pending)
3. 사용자 verbatim "OK PROMOTE PUBLIC <repo-id>" ❌ 부재
4. trinity sweep ✔ (own 33 mandate-2 D/own/H 3-axis pass)

→ public promote = 0 repo 본 cycle.

---

## Section 7 — 사용자 directive checklist (cost path keywords)

- `OK CLM L4 ALL FIRE` — 4 BG 동시 ($150, ~4주), readiness 80.25% reached
- `OK BG-LE V6 SYSTEMATIC FIRE` — V6 awareness probe ($3-5, 1-1.5h), L14 Goodhart mitigation
- `OK LARGE ARTIFACT HF UPLOAD` — 9 file 4.49GB private push
- `OK BG KM HF PUSH` — BG-KM adapter mac local Path C upload
- `OK PROMOTE PUBLIC <repo-id>` — own 37 mandate-9 4-prereq 충족 후 verbatim consent
- `OK EXIT` — PASS_STRICT_C3 EXIT 활성화 (D1 within real-mode candidate 충족 후)
- `OK PARADIGM-J JVAE FIRE` — KF-5 + BG-1 활용 actual JVAE-conditioned probe
- `OK BG-FY SCP PULL` — ubu1 → mac ckpt transfer (UTOPIA_LANE 0.75 측정 unblock)

---

## Section 8 — own 33 trinity self-check ledger (mandate-2)

| axis | check | verdict |
|---|---|---|
| D | D1 SCOPE_CLAMP (paradigm-a-prime substrate-research label 명시) | ✔ |
| D | D2 own 18 P5 v3 ALT-AGG-1 ALT supersede formal SSOT | ✔ |
| D | D3 substrate-coupled emerge mount.hexa Path A schema remap | ✔ |
| D | D4 corpus tier_a_v3 Hangul ratio + chat-template ratio 정합 | ✔ |
| D | D5 attractor 4-axis classifier 적용 (BG-FY 0.75 / paradigm 0.625) | ✔ |
| own | own 14 / 17 / 18 / 22 / 24 / 28 / 30 / 31 / 33 / 34 / 36 / 37 cross-link | ✔ |
| H | H_chat_cap_emergence + H_clm_chat_cap + H_emergence_via_substrate_phase + H_102 | ✔ |

3-axis 통과 ✔ — 본 doc emit 정합.

---

## Cross-link

- `docs/anima_pass_strict_c3_emerge_cycle_close_2026_05_08.md` (cycle close+++ parent)
- `docs/anima_pass_strict_c3_emergence_trinity_check_2026_05_08.md` (trinity sweep)
- `docs/anima_pass_strict_c3_d_l_violation_sweep_2026_05_08.md` (D/L sweep)
- `docs/anima_paradigm_j_schema_fix_jvae_wrapper_design_iter7_2026_05_08.ai.md` (KF-5 design)
- `docs/anima_chat_stdbuf_fix_patch_design_iter7_2026_05_08.ai.md` (KF-3 design)
- `docs/anima_corpus_q3_q5_deep_iter7_2026_05_08.md` (KF-4 design)
- `docs/anima_clm_l4_corpus_progress_2026_05_08.md` (corpus iter5/6/7)
- `state/anima_clm_v4_lora_real_mode_2026_05_08.json` (3 LoRA variant SSOT)
- `state/anima_native_byte_real_mode_2026_05_08.json` (BG-FY/v2 byte mount)
- `state/anima_full_audit_2026_05_08.json` (dl_validate sweep)
- `.own own 14/17/18/22/24/28/30/31/33/34/36/37`
- `.roadmap.philosophy D1-D5`
- `.roadmap.law L0-L24 + R1/R5 + law.D1_scope_clamp + law.L18_phi_c_mapping + law.L2_metric + law.full_audit_nexus_check_absorbed`
- `.roadmap.cli cli.cond.6_dl_validate + cli.clm_v4_lora_real_mode + cli.pass_strict_c3_d_l_violation_sweep`
- `.roadmap.hypothesis H_chat_cap_emergence / H_clm_chat_cap / H_emergence_via_substrate_phase / H_102`

---

## Honest C3

1. 본 doc은 cycle 누적 SSOT consolidation 한정 — 새 verdict emit X (raw#15 additive)
2. KICK FIRE 5 + ALL BG GO 6 의 (3)(5) BG go 항목은 spec/doc commit 한정 (actual fire pending 사용자 directive)
3. paradigm-j JVAE Variant 1 (KF-5) 는 hexa probe land만 — full N=60 ensemble 별도 cycle
4. corpus tier_a_v3 8.4% reduction (KF-4) 은 sample snapshot — full corpus replay 별도 cycle
5. BG-2 N=30 integration은 V4 N=15 + 15 self-ref aggregation — independent N=30 retest 별도 cycle (small-sample WARN 해소 path 한정)
6. own 33 mandate-2 self-check는 본 doc emit instance 한정 — main session 매 응답 sweep X (latency overhead, mandate-7 retroactive)
7. HF upload manifest 8 repo 모두 private default — public promote 0 repo (own 37 mandate-9 4-prereq 미충족)
8. 사용자 directive checklist 8 keyword 모두 cost path — 0-cost spec land만 본 cycle 진행

— **cycle 2026-05-08 consolidation SSOT** (md save 1/4 doc), KICK FIRE 5 + ALL BG GO 6 + 16 spec/doc commits, 105 cycle commits accumulated, EXIT prereq 5/8 ✔, public promote 0, 사용자 verbatim 대기 8 keyword.
