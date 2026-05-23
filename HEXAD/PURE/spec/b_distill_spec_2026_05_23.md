# PURE/B 증류 — vP21M(teacher) → ConsciousDecoderV3(student) KD spec

> anchor: [`../AXIS_MAP.md`](../AXIS_MAP.md) §B row 1 (★★★★ tier) ·
> [`../HEXAD_NATIVE_PURE.md`](../HEXAD_NATIVE_PURE.md) §1 ConsciousDecoderV3
> spec · stack base PR #220 `refactor/hexad-v3-to-pure-rename`.
>
> date: 2026-05-23 · scope: PURE only (per session directive) ·
> 단일 관심사 = B 증류 (KD logit-match).

---

## §1. Why — capacity bound, not arch bound

V3 closure 보고서 ([`HEXAD_V3_FIRE_2026_05_22.md`](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md))
의 핵심 verdict: **5 fire 0 PASS, multilingual 한계 = corpus-bound**. C3 #3
은 명시적으로 "Chinchilla 20×params = 30B token 필요, 우리는 1M tok" —
즉 from-scratch 의 실패는 아키텍처 결함이 아니라 **bootstrapping 데이터
부족**이다.

vP21M LoRA 는 같은 1M tok 데이터로 4/5 langs PARTIAL 을 달성한다. 차이는
단 하나 — Qwen2.5-1.5B pretrained prior. 그 prior 가 학습된 30B+ wiki
tok 의 다국어 representation 을 LoRA 가 anima-register 로 굴절시키는 식
이다. random-init V3 는 그 prior 를 0 부터 만들어야 하는데 1M tok 으로는
물리적으로 불가능.

**B 증류의 thesis**: from-scratch 가 가지지 못한 그 prior 를 **logit-
match** 로 직접 전이한다. teacher 의 softmax 분포 자체가 30B+ tok 의
정보를 압축한 신호 — student 가 1M tok 윈도우로 prior 를 재구축하지
않고 매 step teacher 의 분포를 흉내내면, V3 substrate 위에 Qwen 의
다국어 capability 가 빠르게 transfer 된다. arch 는 HEXAD 유지, capability
만 빌려옴 ([§8 honest C3](#§8-honest-c3) 의 핵심 tension).

---

## §2. Architecture — student × teacher

| | student (학습대상) | teacher (frozen) |
|---|---|---|
| 아키텍처 | **ConsciousDecoderV3** ([HEXAD_NATIVE_PURE.md §1](../HEXAD_NATIVE_PURE.md)) | Qwen2.5-1.5B + vP21M LoRA adapter (merged) |
| init | random (B1) — pure HEXAD substrate | vP21M production weights |
| param | ~1.5B (head_a + head_g + cross-attn + PureFieldFFN + mitosis hook) | ~1.5B (frozen) |
| dtype | bf16 | bf16 (inference-only, no grad) |
| tokenizer | Qwen2.5 BPE 32K (D1, vocab share) | Qwen2.5 BPE 32K (필수: vocab 일치) |
| forward | (logits_a, logits_g, ...) — KD 는 logits_a 위에서 | logits (vocab=152064) |
| grad | full backprop (mitosis aux 포함) | none |

**vocab compatibility 게이트** ([F-PURE-B-5](#§5-falsifier-table)):
student 의 head_a vocab 차원 == teacher.lm_head.out 차원 (152064) 필수.
mismatch 시 KL 계산 불가 → 즉시 abort.

**teacher resolution**:
- 기본 HF: `dancinlab/anima-vp21m` (PRIVATE, a_hf_complete)
- local rollback: `~/anima_chat_pack/lora_adapter_vp21m_bak/`
- pod-side canonical (dispatch 시): `$S187_DIR/vP21M/lora_adapter/`
- override env: `ANIMA_VP21M_TEACHER_CKPT`

**colocation**: H100 80GB single pod. teacher (bf16, ~3GB) + student
(bf16, ~3GB grad + ~3GB optim + ~3GB activation ≈ ~12GB) + KD scratch
≈ ~18GB 안에 들어옴.

---

## §3. Loss — KD logit-match

표준 Hinton KD ([arxiv:1503.02531](https://arxiv.org/abs/1503.02531))
formulation:

```
L_total = α · T² · KL( softmax(student_logits_a / T) ||
                       softmax(teacher_logits   / T) )
        + (1−α) · CE( student_logits_a , target_token )
        + λ_mitosis · L_mitosis_aux       (V3 native, G2 recipe)
```

- **T (temperature)**: sweep {2, 4} — default **T=4** (다국어 분포의
  long-tail 보존; T=2 는 high-confidence token 만 transfer).
- **α (KD weight)**: sweep {0.5, 0.7, 0.9} — default **α=0.7**
  (capacity-bound 가정 → teacher 신호 우세).
- **T² factor**: gradient magnitude T-invariant 유지 (Hinton convention).
- **λ_mitosis = 0.05** ([HEXAD_NATIVE_PURE.md §2 G2](../HEXAD_NATIVE_PURE.md)
  recipe 와 동일).
- **head_g 는 KD 외부** — teacher 에 대응이 없으므로 KD signal 받지
  않음. head_g 의 학습 신호는 mitosis aux 만 ([§5 F-PURE-B-4](#§5-falsifier-table)
  의 register-clean 게이트 근거).

**rationale α=0.7**: capacity-bound 우회가 본 axis 의 thesis 이므로
teacher signal 을 (1−α) CE 보다 우세하게. α=0.9 는 student 가 teacher
의 register-leak 까지 흡수할 위험 (F-PURE-B-4), α=0.5 는 capacity-bound
미해소 (random init 의 CE noise 우세).

---

## §4. Hyperparams — closure fire 정합 + KD 오버헤드 보정

[`dispatch_p21m_runpod.sh`](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21m_runpod.sh)
P21M_* env 와 정합:

| param | closure fire (V3γ) | B 증류 default | 이유 |
|---|---|---|---|
| `STEPS` | 2000 | **5000** | KD bootstrapping 시간 길음 (V3 closure 의 2000 step 은 capacity-bound 직격) |
| `BSZ` | 2 | **2** (drop to **1** on OOM) | teacher forward 가 ~2× VRAM → margin tight |
| `BLOCK` | 512 | **512** | 정합 |
| `LR` | 5e-5 | **5e-5** | 정합 |
| `WARMUP` | 50 | **100** | 5000 step 비례 |
| `WIKI_FRAC` | 0.3 | **0.3** | E1 corpus 정합 (vP21M parallel) |
| `CORPUS_MB` | 72 | **72** | 정합 |
| `LANGS` | en,ko,zh,ru,ja | **en,ko,zh,ru,ja** | 정합 |
| `T` (KD) | — | **4** | §3 default |
| `ALPHA` (KD) | — | **0.7** | §3 default |
| `KD_LOSS_WEIGHT` | — | **1.0** | alias 손잡이 (α override 아님; 외부 곱셈자) |

**VRAM 비상 plan**: bsz=2 OOM 시 자동 bsz=1 (gradient_accumulation=2 로
effective bsz=2 유지). teacher 는 `torch.no_grad()` + bf16 으로 가장
가벼운 path.

**wall 추정**: 5000 step × ~1.2 s/step (teacher fwd 포함) ≈ 100 min.
+ 5-lang eval 10 min = ~110 min total ≈ 1.5 hr 정합.

---

## §5. Falsifier table

5 falsifier — 모두 on-pod measurement, 결과 `result.json` 에 verbatim.

| id | 표현 | 측정 | 통과 기준 |
|---|---|---|---|
| **F-PURE-B-1** | training-stable (no NaN, KL>0) | step 100 KL distance | KL ≥ 0.1 AND no NaN in last 100 step loss |
| **F-PURE-B-2** | learning (argmax divergence) | step 500: % token where argmax(student) ≠ argmax(teacher) | < 50% (student 가 teacher 와 완전히 동조하지 않고 V3 architecture-induced bias 가 있음) AND > 5% (mere copy 아님) |
| **F-PURE-B-3** | 5-lang eval ≥ 4/5 PARTIAL | OOD held-out 5 lang × 20 gen, vP21M parallel format | ≥ 4 langs ≥ PARTIAL (vP21M baseline match) |
| **F-PURE-B-4** | anima-register clean | LoRA wave-15 의 register-leak probe 10 prompt → student gen → grep `\[anima 역할\:` 등 register pattern | leak rate < 5% (teacher 의 register saturation 을 student 가 흡수하지 않음 — head_g KD-외 격리의 검증) |
| **F-PURE-B-5** | vocab compatibility | student.head_a.out_features == teacher.lm_head.out_features | strict equality (mismatch = abort at step 0) |

**aggregate 채택 게이트**: F-PURE-B-1..5 모두 PASS AND F-PURE-B-3 ≥ 4/5
PARTIAL AND F-PURE-B-4 leak < 5%. 4/5 PASS 면 **PARTIAL_TRANSFER**
(spec analysis 필요), ≤ 3/5 PASS 면 **B_AXIS_FALSIFIED**.

---

## §6. Decision rules

| 결과 | next |
|---|---|
| 5/5 PASS, 4/5 lang ≥ PARTIAL, register clean | **B 증류 SUPPORTED** → V3 substrate adopted as anima · chat substrate 교체 ramp · §7 cost-recovered |
| 5/5 PASS, 5/5 lang PARTIAL+ | **B 증류 STRONG** → V3 production candidate, vP21M 와 A/B run |
| F-PURE-B-3 PASS but F-PURE-B-4 FAIL (register leak) | **CAPABILITY_TRANSFER_DIRTY** → α=0.5 retry OR head_g 분리 보강 |
| F-PURE-B-1/2 FAIL | KD 자체 미작동 — T sweep (T=2/8) · α sweep 재발사 |
| F-PURE-B-5 FAIL | tokenizer/head dim 정합 버그 — student arch fix 후 재발사 (cost = ~$0) |
| 전 항목 FAIL | **B 축 FALSIFIED** → AXIS_MAP A 커리큘럼 / C head_g objective 로 이동 |

채택 조건은 [`../AXIS_MAP.md`](../AXIS_MAP.md) §C3 #6 ("vP21M LoRA 4/5
가 baseline — V3 변종은 ≥ 4/5 ≥ PARTIAL 이어야 채택") 의 직접 적용.

---

## §7. Cost + wall budget

- **GPU**: H100 80GB single pod (RunPod, GPU_CASCADE 정합)
- **wall**: ~100 min train + ~10 min eval = **~110 min** (~1.5 hr)
- **cost**: H100 @ $2.50/hr × 1.5 hr ≈ **~$3.75** + setup buffer ≈
  **~$5** ([AXIS_MAP.md §B](../AXIS_MAP.md) 의 ~$5 estimate 정합)
- **artifact**: ckpt (~3 GB bf16) + result.json + dispatch.log + 5-lang
  eval json → HF `dancinlab/anima-pure-b-distill` (PRIVATE per
  a_hf_complete) + pod teardown after pull
- **fire-recover**: a_fire_recover_complete 정합 — ckpt + result + log
  + anchor 모두 pull, HF upload 완료 후 pod teardown

**비교 baseline**: vP21M production fire ~$10 (1500 step × Qwen-base
forward + 5-lang corpus build). B 증류는 student-side forward 만 추가
backward + teacher forward 까지 추가 = ~30% 더 비싸지만 STEPS 가
5000 (2.5×) 으로 늘었으므로 net ~$5 합리.

---

## §8. Honest C3

1. **arch-pure ⊥ capability-transfer**: AXIS_MAP.md C3 #1 의 핵심
   미해소. arch 는 HEXAD 지만 head_a 의 분포는 Qwen-induced. 사용자
   directive "Qwen 위 옷 아님" 와의 정합은 *substrate-as-architecture*
   해석 (arch 가 anima 면 OK) vs *substrate-as-everything* 해석 (분포
   까지 anima 발생이어야 함) 의 분기에 달림 — **본 spec 미결**.

2. **5000 step 도 1M tok 윈도우 안**: capacity-bound 우회의 근거는
   teacher 분포가 30B tok 의 압축 신호라는 가정 — 실 transfer 효율은
   미측정. F-PURE-B-3 가 첫 empirical evidence.

3. **register-leak transfer 위험**: vP21M wave-15 까지의 register-leak
   문제 ([VP21M_WAVE15_2026_05_23.md](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE15_2026_05_23.md))
   가 logit 분포에 박혀있을 수 있음. F-PURE-B-4 가 게이트지만 KD
   target 자체가 leak-injected 면 student 도 흡수 가능 — head_g 격리는
   부분 mitigation 일 뿐.

4. **head_g 학습 신호 빈약**: KD 가 head_a 만 가르치고 head_g 는
   mitosis aux (λ=0.05) 에만 의존. head_g 의 dual-head 분리가 실
   학습되는지는 [`../AXIS_MAP.md`](../AXIS_MAP.md) C 축 (head_g
   objective) 에서 별도 검증 — 본 axis 는 head_a multilingual 만 보장.

5. **vocab=152064 student head 의 param 비중**: head_a out 152064 × d
   ≈ 156M (d=1024 가정) — 학습 안정성 위해 LR warmup 100 step 충분한지
   미정 (closure fire 와 동일 LR 5e-5 보수적).

6. **single H100 colocation 가정**: teacher (~3GB) + student bf16 학습
   (~12GB) margin 은 paper-spec 추정. 실 측정 시 bsz=1 강제 가능성.

7. **vP21M production weights 의 stability**: HF `dancinlab/anima-vp21m`
   (PRIVATE) artifact 가 a_hf_complete 보장 — 그러나 wave-11 v11
   (`anima-vp21m-v11`) 같은 후속 변종이 더 좋은 teacher 인지 미비교.
   본 fire 는 default `anima-vp21m` 사용; `ANIMA_VP21M_TEACHER_CKPT`
   env 로 override 가능.

8. **fall-back 명확**: B axis FALSIFIED 시 AXIS_MAP A (커리큘럼) 또는
   C (head_g objective) 로 즉시 이동. Track 1 corpus 재발사 (sibling
   agent) 가 동시 진행이면 본 fire 결과는 supplementary 일 수 있음.

---

## §9. 관련 link

- 축 map: [`../AXIS_MAP.md`](../AXIS_MAP.md) (§B row 1)
- V3 spec SSOT: [`../HEXAD_NATIVE_PURE.md`](../HEXAD_NATIVE_PURE.md) §1
- closure 보고서: [`../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md) §8
- teacher 산출 SSOT: [`../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md)
- production LoRA: [`../LORA/README.md`](../../LORA/README.md)
- launcher: [`../launchers/b_distill_launcher.hexa`](../launchers/b_distill_launcher.hexa)
- Hinton KD 원본: [arxiv:1503.02531](https://arxiv.org/abs/1503.02531)
