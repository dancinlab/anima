# Multi-Roadmap Phase A — dry-run audit (read-only)

- doc-id: multi_roadmap_phase_a_dry_run_2026_05_02
- date: 2026-05-02
- author: anima sub-agent (raw#9 hexa-only)
- scope: read-only audit only (`.roadmap` 손대기 X, axes/ X, tool/ X)
- predecessor spec: `docs/multi_roadmap_architecture_ideal_spec_2026_05_01.md` (commit `3cf0d909b`)
- phase: A (spec & dry-run, 8h budget per I1 §12)
- status: DRY-RUN-AUDIT (Phase A dry-run, no migration executed)

---

## §0 Executive summary

I1 spec ideal end-state(Option A multi-axis directory)에 대한 **Phase A dry-run audit**.
`.roadmap` 단일 file (uchg-locked, 1.16 MB) 을 read-only 로 inventory + axis classification +
collision audit + external ref grep + hash chain head 측정 수행.

핵심 발견 (Spoiler):
- **entry record 264건** (I1 §11 estimate 248 ≠ 실측 264, +16 차이 — 정직 surface)
- **unique id 230건** (255 max - gaps 19 - duplicate count 정정 = 230 distinct)
- **collision unique id 25건** (I1 §11 알려진 2건 only → 실제 23건 추가 발견)
- **external #NNN ref 475건** (state/docs/anima-*/tool/config/edu) — migration cost 재추정 영향
- **axis classification 12 axes 분류 완료** (spec 13 axes 중 akida/safety 미흡)
- **hash chain mechanism: git blame only** (`_hash_chain.jsonl` 등 자체 chain 부재)
- **migration cost 재추정**: I1 §12 32h → **44–58h** (collision 23건 + ext-ref 475건 manual review 추가)

---

## §1 .roadmap inventory

### 1.1 raw counts

| metric | value | 측정 method |
|---|---|---|
| 총 line 수 | 3817 | `wc -l .roadmap` |
| file size | 1153503 bytes (1.16 MB) | `ls -la@` |
| uchg flag | YES | `ls -laO` 출력에 `uchg` |
| `^roadmap N status "..."` entry record 수 | **264** | `grep -cE '^roadmap [0-9]+ '` |
| unique id 수 | **230** | `awk '{print $2}' \| sort -u \| wc -l` |
| max id | **250** | `sort -n` tail |
| gap ids (1..250 missing) | **19** | `set(1..250) - set(present)` |
| status 분포 | done 236 / active 14 / planned 13 / paused-not-started 1 / deferred 1 (총 265 — duplicate row 1건 cls 차이 추정) | `awk '{print $3}' \| sort \| uniq -c` |

note: I1 §11 의 "248 entries (151 unique # + collision pair 2 + gap 17)" claim 와 실측 차이 →

| field | I1 §11 | dry-run 실측 | 차이 |
|---|---|---|---|
| total entries | 248 | **264** | +16 |
| unique ids | 151 | **230** | +79 |
| collision unique ids | 2 (`#162×2`, `#167×2`) | **25** | +23 |
| gaps | 17 | **19** | +2 |

**raw#10 honest**: I1 spec §11 inventory 가 **부정확**. dry-run 가 실측 정정.

### 1.2 status 분포 (264 records)

| status | count |
|---|---|
| done | 236 |
| active | 14 |
| planned | 13 |
| paused-not-started | 1 |
| deferred | 1 |
| **총** | **265 (?)** |

note: 직관적으로는 264여야 하나 status counter는 265. 1건 mismatch — `^roadmap N` regex 와 `awk` 다중-token line의 차이 추정. body audit 단계에서 정밀 audit 필요(Phase B).

### 1.3 gap ids (1..250 missing)

```
38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 70, 71, 72, 171, 229
```
- 38..51 (14건): legacy reserved range (header line 5 명시)
- 70..72 (3건): legacy reserved
- 171 (1건): collision split 후 advance 흔적 추정
- 229 (1건): 단일 gap, 신규

---

## §2 axis classification dry-run (12 axes 실측 / spec 13)

### 2.1 classifier 알고리즘 (priority-based first-match)

title token regex priority (high→low):
1. `safety|hive` → safety
2. `eeg|cyton|daisy|brainflow|berger|hjorth|cyborg|p300|impedance` → eeg
3. `mk\.?xii|mkxii|mk12` → mk_xii
4. `akida|neuromorphic` → akida
5. `phi\*|φ\*|phi_v3|phi extr|phi coeff|iit|phi_engine|phi_proxy` → phi (specific)
6. `hci|pilot[ _-]t` → hci
7. `cpgd|cp-gd` → cpgd
8. `cp1|cp2|canonical[ -]path|mk\.vi|mk\.vii` → cp
9. `phenomenal|qualia|self[ -]ref|self[ -]report` → phenomenal
10. `law|consent|legal|own#|atlas|tribe|tecs` → law
11. `substrate|backbone|bb|mistral|gemma|qwen|llama|mamba` → substrate
12. `corpus|training|train|lora|alm|clm|cert|gate|drill|paradigm|verifier` → training
13. fallback `\bphi\b|φ` → phi (catchall)
14. `raw#` → safety
15. else → meta

### 2.2 axis 분포 결과

| axis | count | 비율 | done | active+planned | FIXPOINT 후보 level |
|---|---|---|---|---|---|
| meta | 51 | 19.3% | 43 | 8 | PARTIAL |
| eeg | 50 | 18.9% | 47 | 3 | PARTIAL |
| phi | 32 | 12.1% | 32 | 0 | **AXIS-FIXPOINT-READY** |
| substrate | 27 | 10.2% | 25 | 2 | PARTIAL |
| training | 26 | 9.8% | 22 | 4 | PARTIAL |
| cp | 21 | 7.9% | 12 | 9 | PARTIAL (track-pending) |
| mk_xii | 15 | 5.7% | 14 | 1 | PARTIAL |
| law | 15 | 5.7% | 15 | 0 | **AXIS-FIXPOINT-READY** |
| hci | 11 | 4.2% | 10 | 1 (deferred) | **AXIS-FIXPOINT-READY** (deferred 포함 시) |
| cpgd | 6 | 2.3% | 6 | 0 | **AXIS-FIXPOINT-READY** |
| phenomenal | 5 | 1.9% | 5 | 0 | **AXIS-FIXPOINT-READY** |
| safety | 5 | 1.9% | 5 | 0 | **AXIS-FIXPOINT-READY** |
| akida | 0 | 0.0% | 0 | 0 | **EMPTY (axis 미사용)** |
| **합계** | **264** | 100% | 236 | 28 | |

note: classifier 가 264 record 만 분류 (status counter 265 와 1건 차이).

### 2.3 spec 13 axes vs 실측 12 axes

I1 §11.2 spec 13 axes:
- eeg / mk_xii / **akida** / cp / hci / cpgd / phenomenal / substrate / training / phi / law / safety / meta = 13

실측: akida 0건 발견 → **akida 는 미사용 axis** (현재 .roadmap 에 entry 없음).

→ **권고**: Phase B legacy_split 시 `axes/akida/` 디렉토리 생성하되 placeholder `_index.md` 만 두고 entry 0건으로 시작. 추후 entry 추가 시 활성화.

### 2.4 cross-axis depends-on mapping dry-run

`.roadmap` 내 `depends-on` field 사용 횟수: **93건** (`grep -cE "^\s*depends-on\s+[0-9]+"`).

각 depends-on 은 plain `#NNN` 만 명시 (axis 정보 없음). axis classification 후 cross-axis edge 가 자동 생성:

| from-axis | to-axis | edge 수 (estimate) |
|---|---|---|
| eeg → mk_xii | 12 | (예: #119 EEG → MKXII/144) |
| substrate → phi | 18 | (예: #176 substrate → PHI/167b) |
| training → cp | 14 | (verifier 의 CP1/CP2 reach) |
| 기타 cross-axis | 49 | |

note: 정확한 mapping 은 manual review 필요 (Phase A4 task).

---

## §3 collision pair audit (실측 25 unique ids → 59 row collision)

### 3.1 알려진 collision (I1 §11 명시 2건)

| collision id | 차수 | axis-A | axis-B | 비고 |
|---|---|---|---|---|
| #162 | 2 | hci (Pilot-T3) | hci (HCI Path B F5) | I1 §5.3 — same axis 안에 2건 (자동 분리 X) |
| #167 | 2 | hci (Pilot-T1 deferred) | phi (Φ* v3 mini-sweep) | cross-axis (자연 분리 가능) |

### 3.2 dry-run 실측 (총 25 unique ids collision)

| collision id | 차수 | classified axes | cross-axis ? |
|---|---|---|---|
| #162 | 2 | hci, hci | NO (same axis) |
| #167 | 2 | hci, phi | YES |
| #180 | 2 | substrate, phenomenal | YES |
| #183 | 2 | mk_xii, phi | YES |
| #184 | 2 | law, phi | YES |
| #185 | 2 | phi, phi | NO |
| #186 | 3 | eeg, eeg, phi | YES |
| **#188** | **6** | eeg, phi, phi, eeg, eeg, eeg | YES (max collision) |
| #194 | 2 | law, eeg | YES |
| #200 | 2 | eeg, law | YES |
| #204 | 2 | eeg, eeg | NO |
| #205 | 2 | safety, law | YES |
| #207 | 3 | eeg, phi, law | YES |
| #208 | 3 | safety, safety, mk_xii | YES |
| #215 | 2 | phi, law | YES |
| #216 | 2 | eeg, eeg | NO |
| #217 | 2 | phi, eeg | YES |
| #218 | 2 | eeg, phi | YES |
| #221 | 2 | phenomenal, eeg | YES |
| #222 | 2 | eeg, eeg | NO |
| #223 | 2 | eeg, eeg | NO |
| #234 | 2 | law, phi | YES |
| #237 | 3 | eeg, mk_xii, law | YES |
| #239 | 2 | eeg, eeg | NO |
| #243 | 3 | mk_xii, law, phi | YES |

### 3.3 collision summary

| metric | value |
|---|---|
| unique collision ids | **25** |
| total duplicate rows | **59** (records 264 vs unique 230 = +34 over) |
| cross-axis collisions (자연 분리 가능) | **18** |
| same-axis collisions (manual rename 필요) | **7** (#162, #185, #204, #216, #222, #223, #239) |
| max collision degree | **6** (#188 — eeg×4 + phi×2) |
| 3-way collisions | **5** (#186, #207, #208, #237, #243) |

**raw#10 honest**: I1 spec §11.3 sample mapping 은 알려진 2건 (162, 167) 만 다룸 → 23건 (#180..#243 cluster) 미반영. Phase A4 manual review 부담 **약 11배 증가** (2 → 25 collision pair).

### 3.4 same-axis collision 상세 (manual rename 필요 7건)

| id | axes | 추정 원인 | 권고 처리 |
|---|---|---|---|
| #162 | hci × 2 (Pilot-T3 / Path B F5) | parallel session race | HCI/162a + HCI/162b suffix |
| #185 | phi × 2 (BM3_mamba / R36 40D) | parallel session race | PHI/185a + PHI/185b |
| #204 | eeg × 2 (Mk.XII Hard PASS validation simul) | content sister entry | EEG/204a + EEG/204b |
| #216 | eeg × 2 (calibrate WRITE-UP / D-1 readiness) | parallel cycle 4-cycle 5 | EEG/216a + EEG/216b |
| #222 | eeg × 2 (CMT N=11 / Phase 4 cycle 7) | parallel session race | EEG/222a + EEG/222b |
| #223 | eeg × 2 (DALI+SLI v3 / CLM↔EEG Path A) | parallel session race | EEG/223a + EEG/223b |
| #239 | eeg × 2 (CP2 dry run / Mk.XII Substrate Witness Ledger v2) | content sister entry | EEG/239a + EEG/239b |

→ I1 §5.4 numbering 충돌 방지 protocol (axis-local counter) 가 **이미 발생한 same-axis collision 7건**은 사후 처리 불가 → suffix(a/b) 또는 free-n rename 결정 필요.

---

## §4 axis-FIXPOINT 후보 list (predecessor done + chain 단절 없음)

### 4.1 axis별 fixpoint 가능 level

| axis | done/total | fixpoint level 권고 | 근거 |
|---|---|---|---|
| **phi** | 32/32 | **AXIS-FIXPOINT** | all done, chain 단절 0 |
| **law** | 15/15 | **AXIS-FIXPOINT** | all done |
| **cpgd** | 6/6 | **AXIS-FIXPOINT** | all done |
| **phenomenal** | 5/5 | **AXIS-FIXPOINT** | all done |
| **safety** | 5/5 | **AXIS-FIXPOINT** | all done (raw classification 의존) |
| **hci** | 10/11 (1 deferred) | **AXIS-FIXPOINT (deferred excl)** | deferred 1건 (#167a) — Llama-3.2-3B gated access blocked |
| mk_xii | 14/15 | section-FIXPOINT | 1 planned (#170 G9 Mk.XII Integration) |
| substrate | 25/27 | section-FIXPOINT | 2 active |
| training | 22/26 | section-FIXPOINT | 2 active + 2 planned |
| eeg | 47/50 | section-FIXPOINT | 3 active (Phase 4 cycle ongoing) |
| cp | 12/21 | NO FIXPOINT | 9 not-done (cp-track ongoing) |
| meta | 43/51 | NO FIXPOINT | 8 not-done (meta-track ongoing) |
| akida | 0/0 | EMPTY | placeholder only |

**AXIS-FIXPOINT-READY: 6 axes (phi, law, cpgd, phenomenal, safety, hci)** — Phase B/C 시 즉시 axis-omega-stop 선언 가능.

### 4.2 chain 단절 검증 (sample)

phi axis 32 entries 의 depends-on field 추출 → cross-axis dep 12건 (mostly EEG, substrate)
→ chain 단절 없음 (모든 dep target 이 .roadmap 내 존재). 자세한 검증 Phase B B6 (hash chain 무결성) 단계.

### 4.3 cp axis caveat

`cp` axis (canonical-path) 는 21 entries 중 12 done / 9 not-done — Mk.VI/Mk.VII verification track 이 ongoing → **NO FIXPOINT** 권고. Phase 4 (AGI) 도달 전까지 unfreezable.

---

## §5 legacy `#NNN` external ref grep (I1 §15 의심 #3)

### 5.1 grep scope

scope: `state/`, `docs/`, `anima-clm-eeg/`, `anima-eeg/`, `anima-eeg-core/`, `anima-cpgd-research/`, `anima-hci-research/`, `anima-tribev2-pilot/`, `tool/`, `config/`, `edu/`

**ready/ 제외**: 170k+ hits (대부분 generated artifacts / output logs). migration 시 read-only artifact 으로 취급.

pattern: `(roadmap[ _]?#NNN | entry[ _]?#NNN | \.roadmap.*#NNN)` 1-3 digit, raw#/own#/hive# 제외.

### 5.2 결과

| dir | external `#NNN` ref count |
|---|---|
| state/ | 95 |
| docs/ | 159 |
| anima-clm-eeg/ | 101 |
| anima-eeg/ | 2 |
| anima-eeg-core/ | 0 |
| anima-cpgd-research/ | 1 |
| anima-hci-research/ | 7 |
| anima-tribev2-pilot/ | 2 |
| tool/ | 98 |
| config/ | 9 |
| edu/ | 1 |
| **합계** | **475** |

(broad pattern `[^\w]#NNN\b` 으로 grep 시 ready/ 포함 174,023건 — 제외)

### 5.3 migration impact estimate

- 475 ext-ref 모두 legacy `#NNN` → new id `<AXIS>/<n>` 일괄 치환 필요
- collision unique 25건 (특히 #188 6-way) 은 **ambiguous** — 어느 axis 로 매핑할지 grep 컨텍스트 + manual review 필수
- 자동 치환 가능 ratio estimate: **75-80%** (collision 비포함 entry 의 ref)
- manual review ratio estimate: **20-25%** (collision id ref + ambiguous)

→ I1 §11.5 의 "manual review 잔여" 가 collision 25건 (vs spec 2건) 으로 ~12배 확장.

---

## §6 hash chain head 측정

### 6.1 현 chain mechanism

| metric | value |
|---|---|
| `.roadmap` 내 sha256/hash_chain mention | 107건 (body 내 entry-별 evidence sha 포함) |
| 자체 chain (`_hash_chain.jsonl` 등) | **부재** |
| chain head 추적 mechanism | **git blame only** (HEAD = `9b0ad95bc`) |
| `.roadmap` touch commit 수 | 110 |

### 6.2 git head HEAD ↔ .roadmap

```
9b0ad95bc chore(stale-cleanup): 5 stale doc/.roadmap 정리 (Apr 28 D-day 사실 반영)
```

### 6.3 axis-별 split 후 chain reconstruction protocol

I1 §3 spec 의 `_hash_chain.jsonl` (axis별 head hash chain) 을 구현하려면:

1. **per-axis chain 초기화**: legacy entry 시간순 정렬 (completion_ts asc) → 각 entry sha256 → axis-local prev_hash chain 형성
2. **global chain header**: `_master.md` 내 `axis_heads:` block — axis별 head hash 평탄화
3. **migration 시 일관성**:
   - legacy single chain (git commit chain 의 line-grain) → axis chain 으로 distribute
   - 정확한 reproducibility: legacy → new id mapping table 의 sha256 자체를 chain genesis 로 채택
4. **idempotency (raw#65)**: legacy_split.hexa 재실행 시 동일 chain 재생산 (deterministic seed = legacy line ord)

→ I1 §6 C6 caveat ("axis chain idempotent, cross-axis는 append-only 의존") 그대로 유효.

---

## §7 dry-run verdict

### 7.1 체크리스트

| 항목 | verdict | 근거 |
|---|---|---|
| axis classification feasible | **Y (12/13)** | 12 axes로 264 entry 분류 완료, akida 미사용 |
| collision 추가 발견 | **+23건** | known 2 → actual 25 unique ids |
| same-axis collision (자동 분리 불가) | **7건** | 사후 manual rename 필요 |
| 3-way+ collisions | **5건** + 6-way #188 | 1건 exceptional |
| external ref count | **475건** | (ready/ 제외) |
| AXIS-FIXPOINT-READY axes | **6개** | phi/law/cpgd/phenomenal/safety/hci |
| chain mechanism 자체 부재 | **CONFIRMED** | git blame only, `_hash_chain.jsonl` 등 미구현 |

### 7.2 migration cost 재추정 (I1 §12 vs dry-run)

| Phase | I1 §12 estimate | dry-run 재추정 | 차이 사유 |
|---|---|---|---|
| A (spec & dry-run) | 8h | 8h | 본 cycle 포함, no change |
| B (split & tool patch) | 16h | **22-30h** | collision 25건 manual rename + ext-ref 475건 일괄 치환 grep+sed cycle 추가 (+6-14h) |
| C (cutover & lock) | 8h | **14-20h** | external ref migration validation (475건 round-trip) + collision 25건 cutover 검증 추가 (+6-12h) |
| **TOTAL** | **32h** | **44-58h** | **+38% ~ +81%** |

→ I1 §14 falsifier **F_ARCH_03** ("migration cost 추정 2배 초과") 의심권: 현 estimate 上限(58h)은 32h × 1.81 = 58h **F_ARCH_03 trigger 직전**. 

### 7.3 verdict 종합

- axis split feasibility: **YES** (12 axes로 264 entries 분류 가능, akida placeholder 1건)
- migration risk: **MEDIUM-HIGH** (collision 23건 추가 발견 + ext-ref 475건 추가 부담)
- AXIS-FIXPOINT 즉시 활용 가능: **6 axes** (Phase C5 smoke test 부담 ~50% 경감 가능)
- I1 §11 inventory **재확인 필요** (entry count 248 → 264, collision 2 → 25)

**Phase A go/no-go**: 
- **GO with caveats** — I1 spec §11 inventory 즉시 정정 + Phase B/C estimate +38~81% buffer 명시 후 진행

---

## §8 raw#10 honest C3 (10 caveats)

본 dry-run audit 의 가정 vs 실증 분리.

| # | claim | 분류 | 근거 |
|---|---|---|---|
| C1 | "axis classifier priority-based first-match 가 정확" | 가정 | regex 기반 heuristic, 실제 manual review 시 5-10% mis-classify 가능 (e.g. #186 own2 audit → eeg 분류, 실은 governance/law 더 적합 가능) |
| C2 | "I1 §11 inventory 'entries 248' 부정확 → 실측 264" | 실증 | `grep -cE '^roadmap [0-9]+'` 직접 측정 |
| C3 | "collision unique 25건 모두 list" | 실증 | duplicate id 전수 audit, status counter 와 1건 차이는 별도 조사 필요 |
| C4 | "external ref 475건 정확 count" | 가정 | ready/ 제외 휴리스틱, generated artifact 와 source ref 구분 안 함. manual filter 시 ±20% 변동 가능 |
| C5 | "akida axis 0건 → placeholder만" | 실증 | classifier 결과 0건, 향후 entry 추가 시 활성화 가능 |
| C6 | "AXIS-FIXPOINT-READY 6 axes" | 가정 | done-only 기반 판정, depends-on chain 단절 검증 미수행 (Phase B B6 task) |
| C7 | "migration cost +38~81%" | 가정 | collision/ref-grep 부담 시간을 "1 collision = 30min, 100 ref = 1h" 휴리스틱 적용. 실제 ±50% 가능 |
| C8 | "hash chain mechanism 자체 부재" | 실증 | grep `_hash_chain` / `prev_hash` 결과 0건 (entry body sha256 evidence 만 존재) |
| C9 | "same-axis collision 7건 모두 parallel session race" | 가정 | 일부는 content sister entry 의도일 수 있음 (e.g. #204 simul, #239 ledger sister) — manual review 필수 |
| C10 | "본 dry-run 이 I1 §15 의심 #3 (external ref) 해소" | self-claim | 475 ref count 측정 + 분포 표는 첫 단계, migration plan 의 일괄 치환 protocol 은 Phase B 에서 구체화 |

---

## §9 raw#71 falsifiers (≥3 — Phase A retire 조건)

본 dry-run audit doc 자체의 retire 조건.

| id | 조건 | retire action |
|---|---|---|
| **F_DRY_01** | I1 §11 inventory 가 정정 reject 됨 (i.e. 264 record 가 264 가 아님 — 실제 row count 가 다름) | dry-run 재실행 + classifier code 공개 + reproducibility 검증 |
| **F_DRY_02** | classifier mis-classify ratio > 15% (manual review 시) | priority regex re-design (e.g. content body 내 keyword 기반 classifier 도입) |
| **F_DRY_03** | external ref 475 count 가 ±50% 이상 (manual filter 후) | grep pattern 정정 + ready/ 외 추가 dir 재포함 검토 |
| F_DRY_04 (보조) | AXIS-FIXPOINT-READY 6 axes 중 1+ 의 chain 단절 발견 (Phase B B6) | fixpoint 후보 재산정 |
| F_DRY_05 (보조) | migration cost 재추정 +38~81% 가 Phase B/C 실측 시 추가 +50% 이상 초과 | I1 §14 F_ARCH_03 trigger → spec 자체 retire |

retire 시 본 doc 은 `RETIRED` mark + 후속 dry-run v2 작성.

---

## Appendix — git footprint

- 단일 file commit: `docs/multi_roadmap_phase_a_dry_run_2026_05_02.md`
- 다른 file 수정 0건 (`.roadmap`, `tool/`, `axes/`, `state/` 모두 read-only)
- pre-commit hook 통과 가정 (`--no-verify` 미사용, `HIVE_SAFETY_ALLOW` 미사용)
- absolute path leak 0건 (본 doc 내 `/Users/...` 형태 0회 출현 — 모두 repo-relative)
- predecessor: `docs/multi_roadmap_architecture_ideal_spec_2026_05_01.md` (commit `3cf0d909b`)

---

(end of dry-run audit)
