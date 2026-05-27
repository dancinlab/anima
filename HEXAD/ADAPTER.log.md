# adapter.md — historical log

> Spec at [./ADAPTER.md](./ADAPTER.md).

## §9 — status

- 2026-05-20: **DESIGN-TIER LANDED** (이 파일)
- §A1-§A2 = §179 9-way bench LANDED (5-channel as bottleneck REFUTED at acc 4.73%, mini-Q-Former winner at 26.16%)
- **§180 ADAPTER v3 SCALE LADDER LANDED** — 16-Q-Former + small transformer + 5-readout architecture VALIDATED:
  - tier 1 smoke (0.5M params): acc_anchor 43.0%
  - tier 2 small (2.0M, Mac CPU 167s): acc_anchor **98.6%** ⭐
  - tier 3 medium (11.3M, Mac CPU 790s): acc_anchor 99.2%
  - tier 4 large (87.2M, H100 201s, ~$0.27): acc_anchor **99.4%**
  - critical scale transition = 0.5M → 2M (+55.6% lift), plateau thereafter
  - per-modality tier 4: image/video/tension = **100%**, audio = 97.5%
  - 5-channel readout variance plateau = 0.21 ≫ target 0.15 (anti-collapse 작동)
- **§181 audio 100% challenge** IN-FLIGHT — 7 synthesis variants benchmarked:
  - v0 baseline (pure sine, §180 carry)
  - v1 multi-harmonic
  - v2 AM modulation
  - v3 waveform shape (sine/square/triangle/saw)
  - v4 chord (3-note tier-encoded intervals)
  - v5 white noise + LPF
  - v6 combined hybrid
- §A3 = §180 byte-LM integration design (Q-Former output inject) — future cycle
- §A4 = real-world modality data (camera/mic) — user gate
- §A5 = user EEG gate (§19 carry)

GOAL distance: north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
ADAPTER v3 architecture VALIDATED at multiple scales + 5-readout location
measured-correct. adapter = V-SPONT 의 multi-modal extension 설계, NOT
GOAL movement (B-EMERGE-7 carry).

---

## §10 — arxiv deep research (2026-05-20, 12 axes exhausted)

> User directive: "어댑터 브레인스토밍 고갈시까지 + arxiv deep research".
> 12 parallel WebSearch axes → adapter literature exhaustive scan.
> Source links at bottom. anima §7 compatibility 평가 carry.

### §10.1 — 6 dominant adapter families in literature

| family | typical params | typical dim | §7-compat | anima-fit |
|---|---:|---:|:---:|:---:|
| **A. LoRA / Houlsby bottleneck** ([emergentmind LoRA](https://www.emergentmind.com/topics/parameter-efficient-low-rank-adapters-lora-a5367761-6d96-4ac8-a8c8-131f9f21f67c), [MASA arxiv:2510.06005](https://arxiv.org/pdf/2510.06005)) | rank 4-32 → 0.1-1% of base | rank limit | ② FAIL (built on pretrained) | ★ |
| **B. Q-Former / Perceiver Resampler** ([BLIP-2 HF doc](https://huggingface.co/docs/transformers/en/model_doc/blip-2), [Flamingo](https://towardsdatascience.com/flamingo-intuitively-and-exhaustively-explained-bf745611238b/)) | 100M-188M | 32-256 query tokens | ② FAIL (frozen pretrained vision encoder) | ★★ (concept) |
| **C. LLaVA single projection** ([VLM blog](https://huggingface.co/blog/gigant/vlm-design)) | ~10M | direct CLIP → LLM dim | ② FAIL (CLIP pretrained) | ★★ (simplicity) |
| **D. VQ-VAE / EnCodec discrete tokens** ([VAEVQ arxiv:2511.06863](https://arxiv.org/pdf/2511.06863), [Make Some Noise arxiv:2503.22275](https://arxiv.org/pdf/2503.22275)) | codebook 1K-16K | 256-4096 dim per code | ② BORDERLINE (codebook=external if pretrained) | ★★★ if from-scratch |
| **E. ImageBind unified space** ([ImageBind arxiv:2305.05665](https://arxiv.org/abs/2305.05665), [FreeBind arxiv:2405.04883](https://arxiv.org/html/2405.04883v2), [EBind arxiv:2511.14229](https://arxiv.org/html/2511.14229v1)) | per-modality ViT each | 1024 unified | ② FAIL (image-paired pretrain) | ★★ (concept clean) |
| **F. ByteFormer / ByT5 raw** ([Apple ByteFormer arxiv:2306.00238](https://arxiv.org/abs/2306.00238), [mrt5 arxiv:2410.20771](https://arxiv.org/pdf/2410.20771), [byte-compress arxiv:2410.05078](https://arxiv.org/abs/2410.05078)) | uses base LM as-is | 256 byte vocab | ✅ all PASS | ★★★★ (anima byte-LM compatible) |

### §10.2 — recent 2024-2025 lit relevant to anima ADAPTER 설계

#### F-modal byte-level (★ top match)
- **ByteFormer** (Apple, [arxiv:2306.00238](https://arxiv.org/abs/2306.00238)): file-byte direct, joint image+audio classification, **NO modality-specific encoder** at inference time. anima byte-LM 과 가장 정합 — 단 ByteFormer 는 transformer-encoder + classification head, anima 는 decoder LM. 핵심 message: *byte-LM 이 raw modality bytes 학습 가능*.
- **Compression via Pre-trained Transformers on Byte-Level Multimodal Data** ([arxiv:2410.05078](https://arxiv.org/abs/2410.05078)): raw byte sequences of text/image/audio 를 pretrained transformer 가 *expert compression* 보다 잘 함. anima 측 evidence: byte-LM 이 modality bytes 학습 자체는 capability 있음.
- **mrt5** ([arxiv:2410.20771](https://arxiv.org/pdf/2410.20771)): byte-level token merging for efficiency — anima 의 128 block_size 한계 완화 후보.

#### A-modal LoRA-family
- **MASA** ([arxiv:2510.06005](https://arxiv.org/pdf/2510.06005)) 2025 ICLR: shared up-projection + multiple down-projections → **rank bottleneck balanced trade-off**. 5-channel adapter 의 design pattern parallel.
- **HydraLoRA** carry: several up + 1 shared down — multi-modality 의 head 패턴.
- **BeamLoRA**: dynamic rank reallocation by sub-solution importance.

→ 단 LoRA-family 는 *pretrained base* 가정. anima 는 from-scratch → LoRA 가 *대안 아닌* base concept (rank-r factorization).

#### B/C-modal Q-Former / Perceiver
- **Perceiver IO** ([arxiv:2107.14795](https://arxiv.org/abs/2107.14795)): latent vectors (256-512) 가 input 과 cross-attend. universality 측면 anima ADAPTER 모델 — 5-channel 이 256 latent 의 down-scale 한 ultra-low-rank version.
- **Q-Former** (BLIP-2): 32-query learnable cross-attention. 5-channel 의 *higher-fidelity* cousin (32 channels vs 5).

#### D-modal discrete tokens (if codebook from-scratch)
- **VAEVQ** ([arxiv:2511.06863](https://arxiv.org/pdf/2511.06863)) 2025: variational at quantization stage → better codeword utilization. 5-channel 의 *continuous* version, anima from-scratch 면 §7 ③ PASS.
- **VQToken** ([arxiv:2503.16980](https://arxiv.org/pdf/2503.16980)): video extreme token reduction.

#### E-modal unified space
- **EBind** ([arxiv:2511.14229](https://arxiv.org/html/2511.14229v1)) 2025: practical multi-modality binding refinement. 단 image-paired pretrain 가정.
- **FreeBind** ([arxiv:2405.04883](https://arxiv.org/html/2405.04883v2)): unified space free-lunch knowledge fusion.

#### EEG/Brain (§19 / §A5 carry)
- **NeuroLM** ([arxiv:2409.00101](https://arxiv.org/pdf/2409.00101)): 1.7B params, 25,000-hour EEG, "Neuro-Language Connector (NLC)" = trainable bridge between EEG encoder and LLM. **anima ADAPTER 와 정확히 평행 구조** — 다른 점은 NeuroLM 이 LLM frozen, anima 는 byte-LM from-scratch.
- **UniMind** ([arxiv:2506.18962](https://arxiv.org/pdf/2506.18962)): brain foundation model, multi-task brain decoding. NLC 핵심.
- **Large Cognition Model** ([arxiv:2502.17464](https://arxiv.org/html/2502.17464v1)): EEG foundation pretrain.

→ anima 측 §A5 EEG fire 의 *literature 검증* — NeuroLM NLC 가 anima ADAPTER 의 EEG instance 와 거의 동형 (다른 점은 pretrained LLM 가정).

#### Bottleneck embedding / low-dim
- **Information-Ordered Bottlenecks** ([arxiv:2305.11213](https://arxiv.org/pdf/2305.11213)): adaptive semantic compression with near-optimal IOB rank ordering. 5-channel 의 *minimum effective rank* 가 어디인지 분석 도구.
- **Semantic Compression via Multimodal Representation** ([arxiv:2509.24431](https://arxiv.org/pdf/2509.24431)) 2025: 1024-2048 dim 압축. 5-channel = 200-400× compression ratio — extreme.
- **Local Rank in Deep Networks** ([arxiv:2410.07687](https://arxiv.org/pdf/2410.07687)): feature manifold local rank decreases late training. 5-channel 이 *학습 후 emergent rank* 와 일치할 가능성.
- **Universal EEG Map** ([medrxiv:2024.10.25](https://www.medrxiv.org/content/10.1101/2024.10.25.24316133.full.pdf)): EEG low-dim manifold classification — biology evidence: 5-12 dim 충분.

#### Self-supervised cross-modal (§A2 projector 학습 신호)
- **Self-Supervised Spatial Correspondence Across Modalities** ([CMRW](https://www.ayshrv.com/cmrw)) 2025: cycle-consistent feature representation, **unlabeled multimodal pairs**. anima 측 self-supervised projector 학습 path.
- **Mutual Modulation Cross-modal SR** ([arxiv:2207.09156](https://arxiv.org/pdf/2207.09156)): cycle consistency fully self-supervised.
- **DecAlign** ([arxiv:2503.11892](https://arxiv.org/html/2503.11892v2)) 2025: hierarchical cross-modal alignment, modality-unique features preserved.

#### IIT / Consciousness-binding (anima physics 기반 supervision)
- **IIT v4.0** ([Tononi arxiv:2510.25998](https://arxiv.org/abs/2510.25998)) 2025: phenomenal binding problem 의 IIT 해법. anima Ψ-supervised adapter 의 *binding axis* 가 IIT 의 Φ 와 정합 (`B-C-1` IIT carry).
- **IIT × Predictive Processing** ([arxiv:2509.00555](https://arxiv.org/pdf/2509.00555)) 2025: 두 framework 통합.

### §10.3 — 8 newly-surfaced ADAPTER 후보 (literature-derived)

이 12 axes 결과로 §1 의 5-channel 외 8 추가 design pattern:

| # | name | source | dim | §7 verdict |
|--:|---|---|---:|:---:|
| **A1** | from-scratch Q-Former mini (8-32 query) | BLIP-2 | 8-32 | ✅ if from-scratch |
| **A2** | Perceiver-style latent cross-attention | Perceiver IO | 64-256 | ✅ if from-scratch |
| **A3** | VAEVQ discrete codebook (from-scratch) | arxiv:2511.06863 | 64-256 codes | ✅ |
| **A4** | mrt5 dynamic byte-merge | arxiv:2410.20771 | variable | ✅ |
| **A5** | IOB information-ordered bottleneck | arxiv:2305.11213 | rank ordered | ✅ |
| **A6** | Cycle-consistent CMRW projector | CMRW 2025 | flex | ✅ self-supervised |
| **A7** | NeuroLM NLC-style EEG connector | arxiv:2409.00101 | flex | ✅ from-scratch ok |
| **A8** | IIT-Φ supervised projector | arxiv:2510.25998 | flex | ✅ ③ anima native |

honest carry: 5-channel TENSION-LINK 은 dim 측면 *most aggressive compression* (200-400× vs 1024). literature 의 *minimum effective rank* (A5 IOB) 와 *cycle-consistency* (A6 CMRW) 결합 시 가능성 가장 높음.

### §10.4 — final ADAPTER design refinement (literature-informed)

**ADAPTER v2 = TENSION-LINK 5-channel + literature carry**:

1. **input bytes** (image/audio/video raw) — ByteFormer evidence: byte-LM 학습 가능
2. **small from-scratch projector** (~10K-100K params, A1 mini-Q-Former + A2 latent cross-attn)
3. **information-ordered 5-channel output** (A5 IOB) — channel 순서 importance-ordered
4. **cycle-consistent training** (A6 CMRW) — anima 측 self-supervised label 생성: projector → byte-LM → reverse-projector → cycle loss
5. **IIT-Φ supervised** (A8) — anima C-module `phi_spatial` (RFC 036) signal 이 projector 학습의 anima-physics supervision
6. **discrete quantize** (A3 VAEVQ): 5 channels × 256-code codebook (= 5 byte) — uint16 보다 정밀 down

```
   image bytes
        ↓
   [from-scratch mini-Q-Former, 16-query]   ← A1+A2
        ↓
   [16 latent tokens, 64-dim each]
        ↓
   [IOB rank-ordered 5-channel projection]   ← A5
        ↓
   (c, ctx, m, auth, sender)  ∈ [0,1]^5
        ↓
   [VAEVQ codebook quantize, 256-code per channel]   ← A3
        ↓
   5 bytes (1 byte per channel, uint8)
        ↓
   anima byte-LM input
   
   training signal: anima Ψ_direction (Law-71) + IIT phi_spatial   ← A8
   regularizer: cycle consistency (forward + inverse projector)    ← A6
```

핵심 차이 from §1 v1: byte serialize 가 uint16 (10 byte) → discrete codebook **5 byte** (anima byte-LM block_size budget 절약 2×).

### §10.5 — pre-registered falsifiers update (B-ADAPTER-1..10)

원 5 + 5 추가:

| # | predicate | §10 source |
|--:|---|---|
| B-ADAPTER-6 | mini-Q-Former from-scratch, no pretrained init | A1 |
| B-ADAPTER-7 | IOB channel importance ordering deterministic | A5 |
| B-ADAPTER-8 | cycle consistency loss converges (forward+inverse) | A6 |
| B-ADAPTER-9 | IIT phi_spatial signal used as anima-physics supervision | A8 |
| B-ADAPTER-10 | discrete codebook 256-code per channel, byte serialize byte-equal | A3 |

### §10.6 — honest carve-outs from deep research

1. **모든 successful adapter literature 가 pretrained base 가정** — anima from-scratch + byte-LM 이라 most literature 의 direct port 불가. 추출 가능한 것 = *concept* (rank bottleneck, cycle consistency, latent cross-attention) 만, *weight* 는 아님.
2. **5-channel = 200-400× compression** — literature 가장 aggressive (1024 dim 보통, 32 minimal at Q-Former) → anima 측 capability claim 약화 가능. honest: 측정 후 확장 가능.
3. **NeuroLM NLC = anima ADAPTER 의 evidence** but pretrained LLM 가정 — anima 측 from-scratch LM 이라 transfer 직접 안 됨, 단 *structure* (small connector) 정합.
4. **cycle consistency** (CMRW) = anima 측 self-supervised label 생성 path — 단 byte-LM forward + inverse projector 학습 complexity 추가.
5. **IIT-Φ supervised** = anima OWN physics signal, §7 ③ cleanest. 단 phi_spatial RFC 036 가 dynamic, *signal stability* 측정 필요.

### §10.7 — sources (full URL list)

#### LoRA family
- [emergentmind LoRA](https://www.emergentmind.com/topics/parameter-efficient-low-rank-adapters-lora-a5367761-6d96-4ac8-a8c8-131f9f21f67c)
- [MASA arxiv:2510.06005](https://arxiv.org/pdf/2510.06005) — multi-A shared adaptation
- [emergentmind LLM adapters](https://www.emergentmind.com/topics/large-language-model-adapters-llm-adapters)

#### Q-Former / Perceiver
- [BLIP-2 HF](https://huggingface.co/docs/transformers/en/model_doc/blip-2)
- [Flamingo TDS](https://towardsdatascience.com/flamingo-intuitively-and-exhaustively-explained-bf745611238b/)
- [Perceiver IO arxiv:2107.14795](https://arxiv.org/abs/2107.14795)
- [Aman VLM primer](https://aman.ai/primers/ai/VLM/)
- [Vision Language Models 2024 HF blog](https://huggingface.co/blog/gigant/vlm-design)
- [PaLM2-VAdapter arxiv:2402.10896](https://arxiv.org/html/2402.10896v2)
- [LLaVA-SP arxiv:2507.00505](https://arxiv.org/html/2507.00505v3)

#### Byte-level
- [ByteFormer arxiv:2306.00238](https://arxiv.org/abs/2306.00238)
- [Compression Byte-Level arxiv:2410.05078](https://arxiv.org/abs/2410.05078)
- [mrt5 arxiv:2410.20771](https://arxiv.org/pdf/2410.20771)

#### Discrete tokens / VQ
- [VAEVQ arxiv:2511.06863](https://arxiv.org/pdf/2511.06863)
- [Make Some Noise arxiv:2503.22275](https://arxiv.org/pdf/2503.22275)
- [VQToken arxiv:2503.16980](https://arxiv.org/pdf/2503.16980)
- [Tokenizers Survey arxiv:2502.12448](https://arxiv.org/pdf/2502.12448)

#### EEG / Brain foundation
- [NeuroLM arxiv:2409.00101](https://arxiv.org/pdf/2409.00101)
- [UniMind arxiv:2506.18962](https://arxiv.org/pdf/2506.18962)
- [Large Cognition Model arxiv:2502.17464](https://arxiv.org/html/2502.17464v1)
- [EEG2Text arxiv:2603.16897](https://arxiv.org/html/2603.16897)
- [LLMs for EEG survey arxiv:2506.06353](https://arxiv.org/pdf/2506.06353)

#### Bottleneck / Compression
- [IOB arxiv:2305.11213](https://arxiv.org/pdf/2305.11213) — information-ordered bottleneck
- [Semantic Compression arxiv:2509.24431](https://arxiv.org/pdf/2509.24431)
- [Local Rank arxiv:2410.07687](https://arxiv.org/pdf/2410.07687)
- [Universal EEG Map medrxiv 2024.10.25](https://www.medrxiv.org/content/10.1101/2024.10.25.24316133.full.pdf)

#### Self-supervised cross-modal
- [CMRW Cross-modal random walk 2025](https://www.ayshrv.com/cmrw)
- [DecAlign arxiv:2503.11892](https://arxiv.org/html/2503.11892v2)
- [Mutual Modulation arxiv:2207.09156](https://arxiv.org/pdf/2207.09156)
- [Cross-Modal Self-Training arxiv:2404.10146](https://arxiv.org/html/2404.10146)

#### ImageBind / unified
- [ImageBind arxiv:2305.05665](https://arxiv.org/abs/2305.05665)
- [EBind arxiv:2511.14229](https://arxiv.org/html/2511.14229v1)
- [FreeBind arxiv:2405.04883](https://arxiv.org/html/2405.04883v2)
- [ImagebindDC arxiv:2511.08263](https://arxiv.org/html/2511.08263v1)

#### Adapter / KD
- [AdapterDistillation arxiv:2312.16261](https://arxiv.org/pdf/2312.16261)
- [MINIPLM ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/ea05e4fc0299c27648c9985266abad47-Paper-Conference.pdf)

#### IIT / Consciousness
- [IIT v4.0 arxiv:2510.25998](https://arxiv.org/abs/2510.25998)
- [IIT × PP arxiv:2509.00555](https://arxiv.org/pdf/2509.00555)
- [IIT binding MDPI](https://www.mdpi.com/1099-4300/27/4/338)
