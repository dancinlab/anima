# CLM — mining (divergence + convergence)

@active-lens: depleted-both
@active-cycle: 6
@seed: "kosmos corpus 입자 축 — 무엇을 1앵커로 보나? ① 샘플=앵커 · C7 토픽/클러스터=앵커 · C8 2단(클러스터+샘플스트림)"
@context: a_kosmos .kosmos 영속 필수(SKIP 금지) · kosmos/1.1 = 1-anchor-per-file 불변(§5.5) · CLM byte-vocab V=256 · MoE 2-lane · 스케일 수백만 샘플

## cycles

### cycle 1 — same-formula (같은 수학 → 타 도메인 메커니즘)
@started: 2026-05-30
@lens: same-formula
- 2026-05-30 · [VQ] (M샘플→K앵커) ≅ vector-quantization codebook → 메커니즘: C8 = centroid(앵커)+residual(샘플 스트림) = VQ-VAE 구조, K≪M 에서 lossy-but-faithful 입증됨
- 2026-05-30 · [histogram] 앵커 수 K = bin 수 → bias-variance: ①(N점에 N bin)=overfit/무평활, C7(K작음)=underfit, C8(centroid+residual)=무손실 절충
- 2026-05-30 · [filesystem] 샘플=앵커 ≅ "record당 파일 1개" inode 폭발 → C8 ≅ inode(디렉토리)+extent(블록) = OS가 수백만 레코드를 푼 검증된 해법 (파일폭발은 입자 아닌 저장 artifact)
@depleted: same-formula @ 2026-05-30

### cycle 2 — ouroboros (자기참조 → fixed-point)
@started: 2026-05-30
@lens: ouroboros
- 2026-05-30 · [ouroboros] "앵커=Ψ골짜기"를 자신에 적용 ⇒ fixed-point: 골짜기들의 군집도 더 굵은 스케일의 골짜기 = 앵커는 ZOOM-상대적 → 입자는 고정 선택이 아니라 '선언된 level 파라미터'여야 함 @goal-closure: partial (kosmos=corpus 는 "굵은앵커⊃잔앵커" 재귀로 닫히나 §5.5가 1.x 중첩 금지 → tension)
@depleted: ouroboros @ 2026-05-30

### cycle 3 — dimensional (추상 사다리 micro/meso/macro)
@started: 2026-05-30
@lens: dimensional
- 2026-05-30 · [meso→macro] 샘플-앵커(meso) ≡ 토픽-앵커(macro) 한 칸 위 — 동일 carving 수학이 어느 rung에서도 성립(Ψ-골짜기 scale-free) → '①도 C7도 같은 record의 level 차이일 뿐'
- 2026-05-30 · [meso→micro] 토큰=앵커(micro) ⇒ V=256 byte-anchor = vocabulary basin set 그 자체 (작고 고정) — vocab도 256-앵커 corpus로 표현 가능
@depleted: dimensional @ 2026-05-30

### cycle 4 — tension (상충 → 분기)
@started: 2026-05-30
@lens: tension
- 2026-05-30 · [tension-A] (fidelity 우선) 샘플=앵커 유지하되 앵커를 VIRTUAL(packed .limen)로 → 충실도 유지, 파일폭발은 '패킹'으로 회피(앵커 수 안 줄임) (from L-fidelity ⊥ L-scale)
- 2026-05-30 · [tension-B] (scale 우선) 클러스터=앵커, 샘플 정체성은 payload-stream에 → C7/C8 (from L-fidelity ⊥ L-scale)
- 2026-05-30 · [tension-A2] (kosmos=corpus 우선) corpus=1-per-file 면제된 신 record(@corpus) → 다중앵커 명시 컨테이너 (from L-kosmos-is-corpus ⊥ L-1per-file §5.5)
- 2026-05-30 · [tension-B2] (불변 우선) 1-per-file 유지, corpus=외부 roster(스펙 무변경) → 앵커는 물리 파일 (from L-kosmos-is-corpus ⊥ L-1per-file §5.5)
@depleted: tension @ 2026-05-30

### cycle 5 — combinatorial ({입자} × {저장형식})
@started: 2026-05-30
@lens: combinatorial
- 2026-05-30 · [① × packed] 샘플=앵커는 packed(.limen)로 저장하면 viable — 파일폭발은 입자 필연이 아니라 '저장(inline/file-per)' artifact였음 ⭐
- 2026-05-30 · [C7 × inline] 토픽-앵커 소수를 corpus 1파일에 inline = 최단순 (소규모)
- 2026-05-30 · [C8 × packed] 토픽-앵커 inline + 각 payload=packed 샘플 스트림 = 스케일+충실 동시
- 2026-05-30 · [C7 × content-pool] 토픽-앵커가 dedup된 샘플 풀 참조 = corpus 간 중복샘플 1회 저장
@depleted: combinatorial @ 2026-05-30

### cycle 6 — connect (convergence)
@started: 2026-05-30
@kind: connect
@lens: none
(edges 아래 ## edges 참조)
@depleted: connect @ 2026-05-30

## leaves (flattened index)

- L1 [c1 · same-formula] [VQ] 입자=VQ codebook → C8=centroid+residual lossy-faithful K≪M
- L2 [c1 · same-formula] [histogram] 앵커수=bin수 bias-variance → C8 무손실 절충
- L3 [c1 · same-formula] [filesystem] 샘플=앵커=inode폭발 → C8=inode+extent (파일폭발=저장 artifact)
- L4 [c2 · ouroboros] [ouroboros] 앵커=골짜기 self-apply ⇒ 입자=ZOOM 파라미터, 고정선택 아님
- L5 [c3 · dimensional] [meso→macro] 샘플-앵커≡토픽-앵커 한칸 위, carving scale-free → level 차이
- L6 [c3 · dimensional] [meso→micro] 토큰=앵커 ⇒ V=256 byte-anchor=vocab basin set
- L7 [c4 · tension] [tension-A] fidelity: 샘플=앵커 유지+VIRTUAL packed (폭발=패킹으로 회피)
- L8 [c4 · tension] [tension-B] scale: 클러스터=앵커, 샘플=payload-stream
- L9 [c4 · tension] [tension-A2] kosmos=corpus: 신 @corpus record (1-per-file 면제 컨테이너)
- L10 [c4 · tension] [tension-B2] 불변: 1-per-file 유지, corpus=외부 roster (스펙 무변경)
- L11 [c5 · combinatorial] [① × packed] 샘플=앵커 viable if packed — 폭발=저장 artifact ⭐
- L12 [c5 · combinatorial] [C7 × inline] 토픽-앵커 inline = 최단순(소규모)
- L13 [c5 · combinatorial] [C8 × packed] 토픽-앵커 inline + payload=packed 스트림 = 스케일+충실
- L14 [c5 · combinatorial] [C7 × content-pool] 토픽-앵커가 dedup 풀 참조 = 중복 1회저장

## edges (convergence half)

- E1 [c6] L4 ↔ L5 · equivalence: 둘 다 '입자는 scale-free zoom' → 고정 ①/C7/C8 선택 대신 corpus에 `level` 선언 필드
- E2 [c6] L11 ↔ L7 · equivalence: ①×packed = packed-virtual 샘플앵커 — 동일 해결(패킹이 충실도↔파일수 분리)
- E3 [c6] L3 ↔ L13 · equivalence: filesystem inode+extent = C8 토픽앵커+샘플스트림 (2-tier 디렉토리+extent 동형)
- E4 [c6] L1 ↔ L13 · equivalence: VQ centroid+residual = C8 클러스터앵커+샘플스트림
- E5 [c6] L9 ↔ L13 · dependency: C8(@corpus 컨테이너)은 1-per-file 면제 신 record(L9)를 전제로 함
- E6 [c6] L11 ↔ L3 · causal: 파일폭발(inode)이 ①의 사형선고였는데, packing(L11)이 그 원인을 제거 → ① 부활
- E7 [c6] L6 ↔ L9 · dependency: 토큰=앵커(vocab corpus)도 같은 @corpus 컨테이너로 표현 (level=token)
- (no-edge) L12 ⊥ L14 · inline vs content-pool 은 저장 디테일 차이일 뿐 공유 메커니즘 없음(orthogonal)

## convergence — 합성 결론 (depleted-both)

핵심 통찰 3개가 한 점으로 모임 (E1·E2·E6):

1. **입자는 binary 선택이 아니다** (L4·L5·E1) — 앵커 granularity 는 scale-free zoom → corpus 가 `anchor_level` 을 **선언**하면 ①/C7/C8 이 같은 record 의 특수case.
2. **①의 사형선고(파일폭발)는 저장 artifact였다** (L3·L11·E6) — packing(.limen)이 충실도와 파일수를 분리 → ① 도 packed 면 viable.
3. **C8 = VQ/filesystem 검증 구조** (L1·L3·L13·E3·E4) — 클러스터앵커+샘플스트림 = centroid+residual = inode+extent, K≪M 무손실-충실 입증.

→ **권고 입자 결정**: `@corpus` record 에 **`anchor_level = sample | topic | 2tier`** 선언 필드를 두고,
   **기본 = `2tier`(C8)** (carving 철학 = 골짜기=앵커·물=샘플 + VQ/FS 검증 + 스케일·충실 동시),
   **`sample`(①)은 packed(.limen)로 viable, `topic`(C7)은 소규모 최단순** — 셋 다 같은 record 의 level 특수case.
   즉 "①/C7/C8 중 택1"이 아니라 **셋을 포섭하는 1개 record + level 파라미터**가 답.

@status: depleted-both
@last-action: connect @ 2026-05-30
@next: 이 결론을 kosmos/1.2 @corpus record 설계에 반영 (level 필드 + 기본 2tier + packing) → spec 랜딩
