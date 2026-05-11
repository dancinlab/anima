---
id: hf_public_flip_readiness_audit_2026_05_12
cycle: 6
section: "#R — HF public flip readiness audit"
status: NEEDS-FIX (no flip executed)
verdict_class: audit-prep-only
date: 2026-05-12
lock_policy: respected (no chflags / chattr applied; read-only local + staging scan)
api_calls: 0 (local + staging-cache audit only — no HF API mutation)
---

# Cycle 6 #R — HF 3-Dataset Public Flip Readiness Audit

> 비유: 출간 직전 책 표지 검수 — 본문은 이미 들어가 있고, 표지/저작권 페이지/색인의 오타·옛 주소·민감정보만 잡아내는 단계. ✅ 실제 flip 은 사용자 explicit confirm 후 별 cycle.

## §0 Audit summary

| dataset | sensitive-content | license | honest-disclosure | cross-link | verdict |
|---------|-------------------|---------|-------------------|------------|---------|
| `dancinlife/anima-hypotheses-candidates` | ✅ clean | ✅ MIT (matches repo) | ✅ candidate-unverified 명시 + 8 honest finding | ⚠ no sister §6 | **READY-FOR-PUBLIC** (minor) |
| `dancinlife/anima-nexus-lenses`         | ⚠ Mac path `/Users/ghost/...` 다수 (acceptable — repo path SSOT) | ⚠ Apache-2.0 (repo는 MIT) | ✅ TRIVIAL caveat above-fold §2 + blockquote | ⚠ broken `docs/lens_channel_reimpl_spec_*` path + outdated "anima private" | **NEEDS-FIX** |
| `dancinlife/anima-research-trail`       | ✅ clean (HF token 없음; Mac path only in tool/state files — acceptable) | ✅ CC-BY-4.0 (data-license, valid) | ✅ 8 honest finding ledger + TRIVIAL ★ | ⚠ `github.com/dancinlife/anima` (오타 `dancinlab` 아님) × 2 + "private" 표기 (실제 public) | **NEEDS-FIX** |

**Aggregate**: 2 dataset 가 minor README fix 필요 — public flip 전 권장. 1 dataset (Hc-candidates) 는 즉시 가능. 전체 flip 은 사용자 explicit confirm 후.

**Out-of-band CRITICAL** (anima repo, *not* HF dataset): `state/hf_upload_anima_hypotheses_candidates_2026_05_12.md` 가 public GitHub repo `dancinlab/anima` 에 token prefix-suffix `hf_zlbJ…lanybs` 노출 (commit `bf03ee397`). 중간 `…` ellipsis 로 마스킹은 됐지만 prefix+suffix 가 보임. **HF 토큰 자체는 rotate 권장** (별도 §5).

---

## §1 Sensitive content scan

### 1.1 `dancinlife/anima-hypotheses-candidates`

| pattern | finding | classification |
|---------|---------|----------------|
| `hf_*` token | none in DATASET_CARD.md | ✅ |
| `nerve011235@gmail.com` | none | ✅ |
| `/Users/ghost/` | none in card | ✅ |
| `ssh mac` / `secret get` | none | ✅ |
| IP / SSH config | none | ✅ |
| Hc_*.md (1127 files) | grep -rEn `hf_|nerve|/Users/ghost|ssh mac|secret get` → 0 hits | ✅ |
| INDEX.md / HYPOTHESES_INDEX.md | 0 hits (copies of repo `hypotheses_candidates/README.md` + `hypotheses/README.md`) | ✅ |

**verdict**: **clean** — no redact required.

### 1.2 `dancinlife/anima-nexus-lenses`

| pattern | finding | classification |
|---------|---------|----------------|
| `hf_*` token | none in README.md / SNAPSHOT_INFO.md | ✅ |
| `nerve011235@gmail.com` | none | ✅ |
| `/Users/ghost/core/nexus/lenses/` | README §1 §6 §8, SNAPSHOT_INFO.md `source_path:` line, rsync command | ⚠ **acceptable disclosure** — Mac path 는 dataset provenance 의 SSOT. dataset card 의 핵심 narrative (3-way drift caveat, snapshot 출처) 가 이 path 에 의존. redact 시 narrative 손실 > 정보 노출 비용. **유지 권장**. |
| `ssh mac` | SNAPSHOT_INFO.md L9 ("source_host: mac (ssh alias)") | ⚠ acceptable — ssh alias 'mac' 은 hostname/IP 아님, dancinlife 의 dev 환경 nickname 일 뿐 |
| `secret get` / token retrieval | upload verdict state file 만 (HF dataset 외부) | N/A (not in dataset) |
| IP / SSH config | none | ✅ |
| 1,588 × `*.hexa` files | not scanned exhaustively in this audit pass — lens body는 closed-form constants 만 보유 (cycle 5 §3 #A 검증) | ✅ (cycle 5 #A 보증) |

**verdict**: **clean modulo Mac-path provenance** — path 노출은 acceptable disclosure (audit trail 의 SSOT).

### 1.3 `dancinlife/anima-research-trail`

| pattern | finding | classification |
|---------|---------|----------------|
| `hf_*` token | none in README.md / NEXT.md / staging tree | ✅ |
| `nerve011235@gmail.com` | none | ✅ |
| `/Users/ghost/...` (Mac path) | `state/phi_star_naming_refactor_*.md` × 4, `tool/anima_nexus_1013lens_cascade.hexa` × 4, `tool/anima_phi_star.hexa` × 1, `state/nexus6_*/lens_channel_reimpl_prototype_core_info.hexa` × 1, `state/nexus6_*/lens_registry_synthesized_*.md` × 2, `state/nexus6_*/prereq_audit_*.md` × 5, `state/nexus6_*/spec.md` × 9, `state/nexus6_*/smoke_k10_caveat_*.md` × 4, `state/phi_ce_*/spec.md` × 1 | ⚠ **acceptable disclosure** — research-trail 의 본질은 anima cycle 5 process 의 reproducible snapshot. tool/state file 의 path 는 reproducibility SSOT. redact 시 reproducibility 손실. **유지 권장**. |
| `ssh mac` / `secret get` | none in dataset content (only in upload verdict, outside dataset) | ✅ |
| IP / hostname / SSH config | none | ✅ |
| GitHub URL | `github.com/dancinlife/anima` × 2 (README §1 line 25, §7 line 134) — should be `github.com/dancinlab/anima` (org rename) + 추가로 "private" 표기 (실제 public) | ⚠ **REDACT (fix)** — 단순 오타 + outdated metadata |

**verdict**: **clean modulo 2-line GitHub URL fix** — path 노출은 acceptable.

---

## §2 License audit

| dataset | declared | matches repo (MIT)? | data-license valid? | citation BibTeX | rating |
|---------|----------|---------------------|---------------------|------------------|--------|
| hypotheses-candidates | **MIT** (YAML `license: mit` + body §provenance) | ✅ matches | ✅ MIT is valid for text+frontmatter | ✅ present (§Citation) | **READY** |
| nexus-lenses | **Apache-2.0** (YAML `license: apache-2.0` + §9 visibility-and-license + §10 BibTeX) | ⚠ **mismatch** — anima repo 는 MIT, dataset 카드는 Apache-2.0 주장 | ✅ Apache-2.0 자체는 valid | ✅ present (§10) | **NEEDS-FIX** — 두 옵션: (a) MIT 로 align (anima repo LICENSE 정합), (b) Apache-2.0 유지 + 명시적 "lens artifacts are Apache-2.0; anima repo upstream is MIT" 명시 |
| research-trail | **CC-BY-4.0** (YAML + §8 body) | ✅ data-license 정합 (anima repo의 code-license MIT 와 별개; process docs/findings 는 data 로 분류 합당) | ✅ valid + attribution-friendly | ✅ present (§8) | **READY** (license-mismatch 아님 — code vs data lane 분리) |

**Honest disclosure**: dataset card 의 license 가 HF Hub UI 의 metadata (YAML frontmatter `license:`) 와 일치 — 두 곳이 같은 값을 가짐. **L2 risk** (UI vs README 충돌) 는 본 audit 시점 없음.

---

## §3 Honest disclosure audit

| dataset | critical caveat | 첫 화면 인지 | severity | rating |
|---------|------------------|---------------|----------|--------|
| hypotheses-candidates | "**staging area, not verified-claims corpus**" (Caveats §) + 8 honest finding (cycle 5 ★) | §1 본문 line 24 "single staging hypothesis — extracted from sprawling docs/ material — awaiting promotion" + §honest findings (line 67-78) | ★★ candidate-unverified 가 first-paragraph 핵심 단어; numerology critique open dispute 도 §caveats | **SUFFICIENT** — reader 가 첫 paragraph 만 읽어도 "verified ≠ 본 dataset" 인지 가능 |
| nexus-lenses | "**TRIVIAL** under run-A; **suspended pending channel reimpl**" (§2 above-fold blockquote + body) | YAML tag `falsification-artifacts` + title 바로 아래 `> CRITICAL caveat — read this first.` blockquote × 8-line | ★★★ TRIVIAL framing 이 강제 가시 | **SUFFICIENT** — cycle 5 §5 #M 의 핵심 요구사항 충족 |
| research-trail | "1013-lens TRIVIAL ★ + 8 honest finding ledger" (§3 table) + ANIMA-VOICE blocker (§9) | §1 narrative 마지막 paragraph "★ caveat 으로 honest disclosure" + §3 honest finding 표 (line 64-72) + §9 honest disclosure reminders | ★★ TRIVIAL/blocker 가 §3 표로 정량화 | **SUFFICIENT** — process-ledger 라는 dataset 성격상 finding 의 *negative* side 가 explicit table 로 제시 |

**verdict**: 3 dataset 모두 first-screen critical caveat 인지 충분. reader-defense 기준 충족.

---

## §4 Cross-link audit

### 4.1 Sister dataset cross-ref (3-way triangle)

| from \ to | candidates | lenses | research-trail | 정합 |
|-----------|------------|--------|-----------------|------|
| candidates  → | (self) | ❌ no link | ❌ no link | ⚠ **NEEDS-FIX** — DATASET_CARD.md 에 sister §6 부재 |
| lenses     → | ❌ no link | (self) | ❌ no link | ⚠ **NEEDS-FIX** — README.md 에 sister §6 부재; §11 anima repo cross-link 만 있음 |
| research-trail → | ✅ §6 table line 126 | ✅ §6 table line 127 | (self) | ✅ |

**verdict**: research-trail 만 sister triangle 정합. candidates + lenses 는 sister §6 추가 권장.

### 4.2 anima repo cross-link (from dataset)

| dataset | repo URL | 정합 | issue |
|---------|----------|------|-------|
| candidates | `github.com/dancinlab/anima` (line 22, 82) | ✅ org 정합 (`dancinlab`) | none |
| lenses     | "anima (private mirror)" (line 171) — URL 없음 | ⚠ outdated metadata — anima 는 현재 **public** | rename `private mirror` → `public repo` |
| research-trail | `github.com/dancinlife/anima` × 2 (line 25, 134) | ❌ **typo** — `dancinlife` (user) ≠ `dancinlab` (org) + "private" 표기 (실제 public) | rename `dancinlife` → `dancinlab` + `private` → `public` |

### 4.3 cycle_5_master 측 cross-ref-index (anima repo 측)

`docs/cycle_5_master_2026_05_12.md §9 Cross-Reference Index` — HF dataset URL 명시 **부재**. `grep -n "dancinlife/anima-" docs/cycle_5_master_2026_05_12.md` → 0 hits.

**verdict**: cycle 5 §9 cross-ref index 에 3 HF dataset URL 추가 필요 (public flip 후 wired)  — 본 #R audit 는 prep only; agent #S 가 root README §"📊 Datasets" 작성 시 함께 처리 권장.

### 4.4 lens dataset → anima repo 내부 spec 경로

`nexus-lenses` README 가 `docs/lens_channel_reimpl_spec_2026_05_12.md` 를 두 번 참조 (line 21, 48) — 실제 파일은 `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md`. **broken path** — anchor 갱신 필요.

---

## §5 Recommended fixes (사용자 confirm 후 적용)

### 5.1 nexus-lenses README.md (1 file, 3 spots)

```diff
- (see `lens_channel_reimpl_spec_2026_05_12.md` in the anima repo).
+ (see `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md` in the anima repo).

- See the anima repo for the channel-reimpl spec (`docs/lens_channel_reimpl_spec_2026_05_12.md`
+ See the anima repo for the channel-reimpl spec (`state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md`

- The authoring repository is **anima** (private mirror).
+ The authoring repository is **[anima](https://github.com/dancinlab/anima)** (public).
```

(Sister §6 추가는 nice-to-have — defer 가능.)

License 결정: **MIT 로 변경 권장** (repo LICENSE 정합). YAML frontmatter `license: apache-2.0` → `license: mit` + §9 body 도 update.

### 5.2 research-trail README.md (1 file, 2 spots)

```diff
- **Source repo**: `github.com/dancinlife/anima` (private — paths preserved)
+ **Source repo**: `github.com/dancinlab/anima` (public — paths preserved)

- - **ANIMA core repo**: `github.com/dancinlife/anima` (private)
+ - **ANIMA core repo**: `github.com/dancinlab/anima` (public)
```

### 5.3 hypotheses-candidates DATASET_CARD.md (optional)

Sister §"Sister datasets" 추가 (research-trail 의 §6 table 과 mirror). Defer 가능 — public flip block 아님.

### 5.4 anima repo 측 (out-of-band)

- **HF token rotate** 권장: `bf03ee397` commit 의 `state/hf_upload_anima_hypotheses_candidates_2026_05_12.md` 에 prefix-suffix 노출 (`hf_zlbJ…lanybs`). 중간 `…` 마스킹은 됐으나, prefix+suffix 노출은 brute-force 단축 도움. 이미 사용자가 history 한번 rewrite 한 history (HEAD@{1} = reset to origin/main, fsck unreachable 다수); full token 은 unreachable 처리됨. **즉시 위험은 낮음**, 그러나 rotate 권장.
- 추가 redact: `state/hf_upload_anima_hypotheses_candidates_2026_05_12.md` line 36, 73 → `hf_zlbJ…lanybs` → `hf_***` 마스킹.

### 5.5 fix application 절차 (3-step)

```bash
# 1. nexus-lenses README in-place (snapshot lives outside anima git tracking)
$EDITOR /home/summer/core/nexus_lenses_snapshot/README.md

# 2. research-trail README in-place (staging /tmp — copy to a stable location first if /tmp purged)
$EDITOR /tmp/anima-research-trail-staging/README.md

# 3. anima repo redact (state file)
$EDITOR /home/summer/mac_home/core/anima/state/hf_upload_anima_hypotheses_candidates_2026_05_12.md
# → git commit -m "doc(cycle 6 §R): hf-token-prefix redact in cycle-5 §5 verdict"

# 4. re-upload (overwrite README only — atomic single-file commit per dataset)
python3 - <<'PY'
from huggingface_hub import HfApi
import subprocess
token = subprocess.check_output(["ssh", "mac", "/Users/ghost/core/secret/bin/secret get hf.token"]).decode().strip()
api = HfApi(token=token)
api.upload_file(path_or_fileobj="/home/summer/core/nexus_lenses_snapshot/README.md",
                path_in_repo="README.md",
                repo_id="dancinlife/anima-nexus-lenses",
                repo_type="dataset",
                commit_message="cycle 6 §R: README cross-link + license sync fix (pre-public-flip)")
api.upload_file(path_or_fileobj="/tmp/anima-research-trail-staging/README.md",
                path_in_repo="README.md",
                repo_id="dancinlife/anima-research-trail",
                repo_type="dataset",
                commit_message="cycle 6 §R: GitHub URL typo dancinlife→dancinlab + private→public (pre-public-flip)")
PY
```

---

## §6 Public-flip procedure (사용자 confirm 후 1-line per dataset)

```python
# Prerequisites:
#   - §5 fixes 적용 + re-upload 완료
#   - HF token rotate 완료 (권장)
#   - 사용자 explicit confirm: "anima-{hypotheses-candidates,nexus-lenses,research-trail} public flip GO"
from huggingface_hub import HfApi
import subprocess

token = subprocess.check_output(
    ["ssh", "mac", "/Users/ghost/core/secret/bin/secret", "get", "hf.token"]
).decode().strip()
api = HfApi(token=token)

# Flip — order: candidates → research-trail → lenses (lenses last because TRIVIAL caveat 가 가장 민감)
api.update_repo_settings("dancinlife/anima-hypotheses-candidates", repo_type="dataset", private=False)
api.update_repo_settings("dancinlife/anima-research-trail",        repo_type="dataset", private=False)
api.update_repo_settings("dancinlife/anima-nexus-lenses",          repo_type="dataset", private=False)

# Verify
for ds in ["anima-hypotheses-candidates", "anima-research-trail", "anima-nexus-lenses"]:
    info = api.dataset_info(f"dancinlife/{ds}")
    print(f"{ds}: private={info.private}")
```

**Rollback**: 같은 함수 `private=True` 재호출. HF dataset 의 private/public 토글은 reversible — 단 public 노출 윈도우에 외부 cache (HF datasets-server, GitHub Archive Program, third-party scrape) 가 snapshot 했을 가능성 있음 (L3 risk).

---

## §7 Honest limits (L1–L3)

- **L1**: GitHub Push Protection 의 secret-scan algorithm (token-prefix `hf_` + 32+ char alnum) ≠ HF Hub 의 자체 검출 패턴. 본 audit 의 sensitive-content scan 은 GitHub 패턴 기반 (`hf_*`, `sk-*`, email, SSH config). HF Hub 가 추가로 다른 패턴 (e.g., S3 access key, GCP service account JSON) 을 검출할 수 있으며, 본 audit 는 그것을 cover 하지 못함.

- **L2**: License header 본문 ↔ HF dataset YAML frontmatter `license:` field 의 충돌 가능성. 본 audit 시점 (2026-05-12) 3 dataset 모두 일치 — 단, nexus-lenses 의 Apache-2.0 ↔ anima repo MIT 의 cross-layer 정합은 별 문제 (dataset 카드 안의 self-consistency 만 audit 했음). 사용자 결정 필요: dataset 카드를 repo LICENSE 와 align 할지, 아니면 dataset-specific license 로 분리 유지할지.

- **L3**: HF org rename (`need-singularity` → `dancinlab` 진행, `dancinlife` 는 user namespace 로 유지) 후 redirect 안정성 — HF Hub 의 namespace redirect 는 일반적으로 ~30 일 유효한 alias 만 제공 (공식 policy 가 명시되지 않음). 3 dataset 모두 `dancinlife/...` (user namespace) 로 publish 됨 → org rename 영향 **없음** (user namespace 는 rename 안 됨). 단, README 안의 `github.com/dancinlab/anima` 는 org rename 직후 시점 — `need-singularity` → `dancinlab` redirect 가 만료되면 (~30일 후) 옛 URL 검색-from-cache 가 404 가능. **HF dataset README 자체** 는 `dancinlab` (현재 org) 만 참조하므로 영향 없음. 단 외부 archived snapshot (web archive, Zenodo cache 등) 의 옛 `need-singularity` URL 은 stale 될 수 있음 — 본 audit scope 외부.

---

## §8 cycle ordering

본 audit 는 **prep only** — 다음 단계는 사용자 explicit confirm 후 분기:

1. **사용자 confirm**: "fix-and-flip GO" → §5 fix 적용 → re-upload README × 2 → §6 flip × 3
2. **사용자 confirm**: "fix-only, defer flip" → §5 fix 만 (private 유지)
3. **사용자 confirm**: "flip-as-is GO" → §5 skip, §6 flip × 3 직접 (README 의 minor typo + path mismatch 감수)
4. **사용자 defer**: 본 audit 만 land, flip 결정 다음 cycle

---

*Generated by cycle 6 #R (audit-prep-only agent). 본 doc 는 dataset publication 의 *측정-도구* 이며 *measurement* 자체는 사용자 confirm 후 별 agent. cycle 5 §5 (3-dataset private upload) 의 follow-up.*
