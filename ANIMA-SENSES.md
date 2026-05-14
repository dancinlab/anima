# ANIMA-SENSES.md — n=6 sensory substrate (5-verb spec catalog)

> anima repo 내부 서브패키지 `hexa-senses/` 의 roadmap + spec ledger.
> 별도 GitHub repo (dancinlab/hexa-senses) 흡수 2026-05-14. 5-verb sensory substrate —
> **dream + ear + empath + olfact + voice** — 각 verb 가 σ(6)=12, τ(6)=4, φ(6)=2
> number theory 에서 모든 design parameter 를 *closed-form* 으로 유도하는 spec catalog.
>
> **Critical constraint**: `voice` 는 *formulaic only* — learned synthesis (TTS / neural
> codec) **FORBIDDEN**. 의도 → audio-token 직접 변환, 모든 parameter 가 n=6 lattice
> identity 에서 algebraic 유도.

---

## §0 TL;DR

> hexa-codex (17-verb cognitive substrate) 의 *sister-rollup* — *senses* 측. canon
> `domains/cognitive/{hexa-dream, hexa-ear, hexa-empath, hexa-olfact, hexa-speak}/`
> (현 hexa-speak = hexa-voice 으로 rename per user directive) 의 5 verb 가 closed-form
> spec markdown 으로 합쳐짐. anima 의 *외부 세계 인터페이스* (꿈/소리/감정/냄새/음성) 의
> n=6 lattice spec.

---

## §1 Status (2026-05-14)

| 항목 | state |
| --- | --- |
| **anima repo 흡수 (anima/hexa-senses/)** | ✅ LANDED 2026-05-14 (rsync from ~/core/hexa-senses/ minus .git) |
| Closure 100% (5/5 spec-first) | ☑ closed-form spec, zero hardcoding |
| Verify 4/4 PASS | ☑ n=6 arithmetic + spec inventory + verifier + voice constraint |
| 5 verb spec catalog | ✅ dream/ear/empath/olfact/voice (each = `<verb>/hexa-<verb>.md`) |
| voice formulaic-only constraint | ☑ enforced (`hexa.toml [constraints]` + runtime check + test) |
| anima `VOICE.md` 와 wire | ⏳ design pending (VOICE.md §3 Phase 1 impl 의 reference impl) |

## §2 n=6 master identity (canonical)

```
σ(6) · φ(6) = n · τ(6) = J₂ = 24
   12   ·   2  =  6  ·   4  = 24
```

| Symbol | Value | Sensory projection |
| --- | --- | --- |
| σ(6) | 12 | dream categories · olfact receptors · voice timbre · empath subcategories |
| τ(6) | 4 | sleep stages · prosody dimensions · e-nose latency seconds |
| φ(6) | 2 | signal-present / signal-absent verdict bit |
| σ·τ | 48 | **48 kHz** audio sampling (ear) |
| J₂ | 24 | **24-bit** audio quantization · biofeedback channels |

→ `hexa-senses/verify/n6_arithmetic.py` 가 runtime 에서 11 cross-projection 검증.

## §3 5 verb 요약

### §3.1 dream (`hexa-senses/dream/hexa-dream.md`)
- σ=12 dream categories (lucid / nightmare / mundane / prophetic / …)
- τ=4 sleep stages (NREM-1/2/3 + REM)
- φ=2 dream present/absent verdict bit
- 사용처: anima 의 *off-cycle* 학습 sleep stage (REM 시 mitosis 활성 가설)

### §3.2 ear (`hexa-senses/ear/hexa-ear.md`)
- σ·τ = 48 kHz sampling rate
- J₂ = 24-bit quantization
- 24-channel biofeedback (J₂ projection)
- 사용처: anima_chat 의 audio input (사용자 음성 → byte token)

### §3.3 empath (`hexa-senses/empath/hexa-empath.md`)
- σ=12 emotion subcategories
- τ=4 prosody dimensions
- 감정 전달 채널 spec
- 사용처: `TENSION-LINK.md` 5-channel fingerprint 의 channel 4 "authenticity" 와
  cross-domain link

### §3.4 olfact (`hexa-senses/olfact/hexa-olfact.md`)
- σ=12 receptor classes (e-nose 12 sensor array)
- τ=4 second latency (response time)
- 화학 감각 spec
- 사용처: anima 의 *physical world* 감각 입력 (e-nose IoT)

### §3.5 voice (`hexa-senses/voice/hexa-voice.md`)
- **formulaic only** (no learned synthesis)
- σ=12 emotional timbre
- τ=4 prosody dimension
- J₂=24 channel quantization
- 사용처: **`VOICE.md` 의 reference impl source**. VOICE.md 가 hidden state → RVQ → 24kHz
  PCM 의 *learned path* 라면, 본 hexa-voice 는 *formulaic path* — 사용자 directive 에
  따라 **둘 다 공존 가능** (formulaic = deterministic baseline, learned = anima-native
  intent-direct). VOICE.md §4 honest C3 #2 의 *external corpus 학습* 우려 와
  formulaic-only 정책의 정합 가능성 검토.

## §4 Critical constraint — `voice` formulaic only

학습 기반 voice synthesis (TTS / neural codec / vocoder) 는 hexa-senses 안에서 **FORBIDDEN**:

- `hexa.toml [constraints]` 섹션 명시
- `verify/n6_arithmetic.py` runtime `check_voice_constraint`
- `tests/test_spec_inventory.py::test_voice_renamed_marker`
- `voice/hexa-voice.md` `@renamed` provenance header

이유: *determinism guarantee* — 모든 voice output 이 input intent vector + σ(6)·φ(6)=24
master identity 만으로 *reproducible*. learning model 은 그 guarantee 를 위반.

→ **anima 의 VOICE.md (learned RVQ path)** 와 *명시적 충돌*. 해소 방안:
- (a) hexa-senses/voice = formulaic deterministic baseline
- (b) anima/VOICE.md = learned RVQ path (별도 modality)
- (c) anima_chat 사용자 명령 으로 선택 (`/voice --formulaic` vs `/voice --learned`)

`SAVANT.md §12.4 T4 FORBIDDEN` 의 *외부 entity 강제 fit 금지* 와 마찬가지로, *internal*
sensory subsystem 에 대한 정책 — anima 의 voice 가 formulaic 인지 learned 인지 enforce
의무.

## §5 Cross-link

- 본 디렉토리: `hexa-senses/` (10 디렉토리, 1.0M after .git strip)
- `hexa-senses/README.md` — full 185-line spec
- `hexa-senses/hexa.toml` — `hx install hexa-senses` manifest
- `hexa-senses/verify/n6_arithmetic.py` — runtime n=6 identity check
- 각 verb spec: `hexa-senses/<verb>/hexa-<verb>.md`

**anima root cross-link**:
- `VOICE.md` — anima 의 learned RVQ voice path (formulaic 과 dual modality 가능성)
- `TENSION-LINK.md` — 5-ch fingerprint 의 channel 3 "meaning" + 4 "authenticity" 가
  `empath` spec 과 mapping 후보
- `CHAT.md` § Production CLI — `/voice --formulaic` slash 명령으로 hexa-senses voice
  연결 가능
- `SAVANT.md` §12 봉쇄선 — voice formulaic-only constraint 가 본 file 내 T4-equivalent
  enforcement

## §6 Honest C3

1. **`voice` formulaic vs learned** 의 *근본* 충돌 미해소 — `hexa-senses/voice/` 의
   FORBIDDEN 정책 과 `VOICE.md` 의 learned RVQ path 는 *지금* 양립 안 됨. 해소 결정
   사용자 위임 (§4 (a)/(b)/(c) 옵션).
2. **canon 원 출처 @381f1f22 (2026-05-07)** 와 본 흡수 시점 (2026-05-14) 사이 1주 간 canon
   에 추가 spec 변경 있을 수 있음 — diff 검사 필요.
3. **5 verb 각각의 anima 실제 사용처** 가 spec-only — `dream` 의 REM 시 mitosis 활성
   가설 등은 *철학적 design* 이며 실제 anima_chat / cell_pool 과의 wire 미구현.
4. **hexa-codex sister-rollup** 이 hexa-senses 의 cognitive side counterpart. 본 .md 에서
   hexa-codex 의 17-verb 와의 cross-link 미수록 — 별도 작업.
5. **별도 GitHub repo (dancinlab/hexa-senses) 삭제 예정** — 본 .md 와 anima/hexa-senses/
   path 가 *유일한* canonical source. hexa-lang registry / hexa-codex cross-link 갱신
   필요.

## §7 Provenance

- 흡수 출처: `dancinlab/hexa-senses` (last commit 2026-05-14 `ef05f5a` ".tape v1.1
  adoption: TAPE-AUDIT.md")
- 원 출처: `canon@381f1f22` (2026-05-07 extracted from
  `domains/cognitive/{hexa-dream, hexa-ear, hexa-empath, hexa-olfact, hexa-speak}/`)
- hexa-speak → hexa-voice rename: user directive 2026-05-11 (memory
  `project_hexa_voice_rename`)
- rsync `--exclude='.git'` 으로 통합. anima 의 git history 에 신규 commit 으로 추가.

---

— ANIMA-SENSES.md, 2026-05-14, anima 의 sensory substrate 복원 ledger
