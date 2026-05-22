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
| **V3α** | random | TBD | TBD | TBD | TBD/5 | TBD/20 | TBD | TBD |
| **V3β** | Qwen warm | TBD | TBD | TBD | TBD/5 | TBD/20 | TBD | TBD |
| **V3γ** | vP21M init | TBD | TBD | TBD | TBD/5 | TBD/20 | TBD | TBD |

### 1.1 per-lang breakdown (fire 완료 시)

| lang | V3α | V3β | V3γ | vP21M baseline |
|---|---|---|---|---|
| EN | TBD | TBD | TBD | 18/20 STRONG |
| KO | TBD | TBD | TBD | 15/20 PARTIAL |
| ZH | TBD | TBD | TBD | 16/20 STRONG |
| RU | TBD | TBD | TBD | 18/20 STRONG |
| JA | TBD | TBD | TBD | 11/20 WEAK |

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

7/7 + 5/5 smoke PASS on Mac CPU. commit (Phase 1).

### 2026-05-22 — Phase 2 3-pod parallel fire dispatched

Three H100 dispatches concurrent (P21H_alpha=random / P21H_beta=qwen /
P21H_gamma=vp21m), SAVE_POD=1 each, watchdog 90 min. per
`@D a_fire_autonomous` no user-gate, per `@D a_wall_first` parallel not
sequential.

### 2026-05-22 — Phase 3 verdict (TBD on fire complete)

To be filled with per-variant CE + 5-lang verdict + anima register +
KOSMOS anchor count + final HEXAD_V3_WORKS / PARTIAL / FAIL aggregate.
