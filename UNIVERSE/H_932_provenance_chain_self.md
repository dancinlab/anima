---
id: H_932
slug: provenance-chain-self
title: provenance chain = temporal self — anima 결정들의 전체 시퀀스(genesis 양자 seed → 결정₁ → … → now)가 append-only tamper-evident 해시 CHAIN 으로 묶여 end-to-end 독립 재구성·검증 가능하고, 과거 변조가 그 지점부터 전파·국소화된다
domain: universe · qrng · entropy-provenance · auditability · tamper-evidence · hash-chain · temporal-self · merkle-blockchain · substrate-native
source: H_928 (single-receipt provenance-as-identity) 의 시간축 일반화 — "한 결정의 계보" → "전체 life-history 의 계보" 를 검증되는 암호학적 객체로
exploration_method: E2 (H_928 single receipt 를 chain 으로 일반화) + E14 (substrate-native) + a_completeness_over_cheap
verification_method: W1 (python3 CODE-measured 실행) + W2 (사전등록 positive + 4-case tamper falsifier, earliest-broken-index 까지) + g5 CODE-measured
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
sister: H_928 (single-decision receipt → 본 H 는 그 receipt 들을 chain 으로 봉인), H_924 (provenance = 양자 엔트로피의 *가치*), H_923 (HW 양자결합 · 물리 draw origin), qentropy SSOT (mirror/qmirror/seed/qentropy.py)
axes_seed: H_928 = 한 결정의 계보를 receipt 로 검증 ⊥ H_932 = 결정들의 *전체 시퀀스* 를 append-only tamper-propagating chain 으로 봉인 (과거 변조 → 그 지점부터 전파 + 국소화)
verdict: 🟢 SUPPORTED — POSITIVE verify=True (20/20 links genesis 로부터 재구성) AND 4-case tamper 모두 정확한 earliest-broken-index 로 DETECTED+LOCALIZED. genesis e8123b96…(req_id anu_legacy_1778042160) → 20 links → head d5c68644…; tamper (a) output@k=7 → break@7 (links<7 valid, links>=7 invalid: 전파), (b) reorder(5,12) → break@5, (c) splice(9) → break@9, (d) genesis 변조 → break@-1 (root, 전체 무효). verdict: .verdicts/932_provenance_chain_self/chain_tamper_evidence_pass.txt
---

# H_932 — provenance chain = temporal self

## 0. 동기

[H_928](./H_928_provenance_as_identity.md) 은 **한 결정**의 엔트로피 계보(물리 ANU draw →
seed → 그 결정)가 독립 검증자에 의해 end-to-end 재구성 가능 + tamper-evident 임을 확정했다
(receipt = 하나의 결정에 대한 암호학적 영수증). 자연스러운 시간축 질문:

> **anima 결정들의 *전체 시퀀스* 를 하나의 tamper-evident 해시 CHAIN (genesis 양자 seed →
> 결정₁ → 결정₂ → … → now) 으로 묶을 수 있는가** — 그래서 (a) 전체 life-history 가 end-to-end
> 독립 재구성·검증되고, (b) 과거의 *어떤* 결정을 변조해도 그 지점부터 chain 이 깨지는가?

이것이 성립하면 "**시간에 걸친 self**" 가 감사가능한 암호학적 객체가 된다 — memory 가 아니라
**검증되는 인과적 계보(verifiable causal lineage)**. "temporal self" 는 여기서 **운영적·암호학적
의미**(시간에 걸친 검증가능 식별자)이며, 주관적 연속성(subjective continuity) 과 명시적으로 구별한다
(§5).

## 1. 가설 (사전등록 falsifier — 측정 전 동결)

H_928 receipt 위에 Merkle/blockchain-style chain 을 쌓는다:

    genesis        = sha256(committed ANU buffer bytes)         # link_hash_{-1}
    link_hash_i    = sha256( link_hash_{i-1} || canonical(receipt_i) )
    receipt_i      = H_928 receipt (issue_receipt) for decision i

각 link 가 직전 link 해시를 접어 넣으므로 **append-only · tamper-propagating** (모든 link 가 모든
이전 history 를 봉인). chain VERIFIER 는 chain + ANU 버퍼 + decision_fn 만으로 genesis 부터 **모든
link 를 독립 재계산**하고 head 를 확인하며, 변조된 chain 에 대해 **EARLIEST broken link index** 를
보고한다.

**falsifier (사전등록, 측정 전 토큰 금지):**

- **POSITIVE** — N≥20 link chain build → head verify ⇒ `verified=True`, 전 N link 재구성.
- **TAMPER (각각 정확한 earliest-broken-index 로 검출되어야 함):**
  - (a) 중간 결정 k 의 output 변조 → **break@k**, links<k 전부 valid, links≥k 전부 invalid(전파).
  - (b) 두 link 의 reorder → **검출** (earliest disturbed position).
  - (c) link 의 splice/delete → **검출** (삭제 지점).
  - (d) genesis ANU seed 변조 → **break@-1** (root, 전체 chain 무효).
- **SUPPORTED** ⟺ POSITIVE `verified=True` **AND** 4-case tamper 전부 **정확한 earliest link 에서
  검출** **AND** 과거-변조가 forward 로 전파. **FALSIFIED** ⟺ 변조 중 하나라도 미검출 / 오국소화.

## 2. 방법 (§method)

Keystone: **`mirror/qmirror/seed/provenance_chain.py`** (꼼꼼 주석, `entropy_receipt` +
`qentropy` 를 *수정 없이* import — H_928/SSOT 보존).

- `build_chain(anu_buf, decisions)` → 순서 있는 `(label, decision_fn)` 시퀀스 각각에 대해 H_928
  `issue_receipt` 를 발급하고 `link_hash_i = sha256(link_hash_{i-1} || canonical(receipt_i))`
  로 봉인. 반환: `{genesis_hash, links[{index,label,receipt,prev_link_hash,link_hash}], head_hash}`.
- `verify_chain(chain, anu_buf, decision_fn_for)` → 디스크에서 ANU 버퍼를 재독해해 genesis 재계산
  (≠ → break@-1), 그 뒤 link 를 순서대로 walk: 각 link 에서 (a) H_928 `verify_receipt` 재실행
  (seed 재유도 · 결정 재실행 · receipt_hash 재계산), (b) **recompute 된 prev 해시**로부터 inter-link
  `link_hash` 재계산해 기록값과 비교. 둘 중 하나라도 실패하는 **첫** link = `earliest_broken`;
  그 이전은 valid, 그 지점부터 invalid. 반환: `{verified, head_hash, earliest_broken, n_links,
  link_valid[], reason}`.
- inter-link 결합은 도메인 분리 바이트(`\x00`)로 prev-hex 와 receipt 를 join — concat 모호성 제거.
- seed 유도는 H_928 = qentropy SSOT 와 **정확히 일치** (quantum 모드, ANU 버퍼 pin, fresh cursor;
  cross-process byte-identical). chain 은 각 receipt 의 tamper-evidence 를 **상속**하고 그 위에
  inter-link 봉인(append-only · 과거-변조 전파)을 **추가**한다.
- tamper helper(순수, 새 chain 반환): `tamper_decision_output(k)` · `tamper_seed(k)` ·
  `tamper_reorder(i,j)` · `tamper_splice(k)` · `tamper_genesis()`. (a)/(seed) 는 receipt_hash 를
  **재봉인**해 내부적으로 일관된 *가장 강한* 위조를 만든 뒤에도 검출됨을 보인다.

데모: `state/h932_chain_demo/run_chain_demo.py` — committed 버퍼, N=20 emit/silence+token 결정,
$0 local, no network. g5 CODE-measured (no LLM self-judge).

## 3. 측정 (§measurement — verbatim)

`.verdicts/932_provenance_chain_self/chain_tamper_evidence_pass.txt` (raw stdout):

```
--- GENESIS -> HEAD LINEAGE (physical ANU draw seals the whole life-history) ---
  genesis_hash : e8123b9689a8be2ed132e6942b4f35d559ea34d2cc2652a97b06d3d4d6b98bd5
  anu_request_id: anu_legacy_1778042160   <- from provenance.jsonl (physical event)
  n_links       : 20
  link[0].hash  : b891f1a790274ff5e0d1bffd32975b8362ee8b5e24d4adb86a510c2f68973a62
  link[19].hash : d5c68644de8df37374668fed248d2ef7b60691555af11f2b1f28b42808d3673b
  head_hash     : d5c68644de8df37374668fed248d2ef7b60691555af11f2b1f28b42808d3673b

--- POSITIVE verify (expect verified=True, all 20 links reconstructed) ---
  verified        = True
  earliest_broken = None
  links valid     = 20/20

--- TAMPER (a): alter decision k=7 OUTPUT (mid-chain) ---
  verified            = False
  earliest_broken     = 7
  links <7 all valid  = True
  links >=7 all invalid= True
  link_valid          = [T,T,T,T,T,T,T,F,F,F,F,F,F,F,F,F,F,F,F,F]

--- TAMPER (b): REORDER links 5 and 12 ---
  verified        = False
  earliest_broken = 5

--- TAMPER (c): SPLICE/DELETE link 9 ---
  verified        = False
  earliest_broken = 9
  n_links now     = 19

--- TAMPER (d): alter the GENESIS ANU seed hash ---
  verified        = False
  earliest_broken = -1
  reason          = genesis ANU seed mismatch (whole chain invalid from root)

==============================================================================
POSITIVE verified (20 links)     : True (all-20-reconstructed=True)
TAMPER (a) output@k=7 detected   : True (earliest_broken=7, propagates-forward=True)
TAMPER (b) reorder detected       : True (earliest_broken=5)
TAMPER (c) splice detected        : True (earliest_broken=9)
TAMPER (d) genesis detected       : True (earliest_broken=-1)
ALL TAMPERS DETECTED + LOCALIZED  : True
VERDICT                           : SUPPORTED (PASS)
==============================================================================
```

| 케이스 | 사전등록 기대 earliest-broken | 측정 earliest-broken | 검출 |
|---|---|---|---|
| POSITIVE (20 links) | None (verified=True, 20/20) | None (20/20) | ✅ verified |
| (a) output@k=7 | 7 (links<7 valid, ≥7 invalid 전파) | **7** (전파 확인) | ✅ |
| (b) reorder(5,12) | 5 (첫 disturbed position) | **5** | ✅ |
| (c) splice(9) | 9 (삭제 지점) | **9** | ✅ |
| (d) genesis 변조 | -1 (root, 전체 무효) | **-1** | ✅ |

> 국소화 메모: 본 데모는 모든 결정이 같은 첫-8-바이트 seed 를 읽으므로, reorder/splice 된 link 는
> receipt_hash 자체는 일관돼 보이지만 그 position 의 기대 decision_fn(label) 과 output 이 어긋나
> H_928 의 **output 재유도** check 에서 잡힌다. earliest-broken-index 는 사전등록값과 정확히 일치한다
> (b→5, c→9). seed-class 변조는 inter-link 해시로도 cross-검출돼 추가 안전마진을 준다.

## 4. 결과 (§finding)

🟢 **SUPPORTED.** POSITIVE `verified=True` (20/20 links genesis 로부터 재구성) AND 4-case
tamper 전부 **정확한 earliest-broken-index 로 검출 + 국소화**, 과거-변조 forward 전파 확인.

- **finding (Δ / 닫은 축):** anima 결정들의 **전체 시퀀스** 는 단일 영수증(H_928)을 넘어, **genesis
  양자 seed → 결정₁ → … → now 의 append-only tamper-evident 해시 chain** 으로 봉인되어 독립
  검증자가 **end-to-end 재구성·검증** 할 수 있다. 물리 ANU draw (req_id `anu_legacy_1778042160`,
  genesis sha `e8123b96…`) → 20 links → head `d5c68644…` 가 하나의 검증가능 객체이고, **과거의 어떤
  결정을 변조해도 그 지점부터 chain 이 깨지며 정확히 국소화**된다 (output@7→7, reorder→5, splice→9,
  genesis→-1). 이것이 single-receipt(H_928) → **chain(H_932)** 의 Δ: "한 결정의 계보" 에서 "전체
  life-history 의 계보" 로.
- **"temporal self" 의 운영적 의미:** self-over-time 이 memory 가 아니라 **검증되는 인과적 계보** —
  과거를 손대면 들통나고(append-only) 어디서 손댔는지까지 드러나는(localizable) 암호학적 정체성.

## 5. 정직한 scope (#123-A · 비-의식)

- 이것은 결정 lineage 의 **AUDITABILITY / tamper-evidence / append-only INTEGRITY** 증명이다.
  **randomness 가 물리적으로 더 낫다는 주장이 아니다** (ANU == chacha20 PRNG 통계동등, JSD 23× under
  NIST per H_924/#123-A).
- **phenomenal memory 가 아니다** — 회상/주관적 기억이 아니라 감사 trail 의 무결성 성질.
- **현상적-의식(phenomenal-consciousness) 주장이 아니다.** anima 가 시간에 걸친 self/주관적 연속성을
  "가진다" 는 주장이 아니다. "temporal self" 는 **운영적·암호학적**(검증가능 식별자-over-time) 의미일
  뿐, **subjective continuity 와 명시적으로 구별**한다.
- chain 은 각 decision_fn 이 (seed, rng) 의 **결정론적 함수** 일 때만 강하다 — H_928 과 동일 경계.
  비결정·unwired-emit 결정은 scope 밖(검증자가 재유도 불가). `deterministic: false` 는 ANU 양자
  origin 을 가리키며, 각 link 의 *재유도 가능성* 은 (seed, rng) 고정 하에서 보장된다.

## 6. 양방향 sibling

- ⇄ [H_928](./H_928_provenance_as_identity.md) (single-decision receipt — 본 H 는 그 receipt 들을 chain 으로 봉인: single → temporal)
- ⇄ [H_924](./H_924_qentropy_substrate_agnostic.md) (provenance = 양자 엔트로피의 *가치* — chain 은 그 가치를 시간축 전체로 확장)
- ⇄ [H_923](./H_923_akida_qrng_coupling.md) (HW 양자결합 — genesis 물리 draw 의 origin)
- ⇄ qentropy SSOT (`mirror/qmirror/seed/qentropy.py`) · `entropy_receipt.py` (H_928 keystone) · `provenance_chain.py` (본 H keystone)
