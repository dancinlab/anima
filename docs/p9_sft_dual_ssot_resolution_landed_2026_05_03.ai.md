# P9 SFT Dual SSOT Resolution Landed (2026-05-03) — AI-Native Handoff

**Audience**: 다른 Claude Code 세션 + future BG agents
**Status**: LANDED (additive only, soft migration via 1-line edit + cross_link only)
**Cap**: 30min ω-cycle BG subagent task
**Cost**: $0 mac-local destructive 0
**Friendly preset**: 가볍게 읽고 가세요. 핵심만 추렸습니다.

---

## 1. 배경 (Why)

anima/.roadmap.{clm,p9_sft} 측 P9 SFT entry 측 **dual SSOT race risk** 측 발견 (BG-AN-RDM C5 측 명시).

- **.roadmap.clm 측 entry `clm.65.4.p9_sft`**:
  - status=`spec_only`, exec_authorized=false, ts=2026-05-02
  - phase/cost/falsifiers/honest_c3 측 inline 측 land
  - `type=entry`, kind=`plan`
- **.roadmap.p9_sft 측 (peer-level domain)**:
  - status=`active`, since=2026-05-03
  - 3 conds (P0 HF setup partial / S3 sweep unmet / F4 verdict unmet) + 2 blockers
  - peer perspective, ai_native handoff doc + spec dir + p0 dir all referenced

**Race risk**: phase/status/cost/falsifiers 측 어느 측 truth?
- A) clm.65.4.p9_sft inline data = truth → .roadmap.p9_sft 측 redundant
- B) .roadmap.p9_sft = truth → clm.65.4.p9_sft 측 stale snapshot 위험 (예: P0 status=partial 갱신 시 clm 측 stale)
- → **B 채택** (peer domain 측 last update 2026-05-03 fresh, status=active, 3-cond 분리 정밀)

---

## 2. Resolution (What)

### 2.1 .roadmap.clm 측 1-line edit (in-place, additive only)

`clm.65.4.p9_sft` entry 측 변경:

| field | before | after |
|---|---|---|
| `kind` | `plan` | `cross_link` |
| `status` | `spec_only` | `superseded_by_domain` |
| `ts_utc` | `2026-05-02T00:00:00+00:00` | `2026-05-03T00:00:00+00:00` |
| `title` | "P9 multi-objective SFT for CLM self-chat" | "P9 multi-objective SFT for CLM self-chat — superseded by domain SSOT" |

**추가 (additive only)**:
- `superseded_by`: `.roadmap.p9_sft`
- `cross_link`: primary_ssot + primary_header_perspective + primary_conds + primary_blockers + resolution_doc + resolution_marker + redirect_rationale
- `spec_doc_ref`, `handoff_doc_ref` 측 reference 측 보존

**제거 (data not lost — moved to .roadmap.p9_sft as truth)**:
- inline strategies / recommended / cost_usd_band / wall_days_band / phi_risk / success_p / falsifiers_preregistered / verdict_logic / unlock_keyword / honest_c3
- → these 모두 `.roadmap.p9_sft` 측 header.goal + 3 conds + cross_link 측 이미 존재

### 2.2 .roadmap.p9_sft 측 cross_link reverse mention 추가 (additive only)

`cross_link.clm_cross_link` 측 update + 신규 `cross_link.clm_cross_link_resolution` block 추가:

```json
"clm_cross_link":"clm.65.4.p9_sft entry (.roadmap.clm 측 status=superseded_by_domain, kind=cross_link, this domain = primary SSOT, dual SSOT race resolved 2026-05-03 per docs/p9_sft_dual_ssot_resolution_landed_2026_05_03.ai.md)",
"clm_cross_link_resolution":{
  "resolution_date":"2026-05-03",
  "resolution_doc":"docs/p9_sft_dual_ssot_resolution_landed_2026_05_03.ai.md",
  "resolution_marker":"state/markers/p9_sft_dual_ssot_resolution_landed.marker",
  "clm_entry_id":"clm.65.4.p9_sft",
  "clm_entry_status":"superseded_by_domain",
  "truth_priority":"this domain (.roadmap.p9_sft) = primary SSOT; .roadmap.clm entry = navigation cross_link only"
}
```

→ 양방향 cross_link 측 land. clm 측에서 시작하든 p9_sft 측에서 시작하든 navigation 가능.

---

## 3. Verification (How verified)

### 3.1 JSONL syntax

```
=== .roadmap.clm ===
L3: OK type=header id=clm status=active
L4: OK type=entry id=clm.65.4.p9_sft status=superseded_by_domain
=== .roadmap.p9_sft ===
L3: OK type=header id=p9_sft status=active
```

→ 양 파일 측 JSON.loads() 측 PASS.

### 3.2 Cross-link round-trip

- .roadmap.clm L4 `cross_link.primary_ssot` = `.roadmap.p9_sft` ✓
- .roadmap.p9_sft L3 `cross_link.clm_cross_link_resolution.clm_entry_id` = `clm.65.4.p9_sft` ✓
- doc path 양 entry 측 동일 = `docs/p9_sft_dual_ssot_resolution_landed_2026_05_03.ai.md` ✓
- marker path 양 entry 측 동일 = `state/markers/p9_sft_dual_ssot_resolution_landed.marker` ✓

---

## 4. Truth Rules (post-resolution)

이후 P9 SFT entry update 측 다음 rule 적용:

1. **Primary SSOT** = `.roadmap.p9_sft`. cond.1/2/3 status, blockers, cost band, evidence 측 갱신 측 여기.
2. **.roadmap.clm 측 cross_link entry** = navigation only. status=superseded_by_domain 측 freeze. update 시 `cross_link.primary_*` field 측만 동기화 (rare).
3. **Conflict resolution**: .roadmap.p9_sft 측 last write wins. .roadmap.clm 측 entry 측 stale 측 의심 시 `superseded_by` field 측 따라 redirect.
4. **Future domain split**: P9 SFT 측 다른 domain 측 sister 측 land 측 시 (예: serving / training), 각 domain 측 동일 패턴 = peer SSOT + clm 측 cross_link only.

---

## 5. Honest C3 (raw#10)

- (a) 1-line edit 측 spec but actual = entry 측 6 field change + cross_link block 추가 = ~10 field touch (still in-place soft migration, no destructive delete)
- (b) `cross_link` field 측 .roadmap.clm 측 header 측에 이미 존재 → entry 측에 추가 측 schema 측 약간 nesting (2-level cross_link)
- (c) inline data 측 .roadmap.clm 측에서 제거 = 정보 손실 0 (모두 .roadmap.p9_sft 측 보존), but read-only audit 측 `clm.65.4.p9_sft` 단독 읽기 시 cost band 측 즉시 안 보임 → cross_link 측 follow 필요
- (d) `superseded_by_domain` status 측 새 enum value (기존: active/unmet/met/spec_only/deferred 등) → consumer 측 unknown status 측 fallback 측 `unmet`/`active` 외 측 처리 필요할 수 있음
- (e) 양방향 cross_link round-trip 측 manual 측 verify, automated invariant check 미구현 (다음 cycle hook 후보)

---

## 6. Cross-references

- spec doc: `docs/p9_sft_spec_2026_05_02.md`
- handoff prompt: `docs/p9_sft_handoff_prompt_2026_05_02.md`
- P0 landed: `docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md`
- narrative anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §61 + §65.4 + §66.5
- BG-AN-RDM C5 race risk note: peer-level BG 측 land 측 dual SSOT update 측 race 측 명시
- marker: `state/markers/p9_sft_dual_ssot_resolution_landed.marker`
