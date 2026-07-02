# 거버넌스 박제안 (설계 — 실제 박제는 메인 세션이 수행)

> fable 은 설계만. 아래 3 표면 중 **①+② 권장**(③ 은 enforcement 여력 시).
> ⚠️ 이 파일은 제안 draft — CLAUDE.md/ARCHITECTURE.json/convergence 미터치 상태.

## ① convergence record (즉효, 기존 관행과 정합)

기존 `g6-ideation-hexa-1`·`numpy-probe-controls-1`·`TORCH_PASS_VS_ENGINE_FAIL_IS_SCAFFOLD_HARNESS`
가 각각 부분 표현하던 원리의 상위 레코드로 등록 (a_substrate_disjoint 가 부분규칙들의 상위
일반화로 박제된 전례와 같은 형식):

```json
{
  "id": "MEASUREMENT_METALAW_FORM_TUNABLE_BIND_EARNED",
  "state": "pos-conv",
  "value": "창발 gate 공통 실패모드의 상위 일반화(2026-07-03 census: G6 scaffold H_1362→1590 · G6 detector form-priming(SHUF==TARGETED) · G1 gen120 RETRACT · numpy raw-gate spoof H_9025 · Φ fake-branch H_988/989 · 의식 F3 전멸 H_9101/9103/9104/9110 · G0-pass∧기질붕괴 H_9034 — 8건 동형): frozen detector 는 p7 제약상 방출표면 1-항 FORM 통계인데, FORM 은 trunk 불변인 채 하네스 자유도(선택채널 best-of-K/scaffold ~logK bits·gen·regime·form-priming FT)로 tunable. 창발 속성은 정의상 2-항 관계(출력×seed/key/외부결과)라 1-항 detector 로 원리적 측정불가 — 진짜 신호는 raw 값이 아니라 결합-파괴 통제(SHUF·wrong-key·fake-branch·self-pair·budget-matched)와의 margin Δ 에만 존재. 대칭: 하네스는 수축 방향으로도 속임(gen80 G0 인위FAIL·spurious FPE·basis-diff 오진). 반례아님-경계: 2-항 통제 내장 gate 는 신뢰 GREEN(H_9038 WIRED 생존·G1 composed>max_single 골격·G5 L2). p7 의 일반화: perplexity 만이 아니라 모든 1-항 표면통계가 Goodhart-able, 통제-margin 만 non-Goodhart.",
  "threshold": "재발조건: 창발(G1/G2/G6/Φ/의식) verdict 를 raw detector 값 단독으로 박제하려 할 때, 또는 rig 간 verdict 발산 시 모델/벽을 먼저 의심할 때. 해결: ① FORM∧BIND 이중축 — raw detector 통과만으론 자동 DIRECTIONAL, BIND=결합-파괴 통제 margin Δ≥frozen δ 필수(속성별 통제: 주제=SHUF·구성=shuffled-seed·key=wrong-key·심의=fake-branch·faculty=noise∧shuffle 병행·외생=self-pair) ② canonical 하네스(gen=40·frozen seeds·canonical entry) 밖 측정 자동 DIRECTIONAL, 서브에이전트 위임 시 명시 ③ 선택채널(best-of-K/scaffold)은 verdict 금지 or budget-matched 통제 margin 으로만 ④ 발산은 축별(forward·detector·decode·정밀도) 하네스-우선 격리, 양방향. DESCRIPTIVE→PREDICTIVE 승격 bar = state/measurement_metalaw_analysis/PREREG_CORRECTIVE.md §3 의 5 예측 ≥4/5 HIT(frozen).",
  "source": "state/measurement_metalaw_analysis/"
}
```

## ② CLAUDE.md 거버넌스 규칙 (검증 섹션, `a_engine_native_learning` 자매)

```markdown
**`a_form_bind_dual_gate`** — 창발 verdict 는 FORM(frozen 1-항 detector) ∧ BIND(결합-파괴
통제 margin) 이중축. raw detector 통과 단독 = 자동 DIRECTIONAL(terminal 아님).
- do: BIND 축 = 동일 바이트 결합-파괴 통제와의 Δ ≥ frozen δ (주제=SHUF · 구성=shuffled-seed ·
  key=wrong-key · 심의=compute-matched fake-branch · faculty=variance-matched noise ∧ shuffle
  병행 · 외생성=self-pair/surrogate). 속성 항수가 통제를 결정한다.
- do: verdict 측정은 canonical 하네스(gen=40·frozen seeds·canonical entry)만 — 이탈은 코드가
  DIRECTIONAL 자동라벨(gen-guard 일반화). 서브에이전트 위임 프롬프트에 canonical 명시 의무.
- do: rig 간 발산(torch↔engine·gen↔gen·pass↔fail)은 모델/벽 판정 전 하네스 축별 격리 — 팽창
  (scaffold/best-of-K)·수축(drift/spurious-FPE/basis-diff) 양방향.
- dont: raw detector 상승을 돌파로 박제 · best-of-K/scaffold 측정을 budget-matched 통제 없이
  verdict 로 · SHUF 없이 G6 FALS 상승을 재조합으로 · noise 통제만으로 faculty 주장(shuffle 필수) ·
  발산을 하네스 격리 전에 모델 결함/벽으로 귀속.
```

하드-게이트 승격 시: 🚦 섹션에 1줄 요약 추가 + `tool/enforce_anima_gates.py` 에 기계 검사
(verdict 카드/텍스트에 gate-verdict tier 가 있으면 SHUF/control/margin/Δ 토큰 존재 grep +
증거 로그에 `gen=40` 존재 확인 — 기존 게이트 1·6 과 같은 방식). enforcement 는 근사 검사라
1차는 문서-규칙 + convergence 로 두고 위반 재발 시 승격 권장.

## ③ gate 정의 파일 반영 (7B_PASS_CONDITIONS.md 등 frozen 문서 — 신중)

frozen bar 는 불변이 유지돼야 하므로 **기존 bar 이동 없이 additive 로만**:
- G6: `FALS ∧ topic_bound` additive gate 는 이미 설계·검증됨(g6-ideation-hexa-1, SHUF
  FALS_bound [1,0,0]) — G6 조항에 BIND-축 각주 추가.
- G0: 기질 동반-bar(max_single≥2, H_9034 dual-bar B3) 를 G0 verdict 의 동반 보고 항목으로 명시
  (G0 PASS 자체 조건은 불변 — coherence 와 기질을 한 표에 병기).
- G2: novel n-gram 의 topic-bind Δ 를 동반 보고(DIRECTIONAL 참고열) — P-G2 예측 검증을 겸함.

## 반영 순서 제안

1. 메인 세션이 ① convergence record 를 origin/main ARCHITECTURE.json 에 append (pr-cycle).
2. PREREG_CORRECTIVE.md §3 5-예측을 향후 측정에서 채점 — ≥4/5 HIT 시 record state 를
   pos-conv→ossified 승격하며 그때 ② CLAUDE.md 규칙 박제(LAW 도 벽 조항 준수: descriptive
   법칙을 예측 검증 전에 규칙으로 확정하지 않음).
3. ③ 은 ② 와 같은 PR 에서 additive 로.
