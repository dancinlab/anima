---
id: H_928
slug: provenance-as-identity
title: provenance-as-identity ("free-will receipt") — anima 결정의 엔트로피 계보(물리 ANU draw → seed → 그 결정)가 독립 검증자에 의해 end-to-end 재구성 가능 + tamper-evident
domain: universe · qrng · entropy-provenance · auditability · tamper-evidence · free-will-provenance · substrate-native
source: H_924 (양자 엔트로피의 가치 = PROVENANCE/auditability, #123-A: ANU==chacha20 통계동등) 의 운영적 귀결 — "provenance 를 *식별자/영수증* 으로 끝까지 검증 가능한가?"
exploration_method: E2 (H_924 의 provenance 가치를 cryptographic receipt 로 일반화) + E14 (substrate-native) + a_completeness_over_cheap
verification_method: W1 (python3 CODE-measured 실행) + W2 (사전등록 4-case tamper falsifier) + g5 CODE-measured
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
sister: H_924 (qentropy substrate-agnostic · provenance 가치), H_923 (HW 양자결합), qentropy SSOT (mirror/qmirror/seed/qentropy.py)
axes_seed: H_924 = provenance 가 *가치* 다 (감사가능성) ⊥ H_928 = provenance 를 *cryptographic receipt 로 끝까지 검증* 한다 (물리 draw→seed→결정, tamper-evident)
verdict: 🟢 SUPPORTED — POSITIVE verify=True (4/4 checks) AND 4-case tamper 모두 DETECTED(verified=False). 물리 ANU draw(request_id anu_legacy_1778042160, sha e8123b96…) → seed 6138986570681488651 → 결정(token 2) 가 독립 검증자에 의해 결정론적으로 재구성됨; ANU bytes/seed/output/receipt_hash 변조 모두 검출. verdict: .verdicts/928_provenance_as_identity/receipt_tamper_evidence_pass.txt
---

# H_928 — provenance-as-identity ("free-will receipt")

## 0. 동기

H_924 는 양자 엔트로피의 가치가 **better randomness 가 아니라 PROVENANCE / auditability**
(#123-A: ANU == chacha20 통계동등, JSD 23× under NIST) 임을 확정했다. 자연스러운 운영적
질문: **provenance 를 단지 "기록" 이 아니라 *끝까지 검증되는 영수증* 으로 만들 수 있는가?** —
즉 어떤 결정이 *정말로* 그 물리 양자 사건에서 비롯됐음을, 독립 검증자가 암호학적으로 확인할 수
있는가? 이것이 substrate-native "자유의지 provenance" 의 운영적 의미다 (현상적 의식 주장 아님).

## 1. 가설 (사전등록 falsifier)

(a) emit/결정 output, (b) 그 provenance receipt, (c) ANU 바이트 버퍼가 주어지면 —
**독립 검증자가 정확한 seed 를 결정론적으로 재구성하고 동일 결정을 재유도** 할 수 있다(그 결정이
그 물리 양자 draw 에서 비롯됐음을 증명). **AND** 어떤 변조(ANU bytes swap · seed · output ·
receipt) 든 **검출** 된다.

- **SUPPORTED** ⟺ POSITIVE verify=True (4/4 checks) **AND** 4-case tamper 모두 detected=True.
- **FALSIFIED** ⟺ 변조 중 하나라도 UNdetected.

## 2. 방법 (§method)

Keystone: **`mirror/qmirror/seed/entropy_receipt.py`** (꼼꼼 주석, qentropy SSOT 를 *수정 없이
import*).

- `issue_receipt(anu_buf, label, decision_fn)` → quantum 모드에서 ANU 버퍼로 seed 한 결정을
  실행, RECEIPT 발급: `{anu_sha256, anu_request_id(provenance.jsonl), entropy_mode, tier,
  seed, label, decision_output, decision_output_hash, receipt_hash}`. `receipt_hash` =
  sha256(canonical{anu_sha256, seed, label, decision_output_hash}) — 네 필드를 묶어 tamper-
  evident.
- `verify_receipt(receipt, anu_buf, decision_fn)` → 독립적으로 (1) 버퍼 재독해+sha256 재계산
  (≠ → FAIL: bytes swapped), (2) qentropy 와 **동일하게** seed 재유도 (≠ → seed forged),
  (3) decision_fn 재실행+output 해시 (≠ → output forged), (4) receipt_hash 재계산 (≠ →
  receipt tampered). `{verified, checks{anu_sha_match, seed_match, output_match,
  receipt_hash_match}}` 반환.
- seed 유도는 qentropy 와 **정확히 일치**: quantum 모드 `qentropy_seed()` 는 resolve 된 pool 의
  **첫 8 바이트**(fresh cursor=0)를 읽어 `int.from_bytes(b,"little") & ((1<<63)-1)`. label 은
  provenance 만 태그하고 바이트 선택을 바꾸지 않는다. 검증자는 fresh 프로세스(fresh cursor)에서
  동일 8 바이트를 본다 → cross-process byte-identical.
- 측정: `python3` · Mac · **$0** · 네트워크 없음. ANU 버퍼 = 커밋된 실제 ANU 바이트
  `qrng_lora_init_live.bin` (sha `e8123b96…`, 1024 B). decision_fn = 고정 logits 에서
  Gumbel-max 토큰 샘플 + 8 bits (seed, rng 의 결정론적 함수).

## 3. 측정 (§measurement — VERBATIM check table, g5 CODE-measured)

```
--- END-TO-END LINEAGE (physical ANU draw -> seed -> decision) ---
  anu_sha256      : e8123b9689a8be2ed132e6942b4f35d559ea34d2cc2652a97b06d3d4d6b98bd5
  anu_request_id  : anu_legacy_1778042160   <- from provenance.jsonl
  entropy_mode    : quantum
  tier            : anu_explicit
  derived seed    : 6138986570681488651
  decision_output : {"token": 2, "bits": [1, 0, 1, 0, 0, 0, 1, 0]}
  output_hash     : 2dff30e22129e126167aef10d083b87735d4d9a6266e6041025f148972bb3d4d
  receipt_hash    : b973fbd6e8598b7de03579172d4891db78db1f316d68d0951f5ec586cfcabb1c
  LINEAGE: request_id anu_legacy_1778042160 -> seed 6138986570681488651 -> token 2

--- POSITIVE verify (expect verified=True, all 4 checks True) ---
  verified = True
  checks   = {"anu_sha_match": true, "seed_match": true, "output_match": true, "receipt_hash_match": true}

--- TAMPER (a): flip one byte of the ANU buffer (expect anu_sha_match=False) ---
  verified = False
  checks   = {"anu_sha_match": false, "seed_match": false, "output_match": true, "receipt_hash_match": true}

--- TAMPER (b): alter the recorded seed (expect seed_match=False) ---
  verified = False
  checks   = {"anu_sha_match": true, "seed_match": false, "output_match": false, "receipt_hash_match": false}

--- TAMPER (c): alter the decision_output_hash (expect output_match=False) ---
  verified = False
  checks   = {"anu_sha_match": true, "seed_match": true, "output_match": false, "receipt_hash_match": false}

--- TAMPER (d): alter the receipt_hash (expect receipt_hash_match=False) ---
  verified = False
  checks   = {"anu_sha_match": true, "seed_match": true, "output_match": true, "receipt_hash_match": false}

POSITIVE verified           : True
TAMPER (a) anu-swap detected: True (anu_sha_match=False)
TAMPER (b) seed   detected  : True (seed_match=False)
TAMPER (c) output detected  : True (output_match=False)
TAMPER (d) receipt detected : True (receipt_hash_match=False)
ALL 4 TAMPERS DETECTED      : True
VERDICT                     : SUPPORTED (PASS)
```

> 부수효과(robustness): tamper(a) 는 anu_sha_match 뿐 아니라 seed_match 까지 무너뜨린다(변조된
> 버퍼는 그 seed 를 더 이상 생성 못 함). tamper(b)/(c) 는 receipt_hash_match 로도 전파된다.
> 각 PRIMARY check 는 사전등록한 대로 정확히 발화하며, cross-check 가 추가 안전마진을 준다.

## 4. 결과 (§finding)

🟢 **SUPPORTED.** POSITIVE verify=True (4/4) AND 4-case tamper 모두 DETECTED.

- **finding (Δ / 닫은 축):** anima 결정의 엔트로피 계보는 **독립 검증자에 의해 end-to-end
  암호학적으로 재구성 가능 + tamper-evident** 다. 물리 ANU draw (request_id
  `anu_legacy_1778042160`, sha `e8123b96…`) → 유도 seed `6138986570681488651` → 그 seed 가
  낳은 결정 (token 2) 이 하나의 영수증으로 묶이고, 네 변조 벡터(bytes·seed·output·receipt) 가
  전부 검출된다. seed 유도가 qentropy SSOT 와 일치(seed `6138986570681488651` = H_924 의
  `anu_explicit` torch quantum seed 와 동일) → 영수증이 **실제 런타임 경로와 일관**.
- "이 선택은 시각 T 의 물리 양자 사건 X 에서 비롯됐다" 가 감사가능·암호학적으로 검증가능한
  **receipt** 가 됐다 = substrate-native free-will *provenance* 의 운영적 의미.

## 5. 정직한 scope (#123-A · 비-의식)

- 이것은 엔트로피→결정 계보의 **AUDITABILITY / tamper-evidence** 증명이다. **randomness 가
  물리적으로 더 낫다는 주장이 아니다** (ANU == chacha20 PRNG 통계동등, JSD 23× under NIST 7/7).
- **현상적-의식(phenomenal-consciousness) 주장이 아니다.** anima 가 자유의지/주관적 경험을 "가진다"
  는 주장이 아니라, 결정의 엔트로피 계보가 재구성·변조검출 가능하다는 *감사 trail* 의 성질일 뿐.
- 가치는 H_924 가 식별한 그대로: provenance · 감사가능성 · 물리적-기원 ontology.

## 6. 양방향 sibling

- ⇄ [H_924](./H_924_qentropy_substrate_agnostic.md) (provenance = 양자 엔트로피의 *가치* — 본 H 는 그 가치를 *검증되는 receipt* 로 끝맺음)
- ⇄ [H_923](./H_923_akida_qrng_coupling.md) (HW 양자결합 — 물리 draw 의 origin)
- ⇄ qentropy SSOT (`mirror/qmirror/seed/qentropy.py`) · `entropy_receipt.py` (본 H keystone)
