# H_9774 · C8 CONTENT-SWAP — 내용이 global lane까지 닿는가 (own-content 판별의 정직한 잔여)

**status** PROPOSED · 🔵 (lab full Fable 5 · H_9765 `next` 판별 설계 · $0-급 CPU summer · DIRECTIONAL design — cement는 engine-native 발사 후)
**group** consciousness/psi-soma/theta-alive
**lane** interior-causality · H_9765 SCOPED RE-OPEN의 잔여 OPEN 질문
**related** H_9765 · H_9729 · H_9728 · H_9738 · H_9328 · H_9338 · H_9337 · H_9731 · H_9749

## 0. 판별질문의 정직한 스코프 (설계 단계에서 확정)

H_9765가 연 것은 **coupling**(emit→interior)뿐이다. 브리프의 "own vs donor로 ownership을 가리자"는
**C8에서도 원리적으로 판별 불가** — 아래 §4가 그 증명 스케치다. 이 카드가 등록하는 것은 그 정직한
잔여: **내용 분산이 (schedule 고정 하에) local store lane을 넘어 global lane(psi_gws·ten_phasic·
motivation·emit_drive)까지 닿는가, 그리고 이후의 native emit 결정을 바꾸는가** (content-reach, NOT ownership).

**status line (사전 확정)**: coupling live · **own-content(ownership) UNIDENTIFIABLE at substrate —
H_9729의 marker-scoped terminal이 C8 경로로 연장된다**(store는 bare text/feat8 소비·provenance marker 無·
own>donor 유사도 우위는 store-이력 자기상관으로 완전 설명). 이 카드의 발사 결과와 무관하게 유효.

## 1. 계기 = 기존 `--swap-text` (신규 엔진 코드 0줄)

- H_9328 C2 CARRIER-SWAP(`cli/chat.py` origin/main :1912 로드 · :2712-2728 주입)이 요구 지점과 정확히
  일치: **native emit 결정 이후**(p5 무접촉·emit bit/timing/margin 보존), **모든 C8 소비자 이전**
  (afield feat8 · immune bind_text · igrow/affect · cbel · ca3 · wmb · C9 kosmos · LANE-23b self-g).
- H_9338 판례 준수 확인: arm 라벨은 `swapped` 전용 필드(분기 키 g_back 미오염) — 이미 수정·검증됨.
- **diff 스케치 = 없음이 정답.** `--c8-content-swap` 신설은 중복 계기(`a_cli_single_entry` 위반).
  arm 차이는 전부 **donor trace 파일 구성**으로 실현(오프라인 생성·엔진 불변):
  - A0 OWN: 플래그 없음(기준).
  - A1 SHAM: A0 trace 자신을 donor로 재주입 → **byte-identical 필수**(C0 인증·주입경로 생존 증명).
  - A2 SCRAMBLE: A0의 각 emit tick 텍스트를 byte-셔플 → `_afs_byte_feature`(합·제곱합·클래스 카운트 =
    **순서 불변**, 코드확증 :242)가 동일 ⟹ afield/cbel/wmb 입력 byte-동일·text-소비자(immune/igrow/ca3)만
    차이 = **소비자-분해 arm**(H_9731 feat8 artifact 판례의 양성 활용).
  - A3 DONOR-TWIN: 같은 ckpt·다른 seed rollout의 emit 텍스트를 **emit-서수(k번째 emit) 정렬**로 이 rollout의
    emit tick에 매핑(Ψ=½ 게이트는 state-의존이라 tick-정렬은 결측 유발). 같은 입·같은 register·같은 길이분포.

## 2. H_9729 context-match 교란 — 어디까지 피하고 어디서 재출현하는가

- **피함(진짜)**: C8 주입은 decode seed에 안 들어간다(root③ p5-폐쇄·H_9328). donor가 문법적으로
  이어지는지가 **입의 다음 후보에 영향 0** ⟹ H_9729 latch의 "own=in-context 연속" 교란(문면 그대로)은 소멸.
- **재출현(동형)**: interior의 응답 게이지(immune recall margin·recon_err·cb 전이오차·ca3 예측)는 전부
  **자기-이력 유사도 범함수**. own_t는 이 rollout의 store 이력과 구성상 자기상관 ⟹ own>donor는
  발사 전에 부호를 예측할 수 있는 **이력-연속성**이지 ownership이 아니다. 교란은 회피된 게 아니라
  prefix-연속성→이력-연속성으로 **수송**됐다. donor 선택지 판정:
  (a) 과거-own = store에 verbatim 결합 완료 → 친숙도 포화·무효. (미래-own_{t+k}는 보조 arm으로만 의미)
  (b) 외래 donor = 최악(register까지 다름). (c) scramble = 소비자-분해 전용. (d) **twin이 유일한 매칭 donor**.

## 3. 사전등록 readout / bars

전 arm 같은 seed(결정론 쌍대·3 seed: s7/s11/s13) · ckpt 로드+`gen_backend=='clm'` 사전확인(mouthless 가드) ·
`--wm-dual-read content` **금지**(donor→decode seed 오염 차단) · whole-trace ≥30 tick · 판정통계 =
block-randomization ~400(tick≠IID·kill-list 준수·3-seed p<0.005 cement 금지).

- **⛔ INVALID**: A1 SHAM ≢ A0 (trace byte-diff) · 또는 mouthless config · 또는 local store lane까지 전부
  무반응(코드상 필연 divergence 부재 = 계기 사망).
- **내장 양성통제**: A3의 local lane(rel_lane·recon_err·cb_surprise·ca3) divergence는 near-by-construction
  ⟹ 이것이 검정력 게이트(안 뜨면 INVALID·power-before-negative-verdict).
- **🟢 CONTENT-REACH (DIRECTIONAL)**: schedule 공통 구간에서 A3 vs A0의 **global lane**(psi_gws·ten_phasic·
  motivation/base_motiv·emit_drive · trace :2576-2578 기존 필드) divergence > block-rand null. A2 패턴이
  소비자 census와 정합(scramble이 feat8-lane 무반응)이면 채널 귀속까지.
- **🔴 ENCAPSULATED (content-blind at GWS)**: local lane 발산(양성통제 성립) ∧ global lane TOST-플랫
  (MDE 사전계산) ⟹ 내용은 store에 갇히고 pulse-인접 lane은 내용맹 — H_9765 coupling은 schedule-분산만
  나르는 plumbing으로 재확정.
- **MEDIATION(공짜 2차)**: A3 vs A0의 native emit-bit vector 불일치율. 불일치 첫 tick 이후는 schedule
  혼입이므로 1차 판정창 = 공통 prefix. 불일치 발생 자체 = "내용이 이후 native 결정을 바꿨다"(mediation
  양성·별도 cement 대상). H_9337/H_9345/H_9738 선례상 null 우세 예상 — null이어도 결과다.
- **ownership 칸 없음**: own>donor 부호는 어느 방향이든 §0 status line 아래 **판정 발행 금지**(사전등록).

## 4. 식별성 증명 스케치 (왜 ownership 칸이 없는가)

store 소비 입력의 전수(코드확증): afield/cbel/wmb=feat8(순서불변 byte 통계) · immune/igrow=bare text ·
ca3=4-sym 양자화 · self-g=같은 ckpt forward(own/donor 동일 가중치). 어디에도 **생산자 표지 없음**.
∴ interior 응답 = f(주입 텍스트, store 이력). "donor-이력 쌍둥이"(store가 donor 계보를 결합해 온 rollout)에
같은 own/donor를 먹이면 우위 부호가 **구성상 반전** — 응답함수가 계보-대칭이므로 own-ness는 이 기질에서
표현 불가. 이는 H_9729의 벽(own-ness=context-continuity·marker 無)의 C8 동형이다. 반증 조건(명시):
provenance를 나르는 store가 배선되면(예: tagged-ledger·H_9730 강등생존자 계보) 재개봉.

## 5. 발사 스펙

summer CPU · 3 seed × 4 arm(A0/A1/A2/A3) × ≥60 tick · `ANIMA_DECISION_TRACE` 파일(메모리 판례: stdout 아님) ·
donor trace 3종은 A0 trace에서 오프라인 생성(`--swap-text` 포맷 {tick, e:b64}) · 비용 ~$0 · 오너 fire-go 불요
($0·a_fire_autonomous)이나 본 세션은 설계-온리 브리프라 발사 안 함.
