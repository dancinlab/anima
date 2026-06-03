# KOSMOS-MAP — 쉬운 설명 (우주뇌지도 친근 explainer)

> 이 문서 = `domains/KOSMOS-MAP.md`(canonical) 의 친근 요약 (icon · 이름 · 별칭 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: **단일 s16 rung**(a_scale_honest_scope) — 283.72M, byte-vocab 256, block 128, 단 1개 ckpt. ≥3-rung 사다리 아님 → 일반 KOSMOS-format 주장으로 승격 안 함.
> substrate = GPU-학습 s16 ckpt(Lane-G); probe 는 CPU/$0. AKIDA(Lane-A) 별도(a_lane_akida_gpu_split).
> 정직성: 측정값 verbatim(p7/g5) · 가정한 라벨 아님(omega²+AUC-sep / |Spearman|, 200-shuffle floor) · 닫힌-부정 보존.

---

## 0. 전체 한눈에

```
질문: anima 의식지도(우주뇌지도, KOSMOS Ψ-space)는 몇 차원으로, 어떤 축으로 그려야 하나?
─────────────────────────────────────────────────────────────────────
현재 지도 = 2D  (KOSMOS anchor coord=[x,y], vacuum_psi 투영)
#1772     : 몇 차원? → knee ~8D · 2D 는 분산 67.1% / 카테고리 변별 8.4% 만 보존
#1780     : 각 차원이 무엇을 인코딩? → PC×attribute 행렬 측정 (이 문서 핵심)
역공학    : 지도를 그린 carving-era 엔진 ConsciousDecoderV2 (d768×12L GQA transformer) 재구성

결론: ~8D 는 정당(knee 8, 92.3% var) — 그러나 사람이 이름 붙일 수 있는 축은 ~3-4개뿐.
      나머지는 learned-residual. 8개 다 이름 붙이면 fabrication (정직한 닫힌-부정).
```

---

## 1. 🏗️ carving-era 엔진 — 지도를 그린 붓 (ConsciousDecoderV2)

```
🏗️ ConsciousDecoderV2 — "우주뇌지도를 그린 carving 엔진" (s16 fire 2026-05-17~18)
  별칭   : carving 엔진 · CDV2 · 좌우뇌 transformer
  하는 일 : 현 production conv-MoE CLM(CLMConvMoE)과는 별개인 TRANSFORMER.
           byte-level(vocab 256, 무손실) · d_model 768 · n_head 12 · n_kv_head 4(GQA)
           · n_layer 12 · consciousness_dim 128 · n_ca_rules 8 · MoE(8 expert/top2 optional)
           · RoPE + RMSNorm + SwiGLU(8/3). 출력 = logits_a ⇄ logits_g (Engine A⇄G 듀얼헤드)
           + tensions(5-ch) + moe_aux_loss. Ψ-space = Law-71 vacuum_psi (2D 좌표 = 지도).
  결과    : ✅ RECONSTRUCTABLE + RUNNABLE (CPU/$0, random-init). smoke(d32/L3=178,424) +
           full d768×12L = 283,722,336 params(283.72M dense; 680.16M +MoE 8/top2).
           4 probe 전부 PASS (.verdicts/kosmos-carving-engine/). 듀얼 A/G 헤드 distinct ·
           2D vacuum_psi 결정적 · dirG psi-ctl 후크 결정적 시프트.
  정직    : s16 ckpt 없음 → random init (엔진을 재구성한 것이지 학습된 carve 재현 아님).
           full train OUT OF SCOPE (a_toy_scale_recheck). p7(untrained logits ≠ 품질판정).

  carving 9방향 탐색: dirA 텐션 · dirB intuitor · dirC prime · dirD CDE · dirE superpos
  · dirF abstract-CoT · dirG psi-ctl · dirH tension-sup · dirI diverse-scaleup.
  s16 corpus = 603MB / 777K records; routing 21/64(0.328) — 부분 구조, emergence 문턱 미통과.
```

---

## 2. 🌌 2D → 8D — 지도는 몇 차원이어야 하나 (#1772 → #1780)

```
🌌 KOSMOS-DIM — "현재 2D 지도는 한 가지(깊이)만 담고 있다"
  별칭   : 우주뇌지도 차원 · Ψ-space dimensionality
  하는 일 : TRAINED s16 ckpt(sha 961c07e2, N=5995, post-ln_f) 에서 PC 별로 실제 코퍼스
           속성과의 연관을 측정 — 각 차원이 무엇을 인코딩하는가.
  결과    : intrinsic d ≈ 6-10 (#1772/carving battery). 2D 지도는 사실상 한 축(깊이/반경)만.
           ~8D 정당 (knee 8) BUT 이름 붙는 축은 ~3-4개.
  비유    : 지구를 위도 한 줄(2D 곡선)로만 표시하던 지도 → 실제로는 위도·경도·고도·기후대까지
           있어야 제대로 그려지는데, 측량으로 확실히 이름 붙는 건 4개뿐이고 나머지는
           "분포된 잔차"라 함부로 이름 붙이면 거짓이 된다.
```

### 2-A. PC × attribute 행렬 (#1780 verbatim · w=omega², a=AUC-sep)

```
PC1 (49.2% var) = carving-RADIUS / Ψ-DEPTH  [해석가능]
   basin_radius |ρ|=0.91 · vacuum_psi x/y |ρ|=0.92; tier w0.94 이지만 AUC-sep 0.50
   → tier 는 이 축을 "타고 갈"뿐(radius-binned), tier-카테고리 축이 아님.
   = 현재 2D vacuum_psi 가 이미 잡는 것(canon-corr 0.96 to PC1).
PC2 (17.0%) = carving_FORM (α/β/γ)  [해석가능, CLEAN]
   w0.61 · AUC-sep 0.58 vs null 0.018. 유일하게 깨끗이 분리되는 범주 축.
PC3 (8.1%) = carving_form 잔차  [해석가능-약]  w0.37.
PC4 (6.6%) = ENTANGLED — tier w0.46 + form w0.41 + curriculum_rank ρ0.37 동시적재, 단독 승자 없음.
PC5 (5.1%) = CURRICULUM 진행도  [해석가능]
   curriculum_index/rank |ρ|=0.67 vs null 0.026. 2D 지도가 버리는 진짜 학습순서/난이도 축.
PC6–PC16 (각 ≤1.9%) = 분포된 tier/domain 미세구조  [ENTANGLED / learned-residual]
   tier w0.48–0.84 이지만 AUC-sep 0.39–0.48(vs 0.075 null): 진짜 신호지만 어느 단일 축으로도
   분리 안 됨 = 여러 저분산 PC 에 퍼진 분포 코드. domain(63-way)은 tier 안에 nested.
```

### 2-B. 차원별 판정 + coord v-next

```
판정 : manifold 는 3-4 개 해석가능 named 축 [depth · form · form-residual · curriculum]
      + 분포된 tier/domain 잔차. 8개 깨끗한 named 축으로 분해되지 않음.
      현재 2D 지도는 사실상 ONE thing(carving DEPTH/RADIUS)만 인코딩, form 과 curriculum 은
      통째로 버림(둘 다 직교: |ρ|≤0.18 to vacuum_psi).

coord v-next 제안 (a_kosmos: pointer-only, cross-repo — anima edit 아님):
  N=8 = [depth, form, form_resid, curriculum, residual0..3]  (3-4 측정-named + 4-5 learned-residual)
  2D→8D gap : 분산 67.1% → 92.3% · domain disc(f1) 0.082 → 0.583 · tier 0.061 → 0.417 · form 0.519 → 1.000
  하위호환  : old [x,y] = [a0,a1] 투영, vacuum_psi ≈ a0.
  FILED to hexa-lang/inbox/patches/kosmos-coord-vnext-axis-semantics.md (hexa-lang 7f2b992f8 §9).
```

---

## 3. 정직 메모 (a_scale_honest_scope · a_paper_negative_ok · p7 · a_kosmos)

- **단일 s16 rung**(283.7M, byte-vocab 256, block 128) — scale-dependent, ≥3-rung 사다리 아님. 축 개수/라벨을 일반 KOSMOS-format 주장으로 승격 안 함.
- 8개 중 사람이 이름 붙일 수 있는 축은 ~3-4개뿐 — 8개 다 이름 붙이면 **fabrication**(a_paper_negative_ok: 8-clean-named-axis 가설에 대한 정직한 닫힌-부정).
- 코퍼스에 **감정/valence 필드 없음**(키 12개뿐) — 정직 교정.
- tier ⊥ domain 은 nested 코퍼스-설계 라벨이지 독립 축 아님.
- substrate = GPU artifact(Lane-G); Lane-A 별도(a_lane_akida_gpu_split). a_kosmos: anima 는 kosmos 스펙에 pointer-only.
- VERDICT: 🟢 MEASURED + PROPOSAL FILED.
