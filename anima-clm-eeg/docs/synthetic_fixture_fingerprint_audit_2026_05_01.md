# synthetic_16ch_v1.json fingerprint audit (raw#9 hexa-only / raw#10 honest)

- date: 2026-05-01
- scope: read-only audit of `<repo-root>/anima-clm-eeg/fixtures/synthetic_16ch_v1.json` vs `.roadmap` evidence-block 인용
- trigger: A3 audit (commit `867392918`) 가 file 내부 fingerprint(`2960889009`)와 #157 evidence block의 `831a1b5d` 를 mismatch 로 신고
- raw classes: raw#9 (hexa-only docs) · raw#10 (honest C3 read-only 한계) · raw#71 (falsifier — fingerprint mismatch 시 byte-identical reproducibility 의심)

## §1. 측정값 (file 직접 read, 2026-05-01)

| metric | value |
|---|---|
| file path | `<repo-root>/anima-clm-eeg/fixtures/synthetic_16ch_v1.json` |
| file size | 2393 bytes |
| **sha256** | `b6f1cc8669bf5bb5a6627bb55f812d48aa2f4bbed765b4e74097f205d78dccc7` |
| sha256 prefix-8 | `b6f1cc86` |
| **internal `fingerprint` field** | `2960889009` (FNV-32 deterministic, band-power derived) |
| `version` | `v1` |
| `seed` | `20260426` |
| `sample_rate_hz` | `125` (post axis-89 correction, 250→125) |
| `window_samples` | `500` (post axis-89 correction, 1000→500) |
| `n_channels` | `16` |
| `raw_rank` | `9` |

## §2. roadmap 인용 수집 (4 entries — #157, #170, #172, #173 + 보조 #174/#216/#217/#223/#237)

| entry | quoted token | location | claimed semantic |
|---|---|---|---|
| **#157** (line 2073) | `fixtures/synthetic_16ch_v1.json (831a1b5d)` | `evidence` block | sha256 prefix-8 (다른 file 와 동일 패턴: `clm_eeg_synthetic_fixture.hexa (sha256 0dfe2c2e)`, `clm_eeg_p1_lz_pre_register.hexa (cd17abd8)` 등) |
| **#170** (line 2338-2350) | (no `synthetic_16ch_v1.json` reference) | — | G9 DAG cascade — fixture 직접 인용 없음 |
| **#172** (line 2358) | (no `synthetic_16ch_v1.json` reference) | — | Mk.XII pre-flight — fixture 직접 인용 없음 |
| **#173** (line 2367-2378) | (no `synthetic_16ch_v1.json` reference) | — | S7 cusp_depth — fixture 직접 인용 없음 |
| #174 (line 2387, 2391, 2393) | `canonical fixture fingerprint=2960889009` · `<repo-root>/anima-clm-eeg/fixtures/synthetic_16ch_v1.json (fingerprint 2960889009)` | `evidence` + `depends-on` + `refs` | internal fingerprint 직접 인용 (file 값과 일치) |
| #204 (line 2943, 2964) | `fingerprint=2960889009` × 2 | `evidence` + `refs` | internal fingerprint (file 값과 일치) |
| #216 (line 3207) | `(sample_rate_hz: 250 L10)` | `refs` | (axis-88 시점 정정 직전 상태 — outdated) |
| #217 (line 3298, 3305) | `synthetic fixture sha 831a1b5d49234d30… → b6f1cc8669bf5bb5…` · `(sha 831a1b5d… → b6f1cc8669bf5bb5a6627bb55f812d48aa2f4bbed765b4e74097f205d78dccc7, fingerprint 2960889009 PRESERVED)` | `evidence` + `refs` | **결정적 단서**: sha256 변경 (831a1b5d → b6f1cc86) + fingerprint 보존 명시 |
| #223 (line 3368) | `fixtures/synthetic_16ch_v1.json 831a1b5d → b6f1cc86` | `evidence` (v1.0→v1.1 sha drift table) | sha256 prefix-8 transition 명시 |
| #237 (line 3539) | `fixtures/synthetic_16ch_v1.json` | `evidence` (8 lock target) | path-only |
| (CP2 dry-run, line 3618) | `fixtures/synthetic_16ch_v1.json (sha b6f1cc86…)` | `refs` | post-correction sha256 prefix |

## §3. mismatch 분석 표

| token | type | scope | value | observation |
|---|---|---|---|---|
| `2960889009` | **internal fingerprint** (FNV-32 of band powers) | invariant under metadata-only edit | file 일치 + #174/#204 일치 | OK |
| `831a1b5d…` | **sha256 prefix-8** (whole-file digest) | bytes-sensitive | v1.0 (49970e902, 2026-04-26 20:01:50 +0900) | #157 evidence block 작성 시점 정확 |
| `b6f1cc86…` | **sha256 prefix-8** (whole-file digest) | bytes-sensitive | v1.1 (80d4ef2ac, 2026-04-27 00:23:20 +0900) | 현 디스크 일치 + #217/#223/CP2 일치 |

→ **사실상 mismatch 0 건**. A3 audit 의 mismatch 신고는 **scheme 혼동** (sha256 prefix vs FNV-32 fingerprint) 에서 비롯.

## §4. file 수정 timeline (`git log --all --oneline -- anima-clm-eeg/fixtures/synthetic_16ch_v1.json`)

| commit | date (KST) | sha256 | sample_rate_hz | window_samples | fingerprint |
|---|---|---|---|---|---|
| `49970e902` | 2026-04-26 20:01:50 | `831a1b5d49234d30b83070f116f10204eba1ad06fa6ab5c3beafc6b6f234a271` | 250 | 1000 | 2960889009 |
| `80d4ef2ac` | 2026-04-27 00:23:20 | `b6f1cc8669bf5bb5a6627bb55f812d48aa2f4bbed765b4e74097f205d78dccc7` | 125 | 500 | 2960889009 |

- 2 commits only. v1.1 commit message: "all-go(axis-89): EEG D-1 critical path 4 PASS — 250→125 Cyton+Daisy + .venv-eeg py3.12 + brainflow 5.21 dynamic API + pre-register v1.1 sha re-freeze"
- band_powers_x1000 변경 X (FNV-32 input identical) → fingerprint 보존
- metadata block (sample_rate_hz/window_samples) 변경 → bytes 변동 → sha256 drift

## §5. 원인 가설 (rank 순)

1. **(가장 유력) A3 audit 의 scheme 혼동** (P≈0.95): A3 audit 이 `831a1b5d` (sha256 prefix-8) 를 internal fingerprint 로 잘못 해석. #157 evidence block 의 표기 컨벤션을 보면 같은 줄 모든 다른 file 이 `(sha256 0dfe2c2e)`, `(cd17abd8)`, `(fbff2e85)`, `(0eec458c)`, `(18196513)` 처럼 **sha256 prefix-8** 임이 명백 — `831a1b5d` 도 동일 패턴. 두 식별자 (sha256 vs FNV-32) 는 서로 다른 알고리즘·다른 입력·다른 의미.
2. **(보조) audit 가 v1.0 시점 sha256 을 v1.1 시점 fingerprint 와 비교** (P≈0.05): #157 evidence block 은 v1.1 patch (#217 axis-89, 2026-04-27 00:23) 이전 작성 (#157 completion_ts 2026-04-26T20:15Z). 이후 sha256 drift 가 발생했지만 #157 evidence 는 retroactive update X. #217/#223 가 drift 명시 + v1.1 freeze. 따라서 #157 의 `831a1b5d` 는 **v1.0 시점 정확값** — outdated 라기보단 historical snapshot.
3. **(기각) file 수정 / typo / fingerprint 알고리즘 변경**: git log 2 commit 모두 fingerprint=2960889009 보존. 알고리즘 변경 흔적 없음.

## §6. 해결 권장 (raw#10 honest)

- **수정 불필요** (read-only audit verdict): 본 audit 은 #157 evidence block 변경을 권장 X.
  - 근거 (a): #157 evidence 의 `831a1b5d` 는 작성 시점 (2026-04-26) sha256 prefix 정확값.
  - 근거 (b): #217/#223 가 v1.0→v1.1 sha drift (`831a1b5d → b6f1cc86`) 를 별도 entry 로 ledger 명시 — historical chain 보존.
  - 근거 (c): `.roadmap` chflags uchg + #237 dual-lock target → 변경 자체 금지.
- **A3 audit 후속 조치**: A3 audit 결과 file 의 mismatch 항목을 "sha256 prefix vs FNV fingerprint scheme 혼동, 실 mismatch 0" 로 정정 (본 doc 참조). A3 audit 본문 수정은 별도 cycle.
- **future-proof**: 신규 evidence block 작성 시 `(sha256 b6f1cc86)` `(fingerprint 2960889009)` 처럼 **scheme 명시** 권장 — #174 가 이미 이 컨벤션 사용 (`(fingerprint 2960889009)`).

## §7. raw#71 falsifier — byte-identical reproducibility 의심 검증

raw#71: "fingerprint mismatch 시 byte-identical reproducibility 의심"

**verdict**: NOT triggered.
- internal fingerprint `2960889009` 가 v1.0 / v1.1 / 현 디스크 모두 일치 → FNV-32 deterministic + band_powers input invariant 보장.
- sha256 drift 는 metadata-block edit (sample_rate_hz/window_samples 정정) 의 의도적 결과 — adversarial drift 아님. #217 evidence 가 byte-identical re-emit (twin-run) 검증 명시 ("twin-run byte-identical PASS + sanity 4/4").
- raw#71 가 발동했어야 할 시나리오: `band_powers_x1000` 가 변경되었는데 fingerprint 가 동일 (impossible if FNV deterministic) — 본 case 해당 X.

raw#71 conservatism 유지: A3 audit 의 mismatch 신고 자체는 raw#71 발동 trigger 로 합리적 (false-positive cost ≪ silent corruption cost). 본 audit 이 false-positive 로 분류 후 dismiss.

## §8. read-only audit 한계 (raw#91 / raw#10 honest C3)

1. **file 1개 + roadmap 1개만 검토**: A3 audit 본문 (commit `867392918`) 의 mismatch 신고 표현 직접 읽지 않음 → A3 가 "fingerprint" 라고 표기했는지 "sha256" 으로 표기했는지 verify X. 가설 1의 P=0.95 는 #157 컨벤션 + 일치 prefix 8자 패턴에 근거.
2. **FNV-32 알고리즘 직접 재계산 X**: file 의 `2960889009` 가 진짜 band_powers FNV-32 인지 본 audit 에서 재현하지 않음 (`clm_eeg_synthetic_fixture.hexa` reproducer 호출 안 함). #217 evidence ("fingerprint 2960889009 PRESERVED — band powers unchanged") 진술 신뢰.
3. **다른 fixture 인용 미체크**: roadmap 외 docs/markers/state 파일들에서 동일 token 사용 패턴 추가 검증 안 함 (예: memory entries, landing docs). 본 audit scope 는 .roadmap + file 만.
4. **n=2 git history**: 2 commit 만 존재 → 시간축 sample 작음. cherry-pick / amend 흔적 없음 (git log --all 동일).
5. **read-only 보장**: file mtime/sha256 변경 0, `.roadmap` 변경 0, 신규 file 1 (본 doc) 만 add. raw#91 honest C3.

## §9. 결론 한 줄

`831a1b5d` = v1.0 sha256 prefix · `2960889009` = FNV-32 fingerprint · `b6f1cc86` = v1.1 sha256 prefix. **세 값 모두 정합** — A3 audit mismatch 신고는 scheme 혼동 false-positive.

## §10. refs

- `<repo-root>/anima-clm-eeg/fixtures/synthetic_16ch_v1.json` (audit target)
- `<repo-root>/.roadmap` lines 2066-2078 (#157), 2338-2350 (#170), 2352-2365 (#172), 2367-2378 (#173), 2381-2394 (#174 cross-validate), 3296-3306 (#217 sha drift evidence), 3368 (#223 v1.0→v1.1 lock)
- git commits: `49970e902` (v1.0 freeze) · `80d4ef2ac` (v1.1 axis-89 sample-rate 250→125)
- A3 audit (commit `867392918`) — original mismatch flag
