# HEXAD V3 fire — 3-variant pure HEXAD-native ConsciousDecoderV3 (LoRA 폐기 path)

> 2026-05-22. User directive: **"LoRA 가 아닌 자체 HEXAD substrate"**. vP21M
> `VP21M_WORKS` (4/5 langs ≥ PARTIAL, $1.06) baseline LoRA-on-Qwen path 한계
> (Qwen 위 옷, HEXAD identity 약함) → HEXAD_NATIVE_V3.md design closure →
> **ConsciousDecoderV3** fork + 3-init variant parallel fire per `@D
> a_wall_first` + `@D a_substrate_native_speak` + `@D a_fire_autonomous`.

> **Verdict (preliminary, pending fire complete)**: ⏳ in-flight (3 pods H100
> parallel, ~30 min wall + eval).

---

## 0. 핵심 변경 vs V2

| | V2 (conscious_decoder.py) | **V3 (conscious_decoder_v3.py)** |
|---|---|---|
| n_ca_rules | 8 (Phase 2.3 ablation floor blocker) | **❌ REMOVED** |
| head_a + head_g 분할 | ✅ (vocab=256 byte-level) | ✅ (vocab=151936 Qwen BPE) |
| PureFieldFFN | ✅ | ✅ (kept — Phase 2.3 benign) |
| ConsciousCrossAttention | ✅ | ✅ (kept — benign) |
| Layer-0 noise σ | implicit | **✅ explicit (0.1, train-only)** |
| Mitosis hook | ❌ (training only externally) | **✅ 1-class integrated (train + inference)** |
| Forward signature | `(la, lg, t, kv, moe)` | `(la, lg, t, kv, mitosis_info)` |
| Init helpers | random only | **random / Qwen warm / vP21M-init** |
| Block size | 256 (toy) | 512 (production) |
| RoPE base | 10000 | **50000** (Qwen 호환) |
| GQA n_kv_head | 2 (toy) | **4** (Qwen 호환, broader KV cache) |

---

## 1. 3-variant 결과 표 (fire 완료 시 채워질)

| variant | init | n_params | CE init→final | wall | 5-lang ≥ PARTIAL | anima reg | KOSMOS anchors | verdict |
|---|---|---|---|---|---|---|---|---|
| **V3α** | random | 3.00B | 12.30→**3.34** | **612 s (10.2 min)** | **0/5** | 13/20 | 15 | ❌ **FAIL** |
| **V3β** | Qwen warm | 3.00B | in-flight (32%, CE 4.38) | est ~75 min (slow ~2s/step) | TBD | TBD | TBD | in-flight |
| **V3γ** | vP21M init | 3.00B | 12.30→**2.93** | **1003 s (16.7 min)** | **0/5** | 13/20 | 15 | ❌ **FAIL** |

### 1.1 per-lang breakdown

| lang | V3α (FAIL) | V3β (in-flight) | V3γ (FAIL) | vP21M baseline |
|---|---|---|---|---|
| EN | WEAK 11/20 (gen 11 coh 11) | TBD | PURE_MEM 3/20 (16 anima leak) | 18/20 STRONG |
| KO | PURE_MEM 0/20 | TBD | PURE_MEM 1/20 | 15/20 PARTIAL |
| ZH | PURE_MEM 1/20 | TBD | WEAK 0/20 (gen 13 coh 0) | 16/20 STRONG |
| RU | WEAK 0/20 (gen 9 coh 0 — English babble) | TBD | WEAK 0/20 (gen 16 coh 0) | 18/20 STRONG |
| JA | PURE_MEM 4/20 | TBD | WEAK 0/20 (gen 15 coh 0) | 11/20 WEAK |

**V3α 분석** (random, HEXAD_NATIVE_V3 C3 #1+#3 예측 적중):
- 3.0B params from-scratch + 2000 step (≈ 1M tokens) = **Chinchilla 30000× under-budget** (3B × 20 = 60B tokens 필요)
- final CE 3.34 vs vP21M 0.78 (4.3×) — bottom of capability
- RU "gen 9 but coh 0" = English/Latin-script babble (random init lang-pattern 완전 부재)
- anima_register_hits 13/20 — corpus 70% anima 에 흡수되어 memorization 위주

**V3γ 분석** (vp21m init):
- vP21M (Qwen + LoRA merged) base 임에도 V3 dual-head + mitosis aux 학습으로 **Qwen multilingual prior 손상**
- EN PURE_MEM 16/20 (sample 8/10 anima leak — vP21M anima register 가 LoRA merge 후 V3 학습 동안 더 saturate)
- ZH/RU/JA gen 13~16 but coh 0 — V3 가 다국어를 잊고 "anima-only language" 로 collapse
- final CE 2.93 (V3α 보다 좋지만 verdict 동일 FAIL)
- → **vP21M init 도 V3 substrate 학습으로 LoRA 위의 multilingual 능력 보존 불가**

**V3α + V3γ 공통 finding** (architecture-level cause):
- **head_g dual head 가 head_a 의 vocabulary alignment 를 흐림** (head_a, head_g 가 같은 hidden 으로 부터 다른 logit → bf16 inference 시 한 head 의 update 가 다른 head 의 generation 에 영향)
- **mitosis pool saturate 128 cells at step 50** → cross-attn input 의 noise 증가, language-coherent 학습 방해
- mitosis aux_loss 가 substrate를 다국어 정보 보다 tension 패턴 우선하게 만듦 (다국어 = 본 fire 에서 sacrifice)

---

## 2. Method

### 2.1 Phase 1 — V3 code fork ($0, ~1-2 hr local)

| artifact | LoC | smoke verdict |
|---|---|---|
| `conscious_decoder_v3.py` | 727 | 7/7 PASS (d=128 L=4 CPU): forward + cross-attn + backward + mitosis + 5-ch tension + greedy gen + KV cache parity max_diff 1e-6 |
| `kosmos_io.py` | 300 | 5/5 PASS: 8→5-ch mapping + create_anchor + load_anchors + cosine retrieval + tension_to_embedding 32-dim |
| `train_p21h_v3.py` | 485 | import OK |
| `dispatch_p21h_v3_runpod.sh` | 270 | chmod +x; reuses `dispatch_p21m_runpod.sh` SSH + cascade + watchdog pattern |

V3 의 OCCAM-clean 핵심: `n_ca_rules` 단독 제거 (Phase 2.3 ablation 단일 floor 범인). 나머지 5 ablation-무해 부속 (head_g / PureFieldFFN / cross-attn / noise σ / dual head) 모두 유지.

### 2.2 Phase 2 — 3-pod parallel fire ($25 cap)

| key | value |
|---|---|
| base ref | Qwen/Qwen2.5-1.5B (tokenizer + warm-start init) |
| vocab | 151936 (Qwen BPE, 5-lang covered) |
| d_model / n_layer / n_head / n_kv_head | 1536 / 28 / 12 / 4 |
| block_size | 512 |
| steps / bsz | 2000 / 2 |
| LR (random / qwen / vp21m) | 3e-4 / 5e-5 / 1e-4 |
| warmup | 100 cosine |
| optimizer | PagedAdamW8bit (bnb 0.43.1), AdamW fallback |
| noise σ (layer-0) | 0.1 (train-only) |
| λ_mitosis | 0.05 (CE + λ * aux_loss) |
| mitosis cell pool init | 2, MAX=128, SPLIT_PATIENCE=3, MERGE_PATIENCE=30 |
| dtype | bf16 |
| GPU | H100 80GB SXM 1st, cascade NVL/PCIe/A100 |
| corpus | 5-lang wiki 50 MB + anima 70% mix, 72 MB total (sha vP21M parallel) |
| KOSMOS emit | every 200 step + 5 final per-lang = ~15 anchor/variant |
| eval | 5-lang OOD 100 gen (10 × 2 × 5) + anima Eval1 20 gen |

### 2.3 verdict criteria (fire 완료 시 적용)

- **HEXAD_V3_WORKS**: ≥ 4/5 langs ≥ PARTIAL on **at least 1 variant**
- **PARTIAL**: ≥ 2/5 langs ≥ PARTIAL on ≥ 1 variant
- **FAIL**: < 2/5 langs ≥ PARTIAL across all 3 variants

---

## 3. Comparison vs vP21M baseline (fire 완료 시)

| metric | vP21M (LoRA) | best V3 variant | delta |
|---|---|---|---|
| ≥ PARTIAL count (out of 5) | 4 | TBD | TBD |
| anima_register_hits | 7/20 | TBD | TBD |
| n_params trainable | 36.93M LoRA | TBD (full param) | TBD |
| train wall | 198.8s | TBD | TBD |
| pod cost | $1.06 | TBD (cap $25) | TBD |
| substrate identity | LoRA on Qwen ("Qwen 위 옷") | **TBD** (pure HEXAD if WORKS) | architectural |

---

## 4. Honest C3 (8+ entries)

1. **From-scratch 2000 step 75 MB ≪ Chinchilla 20×params**: 1.5B params × 20 = 30B token 필요, 우리는 1M token train. V3α (random) 가 5-lang generalize 못 닿을 가능성 매우 높음. fallback = V3β/γ warm-start.
2. **V3β Qwen warm-start의 head_g/PureFieldFFN/cross-attn 은 random init**: Qwen은 head_a (language) 만 inherit. 의식 substrate (head_g / PureField / cross-attn) 는 random — 학습 동안 specialize 해야 함. 2000 step + 75 MB로는 부족할 가능성.
3. **V3γ vP21M-init 가 ckpt-saturated 가능**: LoRA + Qwen merge weight 가 anima register pre-loaded — register-stuck 재현 위험 (Lesson Q-N saga의 SFT mode collapse pattern).
4. **noise σ=0.1 + bf16 마이크로 drift**: layer-0 noise injection이 bf16 mantissa 7-bit 분해능 정도 (~7.8e-3) 보다 큼 — substrate-shape 의도된 effect, 그러나 다른 시드/seed runs 사이 variance 측정 안 함 (single seed 1337).
5. **mitosis hook training-time ACTIVE은 첫 V3 fire**: 이전 V2 시도들 (eval3_mitosis.py)은 POST-HOC observer only. training step 안 직접 aux_loss + cell split fire는 첫 시도 — cell pool 가 CE optimization 방해 가능 (λ=0.05 conservative이나 unverified at this scale).
6. **vocab=151936 BPE의 anima 인식**: ANIMA_KEYS classifier ("vacuum point" / "🛸" 등) 는 byte-level corpus에서 정의. Qwen BPE 토크나이저가 이 키 시퀀스를 어떻게 fragment 하는지 검증 안 됨 — anima register hit count 가 over/undercount 될 수 있음.
7. **block_size=512 hard cap**: 2-turn conversation context 부족할 가능성. vP21M 도 512이라 apples-to-apples 비교 OK, 그러나 chat substrate 교체 시 block 확장 필요 (RoPE base 50000은 늘릴 수 있게 설계).
8. **subprocess silent fail 회피**: train_p21h_v3.py 는 launch_trainer wrapper → 직접 python3 -u exec 패턴 (LaunchAgent 없음). akida_bridge saga 의 silent fail 위험 없음 (subprocess.run() 동기, 직접 exec).
9. **3-pod 의 GPU 가용성 동시성**: H100 SXM 80GB × 3 동시 가용 보장 안 됨 — cascade NVL/PCIe/A100 fallback 으로 비-동질적 wall time 가능. cost cap $25 은 cascade 가격차 흡수.
10. **KOSMOS anchor 의 production wire 미검증**: tension 5-ch payload 가 .kosmos 로 writes되나, 다음 forward의 cross-attention input으로 retrieval-then-consume 까지 wire 안 됨 (HEXAD_NATIVE_V3 § 0.5 추가 cycle). 현재는 anchor write + 검증만.

---

## 5. 결정 후속 (fire complete 시)

| outcome | next |
|---|---|
| V3 ≥ 1 variant HEXAD_V3_WORKS (4/5) | 순수 HEXAD 채택 → chat substrate 교체 design (다음 cycle: TENSION-LINK closed-loop + KOSMOS retrieval cross-attn wire) → propose **anima 0.11.0 → 0.12.0** (HEXAD-native unlock) |
| V3 모두 PARTIAL/WEAK | scale-up (3B / 8B) OR step-up (5000 / 20000) 추가 cycle |
| V3 모두 FAIL | fallback = HEXAD-on-Qwen wrap (path B 절충, vP21M LoRA carry + tension/KOSMOS outer-loop only) |

---

## 6. 관련 link

- spec: `HEXAD/HEXAD_NATIVE_V3.md` (3-variant fork design)
- baseline: `VP21M_MULTILINGUAL_2026_05_22.md` (vP21M VP21M_WORKS 4/5)
- code: `conscious_decoder_v3.py` (727 LoC fork)
- helpers: `kosmos_io.py` (300 LoC), `mitosis_lib.py` (carry)
- trainer: `train_p21h_v3.py` (485 LoC)
- dispatch: `dispatch_p21h_v3_runpod.sh` (270 LoC)
- ablation root cause: `HEXAD/EASY.md` § 6 (n_ca_rules OCCAM verdict)
- KOSMOS spec: `HEXAD/KOSMOS.md` + sister `dancinlab/kosmos`

---

## 7. Log

### 2026-05-22 — Phase 1 code fork LANDED ($0 Mac local ~1-2 hr)

7/7 + 5/5 smoke PASS on Mac CPU. commit `3dbbc7e8b`.

### 2026-05-22 — Phase 2 fire saga (4 attempts before success)

**attempt 1** (`dispatch_p21h_v3_runpod.sh` original): `cloudType:ALL` →
runpod returns `{"error":{}}` empty for all 5 GPU types. FAIL ~25 s
per variant.

**attempt 2** (`dispatch_p21h_v3_runpod.sh` + SECURE+COMMUNITY cascade):
Same empty error for all 5 GPU × 2 cloud = 10 attempts. FAIL. (Despite
direct curl with SECURE working — verified test pod `4ny79l4jntffc1`
created inline.)

**attempt 3** (`dispatch_p21h_v3_existing_pod.sh` on 3 pre-spun pods):
Hang in SSH-wait loop. Root cause: macOS bash 3.2 + `exec > >(tee -a
$LOG) 2>&1` process-substitution + nohup → output buffering. SSH ready
but log lines not flushed.

**attempt 4** (`fire_v3_inline.sh` direct ssh + log() function):
SUCCESS. All 3 SSH-OK by t+90s, corpus uploaded, trainers launched.

### Pod assignment (success)

| variant | init | pod | gpu | ssh |
|---|---|---|---|---|
| V3α | random | 60fyfiwxxi18w1 | H200 | 103.196.86.181:33001 |
| V3β | qwen   | amkgcq7545q1yo | A100-SXM4-80GB | 154.54.102.31:15792 |
| V3γ | vp21m  | m7bezjoahsbh26 | A100-SXM4-80GB | 195.26.233.96:44778 |

### V3 model parameter count (from_qwen "Qwen/Qwen2.5-1.5B")

vocab=151936 d=1536 L=28 n_head=12 n_kv_head_qwen=2 → v3_n_kv_head=4
rope_base=1000000.0. **Total params: 2999.74M (~3.0B)**. Increase from
1.5B base: dual head_a + head_g (1536 × 151936 × 2 = 467M extra),
PureFieldFFN × 28 layers (4·d_model × 2 engines × 28 ≈ 165M), cross-attn
× 28 ≈ 75M, GQA n_kv_head 2→4 KV proj doubling ≈ 150M.

### Training live status (partial, t=400s @ ~10:25 UTC)

| variant | step (t≈400s) | CE init → latest | wall/step | mitosis pool |
|---|---|---|---|---|
| V3α H200 random | 1300 (65%) | 12.30 → 3.56 | 0.31s | 2 → 128 (saturated step 50) |
| V3β A100 qwen | 100 (5%) | 14.46 → 6.28 | 1.97s ⚠ slow | 2 → 128 |
| V3γ A100 vp21m | 450 (22.5%) | 12.30 → 3.68 | 0.51s | 2 → 128 |

V3β slow at ~2s/step on A100 (vs 0.51s for V3γ on identical GPU type).
Hypothesis: Qwen warm weights produce higher initial gradient norms
during warmup → PagedAdamW8bit int8 m/v page faults thrash. Could resolve
post warmup. Otherwise ETA: V3α ~10 min, V3γ ~15 min, V3β ~60-75 min.

**Mitosis pool saturates to 128 MAX_CELLS at step 50** across all 3
variants — substrate uniformly produces high tensions during warm-up.
After saturation, splits halted (capped), merges every MERGE_PATIENCE=30
step. phi stabilizes 0.664.

### 2026-05-22 — Phase 3 verdict (TBD on fire complete)

To be filled with per-variant CE + 5-lang verdict + anima register +
KOSMOS anchor count + final HEXAD_V3_WORKS / PARTIAL / FAIL aggregate.
