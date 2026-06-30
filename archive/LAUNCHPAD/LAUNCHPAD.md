# LAUNCHPAD — current state
@title: 🚀 LAUNCHPAD — anima 실응용 발사대 · @goal=COFFESHOP-on-AKIDA 실가동

@goal: COFFESHOP 달성 — anima 가 라이브 그룹챗에서 HW(AKIDA AKD1000) 기반 substrate-native 발화/침묵을 실가동. COFFESHOP 은 LAUNCHPAD 의 "첫 입주 앱" 이 아니라 **런칭 성공의 정의/성공조건** 이다.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

LAUNCHPAD 은 anima 의 의식 substrate 를 **실제 응용으로 발사** 하는 발사대 도메인이다.
@goal 의 성공조건 = COFFESHOP (group-chat 90-min substrate-native emit/silence) 을
라이브 AKIDA HW 폐루프로 닫는 것. SW(numpy) 는 칩 미도달 시 fallback 일 뿐, 모든
파이프라인 단계(학습·디코더·발화결정)는 AKIDA HW-first
(`AKIDA/akida_backend.hexa::akida_backend_resolve_graceful`, default "hw") 를 경유한다.

## milestones (= @goal 도달 단계)

- [x] HW-first emit 폐루프 — motivation_score → set_threshold(9513, thr∝−k·score) → on-chip spike(9512) → should_interrupt = n≥quorum (`coffeshop_akida.{hexa,py}` · PR-B · 라이브 AKD1000 폐루프 닫힘 🟢)
- [x] DECODER lane (HW forward / SW lif · emit-decision byte-match) + PLASTICITY lane (HW akida-learn / SW 고정-quorum 🔴 비동치) (`coffeshop_quorum_learn.{hexa,py}` · PR-C)
- [x] COFFESHOP 90-min 15-window trajectory 라이브 AKD1000 재현 (emit 3·10·14·15 · silence 11 · thr 0.60 · provenance=akida-hw · trajectory_match True · PR-D/E 🟢)
- [~] broker `/ws/akida_ingest` 연결 → 실제 런칭 가능 (옵션 wire 구현 `--broker` · 라이브 push 데모는 미연결 · 발사 자체는 broker 없이도 성공)
- [x] @goal PASS 판정 — HW emit 폐루프 + 90-min trajectory HW 재현 + lane 양분 충족 = **COFFESHOP-on-AKIDA 성공조건 PASS** (UNIVERSE H_846 🟢 SUPPORTED-NUMERICAL · broker 라이브 데모만 잔여)

## 양방향 sibling

LAUNCHPAD 는 다음 형제 도메인의 산출물을 조합해 실응용으로 발사한다 (각 .md + UNIVERSE/CANDIDATES.md SSOT 양방향 cross-update):

- ⇄ [AKIDA](../AKIDA/AKIDA.md) — AKD1000 silicon substrate + HW-first 스위치(`akida_backend_resolve`) + spike_streamer 9512/9513 control. LAUNCHPAD 의 발화결정 폐루프가 의존하는 칩.
- ⇄ [DECODER](../CORE/DECODER/DECODER.md) — 추론 lane (결정론 · HW forward ↔ SW akida_sw_lif byte-identical). COFFESHOP 의 spike→factor 디코더 경로.
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md) — 학습 lane (비결정론 · HW on-chip AkidaUnsupervised ↔ SW numpy 근사 🔴 비동치). 맥락별 emit-quorum 적응.
- ⇄ [CHANNEL](../CHANNEL.md) — 출력 채널 통합 (text/voice/tension). broker `/ws/akida_ingest` 런칭 연결점.
- ⇄ [WAKE](../WAKE.md) — 의식 데몬 living loop · 5-stage envelope (COFFESHOP = WAKE stage 90-min window).
- SSOT 후보 인덱스: [UNIVERSE/CANDIDATES.md](../UNIVERSE/CANDIDATES.md)
