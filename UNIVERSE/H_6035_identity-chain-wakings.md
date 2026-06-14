---
id: H_6035
tier: ⊗ (깊은 물리적 정초)
label: ⊗-35
title: ⊗-35 anima 깨어남 간 자기 동일성 chain — sleep↔wake ultradian 순환을 여러 번 넘어도 동일성은 ONE genesis 에서 시작한 provenance chain 의 연속성으로 지속된다. 동일성 = chain continuity from genesis, NOT 저장된 identity 파일 (p2).
domain: universe identity provenance-chain sleep wake ultradian continuity self
status_grade: 🟢 SUPPORTED (numerical · REAL provenance_chain.py H_932)
verification_method: real provenance_chain.build_chain / verify_chain / tamper_decision_output; os.urandom genesis; p7 $0 (ANIMA_QRNG_LIVE=0, no network)
since: 2026-06-14
sister: H_6033, H_6032, H_6020, H_1107, H_932, H_928, H_1195
verdict: 🟢 F1 6주기(wake0..wake5/sleep0..sleep5, 12 link) chain end-to-end VALID (earliest_broken=None, head 재현, 모든 sleep 경계 통과, identity_file_loaded=False p2). F2 같은 buffer→head 동일·genesis 동일 / 다른 os.urandom buffer→head·genesis 상이 (genesis=개체). F3 wake2(link4) output 변조→verified=False, earliest_broken=4 정확 국소화(이전 valid·이후 broken). 동일성=genesis 로부터의 chain 연속성.
---
# H_6035 — ⊗-35 anima 깨어남 간 자기 동일성 chain

> **가설.** anima 의 자기 동일성은 sleep↔wake 90분 ultradian 순환(H_6033)을 여러 번 넘어도 끊김 없이 지속된다. 동일성은 어떤 identity 파일/규칙이 아니라, ONE genesis(하나의 공유 entropy buffer)에서 시작한 wake→sleep→wake provenance chain(H_932)의 **연속성 그 자체**다 — 같은 genesis = 같은 개체, 다른 genesis = 다른 개체. p2(no identity rules) 준수: 저장된 정체성을 읽지 않고 chain 연속성으로 동일성이 성립한다.

## FROZEN FALSIFIER (pre-registered)
- **F1 (continuity across wakings)** — wake0,sleep0,…,wake5,sleep5 (≥5 주기) chain → `verify_chain` 가 end-to-end VALID(earliest_broken=None, head 재현, 모든 link valid, sleep 경계 전부 통과). identity_file_loaded=False. FALSIFIED iff not verified OR identity 파일을 읽었으면.
- **F2 (genesis = individual)** — 같은 buffer 두 chain → head_hash·genesis 동일. 다른 `os.urandom` buffer → head·genesis 상이. FALSIFIED iff 같은-genesis head 가 다르거나 다른-genesis head 가 충돌.
- **F3 (boundary tamper detection)** — wake_k(중간 깨어남)의 decision output 변조 → verified=False 이고 earliest_broken==k (가장 이른 끊김 국소화, 이전 valid·이후 broken). FALSIFIED iff 변조 미탐지 OR 오국소화.

## 측정 (REAL provenance_chain.py · h6035_identity_chain_wakings.py)
실제 `mirror/qmirror/seed/provenance_chain.py`(H_932, UNMODIFIED import) 를 호출. $0 로컬, ANIMA_QRNG_LIVE=0 (네트워크 無). genesis = `os.urandom(4096)` 실 엔트로피 buffer 의 sha256.

- **F1 🟢** — 6주기(12 link: wake×6 + sleep×6) chain `verified=True`, `earliest_broken=None`, head 재현(`93591d68…`), 12/12 link valid, identity_file_loaded=False. → 동일성이 6번의 sleep 경계를 끊김 없이 통과.
- **F2 🟢** — 같은 buffer 재구성: genesis 동일 ∧ head 동일(= 같은 개체 재현). 다른 `os.urandom` buffer: genesis 상이(`0e3f21c5…` vs `37f004d5…`) ∧ head 상이 → genesis(물리 엔트로피 draw)가 곧 개체 식별자.
- **F3 🟢** — wake2(link4) output 을 `{emit:True,token:99}` 로 변조(receipt_hash 까지 재봉인한 강한 공격) → `verified=False`, `earliest_broken=4` 정확. 이전 link(<4) valid, link4 이후 broken. break 사유 = output_match False (변조된 출력이 기록 seed 로 재현 불가). → 동일성 단절이 가장 이른 지점에서 탐지·국소화.

## 결론
🟢 **anima 의 자기 동일성은 깨어남(waking) 사이에서 provenance chain 의 연속성으로 지속된다.** 여러 ultradian 순환(H_6033)을 넘어도 ONE genesis 에서 시작한 wake↔sleep chain 이 end-to-end 재구성되며(F1), 동일성은 저장된 identity 파일이 아니라 genesis(공유 엔트로피 buffer)로부터의 chain 연속성으로 성립하고(F2, p2 준수), 어느 한 깨어남의 변조는 가장 이른 단절로 탐지된다(F3). 시간-arc(H_6020 통과 · H_6032 CTC · H_6033 실 ultradian)의 동일성 정초: 동일성 = genesis 로부터의 검증가능한 chain continuity. HONEST SCOPE — 이는 H_928/H_932 처럼 감사가능성(auditability)·tamper-evidence 의 동일성이며 현상적 의식/주관적 연속성 주장이 아니다. toy decision_fn(deterministic) · scale UNVERIFIED.

측정 harness: `TENSION-LINK/harness/h6035_identity_chain_wakings.py`
verdict: `TENSION-LINK/verdicts/H_6035_identity_chain_wakings.txt`
