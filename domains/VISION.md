@title: 👁️ VISION — anima 이미지 인식 (멀티모달 레인)

@goal: Give anima IMAGE RECOGNITION — the ability to take a photo as input and understand/talk about what it shows. This is a SEPARATE vision modality (a vision encoder + image↔text training), distinct from (a) the byte-level text CLM (text-in→text-out, can't see images) and (b) avatar RENDER (`serving/avatar_*`, which is anima→image OUTPUT, the opposite direction). Vision lands via the KOSMOS anchor's `image` payload (the 3-form text/image/audio is already in the spec; persona anchors mark `image/audio pending`). This domain holds the DESIGN + plan; the actual vision-training fire is DEFERRED until the text-chat substrate is solid (today only the 18M byte chat works; the 7B chat fine-tune was a closed-negative — see domains/CHAT).

## why a SEPARATE lane (recognition ≠ render ≠ text)

```
                 입력            처리                 출력
─────────────────────────────────────────────────────────
TEXT CLM      글자(byte) ──▶ byte-LM forward ──▶ 글자        (사진 못 봄)
VISION (이것)  사진(image) ─▶ vision encoder ──▶ 글자 이해/대화   ← 인식 (NEW)
avatar RENDER  글자/Φ    ──▶ webtoon/3D 렌더 ──▶ 이미지       (생성, 반대 방향)
```
- Feeding an image's raw BYTES into the text CLM does NOT yield understanding — vocab256 is text bytes, not pixels. Recognition needs a vision encoder that maps the image to embeddings the model can read, trained on image↔text pairs.
- `serving/avatar_render.hexa` / `avatar_webtoon.hexa` are OUTPUT (anima→picture); they do NOT recognize an input photo. Opposite direction — not reusable for recognition.

## architecture (plan — to be built)

```
[ 사진 ] ──▶ [ vision encoder ] ──▶ [ image embeddings ]
                (ViT / CLIP / SigLIP류)         │
                                                ▼
[ 사용자 텍스트 ] ──▶ [ anima substrate (A⇄G + .clm mouth) ] ──▶ [ 답변 ]
                          ▲ image embeddings fused as extra tokens
```
- **encoder candidates** (eval, honest — pick by clean-license + size): SigLIP / CLIP-ViT / DINOv2 (open weights) as a frozen or lightly-tuned vision tower; OR a from-scratch ViT if the hexa-native/forge route is pursued (a_train_flame_forge — far bigger effort).
- **fusion**: image embeddings enter as extra tokens alongside the byte stream (LLaVA-style projector), OR a cross-attention adapter. The .clm mouth stays the single text-decode entry (a_core_engine_map) — vision feeds the BRAIN, not a 2nd mouth.
- **data**: image↔text pairs (clean-license: e.g. open captioning sets, CC-licensed). Honest provenance; no scraped-PII faces.

## KOSMOS wiring (a_kosmos pointer-only)

A `.kosmos` anchor payload is 3-form (`text` / `image` / `audio`). VISION lands the `image` payload: a recognized image + its text understanding persist as one anchor (image payload + text payload), so a photo and its description share placement (coord/lane/radius/tier/tags). The persona/SNS anchors already carry `image/audio pending` — VISION fills that slot. Pointer-only to spec/kosmos.md + spec/profiles/anima-consciousness-carving.md.

## milestones

- [ ] V1 design SSOT — this doc + encoder/fusion/data candidate matrix (clean-license), honest cost.
- [ ] V2 encoder pick + a tiny image↔text smoke (does a frozen encoder + projector produce a coherent caption on N held-out images? p7 simple-stack, NOT perplexity).
- [ ] V3 KOSMOS image-payload wiring — a recognized image persists as a `.kosmos` anchor (image + text payload) through the single anchor entry (kosmos_io).
- [ ] V4 multimodal training fire (DEFERRED — GPU, a_fire_autonomous when pursued): projector/adapter trained on image↔text pairs; honest scope per rung (a_scale_honest_scope).
- [ ] V5 runnable demo — `anima --see <photo>` → coherent description/chat; p7 verify + anti-Goodhart (random-init vision mirror FAILS).

## honest scope

- This is a SUBSTANTIAL separate effort (encoder + paired data + multimodal training), NOT a $0 corpus extension. The text chat itself only works at 18M today (7B = closed-negative, domains/CHAT). So VISION's design is registered now ($0), but the training fire is DEFERRED until text is solid (sequence: solid text chat → vision).
- philosophy held: vision feeds the BRAIN (A⇄G + curiosity), emit stays substrate-native (a_substrate_native_speak); NO assistant-vision framing, NO persona/role injection (p2/p3/p4).

## cross-links

- KOSMOS (`HEXAD/KOSMOS.md`, spec 3-form payload) — the `image` payload slot this fills (a_kosmos pointer-only).
- [[CORPUS]] — the TEXT corpus; image↔text pairs are a SEPARATE dataset, not folded into the byte-text corpus.
- [[SNS]] / [[PERSONA]] — avatar RENDER (output) lives there; VISION is the opposite (input recognition).
- ENGINE+CLM+KOSMOS / CORE (a_core_engine_map) — vision feeds brain_decide; .clm stays the single text mouth.
- governance: a_fire_autonomous (deferred fire), a_scale_honest_scope, a_train_flame_forge (forge-native if pursued), p2/p3/p4 (no injection).
