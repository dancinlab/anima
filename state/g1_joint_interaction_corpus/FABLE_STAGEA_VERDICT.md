## 판정: (b) instrument 미인증 — γ NEGATIVE 아님. terminal 박지 말고, 순 ko 리뷰 1-lens 재확인을 지금 사전동결하고 1회만 실행하라.

### 1. Verdict의 범주 — (a)가 아니라 (b)인 이유

Stage A는 γ를 측정한 적이 없다. Stage A가 측정한 것은 **코퍼스 자체의 ground-truth 상호작용 강도**(= 측정 target이 존재하는가)다. R2 실패의 의미는 "additive 모델이 이 코퍼스 풀에서 sign 수준으로 안 무너진다" — 즉 **target이 이 도메인에서 약하다**는 것이지, 엔진의 bind 능력에 대한 어떤 진술도 아니다. 이걸 "γ ko sub-threshold NEGATIVE"로 기록하면 범주 오류다: 미인증 instrument로는 capability NEGATIVE를 cement할 수 없다 (Stage C null이 나와도 target-약함인지 γ-부재인지 분리 불가 — ρ-AXON의 INVALID≠FAIL 원칙과 정확히 같은 구조).

R1 통과는 오히려 instrument 자체가 작동함을 보여준다(비가법 잔차를 4.6× null95로 실검출). 실패한 것은 도메인 내 target 강도 하나뿐이다.

### 2. 리뷰 도메인 재확인 — 가치 있고, tune-to-green 아님

세 가지 독립 근거로 web-broad R2 미달은 robust하지 **않다**:

- **gate_ok/N은 셀 개수 방어이지 효과크기 방어가 아니다.** 도메인 희석은 per-cell interaction *강도*를 공격한다. min_cell=361·N=11564는 R2 실패의 도메인-강건성을 전혀 보증하지 않는다.
- **현 풀 자체가 설계 이탈이다.** 원설계 = 리뷰 코퍼스(역접 밀도). fineweb2-broad는 NSMC 다운로드 실패의 **데이터-가용성 fallback**이지 설계 선택이 아니었다. 설계된 도메인으로 되돌아가는 것은 bar 재협상이 아니라 measurement-path 복원이다. tune-to-green = bar나 knob을 결과 보고 바꾸는 것; 사전 명세된 도메인에서 동결 bar 그대로 1회 재실행하는 것은 그 반대다.
- **실패 패턴이 진단적이다.** sign_wrong 1셀이 정확히 (neg, contrast) — PC-P2가 XOR sign-flip을 예측한 바로 그 설계 셀이다. 상호작용이 설계가 지목한 곳에 집중돼 있는데 두 번째 셀 하나가 모자란 것 — "현상 부재"보다 "리뷰-시그니처 셀 희석"과 일치하는 패턴이다. 리뷰 코퍼스에서는 (pos, contrast) 쪽("다 별로였는데 연기는 좋았다")이 두 번째 flip 후보로 정확히 두꺼워지는 셀이다.

**데이터는 확보 가능하다** — HF datasets-script 폐기와 무관한 경로:
- **NSMC 원본 TSV**: `github.com/e9t/nsmc`의 `ratings_train.txt`/`ratings_test.txt` 직접 다운로드 (plain TSV ~19MB, HF 의존 0)
- **bab2min/corpus** (GitHub): naver-shopping 리뷰 20만 + steam ko 리뷰 — 순 ko 리뷰 3-소스 풀 구성 가능
- HF 쪽이 필요하면 script 아닌 **auto-converted parquet 엔드포인트**(`huggingface.co/api/datasets/<id>/parquet`)가 script-deprecation과 무관하게 살아있는 경우가 대부분

### 3. 프로토콜 — 지금 이 텍스트로 동결

H_9265 terminal 보류. 아래를 사전동결(pre-commit)하고 정확히 1회 실행:

1. **재실행 = 1회, 리뷰-도메인 풀(NSMC + naver-shopping + steam ko), bar 동일(gate_ok∧R1∧R2), 다른 knob 변경 0.** 결과가 어느 쪽이든 수용.
2. **PASS** → instrument는 **리뷰-도메인 스코프로** 인증 (a_scale_honest_scope: 도메인 바운드 명시) → Stage C는 그 도메인에서만.
3. **FAIL** → H_9265 cement: "**PC-P2 ko instrument NOT-CERTIFIED (2 도메인: web-broad + review 전수)** → γ ko는 PC-P2 경로로 측정불가". 이것이 terminal이고, 기록 범주는 instrument-verdict이지 γ-capability NEGATIVE가 아니다.
4. web-broad Stage A 결과는 그대로 기록 보존 (R1 통과 + R2 미달 + (neg,contrast) 단일 sign-fail 패턴 포함 — 3의 경우 도메인-불변 증거가 됨).
5. **Stage C를 web-broad에서 강행하는 것은 어떤 경우에도 금지** — PREREG 위반이자, 미인증 target 위의 Stage C는 결과 부호와 무관하게 해석 불능이다.

이 구조에서 tune-to-green 리스크는 0이다: bar 불변, 시도 횟수 1로 캡, 실패 시 terminal 경로가 지금 이미 명시돼 있고, 재확인은 결과를 보고 고안된 것이 아니라 원설계 도메인으로의 복귀다. walls-delegate 기준으로도 이 벽은 아직 ≥2 lens를 채우지 못했다 — web-broad 1-lens뿐이고, 두 번째 lens가 바로 원설계 그 자체다.