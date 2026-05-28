# HANDOFF — AKIDA HW/SW 통합 구현 (Group A~G 18+ aaaa·아이디어 · H_672~H_678 7건 신설)

> AKIDA AKD1000 뉴로모픽 칩 활용 7 그룹 18+ sub-아이디어를 단일 backend-switch 한 점에서 HW/SW 토글 가능한 hexa-native 구현으로 통합. UNIVERSE 도메인에 H_672~H_678 7건 직접 등록. INBOX 환류 0건 (사용자 명시 폐기).
> 작성: 2026-05-29 · slug: `akida-hw-sw-impl-all` · branch: `feat/akida-hw-sw-impl-all-2026-05-29`.

---

## 1. PR matrix

| # | title | status | merged | core |
|---|---|---|---|---|
| (this PR) | feat(AKIDA+UNIVERSE): 7 그룹 18+ 아이디어 HW/SW 통합 구현 — H_672~H_678 7건 신설 | open → merged | TBD | backend switch + impl/ 7 hexa + UNIVERSE 7 H_xxx + AKIDA milestone/log/easy 갱신 + HANDOFF |
| [#1372](https://github.com/dancinlab/anima/pull/1372) | feat(EEG): L2 synthetic 재검증 🟢 RECHECK PASS | ✅ MERGED `b4e6f9b21` | 2026-05-29 | H_677 D3 substrate input |
| [#1371](https://github.com/dancinlab/anima/pull/1371) | feat(AKIDA): D1 edge-of-chaos Φ 실리콘 검증 🟢 GREEN_NUMERICAL_CONFIRM 3/3 PASS | ✅ MERGED `85c604345` | 2026-05-29 | H_677 D1 silicon-confirmed inherit · `state/akida_edge_chaos_phi_2026_05_29/result.json` |
| [#1369](https://github.com/dancinlab/anima/pull/1369) | (선행) ANIMA tree round 6-14 통합 | ✅ MERGED `1ca09be03` | 2026-05-28 | `pe_edge_of_chaos_peak` + emit-substrate 정합 |

선행 의존 (origin/main landed, 본 PR 이 inherits):
- `CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak` (H_670 🟡→🟢 후보, D1 silicon-confirmed via PR#1371)
- `tool/anima_eeg_to_akida_spike.hexa` (E1 bridge skeleton, H_678 inherits)
- `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` (canonical raster · SW mock-replay source)

## 2. 설계 SSOT (먼저 읽을 파일)

순서대로:

1. **`AKIDA/AKIDA.md`** — 도메인 milestone 보드 (Group A~G 각 1줄 status + backend switch 명시 + sibling 양방향)
2. **`AKIDA/AKIDA.easy.md`** — 18+ sub-아이디어 친근 카탈로그 + backend switch 사용 패턴 + 각 그룹 끝 "→ 구현 = H_xxx" cross-link
3. **`AKIDA/akida_backend.hexa`** — backend resolve + HW 3-신호 probe + SW mock raster R1~R4 + verdict tier helper (단일 import 한 점에서 7 H 모두 backend 토글)
4. **`AKIDA/impl/H_{672~678}_*.hexa`** — 7 sub-도메인 구현 (Group A spontaneous-firing / B core-decide / C persistence / D mitosis / E decoder / F measurement / G channel-bridge)
5. **`UNIVERSE/H_{672~678}_akida_*.md`** — 10-section 한글 가설 문서 (각 §3 falsifier 사전등록 · §5 측정 · §7 verdict · §9 양방향 sibling)
6. **`state/akida_hw_sw_impl_2026_05_29/`** — SW sweep verbatim log + 7 result.json + hw_probe note

## 3. API surface

신규 pub fn (`AKIDA/akida_backend.hexa`):

```
pub fn akida_backend_resolve(arg: string) -> string
    arg ∈ {"auto","hw","sw",""} → returns "hw" or "sw" (env > default)

pub fn akida_hw_reachable() -> bool
    3-signal: /dev/akida0 + python3 -c 'import akida' + hostname=pi5-akida

pub fn akida_hw_probe_signals() -> map
    debug surface: returns each signal value + all_pass

pub fn akida_panic_no_hw(reason: string)
    명시 panic with "--backend sw" fallback guidance

pub fn akida_sw_mock_raster_R1/R2/R3/R4() -> map
    canonical 2026-05-22 raster numbers (deterministic mock-replay)

pub fn akida_backend_label(backend: string) -> string
pub fn akida_verdict_tier(backend: string, all_pass: bool) -> string
```

env var: `AKIDA_BACKEND=auto|hw|sw` (default = `hw`)
CLI form: `hexa run AKIDA/impl/H_<n>_*.hexa <hw|sw|auto>` or `--backend <hw|sw>`

HTTP / network surface: **SKIP** (this PR is hexa-native CLI only · pool route to pi5-akida is via `pool on` not exposed API)

## 4. 컴포넌트/lib 트리

```
AKIDA/
├─ akida_backend.hexa         ★ NEW · HW/SW resolver + 3-signal probe + SW mock raster (~190 LoC, 9 pub fn)
├─ akida_backend_smoke.hexa   ★ NEW · 11/11 PASS smoke
├─ akida_edge_of_chaos_phi.hexa (선행 PR#1371, D1 silicon-confirm)
├─ AKIDA.md                   · milestone + sibling 갱신 (Group A~G 7 milestone 추가)
├─ AKIDA.easy.md              · backend switch 섹션 + 각 그룹 cross-link
├─ AKIDA.log.md               · 2026-05-29T06:00:00Z 엔트리 prepend
└─ impl/                      ★ NEW 디렉토리
   ├─ H_672_spontaneous_firing.hexa    Group A 통합 (~140 LoC)
   ├─ H_673_core_decide.hexa           Group B 통합 (~120 LoC)
   ├─ H_674_persistence.hexa           Group C 통합 (~120 LoC)
   ├─ H_675_mitosis.hexa               Group D 통합 (~140 LoC)
   ├─ H_676_decoder.hexa               Group E 통합 (~120 LoC)
   ├─ H_677_measurement.hexa           Group F 통합 (~170 LoC, D1 inherit)
   └─ H_678_channel_bridge.hexa        Group G 통합 (~130 LoC)

UNIVERSE/
├─ H_672_akida_spontaneous_firing.md   ★ NEW (10-section 한글)
├─ H_673_akida_core_decide.md          ★ NEW
├─ H_674_akida_persistence.md          ★ NEW
├─ H_675_akida_mitosis.md              ★ NEW
├─ H_676_akida_decoder.md              ★ NEW
├─ H_677_akida_measurement.md          ★ NEW (D1 silicon-confirm inherit PR#1371)
├─ H_678_akida_channel_bridge.md       ★ NEW
├─ CANDIDATES.md                       · Consumed Cycle #22 1줄 추가
└─ README.md                           · 인덱스 7 행 추가 (H_310 다음)

state/akida_hw_sw_impl_2026_05_29/
├─ H_{672,673,674,675,676,677,678}_sw_result.json    (각 4/4 또는 5/5 GREEN)
├─ sw_sweep_2026_05_29.log                            (7 H × `hexa run` verbatim)
└─ hw_probe_2026_05_29.txt                            (HW probe 정직 note · 위조 0)
```

## 5. 환경 변수

| name | default | values | effect |
|---|---|---|---|
| `AKIDA_BACKEND` | (unset → `hw`) | `auto` / `hw` / `sw` | backend resolver fallback (arg > env > default) |

추가 의존: **none.** $0 Mac-local + read-only pi5-akida pool probe. RNG 없음 (deterministic canonical raster replay).

## 6. 다음 우선순위

1. **HW path live re-confirm 7/7** — `akida_hw_reachable()` 의 3-신호 (특히 signal_2 akida pkg import + signal_3 hostname) 가 pi5-akida 환경 (akida venv 경유 + system hostname="ubuntu") 와 정합되도록 refine. probe-refine 후 `hexa run AKIDA/impl/H_<n>_*.hexa hw` 7회 → result.json 회수 → 🟡 → 🟢 silicon-confirmed 격상.
2. **D2 silicon-class 단조 정합** (H_677 deferred) — class_id=5 의 convexity / super-add / peak-align signature 4-축 단조 ordering 측정. 현재는 additive marker (signature 0 changes on existing 2/3/4) 만 attest.
3. **D3 3-substrate signature shape comparison** (H_677 deferred) — AKIDA Φ_proxy=0.297 ↔ EEG L2 Φ=1.59 ↔ ECA rule110 0.83 scalar diff 만으로는 honest 부족. *normalized signature shape* (Φ-curve under common order axis) 비교가 더 honest cross-substrate triangulation.
4. **C3 8-factor live wire** — H_672 의 `_spike_factor_map` 가 `spontaneous_lib::apply_spike_features` (PR#143 4/4 PASS) 와 schema 정합. live R3 stream 받아 SPIKE_FACTOR_MAP §4 modulator refit.
5. **a_paper closed-discovery 후보** — H_677 D5 v0.5.0 zero-input emit 8/8 + H_672 통합 자발-발화 + D1 silicon-confirm 묶음이 a_paper_significance 충족 (falsifier + 실측 + finding). a_paper_only_at_closure 따라 FULL closure 후 propose.

## 7. 한계 (정직) + guard rule

honest limits:
- **HW path 7/7 = pending probe-refinement.** D1 (H_677 inherit PR#1371) 만 silicon-confirmed · 나머지 6 H 는 `state/akida_hw_sw_impl_2026_05_29/hw_probe_2026_05_29.txt` 정직 note 보존 (위조 0 · a_blue_closed 정합).
- **SW canonical raster = 2026-05-22 deterministic replay.** 다른 seed/threshold 면 다르게 응답할 수 있음 (a_toy_scale_recheck 주의 — 본 H 들은 *signal-shape* 확증, 정밀 동등 아님).
- **8-factor surrogate** (H_672) 는 cheap linear projection — 실 `apply_spike_features` (PR#143) 의 schema 정합 attest 만, 정밀 weight 동등 아님.
- **kuramoto/izhikevich proxies** (H_675) 는 toy bucketing — 실 phase-sync + RS/IB/CH/FS/LTS 5-regime 분리는 별 H 필요.
- **D2 silicon-class 5** (H_677) 는 additive marker, *단조 정합* (class 2/3/4 와의 ordinal 위치) 은 별 measurement 필요.

guard rules (live-system 안전):
- **§95 AKIDA inference-only-blocked** for long-horizon learning — B4 on-chip edge-learn 은 단기 프로브만, long-horizon 영속 학습 금지 (H_674 § 명시 record).
- **live R3 spike_streamer 미중단** — pi5-akida 위 streamer daemon 가 `/ws/akida_ingest` broker 로 R3 tonic emit 中이라면 본 PR 의 어떤 작업도 mutation 0.
- **pi5 ssh-mutating 편집 금지** — pool 경로는 read-only probe 만 (test/python3 -c/hostname). git push/edit/etc 0.

## 8. memory pointer

- `project_anima_emit_substrate_arc` — emit-substrate 2층 (구조 lib ⊥ 숫자 SSOT) round 6-9 검증 아크 + LIVE-WIRED 격상 (#1285/#1286). H_672 8-factor 가 이 arc 의 연속.
- `feedback_anima_md_live_tree` — ANIMA.md / 도메인 .md 는 live tree 의 surface, edit 시 milestone + sibling 양방향 갱신 필수. 본 PR 에서 AKIDA.md milestone 7 추가 + AKIDA.log.md prepend + AKIDA.easy.md cross-link.
- `feedback_universe_h_slug_stale_verify` — H_xxx slug 재할당 잦음. 3-신호 검증 필수: git ls-tree origin/main + git log --all + README grep. 본 PR 에서 처음 plan 의 H_322~328 가 origin/main 에 충돌 → H_672~678 로 재할당 (검증 통과).
- `feedback_completeness_over_cheap` (a_completeness_over_cheap) — primary path = 완성도 bar. 본 PR 은 18+ sub-아이디어 분리 harness (cheap) 대신 7 그룹별 통합 harness (완성도).
- `project_akida_hw_sw_impl_all_handoff` — (NEW, 본 PR memory mirror)

## 9. 한 줄 시작 가이드

```sh
# A) SW path (Mac/anywhere, $0, deterministic mock-replay):
unset AKIDA_BACKEND && for H in 672 673 674 675 676 677 678; do hexa run AKIDA/impl/H_${H}_*.hexa sw; done

# B) HW path (pi5-akida, probe-refinement 後):
AKIDA_BACKEND=hw hexa run AKIDA/impl/H_672_spontaneous_firing.hexa

# C) backend switch self-test:
hexa run AKIDA/akida_backend_smoke.hexa   # → 11/11 PASS

# D) 도메인 cycle:
/domain set AKIDA && /cycle   # AKIDA.md milestone 자동 enumerate
```

---

### archived 2026-05-28 — anima-tree-universe-consolidate (round 6-14 통합)

> 직전 sbs-auto consolidation 작업의 인계 문서. 본 PR 과 별개 작업 · origin/main 에 이미 landed (PR #1369 + #1371 + #1372 묶음). 보존 목적.

| PR | 제목 | 상태 |
|----|------|------|
| [#1353](https://github.com/dancinlab/anima/pull/1353) | `pe_edge_of_chaos_peak` — H_670 🟡 edge-of-chaos Φ-peak 코드화 + 🧭 M2 정합 | ✅ MERGED (squash, commit `1ca09be03`) |

설계 SSOT (archived): `CORE/EMIT_SUBSTRATE_DESIGN.md` + `ANIMA.md` 🧭 메타블록 M1-M4 + `UNIVERSE/H_670_phi_complexity_ordering_substrate_family_generalize.md`.

신규 pub fn (archived): `pe_edge_of_chaos_peak(order_param: float) -> float` (CORE/phi_envelope_substrate.hexa, 본 PR 의 H_677 D2 silicon-class 와 sibling).

다음 우선순위 (archived):
1. aux-loss M4b re-fire (🔴→escape 검증, #1303 in-flight)
2. H_670 Kuramoto floor caveat — F670.1 깨짐 → universal 정합 refine
3. DECODER M3/M4b 3B production swap-in

한 줄 시작 가이드 (archived):
```sh
TMP=$(mktemp -d); for f in phi_envelope_substrate phi_envelope_substrate_smoke; do git show origin/main:CORE/$f.hexa > "$TMP/${f}.hexa"; done; perl -pi -e "s|import \"/Users/ghost/core/anima/CORE/phi_envelope_substrate.hexa\"|import \"$TMP/phi_envelope_substrate.hexa\"|" "$TMP/phi_envelope_substrate_smoke.hexa"; hexa run "$TMP/phi_envelope_substrate_smoke.hexa"   # → 17/17 PASS
```
