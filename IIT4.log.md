# IIT4 — log

Append-only history sister of `IIT4.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

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
