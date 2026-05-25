# STDLIB — current state

@goal: anima 전반의 general primitive (entropy · mutual info · binning · log · bitops · math · signal processing 등) 를 **hexa-lang stdlib 으로 promote · anima 는 import-only path 로 정리** — phi_native (PHI domain LAND) 가 first 사례, 후속 EEG/clustering/FFT 등 단계 이주

## Scope

- **in scope**: anima 전체 grep 으로 general primitive 후보 도출 · hexa-lang stdlib 구조 설계 · upstream RFC + module land · anima 측 import path 교체 · byte-equal 보장
- **out of scope**: domain-specific 로직 (HEXAD/LIFE/H_* sweep 본체 등) · anima @I (substrate-native chat daemon) 의 substrate 모듈

## Why stdlib

| g | rationale |
|---|---|
| **g0 Occam** | 부품 최소 — duplicate helper 제거, 진본 1 곳 |
| **g1** | hexa-native first — hexa stdlib 가 canonical home |
| **g11** | no gap workarounds — anima 측 _phi_pow2 같은 우회는 hexa stdlib bitops 으로 fix at source |
| **g20** | no hardcoding · implement generically — domain-specific 위치 (HEXAD/LIFE/lib) 가 general primitive 와 부적합 |
| **g59** | hexa-lang upstream — anima 의 general primitive 는 본질적으로 hexa-lang 측 |

## Cross-repo

```
anima (caller)          ⇄          hexa-lang (provider)
─────────────────                  ──────────────────────
HEXAD/LIFE/lib/                    stdlib/
  phi_helper.hexa     ──import──→    info/
  H_*/run_*.hexa                       entropy.hexa
                                       mutual_info.hexa
                                       binning.hexa
                                     math/
                                       log.hexa
                                       bitops.hexa
                                     consciousness/
                                       phi_spatial.hexa
```

본 도메인 = cross-repo 작업 · anima 와 hexa-lang 둘 다 변경 (PHI 와 달리 hexa-lang 측 source 작성 포함).

## Progress milestones

### survey (anima 전체)

- [x] anima 전체 grep — `HEXAD/STDLIB/survey_2026_05_24.md` 228 LoC · 10 카테고리 · 47 candidate fn · ~247 dup sites
- [x] duplicate helper 식별 — hot dup top: abs_f(77) · pow2_int(33) · wolfram_init_row(32) · lcg_next(28) · sqrt_newton(17) · shannon_entropy(7)
- [x] candidate priority 표 — 1st-wave 17 fn · 2nd-wave 11 · deferred 2 · 1st-wave top-5 promote 시 phi_native 200→50 LoC (-75%)
- **🔥 핵심 발견**: hexa-lang stdlib 이미 부분 존재 (`core/math.hexa` · `core/math/float.hexa` · `iit_ei.hexa` · `rng.hexa`) — missing log2/pow2/bit_set 가 anima sprawl 의 root cause · `iit_ei.hexa::LN2_INV` 재활용 가능

### design

- [x] stdlib 구조 설계 — 5 module 의 fn surface + 의존 그래프 (math/bitops ⊥ math/log 병렬 · entropy needs log2 · binning needs floor · mutual_info needs binning+entropy) · 순환 0 · 외부 의존 0
- [x] hexa-lang 측 stdlib 신설 RFC draft — `~/core/hexa-lang/inbox/rfc_drafts_2026_05_24/stdlib_scaffold.md` 132 LoC · YAML frontmatter (slug=stdlib_scaffold, relates_to=rfc_036_c_replica_drift) · 10 § · 6 honest_limits · g59 enforcement filed

### implement (phase 1 — phi_native 분해)

- [~] ~~`stdlib/math/log.hexa`~~ — **DROP**: `log2` 는 이미 동작하는 builtin (`runtime_core.c::hexa_log2` → libm). RFC "missing" 전제 오류. entropy 는 byte-equal 위해 `log(x)/log(2.0)` inline 유지 (libm log2 와 ulp 다름).
- [x] `stdlib/math/bitops.hexa` — `pow2_int(k)` · `bit_set(mask, b)` (native shift/and; phi_native 의 mult-workaround 불필요) — MERGED #769
- [x] `stdlib/info/entropy.hexa` — `shannon_entropy` (`log(x)/log(2.0)` byte-equal) — MERGED #769
- [x] `stdlib/info/binning.hexa` — `bin_values_minmax` (min-max histogram) — MERGED #769
- [x] `stdlib/info/mutual_info.hexa` — `mutual_info_pair` (imports binning+entropy) — MERGED #769
- [x] `stdlib/consciousness/phi_spatial.hexa` — RFC §5 2nd-wave wrapper — MERGED hexa-lang #780 → #792 (rename `phi_spatial_native` for C builtin collision avoidance), 154 LoC

### byte-equal verify

- [x] stdlib 분해 후 `phi_native_spatial` 가 기존 phi_native.hexa 와 byte-equal 유지 — 5/5 rule bit-identical verbatim (rule=110/30/250/184/60 frozen baseline match, M5 verify_phi_native.hexa rerun 2026-05-25)
- [x] Rust phi_rs oracle vs stdlib 합성 — PHI domain dual-tier verdict 보존 (C-replica drift `phi_c vs phi_h byte_equal=false` 은 RFC 036 documented drift, NOT regression)

### migration (phase 2 — anima 측 교체)

- [x] `HEXAD/LIFE/lib/phi_native.hexa` decompose to stdlib import — MERGED anima #424 commit e8158581d (332→56 LoC, -83%)
- [x] `HEXAD/LIFE/lib/phi_helper.hexa` import path — 변경 불필요 (caller 가 phi_native_spatial public surface 만 의존, 새 shim 이 같은 fn 노출)
- [x] PHI verify harness 재실행 — 5/5 PASS, baseline bit-identical

### phase 3 — 후속 candidate

- [x] EEG / signal-processing primitive — signal/ 8 module + griffin-lim + autocorrelation/spectral_density (#901) + pearson_autocorr (#911) all MERGED
- [x] clustering / classification primitive — MERGED hexa-lang #869 (k-means) + #883 (k-means++ D²) + cluster trio (distance/knn/kmeans) RFC-037 complete
- [ ] anima 의 MITOSIS / CHAT / etc. 도메인 의 general 후보 단계 이주

### phase 5 — sha256 + l2_norm (대량 sweep)

- [x] phase 5 M1 (1/2) — sha256 alias surface (`sha256_of_string` / `sha256_of_file`) — MERGED #884
- [x] phase 5 M1 (1/2+) — sha256 bytes/stream surface (`sha256_of_bytes` / `sha256_of_lines_filtered`) — MERGED #924
- [x] phase 5 M1 (2/2) — `stdlib/linalg/norm.hexa` (l2_norm · frobenius · l2_normalize · cosine_distance) — MERGED #885
- [x] phase 5 M1 (2/2+) — norm tunable-epsilon variants (l2_norm_eps · l2_norm_floored · l2_normalize_eps) — MERGED #910
- [x] anima sha256 sweep — MERGED #461 (~104 site / 105 file, net -89 LoC) + #463 (superseded)
- [x] anima l2_norm sweep — MERGED #462 (w1) + #467 (w2a, 12 alm) + #473 (phi_vec_logger byte-equal)
- [ ] anima sha256 wave 2b 잔여 — directory-walk / `sha256sum -c` manifest / remote-SSH (deferred, #461 list)
- [x] anima l2_norm wave 2b — serving/tool #482 (1/39 migrate) + HEXAD (0/9) → **natural-floor 확정**: 잔여 site 는 non-libm custom sqrt(sqrt_newton/fsqrt/isqrt) · guard · 통계량 · complex mag 로 byte-equal 부적합

### natural-floor 발견 (cycle 13)

- [x] anima pearson_autocorr 9 site — **0/9 migrate**: guard epsilon (`<1e-10` vs stdlib `==0.0`, 실측 divergence) + vector-pair Pearson + farr storage. 이질성으로 byte-equal 불가. pearson_autocorr (#911) 는 future-code 용.
- [x] anima l2 custom-epsilon 3 site — **1/3 migrate** (#473): phi_vec_logger byte-equal. holographic_mapping(Newton-Raphson fsqrt ≠ libm) + unity_loss(pre-sqrt floor) defer.
- **결론**: 대량 byte-equal sweep (matvec/entropy/sha256/l2-plain) LAND 완료. 잔여 site 는 도메인-특화 수치 규약(fsqrt·pre-sqrt floor·near-zero guard·vector-pair·farr)으로 generic stdlib 와 byte-equal 부적합 — 실패 아닌 발견.

## Honest limits

- L1: hexa-lang stdlib 구조가 현재 미정립 — 본 도메인이 사실상 stdlib 의 first user · upstream maintainer 협의 필수
- L2: cross-repo coordination 부담 — anima 측 PR ↔ hexa-lang 측 RFC/PR 의 land 순서 정합 필요
- L3: byte-equal 보존 = 분해 시 IEEE 부동소수 순서 보존 책임 (Agent E 의 1-2 ulp noise 가 stdlib 분해 후 늘어나지 말 것)
- L4: 본 도메인 = code authoring + spec authoring 의 mixed lane · anima 만 PR 로 닫을 수 없음 (hexa-lang 의존)
- L5: anima @I 의 "substrate-native chat daemon" 과 별개 — stdlib 은 도구함, substrate 가 아님

## Cross-link

- PHI.md — 첫 사례 · phi_native.hexa 분해 source
- LIFE.md — phi_helper.hexa 가 caller · stdlib import 후도 LIFE 도메인 의사결정 byte-equal 보존
- hexa-lang RFC 036 — phi_spatial builtin · 본 stdlib 의 consciousness/phi_spatial.hexa 가 reference impl 될 수 있음
- hexa-lang `inbox/notes/rfc_036_c_replica_drift_2026_05_24.md` (g59 enforcement) — 본 stdlib 작업이 그 drift 의 hexa-side fix path

## Notes

- 본 도메인 = anima ↔ hexa-lang dual-repo · 단순 PR 1 개로 안 끝남 · 여러 cycle 통한 점진적 migration
- 첫 cycle = survey (anima 전체 grep) · 결과 위에 design + impl 단계 fan-out
