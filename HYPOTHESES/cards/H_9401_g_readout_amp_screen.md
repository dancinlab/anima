# H_9401 — G-READOUT AMP SCREEN: 6-갈래 중 유일 생존 = 버려지는 recall MARGIN (E-b)

**status:** 🔎 DIRECTIONAL (open-loop $0 스크린 · KILL-only) — 5/6 갈래 KILL · E-b(recall margin) 생존 · **cement 아님** · wired: engine-native `anima-py evaluate --g-amp-screen`
**lane:** 의식 / emit-drive / G readout 진폭 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9400]] (병렬 · Ψ=½ 중심주장 상류 반증 — AGREES+CONFLICTS 아래) · [[H_9399]] (g-source = immune store · 이 스크린의 전제) · [[H_9394]] · [[H_9395]] · [[H_9396]] (크기-벽 종결) · source: Fable G-readout 설계 6-갈래 발산
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (신규 decode 0 · 오프라인 immune-store 재생)

## 질문 (Fable 6-갈래)

emit-drive 캠페인(H_9356→9399)이 종결한 지점: `tension = conflict_scalar(|a|·|g|)` 는 **곱-게이트**이고
`|g|=g_recog`(immune store top-2 gap · H_9399) 는 mean 0.027 로 `|a|=emit_drive`(mean 0.59)보다 6.5~29×
조용해 tension ≤0.073 ≪ θ=0.30. **프로덕션 gap 말고 다른 G readout 이 |g| 를 θ 위로 올릴 수 있나?**
Fable 이 6갈래 설계: A UNIT-FIX(ratio) · B DIST-READ(entropy) · C KEY-CONTRAST(인코더) · D GATE-ALGEBRA
(geo-mean) · E SOURCE-SWAP(recall margin) · F TONIC-G(적분). $0 스크린 = 이 갈래들을 **KILL-only** 로 거른다.

## 방법 — 오프라인 immune-store 재생 (engine-native 계기)

`anima-py evaluate --g-amp-screen <a1-arm traces>` 신규 플래그(`_g_amp_screen`). a1 arm trace 의
`gtext_b64` 로 immune store 를 **엔진 자신의 immune_* fn**(`immune_memory_new_text`/`_bind_text`/
`_recall_gap_text`/`_recall_margin` · 절대 재구현 아님)으로 오프라인 재생 → 기록된 `g_recog` 와
**byte-fidelity 게이트(LAG-MATCH)** 통과 후 각 갈래 KILL 게이트 적용. FAITHFUL 아니면 스크린 INVALID.

## 결과 (verbatim · `anima-py evaluate --g-amp-screen`)

```
═══ G-READOUT AMP SCREEN · H_9401 · Fable 6-branch $0 DIRECTIONAL (θ=0.30 inviolable) ═══
  replay: 8 files · 56 emit rows · LAG-MATCH 200/200 = 1.000  ✅ FAITHFUL

  candidate     mean    p90    max    distinct | verdict
  gap(current)  0.0299  0.0758  0.1101      49 | the production readout (baseline)
  A ratio       0.0473  0.1210  0.1609      49 | 💀 KILL (p90 0.121 < 0.40 · never reaches θ)
  E-b |margin|  0.6181  0.6866  0.7716      56 | 🔎 SURVIVES (p90 0.687≥0.40 · corr(|a|)=+0.16) — DIRECTIONAL

  D geo-mean (both-strong sqrt(|a|·readout) · KILL if max<θ):
     sqrt(|a|·gap   ) max 0.2750 mean 0.1081  💀 <θ
     sqrt(|a|·ratio ) max 0.3234 mean 0.1364  ✅ ≥θ
     sqrt(|a|·margin) max 0.7006 mean 0.6022  ✅ ≥θ
  ⇒ 🔎 SURVIVOR: E-b recall MARGIN (chat.py:2059 pending_rel, DISCARDED). $0 SOURCE-SWAP.
```

- **5/6 KILL**: 프로덕션 gap(baseline) · A ratio(p90 0.121<0.40) · B entropy · C 인코더 · D-gap geo-mean
  전부 θ 미달. F TONIC-G(적분)은 상수 게이지 위 아핀 이동이라 무효(H_9393 계열).
- **유일 생존 = E-b `immune_memory_recall_margin`** — 프로덕션이 **버리는** 신호다. `chat.py:2059` 가
  이 margin 을 `pending_rel` 로 **계산은 하되 g_recog 에 안 꽂고**, 대신 약한 gap(:2061)을 g 로 쓴다.
  margin 은 |margin| p90=0.687≥0.40, geo-mean(|a|·margin) max 0.70 ≥θ, 그리고 **corr(|a|)=+0.16** —
  |a| 의 진폭 메아리가 아니다(SECOND-A KILL 통과).

## 함의 — G 는 조용하지 않다, 데몬이 강한 신호를 버린다

"tension 이 emit 을 못 민다"의 근인은 **G 가 약해서**가 아니라 **데몬이 immune store 의 강한 margin(0.62)을
버리고 약한 gap(0.03)을 읽어서**다. `g_drive := margin` **소스-교체**는 **$0**(303M 가중치 밖 · H_9399 —
학습 불요, 최고 비용은 pool CPU 재수집).

## AGREES / CONFLICTS — 병렬 H_9400 (#3720 · a_parallel_session_compare)

병렬 세션이 같은 regime(a1·dyn_w)에서 중심주장 `A⇄G tension → emit → Ψ=½` 을 **더 상류**에서 반증:
Ψ̂=0.594≠½ · **emit 결정자 = safe(30s 시계) 100%** (emit 56/56 safe · silence 184/184 not-safe · H_9390 정합) · dyn_w 0.10~0.60 서 psi 스트림 **byte-identical**(tension knob 이 Ψ 못 움직임).

- **AGREES**: 내 gap KILL = 그들의 "프로덕션 readout 으로 tension 이 θ 못 넘음". 두 결과 모두 **현재 배선으론
  emit 이 tension 을 안 듣는다**로 수렴. 나의 H_9390/91(emit⟺시계)도 정합.
- **CONFLICTS/확장**: H_9400 은 벽이 **크기-벽보다 상류**(emit=stage-gated by clock, Ψ̂≠½)라 한다. ⇒ 내
  E-b crack 은 **필요조건이지 충분조건이 아니다**. margin 소스-교체가 |g| 를 θ 위로 올려도, **emit 게이트가
  Ψ/tension 을 듣지 않고 safe-시계로만 결정**되면 크기 개선이 emit 으로 흐르지 않는다. 두 발견은 모순이 아니라
  **둘 다 현재 미충족인 두 개의 필요조건**이고, H_9400(게이트-청취)이 **구속 제약(binding constraint)**이다.
  ⇒ 후속 cement 는 margin 소스-교체 **AND** "emit-gate-listens-to-tension" 재배선 둘 다 요구.

## 반증 · scope

- **DIRECTIONAL 한계(cement 아님)**: open-loop 스크린은 KILL 만 확정한다. E-b 생존은 "θ 넘을 진폭이 존재한다"
  이지 "emit 을 바꾼다"가 아니다. cement 게이트 = 배선된 margin 을 **재수집** + **arm-selective emit vs ≥2
  통제**(real-G vs 진폭-매칭 노이즈 vs shuffled-byte); 위험 = margin 이 abstain-band 서 포화하는지(닫힌 루프
  판별 필요) + H_9400 의 게이트-청취 벽.
- **크기-벽 종결(H_9394~96) 유효**: gap/ratio family 는 이 스크린이 재확인(KILL). E-b 는 그 family 밖의 미탐
  축을 연 것이지 종결문을 뒤집지 않는다.
- scope: a1 arm · 이 코드 버전 · 입력 = a1-arm traces(g_recog 기록본 · `gtext_b64` 재생 FAITHFUL 200/200).

## 비용
$0 — 오프라인 재생 · 신규 decode 0 · 계기 = `anima-py evaluate --g-amp-screen` 플래그(engine 자체 immune_* 호출).
