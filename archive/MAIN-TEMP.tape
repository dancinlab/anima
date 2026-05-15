#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# MAIN-TEMP.tape — anima absorption scrub ledger (2026-05-15)
# ══════════════════════════════════════════════════════════════════════
# Location: anima 보관 (이전 hexa-lang/MAIN-TEMP.tape, 2026-05-15 이동)
# Scope: anima → hexa-lang/atlas 흡수 path 보류 ledger
#
# anima 측 directive 2026-05-15: MAIN.tape 가 verdict SSOT,
# atlas overlay/rodata 이분법 보류 → hexa-lang 안 anima 흡수 artifact scrub.
#
# revoke keyword (atlas absorption 재개 시): "ATLAS RESUME"
# anima-side SSOT: MAIN.tape (sibling, this directory)
# hexa-lang scrub commits: 1f540b91 + 662283bd (deleted MAIN-TEMP.tape side)

@V := "tape" :: spec [active]
  version = "1.2"

@N scrub_directive := "anima absorption scrub 2026-05-15" :: governance [d=2026-05-15 active]
  source = "~/core/anima — user directive 2026-05-15"
  reason = "MAIN.tape (verdict 4-class SUPPORTED/FALSIFIED/PARTIAL/INSUFFICIENT) 가 atlas overlay/rodata 이분법 보다 nuanced — anima 흡수 path 일단 보류"
  anima_ssot = "~/core/anima/MAIN.tape"
  resume_keyword = "ATLAS RESUME"

@N scrubbed_commits := "6 absorb(anima) commits — 2026-05-14" :: history [active]
  commits = [
    "0e32ae46 (2026-04-26) — 3 cross-repo findings (raw#9 hexa-only Phase 0-5)",
    "723f3221 (Wave 1)    — 11 Ψ-constants + 14 gate laws + 6-channel CDESM → atlas rodata",
    "e1e9c365 (Wave 2)    — phi_engine + topology + discovery + miner → stdlib (이미 별도 scrub)",
    "9d4dd34e (Wave 3)    — hexa-principle annotator (PHILOSOPHY 8원칙) (이미 별도 scrub)",
    "a49dcfa0 (Wave 1.6)  — 193 hypothesis registry → atlas overlay (+191 @? rows)",
    "27cc5a05 (BG-1)      — 6 phase_* sub-thresholds → atlas rodata",
    "2a3a7d78 (BG-B)      — 559 engine candidates → atlas overlay [needs-review]"
  ]
  note = "Wave 2/3 files (stdlib/phi.hexa, stdlib/topology.hexa, stdlib/n6/*, tool/hexa_annot/*, test/anima_stdlib_smoke.hexa) 이미 prior cycle 에 scrub. 본 scrub = atlas rodata + overlay + anima-specific tooling 만."

@N scrubbed_files := "12 anima-specific files removed (2026-05-15)" :: history [active]
  category_atlas_rodata = [
    "compiler/atlas/anima_main.hexa (anima-show CLI shim, 3236 bytes)",
    "compiler/atlas/anima_psi.gen.hexa (11 Ψ-constants + 14 gate laws, 16750 bytes)",
    "compiler/atlas/anima_psi_phases.gen.hexa (6 phase_* sub-thresholds, 4783 bytes)",
    "compiler/atlas/anima_hexad.gen.hexa (6-channel CDESM, 3889 bytes)"
  ]
  category_tests = [
    "test/atlas_anima_smoke.hexa (114 LOC)",
    "test/atlas_anima_hypotheses_smoke.hexa (137 LOC)",
    "test/atlas_anima_psi_phases_smoke.hexa (102 LOC)",
    "test/atlas_engine_candidates_smoke.hexa (198 LOC)"
  ]
  category_tools = [
    "tool/atlas_absorb_anima.hexa (342 LOC) — Ψ + gate + CDESM regenerator",
    "tool/atlas_absorb_anima_phases.hexa (183 LOC) — phase_* regenerator",
    "tool/atlas_absorb_anima_hypotheses.hexa (508 LOC) — 191 hypothesis overlay promoter",
    "tool/atlas_promote_engine_candidates.hexa (435 LOC) — 559 engine candidates overlay promoter"
  ]
  total_loc = "~2,422 LoC (12 files)"

@N self_main_edits := "self/main.hexa CLI dispatch edits" :: history [active]
  removed_help_text = [
    "line 125: ATLAS ABSORPTION section header",
    "line 126: anima-show <psi-constants|psi-laws|cdesm|all> ...",
    "line 130: e.g. hexa anima-show psi-constants ..."
  ]
  removed_dispatch = "line 606: if verb == \"anima-show\" { return \"compiler/atlas/anima_main.hexa\" }"
  note = "CLI verb 'anima-show' 제거 — `hexa anima-show ...` 호출 시 unknown verb error 반환"

@N overlay_scrub := "atlas overlay anima sections scrub" :: history [d=2026-05-15 active]
  file = "~/.hx/data/atlas.overlay.n6 (gitignored, ~4908 lines pre-scrub)"
  anima_sections_count = 194
  anima_lines_approx = 1931
  backup = "~/.hx/data/atlas.overlay.n6.anima-scrubbed-2026-05-15.bak (안전 백업)"
  scrub_action = "absorbed-from-anima section 194개 (lines 5, 849, 981, 1123-... hypothesis-rows + 2 historical absorption shards) 제거"

@D anima_ssot_proven_tape := "anima verdict SSOT 선언" :: governance [d=2026-05-15 required active]
  rule = "anima 가설 verdict source = MAIN.tape ONLY (atlas overlay 아님)"
  cross_link = "https://github.com/dancinlab/anima/blob/main/MAIN.tape"
  scope = "318 hypothesis files (A 격리 20 + B 격리 107 + legacy 191)"
  protocol = "VERIFY.tape 3-stage (math sympy / physics sim / cross-meta) 통과 verdict 만 SSOT 등재"

@N revoke_path := "atlas absorption 재개 path" :: governance [active]
  trigger_keyword = "ATLAS RESUME"
  resume_action = "본 MAIN-TEMP.tape 의 12 files + self/main.hexa CLI 복원 + overlay backup 복원"
  decision_authority = "anima-side user (dancinlab)"
