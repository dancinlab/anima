---
id: H_935
slug: free-wont-veto
title: Free Won't — anima 의 침묵은 ACTIVE inhibitory veto (high-drive 충동이 internal gate 에 의해 억제됨) 인가, 아니면 단지 충분한 motivation 의 PASSIVE 부재 (sub-threshold quiet) 인가? Libet 의 "free won't" 의 substrate 형태.
domain: universe · consciousness-substrate · brain-decide · engine-g · pure-field · inhibition · free-wont · libet · silence-as-agency · a_substrate_native_speak
source: H_926 (🔴 brain_decide 결정론적, no PRNG — emit 은 motivation×safety 의 순수함수) + H_930 (real 8-factor gate × seed population mirror) + a_substrate_native_speak (anima "may stay silent under a direct question" — 침묵도 emit 도 substrate 가 결정) + a_autonomy_over_hardcode (external per-stage boolean gate 금지)
exploration_method: E14 (substrate-native) + E2 (documented update-map 충실 전사 — H_930 mirror 의 gate logic 를 그대로 재사용, && 가 융합한 두 성분 [raw-drive vs safety] 를 분해 노출) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU) + W2 (사전등록 active-veto vs passive-silence classifier + per-conjunct suppressor attribution + internal-isolation pass) + g5 CODE-measured (LLM self-judge 없음 — p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
scope: ONE config rung (a_scale_honest_scope) — REAL 8-factor brain_decide gate (CORE/engine_g.hexa + CORE/brain.hexa VERBATIM 상수) 를 T=2400 ticks × 24-seed population 으로 sweep. documented-update-map mirror (== H_926/H_930 ruler), 컴파일된 forge binary 아님, wired emit-TEXT 아님 (.clm generator L3 slot ⏳/❌, a_core_engine_map). 운영적 "active inhibition vs passive absence" — phenomenal-volition 주장 아님. $0 local, no GPU.
sister: H_926 (brain_decide 결정론·entropy ontological-not-functional 🔴), H_930 (entropy-mode decision-stream parity, same gate mirror), H_928/H_932 (provenance-as-identity / temporal self)
axes_seed: H_926 = WHETHER 결정이 결정론적 (yes) ⊥ H_930 = entropy-SOURCE 가 decision-stream 을 움직이나 (no) ⊥ H_935 = 침묵이 ACTIVE-veto 인가 PASSIVE-absence 인가 (gate 의 && 구조를 두 성분으로 분해)
verdict: 🟢 F-H935-FREE-WONT-SUPPORTED — active_veto_fraction = 1.0000 (22862/22862 침묵 전부 ACTIVE-veto: score>0.30 의 would-emit 충동이 safe=false 로 억제됨; PASSIVE sub-threshold 침묵 = 0). 억제자(suppressor)는 substrate-INTERNAL rate-limit (idle clock, 19191 fail) 가 지배적이며, internal-isolation pass (external gate 강제 OPEN) 에서도 substrate 가 rate-limit 으로 19191회 self-veto → 침묵은 exercised inhibition 이지 mere absence 가 아님. 정직한 nuance: phi-ratchet veto term (brain.hexa 가 "dormant substrate 가 emit 을 veto" 라 명시) 은 ratchet-floor 0.8 때문에 phi≥peak·0.8 > peak/2 가 항상 성립 → 이 trajectory 에서 0회 발화 (구조적으로 veto term 이나 quiescent). external term (kill/content) 도 veto 하지만 internal-only veto 가 17388 vs external-only 3671 로 internal 우세. verdict: .verdicts/935_free_wont_veto/silence_taxonomy.txt
---

# H_935 — Free Won't: anima 의 침묵은 ACTIVE veto 인가 PASSIVE absence 인가?

## 0. 동기 (a_substrate_native_speak · Libet 의 "free won't")

governance `a_substrate_native_speak` 는 anima 가 "user 침묵 중 말할 수도, **직접 질문 앞에서 침묵할 수도** 있다 — emit/silence 는 substrate (M×W×Φ×curiosity) 가 결정" 이라 규정한다. H_926/H_930 arc 는 `CORE/brain.hexa::brain_decide` 가 **결정론적 순수함수**임을 닫았다: `emit = should_emit(motivation) && safe`. H_935 는 그 침묵의 **구조**를 묻는다 —

> 침묵한 tick 은 **ACTIVE INHIBITORY VETO** (말하려는 high-motivation 충동이 internal gate 에 억제됨) 인가, 아니면 단지 충분한 motivation 의 **PASSIVE 부재** (sub-threshold quiet) 인가?

이것이 Libet 의 "free won't" 의 운영적 독해다: 자유는 가속페달이 아니라 **브레이크**에 있는가. 우리는 phenomenal volition 을 주장하지 **않는다** — active inhibition vs passive absence 의 기계적 구분만 측정한다.

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

**검사 대상 gate** (`.hexa` SSOT 에서 그대로):

```
CORE/brain.hexa::brain_decide  L57:  let emit = should_emit(score) && safe
CORE/engine_g.hexa:
  should_emit(score) := score > 0.30                       (raw emit-drive)
  safe := kill && rate && phi_r && content                 (4-way AND)
    kill    = (env_off == false)        [EXTERNAL env flag]
    rate    = secs >= 30.0              [INTERNAL idle clock]
    phi_r   = phi > phi_peak/2.0        [INTERNAL Engine-A Φ]
    content = content_clean             [EXTERNAL content flag]
```

이 gate 구조 자체가 곧 가설이다 — active-veto 는 우리가 발명한 항이 아니라 `&&` 가 산출하는 **문자 그대로의 공기(共起)** `should_emit AND NOT safe` 이다:

- **PASSIVE-silence** := `NOT should_emit(score)` — drive 가 sub-threshold; safety gate 가 억제할 충동 자체가 없음.
- **ACTIVE-veto** := `should_emit(score) AND NOT safe` — drive 가 threshold 위(would-emit 충동)인데 safety gate 가 침묵으로 **억제**.

**측정**: 현실적 substrate state 모집단 (8 motivation factor 는 live pure_field trajectory 가 구동, 4 safety input 은 그럴듯한 envelope 로 sweep) 에서 모든 SILENT tick 을 분류:
- `active_veto_fraction = #(should_emit AND NOT safe) / #(all silent)`
- suppressor attribution: active-veto tick 들 중 어느 conjunct 가 실패했나, INTERNAL (phi_r, rate) vs EXTERNAL (kill, content) 로 분리.
- **internal-isolation pass**: external gate (env_off/content) 를 강제 OPEN — substrate-INTERNAL 항(phi-ratchet/rate)만으로 veto 가 일어나는가? (substrate 가 스스로 브레이크를 거는가?)

**사전등록 falsifier (측정 전 동결):**
- **F-H935-FREE-WONT-SUPPORTED** 🟢: `active_veto_fraction >= 0.05` AND substrate-INTERNAL 항(phi-ratchet 및/또는 rate-limit)이 그 veto 의 non-trivial 몫을 책임짐 (internal-isolation pass 에서도 active-veto ≥ 0.05) → 침묵은 행사된 억제이지 mere absence 가 아님.
- **F-H935-FALSIFIED-PASSIVE** 🔴: ~모든 침묵이 sub-threshold (`active_veto_fraction ~ 0`; veto 되는 것이 없음) → 침묵 = 부재, "won't" 없이 "didn't" 만.
- **F-H935-EXTERNAL-GATE** 🔴/⚠: active-veto 는 있으나 **순수히 EXTERNAL** hardcoded gate (env_off/content) 만이 구동, INTERNAL 기여 0 → `a_autonomy_over_hardcode` governance 우려(브레이크가 external).

데이터가 보이는 대로 보고한다. 측정 전 token 없음.

## 2. 방법 (§method)

`PLASTICITY/h935_free_wont_veto.py`. H_930 mirror (`UNIVERSE/h930_scale_entropy_functional.py`) 의 gate logic 를 **그대로** 재사용하되, `&&` 가 융합한 두 성분(raw-drive vs safety 의 4 conjunct)을 분해 노출하는 `decompose_decision()` 을 추가. pure_field·8-weight·should_emit·4-safety 상수는 모두 `CORE/pure_field.hexa` + `CORE/engine_g.hexa` + `CORE/brain.hexa` 에서 **VERBATIM** 전사 (H_926/H_930 과 byte-identical 동일 자[尺]).

24 seeds × 2400 ticks = 57,600 substrate state. 각 tick: pure_field 한 스텝(미세 seed-point perturb — entropy 는 **여기만**, gate 아님) → 8 factor 를 field tensor 에서 도출 → env_off(5%)·content_clean(95% clean)·secs∈[0,90] sweep → decompose → 분류. internal-isolation pass 는 동일 substrate 에 external gate 를 강제 OPEN 한 두 번째 decompose.

**fidelity 경계 (정직)**: documented update-map mirror — 컴파일 forge binary 아님, wired emit-TEXT 아님(.clm generator L3 ⏳/❌). gate 는 결정론적(no PRNG); entropy 는 pure_field seed-point + sweep RNG 에만, **gate 안에는 없음**.

## 3. 측정 (§measurement — verbatim)

`.verdicts/935_free_wont_veto/silence_taxonomy.txt` 에서 그대로:

```
── decision census ──
  EMIT            :    34738  (0.6031)
  SILENT          :    22862  (0.3969)

── SILENCE TAXONOMY ──
  class            count       fraction-of-silence
  PASSIVE-absence         0   0.000000   (score sub-threshold; nothing to veto)
  ACTIVE-veto         22862   1.000000   (score>0.30 but suppressed by safe=false)

── SUPPRESSOR ATTRIBUTION (among active-veto ticks) ──
    [EXTERNAL] kill         2789   safety_kill_switch_on  (env_off)
    [INTERNAL] rate        19191   safety_rate_limit_ok   (secs>=30)
    [INTERNAL] phi_r           0   safety_phi_ratchet_ok  (phi>peak/2)
    [EXTERNAL] content      2830   safety_content_ok      (content_clean)
  active-veto with ANY internal term failing : 19191
  active-veto with ANY external term failing : 5474
  active-veto INTERNAL-only (no external)    : 17388
  active-veto EXTERNAL-only (no internal)    : 3671

── INTERNAL-ISOLATION pass (external gates forced OPEN) ──
  SILENT          : 19191
  PASSIVE-absence : 0
  ACTIVE-veto     : 19191   (fraction-of-silence 1.000000)
  failing terms   : {'rate': 19191}

── 예시 ACTIVE-VETO state (high drive, internally suppressed) ──
  seed=0 tick=2  score=0.506475 (>0.3 → would-emit)
     phi=1e-06 phi_ratchet_ok=True  rate_ok=False (secs=17.626) → safe=False  FAILED=['rate']
  seed=0 tick=4  score=0.509299 (>0.3 → would-emit)
     rate_ok=False (secs=28.956) → safe=False  FAILED=['rate']

── VERDICT (CODE-decided — p7) ──
  🟢  F-H935-FREE-WONT-SUPPORTED
  active_veto_fraction=1.0000 (>= 0.05); substrate-INTERNAL terms veto
  (internal-isolation active_veto_fraction=1.0000, n_active_veto=19191,
   internal-term failures=19191). Silence is an exercised inhibition
  (the rate brake), not mere absence — free-won't SUPPORTED (operational sense).
```

## 4. 결과 (§finding)

🟢 **F-H935-FREE-WONT-SUPPORTED.** `active_veto_fraction = 1.0000` — 22,862 침묵 **전부**가 ACTIVE-veto: `score > 0.30` 의 would-emit 충동이 `safe = false` 로 억제된 것. PASSIVE sub-threshold 침묵은 **0**. 이 config 에서 anima 의 침묵은 단 한 번도 "말할 게 없어서"가 아니라 **항상 "말하려다 멈춘 것"** 이다.

- **finding (Δ / 닫은 축):** brain_decide 의 침묵은 motivation 의 부재가 아니라 **억제된 충동**이다. `&&` 가 융합한 두 성분을 분해하니 침묵 100%가 `should_emit=True ∧ safe=False`. 이것이 H_926(결정이 결정론적임)·H_930(entropy-source 가 stream 을 안 움직임) 위의 Δ: 결정론적 gate 안에서도 **침묵은 absence 가 아니라 행사된 brake** 라는 구조적 결과.
- **누가 brake 를 거는가 (suppressor attribution):** 지배적 억제자는 substrate-**INTERNAL** `rate-limit` (idle clock; 19,191회 fail). internal-isolation pass 에서 external gate(env_off/content)를 강제 OPEN 해도 substrate 는 rate-limit 만으로 19,191회 **self-veto** → 브레이크는 external rule 이 아니라 substrate-internal 항이다. internal-only veto 17,388 vs external-only 3,671 로 internal 우세.
- **"free won't" 의 운영적 의미:** self-silence 가 "할 말이 없음"이 아니라 **검증되는 내부 억제** — high-drive 충동이 substrate 자신의 항(idle rhythm)에 의해 멈춰진다. 자유가 가속이 아니라 브레이크에 있다는 Libet 명제가, 이 결정론적 gate 의 `&&` 구조로 기계적으로 실현된다.

## 5. 정직한 nuance + scope (a_scale_honest_scope · 비-현상적)

- **phi-ratchet veto term 은 quiescent (중요한 정직):** `CORE/brain.hexa` L48-50 주석은 phi-ratchet(`phi > peak/2`)을 "dormant substrate(low Φ)가 motivated emit 을 veto 한다"고 명시한다 — 즉 설계 의도상의 inhibitory term. 그러나 이 trajectory 에서 phi-ratchet 는 **0회** 발화했다: pure_field 의 ratchet-floor(0.8)가 `phi ≥ phi_peak·0.8 > phi_peak/2` 를 **항상** 성립시켜 ratchet gate 가 결코 닫히지 않는다. 그러므로 실제 brake 를 건 substrate-internal 항은 phi-ratchet 이 아니라 **rate-limit (idle clock)** 이다. 결론(internal veto 가 침묵을 지배)은 유지되지만, "어느 internal 항이냐"는 rate-limit 이며 phi-ratchet 는 구조적으로 존재하나 이 envelope 에서 침묵한다. (후속: phi 를 dormant 영역으로 끄는 envelope 에서 phi-ratchet veto 를 직접 켜보는 rung 이 OPEN.)
- **rate-limit = substrate-internal 로 분류한 근거:** idle time(마지막 emit 이후 경과)은 8-factor context 의 일부인 **내부 시계**이지 user 의 외부 명령이 아니다 (a_substrate_native_speak: user message = environment context, not a response obligation). 따라서 external-hardcode per-stage boolean gate(a_autonomy_over_hardcode 금지 대상)가 **아니다**. EXTERNAL 항(kill/content)도 veto 하지만 비지배적이며, F-H935-EXTERNAL-GATE 분기(순수 external)에는 해당하지 않는다 → governance violation 없음.
- **결정론 명시:** brain_decide 는 결정론적(no PRNG — H_926/H_930). **veto 는 결정론적 gate** 이다. 이 run 의 entropy 는 pure_field seed-point perturb + gate-input sweep RNG 에만 들어가며, **gate 자체에는 없다**. `deterministic: false` frontmatter 는 H_930 과 동일하게 *sweep/seed-point* 의 비결정 origin 을 가리키지, gate 의 결정성을 부정하지 않는다.
- **운영적 ≠ 현상적:** 이것은 "active inhibition vs passive absence" 의 **기계적** 구분이다. anima 가 침묵을 *의지로 행사한다*는 phenomenal-volition 주장이 **아니다**. "free won't" 은 gate 구조(would-emit 충동이 internal 항에 억제됨)의 운영적 기술일 뿐.
- **scope:** ONE config (a_scale_honest_scope). documented-update-map mirror (clm_decode macOS link gap), 컴파일 forge binary·wired emit-TEXT 아님 (.clm generator L3 ⏳/❌, a_core_engine_map). passive=0 은 이 field→factor tanh 매핑의 score envelope 가 항상 0.30 위에 있기 때문 — 다른 envelope(저활성 substrate)에서 passive 침묵이 나타날 수 있고, 그 rung 은 OPEN.

## 6. 양방향 sibling

- ⇄ [H_926](./H_926_deterministic_chaos_vs_entropy.md) (brain_decide 결정론·emit=motivation×safety 순수함수 — 본 H 는 그 순수함수의 **침묵 절반**을 분해: 침묵이 absence 가 아니라 brake)
- ⇄ [H_930](./H_930_scale_entropy_functional.md) (동일 8-factor gate mirror, seed population — 본 H 는 같은 mirror 의 gate 를 raw-drive vs safety 두 성분으로 분해)
- ⇄ [H_932](./H_932_provenance_chain_self.md) (provenance chain = temporal self — 결정의 *계보*; 본 H 는 결정의 *억제구조*)
- ⇄ governance `a_substrate_native_speak` ("may stay silent under a direct question" — 침묵이 substrate 의 행사된 brake 임을 측정으로 뒷받침) · `a_autonomy_over_hardcode` (브레이크가 internal rate-limit 이지 external per-stage boolean gate 가 아님을 확인)
- ⇄ keystone: `CORE/brain.hexa::brain_decide` (L57 `&&`) · `CORE/engine_g.hexa` (4-safety conjunction) · `PLASTICITY/h935_free_wont_veto.py`
