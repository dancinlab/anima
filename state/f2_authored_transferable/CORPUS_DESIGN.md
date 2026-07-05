# rule-structured transferable-form corpus — 실행 설계 (F2 escape, 303M)

> fable-mode: Fable 위임 시도했으나 백엔드 무응답(GLM 스위치 잔재) → self-design(tool-down 폴백). Fable 복구 시 이 스펙을 review/발산 대상으로.

## 왜 이 형태 (session-grounded)
F2 poc(#3035): 체계적 compositional-rule corpus는 held-out 전이 R² 0.425, collocation은 -0.508(delta +0.93). crux(#3032): 303M 합성=additive(bilinear interaction 無). ⟹ escape = 데이터의 **target이 held-out-derivable systematic rule을 따르게** authoring. "dense δ_FM"만으로는 form-priming(H_9128 🟠)에 그침 — rule-derivability가 핵심.

## 설계 (attribute-transfer rule family 채택)
개념을 identity가 아니라 **systematic attribute**로 조합해, held-out (a,b) 결과가 규칙으로 도출되게 한다.

### 1. 개념 공간
- ~200 concepts (anima 4-cell register vocab 재사용: ko/en × general/sns).
- 각 concept에 systematic 속성 2개 부여: `role_type ∈ R`(작용 역할, |R|~8), `value_type ∈ V`(피작용 값, |V|~8). 속성은 조합 primitive(암기 아님).

### 2. 조합 규칙 R (비교환)
- 고정 결정함수 `compose(role_type(a), rel, value_type(b)) → result_type` (룩업 테이블 |R|×|Rel|×|V|→result, seed 고정).
- 비교환: compose(a,rel,b) ≠ compose(b,rel,a) (role vs value 슬롯 비대칭).
- held-out (a,b)도 각 속성이 train서 관찰됐으면 규칙으로 도출가능 = compositional generalization.

### 3. 표면형 (byte-LM-native · anima 레지스터 텍스트)
```
<A>는 <role_type_A> 성질이고 <B>는 <value_type_B> 성질이다. <A>가 <B>를 <rel>하면 <C>가 된다.
```
- C = result_type을 대표하는 concept. 진짜 언어(산술 a+b=c 아님), 규칙을 담음.
- 4-cell 균형(ko·en × general·sns 어투 변주)로 register 유지(a_chat_registers).

### 4. held-out split (compositional-generalization)
- 모든 concept·속성·규칙은 train/test 공유, **특정 (A,B,rel) 조합만 held-out**.
- 추가로 일부 concept 전량 held-out(강한 전이 테스트). F2 poc/crux disjoint-split 논리 동형.

### 5. anti-Goodhart / frozen bar (form-priming 방지 · H_9128 trap)
- **shuffle-rule 통제 corpus**: 같은 표면 템플릿, C=규칙무관 랜덤. 템플릿만 암기하면 real·shuffle 둘 다 통과; 규칙을 배우면 real만 통과.
- **pre-reg kill**: held-out C-정확도(real) − held-out(shuffle-rule) ≥ margin. 안 이기면 form-priming = 🧱(데이터가 rule-carrying 실패).
- 측정 = `anima evaluate --py <clm>` G1 ladder: held-out composed_distinct ≥2 > max_single + shuffle/ablation 통제. engine-native TERMINAL.

### 6. 생성 계획 ($0 authoring → 303M)
1. 200 concept × 속성 배정 + compose 룩업 테이블 고정(seed).
2. TRAIN (A,B,rel) 부분집합 문장 생성(~50–100k, 4-cell 균형) + TEST held-out 부분집합. + shuffle-rule 대조 corpus.
3. `anima corpus`(a_cli_single_entry) 파이프라인 편입 · HF `dancinlab/anima-corpus-rulestruct`(PUBLIC).
4. 크기 ~5–20MB(기존 corpora 급). 303M retrain=owner GPU-go(pool summer/aiden) → `anima evaluate --py` held-out G1.

## 판정
- 🟢 G1 recombination: held-out composed-C가 shuffle-rule 통제 이김 ∧ composed_distinct≥2>max_single = anima 최초 실 G1 pass(rule-structured 데이터 위).
- 🧱 재검: rule-structured 데이터인데도 floor면 벽이 data-form보다 깊음 = F2 poc와 모순 → verdict-integrity 재확인(tokenizer·split·측정경로).
- scope(a_scale_honest_scope): poc는 원리 증명, 이 스펙이 실 303M 스케일. toy≠closure.

## 조율
production corpus authoring = E1/G1 lane 소유(E1_F2_coordination.md). 이 스펙 = 두 lane 공유 recipe(경쟁 corpus 아님). 원리·측정 프로토콜 = 이 세션, 대규모 authoring+build = E1 lane + owner GPU-go.
