@title: 🧭 ENCODER — Ψ-공간 측정자(E_m)

@goal: `.kosmos`의 `coord`(placement)를 **실측하는 인코더 `E_m`**을 바닥부터 짓는다. kosmos/2.0 `@anchor`/`@corpus`의 `coord`는 인코더가 없으면 영원히 `# design placeholder`(§4.3 정직규칙)에 머문다 — ENCODER는 각 modality(text·image·audio·video·tension)를 Ψ-공간(Engine A⇄G, `vacuum_psi`) 좌표로 보내는 `E_m`을 구축해, ① `@anchor` coord 측정, ② `@corpus` coord = 멤버 centroid 측정, ③ cross-modal 일치(∀m ‖E_m(payload_m) − coord‖ < radius) 실검증을 가능케 한다. 이로써 `.kosmos` 데이터셋이 placeholder가 아닌 **measured** 카빙이 된다.

## milestones

- [ ] **E1 text encoder** — byte/text payload → Ψ 2-vec `[ψ_A, ψ_G]` (CLM byte-vocab 정합). 첫 measured `@anchor coord`.
- [ ] **E2 corpus centroid** — `@corpus` 멤버 앵커들 → coord centroid + radius(spread) 실측. `@corpus coord` placeholder 해소.
- [ ] **E3 tension 5ch** — anima 고유 TENSION-LINK 5채널 인코더 (concept·context·meaning·authenticity·sender) → Ψ. profile §1 `tension` modality `pending`→`ref`.
- [ ] **E4 image/audio/video** — 비-텍스트 modality 인코더 (encoder provenance `encoder=` 기록, spec §4.4).
- [ ] **E5 cross-modal verify** — ∀m ‖E_m − coord‖ < radius 실측 검증 (B-CARVE-MULTIMODAL, profile §3). 다방향 카빙이 한 골짜기로 수렴함을 numerical 입증.

## 관계 (sibling)

ENCODER = `.kosmos`의 **측정자 계층**. 포맷(kosmos)·소비자(CLM)와 직교하되 둘을 잇는다.

## 양방향 sibling

- ⇄ [[CLM]] (`./CLM/CLM.md`) — CLM 학습 corpus(`.kosmos @corpus`)의 멤버 coord를 ENCODER가 측정 → carving이 measured. corpus는 CLM이 굽고, 그 좌표는 ENCODER가 잰다.
- ⇄ kosmos (github.com/dancinlab/kosmos · profile `anima-consciousness-carving` §5.5) — `E_m`은 spec §4.4의 encoder provenance를 채우는 주체. coord/radius placeholder → measured 전환의 유일 경로.
- ⇄ [[UNIVERSE]] (`./UNIVERSE/UNIVERSE.md`) — E_m 측정 결과(coord·cross-modal 일치)는 UNIVERSE H_xxx falsifier로 검증·기록.
- UNIVERSE/CANDIDATES.md SSOT 링크: ENCODER (Ψ-공간 측정자) 후보 등록.
