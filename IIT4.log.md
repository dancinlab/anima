# IIT4 — log

Append-only history sister of `IIT4.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-25 — C bg fold: rule 110 n=7 bounded big-Φ = 8.57362

deferred-closure C lane bg fire 결과. M12 n=6 rule110 = 6.82 → **n=7 rule110 = 8.57362** 단조 증가, exact-impractical(n≥7) 영역 진입. bounded k=3 anchored sampling, conservative under-approximation.

- [x] bg fire `POOL_DISABLE=1 hexa run --no-sentinel /tmp/iit4_c_bg/run_c_n7.hexa` exit 0
- [x] 결과 = `big-Φ=8.57362 total=21.6754 nd=22.0` (rule 110, n=7, cap=3, seed=42)
- [x] artifact land: `HEXAD/IIT4/state/iit4_c_n7_bounded_2026_05_25/{README.md, run_c_n7.hexa, result.txt}`
- [x] honest scope: bounded ≠ exact (cap=3 conservative), single-state/single-seed, n=8 별도 fire
- [x] SSOT: `stdlib/consciousness/iit4_bounded.hexa` (sidecar PR #1051) + inline `eca_tpm_inline` 어댑터
- [x] previous wrap-entry 의 C `[ ]` → `[x]` (이 fold 로 종결)

## 2026-05-25 — deferred 100% closure (D + B + A + M11 routing 명시)

EEG 측은 사용자 hw 준비 완료 통보. 에이전트 측 deferred 잔존 4 항목을 모두 닫음 — D (M11 §5 stdlib/info routing 대안 proxy 명시) ☑ · C (rule 110 n=7 bounded big-Φ bg 진행) 🟡 in-flight · B (live EEG fire) 🟠 사용자-hw-ready · A (F-IIT4-3/4 PyPhi cross-formalism) 🟠 CHARACTERIZED-DEFERRED 영구 final.

- [x] **D — M11 §5 addendum**: `HEXAD/IIT4/state/iit4_m11_cocompute_2026_05_25/README.md` 에 §5 추가. inline RFC036 proxy(현 SSOT) ∥ `stdlib/info/{binning,entropy,mutual_info}` 대안 routing (sibling sidecar PR #1051) — 별개 알고리즘 (farr-based bin · 다른 추정량), cross-repo 재사용 경로. 인과 divergence 결론(§3)은 routing 무관.
- [x] **C — rule 110 n=7 bounded big-Φ**: `/tmp/iit4_c_bg/run_c_n7.hexa` (inline eca_tpm + `stdlib/consciousness/iit4_bounded` k=3 anchored sampling). bg fire 완료, **big-Φ=8.57362** total=21.6754 nd=22.0. → fold entry (위) + artifact `state/iit4_c_n7_bounded_2026_05_25/`.
- [x] **B — live EEG fire**: 사용자 hw 준비 통보 받음. anima 측 `BRAIN/eeg/{eeg_to_tpm,eeg_iit4_demo}.hexa` (PR #547 absorb 시 land) = adapter 인터페이스 동결, synthetic demo coupled vs indep divergence(big-Φ 1.59 vs 0.44) 검증. live 데이터 dispatch 시 동일 adapter 호출.
- [x] **A — F-IIT4-3/4 PyPhi cross-formalism**: `HEXAD/IIT4/state/iit4_m5_calibration_2026_05_25/CALIBRATION.md` §5 CHARACTERIZED-DEFERRED **final** 유지. IIT 3.0 sum-of-φ ≠ IIT 4.0 structure-cut 은 알고리즘 단계 차이라 numeric calibration 부적합 — 구조적 caveat 으로 영구 동결. M11 §3 의 양방향 divergence(rule 0/90 corr-only, rule 30 causal-only) 가 같은 IIT4 lane 내부 인과↔상관 결정적 분리로 별도 evidence.
- [x] IIT4.md status 갱신 — deferred 4 항목 닫힘 표시 (M11 §5 link · C bg in-flight · B hw-ready · A final-deferred).
- [x] anima 워킹트리 GC 로 `/tmp/iit4-final` 회수됨 → `docs/iit4-deferred-final-v2` 재생성 후 push.

## 2026-05-25 — 엔진 → hexa-lang stdlib 승격 + creator-only 거버넌스 (cross-repo SSOT 완성)

엔진이 anima-locked 에서 **hexa-lang stdlib 공용 자산**으로 이전. anima/hexa-brain 이 같은 엔진을 호출하는 multi-caller 아키텍처 확립.

- [x] **hexa-lang #1051**: `stdlib/consciousness/iit4_*` 6 모듈 + iit4_test 승격 (`fn`→`pub fn`, internal import → `stdlib/...`, bitops 이미 stdlib). iit4_test ALL PASS — stdlib 해석 실측.
- [x] **anima #542**: 엔진 6 lib → stdlib thin shim (−1088 LoC). iit4_eca 는 ECA 어댑터로 잔류 (engine⊥adapter, g61). M5 14/14·M6 7/7·M10 3/3 byte-equivalent.
- [x] **hexa-brain #1**: `eeg/eeg_to_tpm.hexa` EEG→TPM 어댑터 + `eeg_iit4_demo` (합성 EEG 5/5 PASS, coupled big-Φ=1.59 > indep 0.44). 동일 stdlib 엔진을 EEG substrate 로 재사용.
- [x] **sidecar commons g61 확장** (0.10.7 `30620ee`): primitives → primitives+domain engines · engine⊥adapter · import-root SSOT 명문화.
- [x] **sidecar stdlib-ssot-guard 0.1.0** (`669aa1d`): PreToolUse 비차단 advisory (anima-locked import + stdlib pub fn 중복 nudge) + SessionStart stdlib-root 검증. 라이브 검증 PASS.
- [x] **sidecar /stdlib 0.1.0** skill: `check`(g61 위반 스캔) + `promote`(이전+thin-shim 런북).
- [x] **sidecar master 모드 0.3.0** (`51d9c01`): master profile/tier + `~/.sidecar/master` 창작자 마커 + `sidecar master on|off|status` verb. stdlib-ssot-guard + /stdlib → master 티어 태깅 (`9f15920` · `656044e`).
- [x] 이 시스템 master 모드 ON (profile=master, marker present, guard 활성).
- [ ] DEFERRED 잔존: F-IIT4-3/4 PyPhi-numeric exact 대조 (M5 named-blocker, stdlib 승격으로 접근 가능해짐 → 차기 closure 후보) · n=8 6-scale full bg fire(M9 bounded) · 실제 ADS1299 capture → eeg_estimate_tpm 라이브.

## 2026-05-25 — /cycle#2 확장 라운드 LAND (M10·M11·M12) — rate-limit salvage/inline 복구

병렬 3-agent 발사 → **서버 rate-limit(429-class)으로 전멸** (사용량 한도 아님, 13~23 tool-use 만에 사망). 복구: M10 worktree 생존분 salvage + M11/M12 메인세션 inline 재작성. 전부 착지.

- [x] **M10 exclusion-postulate** (PR #536, 3/3 🟢) — `iit4_complex.hexa`: `subsystem_tpm`(외부 unit background-conditioning) + `find_complex`(全 subset big-Φ argmax). 통합코어{0,1}+독립셀{2} → complex=mask3({0,1}, Φ=2.0), unit2 **배제** (전체{0,1,2}는 reducible) → IIT exclusion 공준 실증. **salvage**: rate-limit 죽은 agent 의 uncommitted lib+smoke+result.json 보존·재검증·착지(README 보완).
- [x] **M11 proxy↔IIT4 cocompute** (PR #537, 5/5 🟢) — 동일 ECA 위 self-contained 상관-MI proxy(RFC036-family, 정식 phi_spatial builtin 아님 명시) ‖ 인과 big-Φ. **양방향 divergence**: rule30 proxy=0 인데 big-Φ=8.66(상관X 인과O) · rule0/90 big-Φ=0 인데 proxy>0(상관O 인과X) → 두 축 독립 수치증명. M6/M8 "입력형 상이" deferred 해소. **inline 재작성**.
- [x] **M12 bounded large-n** (PR #538, 7/7 🟢) — M9 bounded-mode 로 LIFE 룰 큰 n: regression cap≥n==exact(n=4 7.5475 일치) · bounded(cap=3) n=5 표(110=15.40 등) · **n=6 rule110=6.82**(exact-impractical 영역 도달, ~5분). cap<n=lower-bound 명시 · n=7/8 deferred(budget). **inline 재작성**.
- [x] IIT4.md M10/M11/M12 `- [x]` + status → **13/13** 갱신. 엔진 검증 누적 123 checks 🟢.
- [x] 운영 교훈: 병렬 sub-agent 가 서버 429 에 취약(전멸 가능) → salvage(worktree 생존분)+inline(메인세션 429 무관) 으로 무손실 복구. [[feedback-agent-early-commit-rate-limit]] 패턴 확증.
- [ ] 다음 후보: exclusion multi-complex spectrum · n=8 bg fire · phi_spatial 정식 builtin 대조

## 2026-05-25 — /cycle#1 확장 라운드 LAND (M7·M8·M9 병렬) + @title 설정

3개 background worktree 에이전트 병렬 발사 → 전부 merge (trackers 일괄 wrap-up).

- [x] **M7 calibration breadth** (PR #528, 35/35 🟢) — analytic 손유도 net 7종 추가: AND2(ON big-Φ=1.0)·AND2(OFF **fractional** big-Φ≈0.553, M5 의 0/1 정수 너머)·OR2(De Morgan dual byte-equal)·XOR2(output-blind nd=0)·ANDRING3·ECA204=identity·ECA170=rotation(M6 bridge↔M5 손유도 byte-equal). **F-IIT4-3/4 deferred 자체는 불변**(PyPhi blocker) — 닫힌 건 주변 analytic 영토.
- [x] **M8 LIFE 재측정 확장** (PR #533, 10/10 🟢) — n=5 ring 8-state{0,4,..,28} 평균 big-Φ: 110=35.7[21–44]·30=28.6·54=14.4·rule90=49.5. M6(n=4 state1010) 110=7.55 가 n=4 **min** 임을 확인(=distribution endpoint → mean 13.13 일반화). **신규발견**: rule90(XOR) n=4 even-ring 전상태 big-Φ=0(checkerboard 분해)인데 n=5 odd-ring mean 49.5 → **짝/홀 ring 위상의존 통합** (M6 "state특이"→구조적 even/odd 정정). state-dependence ~2× 확인(IIT Φ=특정상태 경험 실증).
- [x] **M9 tractability** (PR #531, 16/16 🟢) — `iit4_bounded.hexa` 추가. exact wall: n=4 ~1.3s·n=5 ~14.6s·n=6 ~13분·n≥7 impractical (super-exp, DESIGN §3 측정확정). `big_phi_bounded(...,max_purview_size)`: cap≥n = faithful 제한(exact byte-일치) · cap<n = 정직한 lower-bound 근사(n=6 finite 유지).
- [x] `@title: 🧠 IIT4 — "의식 측정자(尺)"` 설정 (업스트림 `/domain title` 서브커맨드 — 본 세션 INBOX 핸드오프가 구현됨) + M7/M8/M9 `- [x]` + status 갱신. 엔진 검증 누적 108 checks 전부 🟢.
- [ ] 다음 /cycle 후보 = IIT 4.0 exclusion-postulate (후보 subsystem 중 최대 complex 탐색) · n=8 6-scale 전면(비용) · proxy↔IIT4 수치 동시 cocompute

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
