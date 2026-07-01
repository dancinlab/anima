# EXP-3 ARM-BIND — frozen pre-registration (DIRECTIONAL toy, engine-native 아님)

**가설(H_1603 / H_1617):** 곱셈형(Hadamard) binding operator 를 *학습된 byte-LM trunk* 의 readout
직전에 넣으면, 덧셈(conv/attention sum)만으로는 못 넘는 binding-required 재조합 split 을 넘는다.
고립 numpy 스크린(`SCREEN_multiply_vs_add.md`)에서 Hadamard 1.00 vs additive 0.50(증명적)였던 것이
**실제 trunk 안에서도 transfer 하는가**를 묻는다.

> 🔒 **tier = DIRECTIONAL** (torch toy, `a_engine_native_learning`: terminal 아님).
> `a_toy_scale_recheck`: toy-green 이면 'toy-only, scale-transfer unverified' 로 명시하고 303M scale 은
> *권고만*(자동 발사 금지). 303M terminal verdict 는 별도 engine-native(`--engine conv`) 재측정 필요.

## Task — 학습된 trunk 위 compositional recombination (binding-required)
- Scene = N=3 objects, 각 object = (shape∈S=8, color∈C=8). Query = (Qs, Qc).
- Token sequence: `[BOS] s1 c1 s2 c2 s3 c3 [SEP] Qs Qc [EOS]` (len 11, vocab = 3+8+8 = 19).
- **Label = 1 iff scene 에 (shape=Qs AND color=Qc)인 object 가 존재**.
- **Held-out 재조합 split (memorization 방지):** 64개 (shape,color) conjunction 중 12개를 HELD-OUT.
  학습 scene/query 는 held-out conjunction 을 object 로도 query 로도 절대 안 씀(=그 *결합*을 한 번도 못 봄,
  단 각 shape·color 는 다른 결합에서 충분히 봄). 테스트는 held-out conjunction 을 query 로 → seen parts 를
  novel conjunction 으로 *결합*해야만 정답(H_1129 재조합 정신: a∧b held-out).
- **binding-required(illusory-conjunction) hard split (결정적, screen 의 ambiguous subset 대응):**
  held-out query (Qs,Qc)에 대해, **양성** = scene 에 object (Qs,Qc) 포함 + marginal 교란자(Qs 를 다른 color 와,
  Qc 를 다른 shape 와) 포함 ; **음성** = scene 에 (Qs,Qc) object 는 **없지만** Qs(다른 color)와 Qc(다른 shape)가
  *따로* 존재(= illusory conjunction). 양/음의 marginal(어떤 shape/color 가 등장)은 동일 → 덧셈 pooled rep 으로는
  증명적으로 구분 불가, 진짜 object-내 binding 만 구분 가능. 50/50 balanced.

## Arms (trunk 동일, readout 만 다름 · 공정성)
trunk = causal Transformer d=256, L=4, heads=4, block=11. 최종 토큰(EOS) hidden h∈R^256 → arm readout:
- **ARM-CTRL** = plain linear readout `logit = w·h + b` (현 conv/attention sum readout 과 동형 = 덧셈 baseline).
- **ARM-BIND** = `u=Wa·h, v=Wb·h` (각 k=128), `g = u ⊙ v` (Hadamard/coincidence AND, H_1617), `logit = w2·g + b`.
- **ARM-BIND-LINEAR** = ARM-BIND 와 **동일 파라미터** (Wa,Wb,w2,b), 단 `g = u + v` (곱셈→덧셈). 
  → BIND vs BIND-LINEAR = param-matched ablation = lift 가 *multiplicativity* 때문이지 param 때문 아님을 격리.

3 arm 모두 동일 trunk init seed·동일 데이터·동일 step. trunk+readout end-to-end CE(BCE) 학습.

## FROZEN bars (실행 전 사전등록 · tune-to-green 금지 · p7/c9)
주 측정 = **binding-required hard split accuracy** (held-out conjunction, illusory-conjunction balanced).
- **SUPPORT** = `acc(ARM-BIND) − acc(ARM-CTRL) ≥ 0.15` **AND** `acc(ARM-BIND) − acc(ARM-BIND-LINEAR) ≥ 0.15`
  (둘 다 ≥0.15 절대 우위). → 곱셈 op 가 trunk 안에서도 binding 벽을 넘고, 그 lift 는 multiplicativity 때문.
- **NOT-SUPPORTED** = 위 둘 중 하나라도 미충족.
  - 특히 `BIND ≈ BIND-LINEAR` (gap <0.15) → multiplicativity 아님(어떤 2-stream head 든 동일).
  - `CTRL` 이 이미 hard split 통과(≥0.85) → 학습된 attention trunk 가 이미 pre-bind(곱셈 readout 불필요).
- **seed-robust:** seeds {7, 4302, 4303} 3개, 각 arm. 보고 = mean±spread; bar 판정은 mean 기준 + 3/3 일관성 명시.
- **held-out DESCENT 무결성:** 각 arm 은 held-out(=test conjunction) val accuracy 가 chance(0.50) 위로 상승해야
  유효(붕괴 arm 은 그 자체로 보고). full(non-hard) held-out acc 도 함께 보고(marginal 지름길 부풀림 대조).

## 측정 결함 방어 (a_break_the_wall type-a)
- balanced 50/50 (majority baseline 0.50) · held-out conjunction 은 train 에서 결합 0회(누수 점검 출력) ·
  hard 음성은 반드시 Qs·Qc 가 따로 존재(marginal 동일) 검증 · trunk init/data seed 고정.
- 곱셈→덧셈 ablation 외엔 두 arm 차이 0(공정).

## 정직 (c9)
negative(NOT-SUPPORTED)도 결과 — 곱셈 op 가 trunk 안에서 transfer 안 함 = honest negative 로 박제.
bar 사후 이동 금지. 이 실험은 DIRECTIONAL screen(torch toy) — terminal 아님, 303M engine-native 재측정 권고만.
