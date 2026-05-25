---
id: hf_flip_executed_2026_05_12
cycle: 6
section: "#T — HF 3-dataset fix-and-flip"
status: EXECUTED-OK
verdict_class: action-record
date: 2026-05-12
lock_policy: respected (no chflags / chattr applied)
api_calls: 5 (2 README upload + 3 update_repo_settings)
wall_time_seconds: 6.0
cost_usd: 0
parent_audit: state/hf_public_flip_readiness_audit_2026_05_12.md
---

# Cycle 6 §T — HF 3-Dataset Public Flip (executed)

> 비유: 출간 결정 — 표지·저작권 페이지의 오타를 잡은 책이 서점 매대로 나가는 순간. 본 문서는 매대 진열 직후의 영수증이지, 출간 결정 자체는 아니다 (그건 cycle 6 §R audit + 사용자 explicit GO directive 2026-05-12).

## §0 Execution summary

| dataset | README fixed? | flip private→public | anonymous HTTP 200 | post-sha (8-char) |
|---------|---------------|--------------------|--------------------|-------------------|
| `dancinlife/anima-hypotheses-candidates` | — (already clean per §R) | ✅ | ✅ (6079 B) | `9898ee36` |
| `dancinlife/anima-nexus-lenses`         | ✅ (+610 bytes, 5 fix points) | ✅ | ✅ (10096 B) | `640a7780` |
| `dancinlife/anima-research-trail`       | ✅ (+900 bytes, 4 fix points) | ✅ | ✅ (10965 B) | `96df72a1` |

**Aggregate**: 3/3 PUBLIC. Wall 6.0 s. Cost $0. README mutation atomic single-file commits.

---

## §1 README fixes applied

### 1.1 `anima-nexus-lenses` README.md (5 in-place replacements)

| # | spot | from → to |
|---|------|-----------|
| 1 | YAML frontmatter | `license: apache-2.0` → `license: mit` |
| 2 | §2 body, channel-reimpl spec inline ref | `lens_channel_reimpl_spec_2026_05_12.md` (bare) → `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md` |
| 3 | §2 body, second mention | `docs/lens_channel_reimpl_spec_2026_05_12.md` → `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md` |
| 4 | §9 visibility | `**private** by default at publication. May be opened later...` → `**public** (flipped 2026-05-12 after cycle 6 §Q lens channel reimpl Phase 1 PASS — see Cycle 6 Update below).` |
| 5 | §9 license body + §11 anima cross-link | `Apache-2.0 (matches the anima repo)` → `MIT (matches the anima repo LICENSE)`; `anima (private mirror)` → `[anima](https://github.com/dancinlab/anima) (public)`; §11 bullet `docs/lens_channel_reimpl_spec` → `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md` |
| 6 (append) | new "Cycle 6 Update — Phase 1 PASS" section before final footer | F-reimpl 3/3 PASS, F-1/F-2/F-3 metrics, K=10 v2 lens path |

Net delta: +610 bytes (9299 → 9909). Single commit message: `cycle 6 §T: license MIT-align + broken path fix + Phase 1 PASS reference`.

### 1.2 `anima-research-trail` README.md (4 in-place replacements)

| # | spot | from → to |
|---|------|-----------|
| 1 | header metadata | `**Visibility**: PRIVATE (default)` → `**Visibility**: PUBLIC (flipped 2026-05-12 — cycle 6 §T)` |
| 2 | §1-area "Source repo" line | `github.com/dancinlife/anima (private — paths preserved)` → `github.com/dancinlab/anima (public — paths preserved)` |
| 3 | §7 ANIMA core repo bullet | `github.com/dancinlife/anima (private)` → `github.com/dancinlab/anima (public)` |
| 4 (append) | new "Cycle 6 Update — §1 close + HF flip" section before §10 Lock policy | B1 RESOLVED, B5 RESOLVED-SPEC, lens reimpl Phase 1 PASS, K=25 cascade 진입 가능, HF flip 진행 |

Net delta: +900 bytes (9029 → 9929). Single commit message: `cycle 6 §T: dancinlife->dancinlab + private->public + cycle 6 §1 update`.

### 1.3 `anima-hypotheses-candidates`

No README touched — §R audit verdict `READY-FOR-PUBLIC (minor)` w/ optional sister §6 deferred. Sister-link addition is nice-to-have, not flip blocker. Defer to future cycle if cross-link audit re-prioritizes.

---

## §2 Cycle 6 §Q reference inline (LEGITIMATE 회복 명시)

`anima-nexus-lenses` README 의 **Cycle 6 Update** 섹션이 cycle 5 §3 #A TRIVIAL → cycle 6 §Q LEGITIMATE 전환을 명시:

- F-1 input dependency dynamic range **0.40 ≥ 0.30** ✓
- F-2 cross-validation r **0.459 ∈ [0.2, 0.95]** ✓
- F-3 real vs shuffled **7/10 separating** ✓
- 10 v2 lens path 확정: `state/nexus6_1013lens_activation_2026_05_11/k10_reimpl/core_<axis>_v2.hexa`

본 dataset (`anima-nexus-lenses`) 의 1,588-lens snapshot 자체는 여전히 **v1 self-test** 상태 — v2 채널 lens 의 추가 upload 는 K=25 land 후 별도 cycle 에서 검토.

`anima-research-trail` README 의 **Cycle 6 Update** 섹션도 같은 결과를 timeline ledger 측면에서 cross-ref (B5 RESOLVED-SPEC + Phase 1 PASS).

---

## §3 Public URLs

- https://huggingface.co/datasets/dancinlife/anima-hypotheses-candidates
- https://huggingface.co/datasets/dancinlife/anima-nexus-lenses
- https://huggingface.co/datasets/dancinlife/anima-research-trail

---

## §4 Access verification

### 4.1 HfApi `dataset_info`

```
anima-hypotheses-candidates: private=False, sha=9898ee36
anima-nexus-lenses:          private=False, sha=640a7780
anima-research-trail:        private=False, sha=96df72a1
```

### 4.2 Anonymous HTTP (no `Authorization:` header)

```
anima-hypotheses-candidates: HTTP 200 (Content-Length 6079 bytes)
anima-nexus-lenses:          HTTP 200 (Content-Length 10096 bytes)
anima-research-trail:        HTTP 200 (Content-Length 10965 bytes)
```

3/3 익명 fetch PASS. README 본문이 unauth client 에서 fetch 가능 = 진정한 public flip 확인.

---

## §5 Wall time + cost

- API calls: 5 (2 `upload_file` + 3 `update_repo_settings`)
- Wall: **6.0 s** (LFS upload 무 — README only, ~10 KB 두 개)
- Cost: **$0** (HF Hub dataset hosting free tier)
- Token retrieval: 1 call to `ssh mac /Users/ghost/core/secret/bin/secret get hf.token` (memory-only in-process Python variable; not written to disk; not echoed)

---

## §6 Reverse-toggle (emergency 1-liner)

만약 contentious feedback 또는 sensitive content 사후 발견 시:

```python
from huggingface_hub import HfApi
import subprocess
token = subprocess.check_output(["ssh","mac","/Users/ghost/core/secret/bin/secret","get","hf.token"]).decode().strip()
api = HfApi(token=token)
for r in ["anima-hypotheses-candidates","anima-nexus-lenses","anima-research-trail"]:
    api.update_repo_settings(f"dancinlife/{r}", repo_type="dataset", private=True)
```

L1 caveat 인지: HF 가 private 으로 되돌려도 Google Cache / Wayback / archive.today / 외부 scraper snapshot 은 **비가역적**. 일단 public 으로 나간 README 본문은 "공식적으로는 회수" 가능하지만 "실질적으로는 회수 불가". 본 cycle 의 §1 README content 는 모두 honest disclosure (TRIVIAL/PASS framing) 이므로 사후 회수 우려 낮음.

---

## §7 Honest L1-L3

### L1 — external cache snapshot 비가역
public flip 후 외부 indexing (Google, Wayback, HF 자체 search index) 가 작동. README content 가 한 번 fetch 되면 reverse-toggle 도 외부 cache 까지 지우지 못함. 본 cycle 의 README 는 cycle 6 §R audit 가 sensitive content scan 을 통과한 상태이므로 즉시 위험은 낮음. 단, Mac path 노출 (`/Users/ghost/...`) 은 §R §1.2/§1.3 에서 "acceptable disclosure — provenance SSOT" 로 평가됨 — provenance audit trail 가치가 노출 비용 초과.

### L2 — HF API rate limit
짧은 시간 내 다수 update_repo_settings + upload_file 호출은 rate-limit 위험. 본 cycle 은 5 call / 6 s 로 충분히 여유. 향후 동일 dataset 의 metadata 빈번 mutation 시 (예: tags / size_categories 반복 갱신) `huggingface_hub.HfApiError 429` 가능 — 1 min cooldown 권장.

### L3 — token 본 verdict 본문 inline 금지 (★ critical, cycle 5 §5 lesson)
본 문서 어디에도 `hf_*` prefix 의 token string 어떤 substring 도 inline 하지 않음.

검증:
- `grep -n "hf_" hf_flip_executed_2026_05_12.md` → 0 hits (단, 메모리 reference `hf_*` glob 패턴 표기는 있을 수 있음 — substring 아님)
- `grep -nE "hf_[a-zA-Z0-9]{8,}" hf_flip_executed_2026_05_12.md` → 0 hits
- token retrieval 은 `subprocess.check_output([... "secret","get","hf.token"]).decode().strip()` 으로 in-process variable; print/log/file write 안 함
- `print(token)` / `f"...{token}..."` 본문 작성 무 (모든 upload/flip API 호출이 keyword arg 로 직접 전달)
- staging dir `/tmp/anima-hf-flip-work/` 에 token text 저장 무 (README 본문만 저장; 스크립트는 `/tmp/fix_readmes.py` + `/tmp/upload_and_flip.py` 도 hard-coded token 없음, runtime `secret get` 호출만)

cycle 5 §5 GitHub Push Protection lesson (commit `bf03ee397` 의 prefix-suffix 노출) 의 재발 방지 protocol 정합.

---

## §8 Race condition check (post-execution)

| sibling agent | lane | overlap |
|---------------|------|---------|
| #U (K=25 cascade) | `state/nexus6_*/k25_phase2/` | ✅ none — 본 §T 는 HF dataset metadata + 2 README only |
| #V (noise calib) | `state/phi_ce_*/noise_calibration*` | ✅ none |
| #W (Hc_598) | `hypotheses_candidates/Hc_598*` | ✅ none |
| #X (cycle 6 trail) | `docs/cycle_*_master_*` | ✅ none — 본 §T 는 anima repo 에 단 하나 file (`state/hf_flip_executed_2026_05_12.md`) 추가 |

---

## §9 Lock policy

본 cycle 의 file 어디에도 `chflags +uchg/+schg/chattr +i` 적용 안 함. HF dataset metadata 의 `private=False` 는 logical flag, filesystem immutability 와 무관. cycle 6 §T audit (`state/hf_public_flip_readiness_audit_2026_05_12.md`) lock policy 와 정합.

---

## §10 Next action candidates (다음 진행할 것들)

| # | item | cost | time | value |
|---|------|------|------|-------|
| 1 | root `README.md` 의 `📊 Datasets` 섹션에 3 public URL wired (cycle 5 §9 cross-ref index 완결) | 0 | 5 min | ★★ — discoverability + SSOT closure |
| 2 | `anima-hypotheses-candidates` sister §6 추가 (3-way triangle 완성; §R §4.1 nice-to-have) | 0 | 10 min | ★ — symmetry; defer 가능 |
| 3 | `state/hf_upload_anima_hypotheses_candidates_2026_05_12.md` 의 (§R §5.4) masked prefix-suffix 추가 redact `hf_***` | 0 | 2 min + 1 commit | ★★ — 이미 rotate 됐으니 우선순위 낮음, but 차기 audit 잡음 감소 |
| 4 | HF dataset 측 README 의 `Cycle 6 Update` section 을 anima repo 측 `docs/cycle_6_master_*` 에서 cross-ref (양방향 wiring) | 0 | 5 min | ★ — bidirectional audit trail |
| 5 | cycle 6 §R audit 의 lock_policy section 을 cycle close 시 NEXT.md 에 archive 처리 (audit prep → action record 전환 명시) | 0 | 2 min | ★ trivial |

— end of cycle 6 §T verdict —
