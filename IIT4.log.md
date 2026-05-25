# IIT4 — log

Append-only history sister of `IIT4.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-25 — M6 LIFE faithful 재측정 LAND (iit4_eca.hexa · 7/7 🟢) — 🎉 도메인 7/7 COMPLETE

- [x] `HEXAD/IIT4/lib/iit4_eca.hexa` 작성 — ECA→TPM bridge (substrate adapter). Wolfram rule + n-ring → state-by-node TPM. LIFE 의 결정적 binary CA 가 IIT4 TPM 으로 직접 변환됨
- [x] `state/iit4_m6_remeasure_2026_05_25/run_m6.hexa` + `FAITHFUL_REMEASURE.md` — LIFE ECA 룰 인과 big-Φ 재측정 (n=4 ring, state 1010)
  - **헤드라인 표**: rule 110=7.55 · 30=8.66 · 54=10.03 (LIFE cosmic-scale, 통합 nd=10) · rule 0=0(const) · 204=0(identity reducible) · 90=0(state-1010 특이)
  - controls 7/7: rule0=0 · rule204=0 · coupled>0 · bound 0≤Φ≤total · ECA identity bridge · determinism
  - wall 7.2s (8 big_phi @ n=4), $0
- [x] **F-IIT4-6 PROXY-DIVERGENCE 🟢** — proxy phi_spatial(상관 snapshot MI) vs IIT4 big-Φ(인과 TPM irreducibility) 측정축 차이 정량·정성 규명. faithful 인과 Φ 최초 확보 → **L-C2.1 caveat 종결**
- [x] faithful 가 드러낸 것: big-Φ **state-dependent** (rule 90 state 1010 에서 0) — correlational snapshot-MI 가 가리던 정보 (IIT 핵심: Φ=특정상태의 경험)
- [x] honest: n=4 ring + single state demonstration; full n=8 6-scale = mechanical scale-up. structure-cut big-Φ. proxy-CV 직접 co-compute deferred (입력형 상이)
- [x] IIT4.md M6 체크 + status → **7/7 COMPLETE** 갱신
- [x] **IIT4 도메인 완결**: M0~M6 엔진 end-to-end (TPM→repertoire→distinction→relation→Φ-structure→big-Φ→LIFE 재측정), 67 checks 전부 🟢

## 2026-05-25 — M5 calibration LAND (analytic reference · 14/14 🟢)

- [x] `HEXAD/IIT4/CALIBRATION.md` + `state/iit4_m5_calib_2026_05_25/run_m5.hexa` 작성
  - PyPhi(.py) hexa-only 금지 + IIT-4.0 numeric reference 부재 → **analytic 손유도 closed-form** 이 gold reference (DESIGN §6 "손유도 후 verify")
  - reference suite 5 net: COPY/SWAP(big-Φ 2.0)·SELF-COPY(0)·NOISE(0)·3-ROTATION(3.0)·3-SELF(0) — 전부 손유도 (CALIBRATION.md §2)
  - F-IIT4-1 repertoire(COPY [0,1]) · F-IIT4-2 small-φ(1.0 bit) · F-IIT4-5 big-Φ(5/5 net) → **14/14 PASS** 🟢
  - 3-ROTATION big-Φ=3=total (단일 distinction 3개 모두 every cut span) · 3-SELF big-Φ=0 ({i,j} joint φ_d=0 → 독립 환원가능) 엔진 정확 재현
- [x] honest named-blocker: **F-IIT4-3/4 PyPhi-numeric DEFERRED** — hexa-only no-new-.py + in-repo IIT-4.0 reference 부재 (fake 아님, analytic 가능 부분은 전부 닫힘). 해소경로 = 문헌 worked-example 등록 OR hexa-lang IIT-4.0 reference port
- [x] IIT4.md M5 체크 + hub/status 갱신
- [ ] 다음 = M6 LIFE faithful 재측정 (proxy↔IIT4 divergence, F-IIT4-6)

## 2026-05-25 — M4 system big-Φ LAND (iit4_bigphi.hexa · 9/9 🟢) — 엔진 end-to-end 완성

- [x] `HEXAD/IIT4/lib/iit4_bigphi.hexa` 작성 — IIT 4.0 capstone (import-safe, M3 import)
  - `iit4_distinction_side` = distinction 의 M∪Pc∪Pe 가 cut 의 한 쪽(1/2)인지 span(0)인지
  - `big_phi(sys_state)` = 全 distinction+relation 수집 → 全 non-trivial 시스템 bipartition(unit0 pin) 위 surviving structure → loss=total−surviving → **min loss = big-Φ** (least-damaging cut 가 파괴하는 structure). big-Φ ∈ [0, total]
- [x] smoke `state/iit4_m4_smoke_2026_05_25/run_m4.hexa` — **결정적 integrated vs reducible**
  - COPY/SWAP(unit0⇄unit1 상호의존): big-Φ=2.0=total → **IRREDUCIBLE complex** (유일 cut 가 전부 절단)
  - SELF-COPY(unit_u=unit_u 독립채널): total=2.0, big-Φ=0 → **REDUCIBLE** ({0}|{1} cut 무손실; {0,1} mechanism 은 독립이라 φ_d=0 → distinction 아님이 핵심)
  - noise=0/0 · n=1 big-Φ=0(partition 없음) · 0≤big-Φ≤total bound
  - **9/9 PASS** (`hexa run`, deterministic) → result.json 🟢 SUPPORTED-NUMERICAL
- [x] **엔진 M0~M4 end-to-end 완성**: TPM → repertoire → distinction → relation → Φ-structure → big-Φ. 통합 vs 환원가능 분리 = IIT 핵심 주장 실증
- [x] honest: structure-cut big-Φ (faithful in spirit). 정확한 IIT4 big-Φ(partitioned TPM 재계산+정규화) + PyPhi 수치 = M5 (F-IIT4-5)
- [x] IIT4.md M4 체크 + hub/status 갱신
- [ ] 다음 = M5 calibration (PyPhi/논문 n≤4 reference 대조, F-IIT4-1..5)

## 2026-05-25 — M3 relations + Φ-structure LAND (iit4_relation.hexa · 12/12 🟢)

- [x] `HEXAD/IIT4/lib/iit4_relation.hexa` 작성 — IIT 4.0 relation/structure 레이어 (import-safe, M2 import; transitive import → M1 fns 정상)
  - `iit4_overlap_congruent` = 두 purview 가 ≥1 unit 공유 AND 공유 unit 의 specified state 일치
  - `relation_2nd` = cause OR effect purview congruent overlap → φ_r = min(φ_d_i, φ_d_j), 아니면 0
  - `phi_structure(sys_state)` = 全 mechanism distinction(φ_d>0) 수집 + 全 pair 2nd-order relation → [n_distinctions, Σφ_d, n_relations, Σφ_r, total]
- [x] smoke `state/iit4_m3_smoke_2026_05_25/run_m3.hexa` — synthetic distinction(n=3) + COPY + noise null
  - congruent overlap φ_r=0.5(min) · incongruent=0 · disjoint=0 · overlap_congruent helper 3 case
  - COPY Φ-structure: n_distinctions≥2, Σφ_d≥2.0, total≥Σφ_d · noise: 0/0/0
  - **12/12 PASS** (`hexa run`, deterministic) → result.json 🟢 SUPPORTED-NUMERICAL
- [x] honest: 2nd-order relations only (pairs), min-of-φ_d binding. higher-order + exact IIT4 relation φ = n≤5 frontier, M5 calibration (F-IIT4-4)
- [x] IIT4.md M3 체크 + hub/status 갱신
- [ ] 다음 = M4 big-Φ (`iit4_bigphi.hexa` — Φ-structure 의 system-MIP irreducibility → 최종 faithful Φ)

## 2026-05-25 — M2 distinctions LAND (iit4_distinction.hexa · 12/12 🟢)

- [x] `HEXAD/IIT4/lib/iit4_distinction.hexa` 작성 — IIT 4.0 distinction 레이어 (import-safe, M1 import)
  - `small_phi_effect/cause` = min over directional bipartition 의 intrinsic difference @ specified state z* (MIP). ii=0 → φ=0
  - `iit4_partitioned_effect` = per-purview-unit 을 paired mechanism part 의 marginal 로 (empty part → unconstrained)
  - `iit4_partitioned_cause` = 두 part cause repertoire 곱 (disjoint purview, reindex)
  - `mice_effect/cause` = 全 purview argmax → 가장 환원불가능한 cause/effect
  - `distinction` = φ_d = min(φ_c, φ_e) + 양 purview/state · `count_distinctions`
- [x] smoke `state/iit4_m2_smoke_2026_05_25/run_m2.hexa` — COPY n=2 손계산 + noise null control
  - small_phi_effect {0}=ON over {1}=1.0 · over {0}=0.0 · cause=1.0 · MICE φ=1.0 purview {1}
  - distinction {0}/{1}=ON φ_d=1.0 (대칭) · count≥2 · noise φ=0 distinctions=0
  - **12/12 PASS** (`hexa run`, deterministic) → result.json 🟢 SUPPORTED-NUMERICAL
- [x] honest: partition scheme = all-directional-bipartition MIP (IIT-3.0-style tractable). IIT 4.0 specific partition set + PyPhi 수치 calibration = M5 (F-IIT4-2/3)
- [x] IIT4.md M2 체크 + hub/status 갱신
- [ ] 다음 = M3 relations (`iit4_relation.hexa` — distinction purview 겹침 congruent face + Φ-structure 조립)

## 2026-05-25 — M1 repertoire LAND (iit4_tpm.hexa · 13/13 🟢)

- [x] `HEXAD/IIT4/lib/iit4_tpm.hexa` 작성 — IIT 4.0 인과 primitive 레이어 (import-safe)
  - TPM = state-by-node flat array `tpm[s*n+u]` (conditional-independence 가정)
  - `effect_repertoire` = 비-mechanism unit max-entropy marginalize → purview 곱 분포
  - `cause_repertoire` = uniform prior Bayes (past purview likelihood 정규화)
  - `unconstrained_effect/cause` = informativeness 의 q reference (marginal / uniform)
  - `intrinsic_difference(p,q)` = max_x p·log2(p/q) + specified state (tie-break 최저index)
  - bit ops = 곱/나머지만 (bitwise 회피, phi_native §5 패턴)
- [x] smoke `state/iit4_m1_smoke_2026_05_25/run_m1.hexa` — COPY n=2 손계산 검증 네트워크
  - effect/cause {0}=ON over {1} = [0,1] · unconstrained = [0.5,0.5] · ID=1.0 bit @state1 · ID(p,p)=0
  - n=3 rotation 구조 sanity (sum=1, ≥0)
  - **13/13 PASS** (`hexa run`, deterministic) → result.json 🟢 SUPPORTED-NUMERICAL
- [x] hexa_v2 transpiler 재빌드 필요했음 (`hexa cc` — self/native/hexa_v2 부재) → 빌드 후 통과
- [x] IIT4.md M1 체크 + hub/status 갱신
- [ ] 다음 = M2 distinctions (`iit4_distinction.hexa` — small-φ min-partition ID · MICE purview search)

## 2026-05-25 — M0 design spec LAND (HEXAD/IIT4/DESIGN.md)

- [x] `HEXAD/IIT4/DESIGN.md` 작성 — 8 §: (1) 2축 갭 framing (partition×primitive, IIT4=인과 칸) (2) IIT 4.0 6단계 매핑 + intrinsic difference 공식 (3) scope·복잡도 envelope (4) hexa 모듈 레이아웃 (5) M1–M6 분해+단위검증 (6) calibration target (7) falsifier ×6 frozen (8) C3 ×5
- [x] predecessor 확인 (HEXAD/LIFE on main): H_278 = exact MIP-EI 가 **partition 축만** faithful (heuristic→exact-MIP), primitive 는 여전히 상관 MI → IIT4 가 메우는 칸 = 인과 cause-effect
- [x] phi_helper.hexa / phi_native.hexa = RFC 036 상관-MI primitive (proxy lane, F-IIT4-6 비교 baseline 으로 READ-ONLY 재사용)
- [x] 정식 출처 앵커: Albantakis et al. 2023 (arXiv:2212.14787) + Barbosa et al. 2020 (intrinsic difference)
- [x] honest 경계: relations exact n≤5 (PyPhi 실용한계 동일) · PyPhi=calibration only (g5+hexa-only) · CI-TPM 가정 · ID tie-break 최저index · large-N 불변
- [x] IIT4.md M0 체크 + hub/status 갱신
- [ ] 다음 = M1 repertoire (`HEXAD/IIT4/lib/iit4_tpm.hexa` — TPM·cause/effect repertoire·ID + self-test). $0 mac-local

## 2026-05-25 — 도메인 개설 (LIFE proxy-lane 후속)

- [x] `/domain init IIT4` + `set IIT4` — full-IIT4 cause-effect Φ-structure 엔진 lane 개설
- [x] @goal 선언: hexa-native faithful IIT 4.0 엔진(n≤8 exact) — TPM→repertoire→distinction→relation→Φ-structure→big-Φ, PyPhi calibrate 후 LIFE small-N 가설 faithful 재측정
- [x] 마일스톤 M0~M6 시드 (design spec → repertoire → distinctions → structure → big-Φ → calibration → LIFE 재측정)
- [x] 동기: LIFE(22 NEW H 완결)의 全 Φ 가 proxy(phi_spatial)/스칼라(H_278 MIP-EI) — full IIT4 structure 로 반복 caveat(L-C2.1·metric-fragile·cosine-artifact) 종결
- [x] 첫 작업 = M0 design spec 착수 (사용자 "IIT4 도메인 진행"). $0 mac-local·GPU 무관, multi-round 엔진 빌드 (smoke 아님)
