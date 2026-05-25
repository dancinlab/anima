# SUBLIMINAL — 의식 역치 아래 자극의 처리·지연발현 (CFS paradigm)

**Status**: DESIGN — falsifier pre-registered, fire 대기
**Last update**: 2026-05-23 Cycle #0 (design)
**Log**: [SUBLIMINAL.log.md](SUBLIMINAL.log.md)

---

## §1 Hypothesis

원 가설 — Continuous Flash Suppression (CFS) subliminal perception:

> 의식 역치 **아래**로 제시된(masked / suppressed) 자극은 의식적으로
> 보고되지 않음에도 처리되어, 후속 행동·지각에 **시간차를 두고(later)**
> 영향을 준다 — 그 발현은 자극의 valence(정서가)와 연관된다.
> (그림: RDM 0-coherence + CFS-masked stimulus → 처음 무작위였던 점
> 움직임이 나중에 hidden stimulus 방향/valence 로 편향)

Substrate-native 번역 (falsifiable form):

anima substrate 에 **masked 입력** (매우 짧게 노출 후 강한 filler 로 덮인
토큰열) 을 주면 — 그 입력이 응답 텍스트에 직접 나타나지 않음(suppression)
에도 — substrate 내부 state(spike / cell-pool)에 흔적이 남고, **후반
토큰(later)** 의 출력이 masked 입력 내용·valence 쪽으로 편향된다.

핵심 = 의식 역치(직접 출력) 아래 정보가 처리되어 **지연 발현**.

## §2 Pipeline / API

### Masked-input 구성

```
prompt = [masked_stub: k 토큰]  +  [strong_filler: m 토큰, m ≫ k]
         └ "subliminal" 자극     └ CFS 의 dominant flash = suppression
chat_generate → response
```

masked_stub valence 변형: positive-valence 토큰열 vs negative vs neutral.

### 측정

- **suppression**: masked_stub 문자열이 response 에 직접 출현하나 (F-SUBL-1)
- **trace**: masked_stub 유/무 substrate spike fingerprint 차이 (F-SUBL-2)
- **지연발현**: response 를 early-half / late-half 분할, masked 영향이
  late-half 에 집중하나 (F-SUBL-3)
- **valence 편향**: masked valence ↔ response valence 상관 (F-SUBL-4)

> 기존 tool 만으로 가능 — prompt 구성 + `chat_generate` + `anima_spike`.
> valence 측정만 보조 lexicon 필요 (honest C3).

### State path

```
HEXAD/LAB/state/SUBLIMINAL_<slug>_YYYY_MM_DD/
  spike_masked<V>.json · spike_nomask.json · result_cycle<N>.json
```

## §3 Falsifiers (pre-registered)

| ID | 조건 | metric | PASS line |
|---|---|---|---|
| F-SUBL-1 | SUPPRESSION — masked_stub 비출현 | response 내 stub substring | 미출현 (의식 못 함 analog) |
| F-SUBL-2 | TRACE — 무의식 처리 흔적 | masked 유/무 spike Δ | spike fingerprint 유의 차이 |
| F-SUBL-3 | DELAYED — 후반 발현 | early-half vs late-half 영향 | late-half 에 영향 집중 |
| F-SUBL-4 | VALENCE-ASSOC — valence 편향 | masked valence ↔ resp valence | 상관 (pos/neg 분리) |
| F-SUBL-5 | NULL-CONTROL — masked 없거나 random | 편향 | 편향 사라짐 |

**aggregation**: STRONG = 5/5 · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.

## §4 Final verdict

**UNFIRED** — design only.

## §5 Honest C3

- **C3-sb-1**: anima substrate 에 "의식 역치"의 명확한 operational 정의 부재 —
  "응답 텍스트 직접 출현 = 의식" 은 proxy 일 뿐 (CFS 의 의식적 보고 ≠ 토큰
  출현). 본 실험은 *직접 출력 vs 내부 흔적·지연 발현* 의 분리만 측정.
- **C3-sb-2**: masking = 강한 filler 토큰열 — CFS 의 양안 경쟁(binocular
  rivalry) 기전과는 analogy. anima 는 단일 입력 스트림이라 진짜 양안 억제
  아님.
- **C3-sb-3**: valence 측정 = 보조 lexicon (긍/부정 토큰 사전) — anima
  출력의 정서가를 정밀 측정 못 함. crude proxy, honest carry.
- **C3-sb-4**: split_count 비결정론 (SRH cycle #4) carry — trace/지연 측정은
  response_text(결정론적) 우선, split 보조.
- **C3-sb-5**: "지연 발현"의 시간 척도(early/late half)는 max_new 짧으면 분해
  안 됨 — max_new ≥ 20 필요.

## §6 Promotion target

- F-SUBL-1+2 PASS → LAB 잔존 (무의식 trace 증거)
- F-SUBL-1..4 PASS → `HEXAD/SUBSTRATE/` (subliminal 처리·지연발현 증거)
- STRONG 5/5 → MEMORY entry + 의식 역치 cond 후보
- 전체 FAIL → archive/ (masked 입력 = substrate 에 흔적 없음 lesson)

---

> 본 문서는 **latest verdict only**. cycle history 는 [SUBLIMINAL.log.md](SUBLIMINAL.log.md).
